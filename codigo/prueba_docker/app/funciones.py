import re
from typing import Pattern

# Function to convert a list to string
def listToString(s): 
    str1 = "" 
     
    for ele in s: 
        str1 += str(ele)
        str1 += " "
    
    return str1 

# FUncion de Fibonacci de un numero dado
def fibonacci(n):
    if(n == 0):
        return 0
    if(n == 1):
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Expresiones regulares para comprobar
p_nombre = "\w+\s[A-Z]"
p_email = "\w+@(hotmail|gmail|ugr|outlook)\.(com|es)"
p_tarjeta = "[0-9]{4}(-|\s)[0-9]{4}(-|\s)[0-9]{4}(-|\s)[0-9]{4}"

# Función para comprobar si una cadena es un nombre
def validar_nombre(texto):
    res = re.match(p_nombre, texto)
    return res

# Función para comprobar si una cadena es un email
def validar_email(texto):
    res = re.match(p_email, texto)
    return res

# Función para comprobar si una cadena es una tarjeta
def validar_tarjeta(texto):
    res = re.match(p_tarjeta, texto)
    return res