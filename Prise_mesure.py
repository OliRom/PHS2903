import numpy as np
import time
import nidaqmx
from nidaqmx.constants import (BridgeConfiguration, VoltageUnits, BridgeUnits, AcquisitionType)
import matplotlib.pyplot as plt
###############################################################################################################################################

## Nom des différents ports physiques (id) [ces informations peuvent être changées dans NI MAX]: myDAQ1/ai0 ; myDAQ1/ai1 ; myDAQ1/ao0 ; myDAQ1/ao1
##                                                                                     myDAQ1/audioOutputLeft ; myDAQ1/audioOutputRight

# L-->  https://www.ni.com/docs/fr-FR/bundle/ni-daqmx/page/mxdevconsid/mydaqphyschanns.html

## Limites d'entrée (valeurs maximales et minimales)
# L--> https://www.ni.com/docs/fr-FR/bundle/ni-daqmx/page/measfunds/limitsettings.html 

# Demander au prof si on peut configurer un gain avec nidaqmx pour les entrées analogiques

# Chercher de l'info pour de la lecture en simultané de plusieurs ports analogiques

###############################################################################################################################################

#Conditions d'échantillonnage

task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan(physical_channel="myDAQ1/ai0", min_val=0.000000,max_val=1.900000,units=VoltageUnits.VOLTS)
task.timing.cfg_samp_clk_timing(10, sample_mode = AcquisitionType.CONTINUOUS)
task.start()
      #Bug potentiel dans l'appel de constants.
sample = 0
while sample <1000:
    data = task.read()  
    print(data)
    sample = sample + 1
task.stop()
task.close()