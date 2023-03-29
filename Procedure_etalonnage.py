import nidaqmx as ni
import pandas as pd
import numpy as np
import Parameters as param

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

courbe1=[]
courbe2=[]
while True:
    i1=int(input('Numero de la première thermistance (3 pour ext): '))
    if i1 in (1,2,3):
        thermi= {i1:courbe1}
        break
    print('Mauvaise valeur')
while True:
    i2=int(input('Numero de la deuxième thermistance (3 pour ext, 0 si aucune): '))
    if i2==0:
        break
    elif i2==i1:
        print('Valeur déjà utilisée')
    elif i2 in (1,2,3):
        thermi[i2]=courbe2
        break
    else:
        print('Mauvaise valeur')

while True:
    T=input('Q: quitter D: supprimer R: relecture. float: Température RTD.  ')
    if T=='Q' or T=='q':
        break
    elif T=='D' or T=='d':
        for i in thermi:
            thermi[i].pop(-1)
    elif T=='R' or T=='r':
        for i in thermi:
            print(f'thermi{i}: {thermi[i][-3:]}')
    else:
        try:
            float(T)
        except:
            print('Mauvaise valeur')
        else:
            for i in thermi:
                V=ut.mesure_v(para.daq_ports[f"thermi_{i}"])
                thermi[i].append((V,float(T)))

for i in thermi:
    df=pd.DataFrame(thermi[i], columns=["V","T"])
    print(f'Courbe thermi{i}')
    print(df)
    df.to_csv(param.etal_data_file_paths[f'thermi_{i}'])