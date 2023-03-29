import nidaqmx as ni
import pandas as pd
import numpy as np
import Parameters as param
import Utils as ut

#i= int(input('Numero de la thermistance (1 ou 2): '))
#courbe = []
#
#while True:
#    T=input('Q: quitter D: supprimer R: relecture. float: Température RTD.  ')
#    if T=='Q' or T=='q':
#        break
#    elif T=='D' or T=='d':
#        courbe.pop(-1)
#    elif T=='R' or T=='r':
#        print(courbe[-3:])
#    else:
#        try:
#            float(T)
#        except:
#            print('Mauvaise valeur')
#        else:
#            V=ut.mesure_v(para.daq_ports[f"thermi_{i}"])
#            courbe.append((V,T))
#
#df = pd.DataFrame(courbe, columns=["V","T"])
#print(df)
#
#df.to_csv(param.etal_data_file_paths[f'thermi_{i}'])

courbe1 = []
courbe2 = []
thermi = dict()

while True:
    i1=input('Numero de la première thermistance (1, 2 ou ext): ')
    if i1 in ("1", "2", "ext"):
        thermi[i1] = courbe1
        break
    print('Mauvaise valeur')
while True:
    i2 = input('Numero de la deuxième thermistance (1, 2 ou ext; 0 si aucune): ')
    if i2=="0":
        break
    elif i2==i1:
        print('Valeur déjà utilisée')
    elif i2 in ("1", "2", "ext"):
        thermi[i2] = courbe2
        break
    else:
        print('Mauvaise valeur')

while True:
    T=input('Q: quitter D: supprimer R: relecture. float: Température RTD.  ')
    if T=='Q' or T=='q':
        break
    elif T=='D' or T=='d':
        for i in thermi.keys():
            thermi[i].pop(-1)
    elif T=='R' or T=='r':
        for i in thermi.keys():
            print(f'thermi{i}: {thermi[i][-3:]}')
    else:
        try:
            float(T)
        except:
            print('Mauvaise valeur')
        else:
            for i in thermi:
                V=ut.mesure_v(param.daq_ports[f"thermi_{i}"])
                thermi[i].append((V,float(T)))

for key, val in thermi.items():
    df=pd.DataFrame(val, columns=["V","T"])
    print(f'Courbe thermi[{key}]')
    print(df)
    df.to_csv(param.etal_data_file_paths[f'thermi_{key}'])