degrees = float(input("Please type a value for degrees: "))

scale = input("Please type 'F' if you want to convert from Celcius to Fahrenheit and 'C' otherwise.")

if scale == 'F':
    result = round(degrees * 1.8 + 32, 2)
    print(str(degrees) + "℃ is " + str(result) + "℉.")

elif scale == 'C':
    result = round((degrees - 32) / 1.8, 2)
    print(str(degrees) + "℉ is " + str(result) + "℃.")

print("Finished!")


