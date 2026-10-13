# Lab 04 - Proving the tests can fail

I changed the / to * in pct() and ran the tests:

 3 failed, 25 passed

After undoing the change:

 28 passed

## Which double is which

- Stub: fixed_now in tests/test_add_mark.py. It always returns the same time, so the expected "at" value is known.
- Fake: the state fixture in tests/conftest.py. It is a plain dict that works like the real gradebook. The files in tests/test_storage.py are real files in tmp_path.
- Mock: Mock() passed as save in tests/test_add_mark.py. It records the call, so the tests can check "called once" and "not called".

## Why I did not mock pct() or the file in Task 5

- pct() is plain logic inside my own program. I can call it directly, and mocking it would hide the very calculation under test.
- tmp_path gives a real, empty file for each test. Testing load() and save() against it checks what really happens (JSON written and read back, a missing file, a corrupt file). A mock would only check that I called open.
