#python 3.7.1
import random
import string

print ("Welcome to Password Generator!")
length = int(input('\nEnter the length of password: '))

lower = string.ascii_lowercase
upper = string.ascii_uppercase
num = string.digits

all = lower + upper + num

temp = random.sample(all,length)
password = "".join(temp)

print(password)
