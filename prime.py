num = int(input("Please type a number: "))

divisors = []

def div(num):
    for x in range(2, num-1):
        if num % x == 0:
            divisors.append(x)
    return divisors


if len(div(num)) == 0:
    print(str(num) + " is a prime number")

else:
    print(str(num) + " is not a prime number. Its divisors are: ")
    for x in divisors:
        print(x, end=" ")


print("Finished!")