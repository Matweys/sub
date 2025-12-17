def make_counter(start):
    def inner():
        nonlocal start
        start += 1

    return inner


c1 = make_counter(10)
print(c1())


