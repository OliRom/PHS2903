import numpy as np ; import math as mt
import time ;
import nidaqmx
from nidaqmx.stream_readers import AnalogSingleChannelReader, AnalogMultiChannelReader
from nidaqmx.constants import (BridgeConfiguration, VoltageUnits,
                               BridgeUnits, AcquisitionType)
import Parameters as para
###############################################################################################################################################

"""Nom des différents ports physiques (id) [ces informations peuvent être changées dans NI MAX]: 
myDAQ1/ai0 ; myDAQ1/ai1 ; myDAQ1/ao0 ; myDAQ1/ao1
myDAQ1/audioOutputLeft ; myDAQ1/audioOutputRight

L-->  https://www.ni.com/docs/fr-FR/bundle/ni-daqmx/page/mxdevconsid/mydaqphyschanns.html

 Limites d'entrée (valeurs maximales et minimales)
L--> https://www.ni.com/docs/fr-FR/bundle/ni-daqmx/page/measfunds/limitsettings.html 

Demander au prof si on peut configurer un gain avec nidaqmx pour les entrées analogiques

Chercher de l'info pour de la lecture en simultané de plusieurs ports analogiques"""

###############################################################################################################################################