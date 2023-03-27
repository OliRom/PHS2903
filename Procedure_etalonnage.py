import nidaqmx as ni
import pandas as pd
import numpy as np
import Parameters as param

i= int(input('Numero de la thermistance (1 ou 2): '))
courbe = []
chiffre=[f'{j}' for j in range(10)]

while True:
    while True:
        T=input('Temperature affichage RTD: ')
        if T=='':
            print('Mauvaise valeur, recommencer')
        elif T[0] not in chiffre or T[-1] not in chiffre:
            print('Mauvaise valeur, recommencer')
        else:
            break
    V=ut.mesure_v(para.daq_ports[f"thermi_{i}"])
    courbe.append((V,T))
    if str(input('Q pour quitter, enter pour continuer: '))=='Q':
        break

df = pd.DataFrame(courbe, columns=["V","T"])
print(df)

df.to_csv(param.etal_data_file_paths[f'thermi_{i}'])