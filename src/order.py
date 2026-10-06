def calc(o):
    t = 0
    for i in o["items"]:
        p = i["price"]
        q = i["qty"]
        if p > 0:
            if q > 0:
                t = t + p * q

    if o["member"] == True:
        if t > 100:
            d = t * 0.2
        else:
            if t > 50:
                d = t * 0.1
            else:
                d = 0
    else:
        d = 0

    t = t - d

    if o["country"] == "PK":
        s = 5
    else:
        if o["country"] == "US":
            s = 15
        else:
            s = 25

    t = t + s

    print("Total: $" + str(t))
    return t