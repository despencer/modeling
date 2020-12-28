def timerange(start, stop, delta):
    while start <= stop:
        yield start
        start += delta