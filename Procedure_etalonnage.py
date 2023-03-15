import nidaqmx as ni
import pandas as pd
import numpy as np
import Parameters as param

therm=1

def V(x): #tension de thermistance sur myDAQ
    return x

def T(x): #temperature selon RTD
    return x


list = []
print(list)

tuple=(1,2)

for i in range(10):
    list.append((V(i),T(i)))

df=pd.DataFrame(list, columns=["V","T"])
print(df)

df.to_csv(param.etal_data_file_paths[therm])