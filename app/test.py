import time
start_time = time.time()
count = 1
x = 20
while count < 14365:
    x = 20 * 20
    print(count)
    count = count + 1
print("--- %s seconds ---" % (time.time() - start_time))

