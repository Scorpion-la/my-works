#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      ADITYA
#
# Created:     14/02/2025
# Copyright:   (c) ADITYA 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import random
import names
def generate_random_person():
    name = names.get_full_name()
    age = random.randint(18, 65)
    city = random.choice(["New York", "London", "Tokyo", "Paris","Delhi","Mumbai","Wasington DC"])
    return name, age, city
r=int(input("Enter number of people : "))
for _ in range(r):
    print(generate_random_person())


