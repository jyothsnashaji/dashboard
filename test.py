import re

str="/Network_Health"
if (re.findall(r'_Health$',str)):
    strip=str.split('/')
    print(strip)
    split=strip[1].split('_')
    print(split)
    