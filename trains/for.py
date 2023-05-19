x = 0
while x:
    age = int(input("Please enter your age:"))
    if age > 0 and age < 10:
        print("children")
    elif age > 10 and age <= 18:
        print("student")
    else:
        print("youth")
