# -*- coding: UTF-8 -*-
#!/usr/bin/python3

numVar = 999
str1 = "test is: %s" %numVar

strVar = "999"
str2 = "test is: %s" %strVar

print("str1 is:" + str1)
print("str2 is:" + str2)

numVar = 999
str3 = "test is: %d" %numVar

#strVar = "999"
#str4 = "test is: %d" %strVar #TypeError: %d format: a number is required, not str

print("str3 is:" + str3)
#print("str4 is:" + str4)