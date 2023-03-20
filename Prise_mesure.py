import numpy as np ; import math as mt
import time ;
import nidaqmx
from nidaqmx.stream_readers import AnalogSingleChannelReader, AnalogMultiChannelReader
from nidaqmx.constants import (BridgeConfiguration, VoltageUnits, 
                               BridgeUnits, AcquisitionType)
import Parameters as para

import matplotlib.pyplot as plt
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


def GET_V(freq = float, channel_list = list, nb_samples = bool, task = nidaqmx.Task()):     
    
    """Insérer une list de str des ports AI
    qu'on veut utiliser  ex: ["myDAQ1/ai0", "myDAQ1/ai1"]
    
    Entrer l'argument True si on veux un nombre
      spécifique d'échantillons pour les ports sélectionnés"""
    
    for channel in channel_list:
        task.ai_channels.add_ai_voltage_chan(
            physical_channel=channel, min_val=0.0,max_val=2.0,units=VoltageUnits.VOLTS) #init. AI channels
   
    task.timing.cfg_samp_clk_timing(freq, sample_mode = AcquisitionType.CONTINUOUS)

    if nb_samples == True:
        nb = 1
        nb_ask = input("ENTRER LE NOMBRE D'ÉCHANTILLON(S) :   ") ; nb_ask = int(nb_ask)
        while nb <= nb_ask: