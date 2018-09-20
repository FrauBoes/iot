num = int(input("Please type a number: "))

result = 1

if num == 0:
    result = 0

else:
    while num > 1:
        result *= num
        num -= 1

print('The factorial of ' + str(num) + ' is: ' + str(result) + '.')

