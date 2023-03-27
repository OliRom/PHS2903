import nidaqmx as ni
import pandas as pd
import numpy as np
import Parameters as param

i= int(input('Numero de la thermistance (1 ou 2): '))
courbe = []
print(courbe)

while True:
    T= float(input('Temperature affichage RTD: '))
    V=ut.mesure_v(para.daq_ports[f"thermi_{i}"])
    courbe.append((V,T))
    if str(input('Q pour quitter, enter pour continuer: '))=='Q':
        break

df = pd.DataFrame(courbe, columns=["V","T"])
print(df)

df.to_csv(param.etal_data_file_paths[f'thermi_{i}'])