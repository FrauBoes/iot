limit = int(input("Please type the limit of the Fibonacci sequence: "))

def fib(n):
    if n < 3:
        return 1
    else:
        return fib(n-1) + fib(n-2)


print('The sequence up to number ' + str(limit) + ' is: ')

sequence = ""

while limit > 0:
    sequence = str(fib(limit)) + " " + sequence
    limit -= 1

print(sequence)
