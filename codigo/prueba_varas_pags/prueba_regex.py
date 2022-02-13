import re

pattern = re.compile("^[+-]?((\d+(\.\d+)?)|(\.\d+))$")
# Regex sacada de https://codereview.stackexchange.com/questions/223970/a-regex-pattern-that-matches-all-forms-of-integers-and-decimal-numbers-in-python

prueba = "10"
print(bool(pattern.match(prueba)))

prueba = "1.0"
print(bool(pattern.match(prueba)))

prueba = "0.9"
print(bool(pattern.match(prueba)))

print("A partir de aqui DEP")

prueba = "0.9.8"
print(bool(pattern.match(prueba)))
prueba = "10."
print(bool(pattern.match(prueba)))
prueba = "a"
print(bool(pattern.match(prueba)))
prueba = "10.1a"
print(bool(pattern.match(prueba)))
prueba = "10a2"
print(bool(pattern.match(prueba)))
prueba = ""
print(bool(pattern.match(prueba)))