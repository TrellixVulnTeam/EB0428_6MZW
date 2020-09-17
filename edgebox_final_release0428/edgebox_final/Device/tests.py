from django.test import TestCase

# Create your tests here.
a = 3
b = None

try:
    if a == 1:
        b = a * 1
    if a == 2:
        b = a * 2
    if a == 3:
        b = a * 3

    if b == 9:
        print(a, b)
        a = 1
        if a == 3:
            print("ab")
        else:
            print("ba")

    else:
        print("cc")

except Exception as e:
    print(e)
