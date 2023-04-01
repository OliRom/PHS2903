import time
import Utils as ut
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import Parameters as para

colonnes = ["thermi_2","thermi_ext"]
data1 = pd.read_csv(para.etal_data_file_paths[colonnes[0]])
data2 = pd.read_csv(para.etal_data_file_paths[colonnes[1]])

plt.plot(data1["T"],data1["V"],label=colonnes[0])
plt.plot(data2["T"],data2["V"],label=colonnes[1])
plt.legend()
plt.show()

