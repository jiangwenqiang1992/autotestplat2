from django.test import TestCase

# Create your tests here.
import re

str1 = "{'aa':'bb','cc':'dd'}"
str1_re = "'aa':'(.+?)'"
value = re.search(str1_re,str1)
print(value.group(1))