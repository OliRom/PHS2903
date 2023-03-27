import nidaqmx as ni
import pandas as pd
import numpy as np
import Parameters as param

i= int(input('Numero de la thermistance (1 ou 2): '))
courbe = []
chiffre=[f'{j}' for j in range(10)]

while True:
    T=input('Q: quitter D: supprimer R: relecture. float: Température RTD.  ')
    if T=='Q' or T=='q':
        break
    elif T=='D' or T=='d':
        courbe.pop(-1)
    elif T=='R' or T=='r':
        print(courbe[-3:])
    else:
        try:
            float(T)
        except:
            print('Mauvaise valeur')
        else:
            V=ut.mesure_v(para.daq_ports[f"thermi_{i}"])
            courbe.append((V,T))

df = pd.DataFrame(courbe, columns=["V","T"])
print(df)

df.to_csv(param.etal_data_file_paths[f'thermi_{i}'])