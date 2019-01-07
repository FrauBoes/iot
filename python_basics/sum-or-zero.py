n1 = int(input("Please type a number: "))
n2 = int(input("Please type a second number: "))
n3 = int(input("Please type a third number: "))

sum = 0

if n1 == n2 and n2 == n3:
    print('The numbers are equal. The result is: ' + str(sum))
else:
    sum += n1 + n2 + n3
    print('The result is: ' + str(sum))

print("Finished!")


