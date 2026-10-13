import datetime
import http.server
import json
import logging
import sys
from typing import Any, Callable

from errors import ConflictError, NotFoundError, ValidationError
from models import Mark, parse_assessment, parse_mark, parse_student

logger = logging.getLogger(__name__)

DATA = "gradebook.json"
STATE: dict[str, Any] = {"students": {}, "assessments": {}, "marks": []}


def load() -> None:
    global STATE
    try:
        with open(DATA) as f:
            STATE = json.load(f)
    except FileNotFoundError:
        STATE = {"students": {}, "assessments": {}, "marks": []}


def save() -> None:
    with open(DATA, "w") as f:
        json.dump(STATE, f)


def pct(sid: str) -> str:
    total = 0.0
    got = 0.0
    for m in STATE["marks"]:
        if m["student"] == sid:
            a = STATE["assessments"].get(m["assessment"])
            if a:
                got = got + float(m["score"]) * float(a["weight"]) / float(a["total"])
                total = total + float(a["weight"])
    if total == 0:
        return "0"
    return str(round(got, 2))


def now() -> str:
    return str(datetime.datetime.now(datetime.timezone.utc))


def add_mark(
    state: dict[str, Any],
    mark: Mark,
    now: Callable[[], str],
    save: Callable[[], None],
) -> None:
    """Check a mark against the gradebook, then record it and save."""
    if mark.student not in state["students"]:
        raise NotFoundError("student not found")

    if mark.assessment not in state["assessments"]:
        raise NotFoundError("assessment not found")

    assessment = state["assessments"][mark.assessment]

    if mark.score > float(assessment["total"]):
        raise ValidationError("score cannot be greater than total")

    state["marks"].append(
        {
            "student": mark.student,
            "assessment": mark.assessment,
            "score": mark.score,
            "at": now(),
        }
    )
    save()


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args: object) -> None:
        pass

    def _send(self, code: int, obj: object) -> None:
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle(self, method: Callable[[], tuple[int, object]]) -> None:
        try:
            status, body = method()
        except ValidationError as e:
            self._send(400, {"error": str(e)})
        except NotFoundError as e:
            self._send(404, {"error": str(e)})
        except ConflictError as e:
            self._send(409, {"error": str(e)})
        except Exception:
            logger.exception("unexpected error")
            self._send(500, {"error": "internal error"})
        else:
            self._send(status, body)

    def do_GET(self) -> None:
        self._handle(self._get)

    def _get(self) -> tuple[int, object]:
        if self.path == "/students":
            return 200, list(STATE["students"].values())

        if self.path.startswith("/students/"):
            sid = self.path.split("/")[2]

            if sid not in STATE["students"]:
                raise NotFoundError("student not found")

            student = dict(STATE["students"][sid])
            student["percentage"] = pct(sid)
            return 200, student

        if self.path == "/assessments":
            return 200, list(STATE["assessments"].values())

        if self.path == "/report":
            out = []

            for sid in STATE["students"]:
                out.append(
                    {
                        "id": sid,
                        "name": STATE["students"][sid]["name"],
                        "pct": pct(sid),
                    }
                )

            return 200, out

        raise NotFoundError("not found")

    def do_POST(self) -> None:
        self._handle(self._post)

    def _post(self) -> tuple[int, object]:
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n)

        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            raise ValidationError("bad json")

        if self.path == "/students":
            student = parse_student(d)

            if student.id in STATE["students"]:
                raise ConflictError("student already exists")

            STATE["students"][student.id] = {
                "id": student.id,
                "name": student.name,
                "joined": str(datetime.datetime.now(datetime.timezone.utc)),
            }

            save()
            return 201, STATE["students"][student.id]

        if self.path == "/assessments":
            assessment = parse_assessment(d)

            if assessment.id in STATE["assessments"]:
                raise ConflictError("assessment already exists")

            STATE["assessments"][assessment.id] = {
                "id": assessment.id,
                "title": assessment.title,
                "weight": assessment.weight,
                "total": assessment.total,
            }

            save()
            return 201, STATE["assessments"][assessment.id]

        if self.path == "/marks":
            mark = parse_mark(d)

            add_mark(STATE, mark, now, save)

            logger.info(
                "recorded mark for %s score %s",
                mark.student,
                mark.score,
            )
            return 201, {"ok": True}

        raise NotFoundError("not found")


def main(argv: list[str] = sys.argv) -> None:
    load()
    port = 8000

    if len(argv) > 1:
        try:
            port = int(argv[1])
        except ValueError:
            raise SystemExit("port must be a whole number from 1 to 65535")

        if port < 1 or port > 65535:
            raise SystemExit("port must be a whole number from 1 to 65535")

    logger.info("gradebook on %s", port)
    http.server.HTTPServer(("", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
