failist = [123,234,345,456,567,678,789,890,901]
while len(failist) > 0:
    for x in failist:
        print(len(failist), x)
        if x == 345:
            failist.remove(x)
        else:
            pass