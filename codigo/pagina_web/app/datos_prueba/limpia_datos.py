import pandas as pd
import numpy as np

from datetime import datetime

df = pd.read_csv("owid-covid-data.csv")

df_spain = df[df["location"] == "Spain"]
df_spain = df_spain.reset_index()

t0 = df_spain.loc[0].at["date"]
t0 = datetime.strptime(t0, '%Y-%m-%d')

tiempo = []

for fecha in df_spain["date"]:
    aux = datetime.strptime(fecha, '%Y-%m-%d')
    aux = (aux-t0).days
    tiempo.append(aux)

df_spain = df_spain.fillna(0)

poblacion_spain = 46787961

I = np.array(df_spain['new_cases'])
R = np.empty(len(df_spain['new_deaths']))
S = np.empty(len(df_spain['new_deaths']))

S[0] = poblacion_spain-I[0]-R[0]
R[0] = df_spain.loc[0].at["new_deaths"]
for j in range(1, len(df_spain['new_deaths'])):
    R[j] = df_spain.loc[j].at['new_deaths']+ R[j-1]
    S[j] = poblacion_spain-I[j]-R[j]

for j in range(10, len(df_spain["new_deaths"])):
    I[j] = df_spain.loc[j].at['new_deaths']+df_spain.loc[j-1].at['new_deaths']+df_spain.loc[j-2].at['new_deaths']+df_spain.loc[j-3].at['new_deaths']+df_spain.loc[j-4].at['new_deaths']+df_spain.loc[j-5].at['new_deaths']+df_spain.loc[j-6].at['new_deaths']+df_spain.loc[j-7].at['new_deaths']+df_spain.loc[j-8].at['new_deaths']+df_spain.loc[j-9].at['new_deaths']+df_spain.loc[j-10].at['new_deaths']
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
