import pandas as pd
import numpy as np

import math 
from datetime import datetime

df = pd.read_csv("owid-covid-data.csv")

df_spain = df[df["location"] == "Spain"]
df_spain = df_spain.reset_index()

df_spain = df[:180]

t0 = df_spain.loc[0].at["date"]
t0 = datetime.strptime(t0, '%Y-%m-%d')



tiempo = []

for fecha in df_spain["date"]:
    aux = datetime.strptime(fecha, '%Y-%m-%d')
    aux = (aux-t0).days
    tiempo.append(aux)

columnas = ['new_cases', 'new_deaths']
#for columna in columnas:
#    df_spain[columna] = df_spain[columna].fillna(df[columna].mean())

poblacion_spain = 46787961

I = np.array(df_spain['new_cases'])
R = np.empty(len(df_spain['new_deaths']))
S = np.empty(len(df_spain['new_deaths']))

for j in range(10, len(df_spain["new_cases"])):
    I[j] = df_spain["new_cases"][j-10:j].sum()

R[0] = df_spain.loc[0].at['new_deaths']
for j in range(1, 10):
    if not math.isnan(df_spain.loc[j].at["new_deaths"]) and not math.isnan(R[j-1]):
        R[j] = R[j-1]+df_spain.loc[j].at["new_deaths"]
    elif not math.isnan(df_spain.loc[j].at["new_deaths"]) and math.isnan(R[j-1]):
        R[j] = df_spain.loc[j].at["new_deaths"]
    elif not math.isnan(R[j-1]) and math.isnan(df_spain.loc[j].at["new_deaths"]):
        R[j] = R[j-1]
    else:
        R[j] = float('NaN')

for j in range(10, len(df_spain["new_cases"])):
    if not math.isnan(df_spain.loc[j-10].at["new_cases"]) and not math.isnan(R[j-1]):
        R[j] = R[j-1]+I[j-10]
    elif not math.isnan(df_spain.loc[j-10].at["new_cases"]) and math.isnan(R[j-1]):
        R[j] = I[j-10]
    elif not math.isnan(R[j-1]) and math.isnan(df_spain.loc[j-10].at["new_cases"]):
        R[j] = R[j-1]
    else:
        R[j] = float('NaN')


#R = df_spain["new_deaths"].cumsum()
S = poblacion_spain-I-R

#S = poblacion_spain-I-R

columns = ["t", "S", "I", "R"]
rows = tiempo
data = np.transpose(np.array([tiempo, S, I, R]))
df_def = pd.DataFrame(data=data, index=rows, columns=columns)

# Escribo fichero
f = open("datos_reales_spain.csv", "w")

formato = "t,S,I,R\n"
f.write(formato)

for i in range (0, len(S)):
    aux = str(tiempo[i]) + "," + str(S[i]) + "," + str(I[i]) + "," + str(R[i]) + "\n"
    f.write(aux)

f.close()
