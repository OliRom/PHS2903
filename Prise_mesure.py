import numpy as np ; import math as mt
import time ;
import nidaqmx
from nidaqmx.stream_readers import AnalogSingleChannelReader, AnalogMultiChannelReader
from nidaqmx.constants import (ResolutionType, VoltageUnits, 
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


def GET_V(channel_list, sample_request, freq):     
    
    """Insérer une list de str des ports AI
    qu'on veut utiliser  ex: ["myDAQ1/ai0", "myDAQ1/ai1"]
    
    Entrer l'argument True si on veux un nombre
      spécifique d'échantillons pour les ports sélectionnés"""
    
    # init. AI channels
    
    task = nidaqmx.Task()

    for channel in channel_list:
        task.ai_channels.add_ai_voltage_chan(
            physical_channel=channel, min_val=0.0,max_val=2.0,units=VoltageUnits.VOLTS)    
            #"myDAQ1/ai{}".format(channel), min_val=0.0,max_val=2.0,units=VoltageUnits.VOLTS) 
            # version alternative avec [0,1]

            
    # Spécification lecture DAQ
    
    task.timing.cfg_samp_clk_timing(freq, sample_mode = AcquisitionType.CONTINUOUS)
    task.start()

    # Affichage du nombre d'échantillons de tension fini
    
    if sample_request == True:
        nb = 0
        nb_ask = input("ENTRER LE NOMBRE D'ÉCHANTILLON(S) :   ") ; nb_ask = int(nb_ask)
        while nb <= nb_ask:
            data = task.read(number_of_samples_per_channel = 1)
            V0 = data[0][0] ; V1 = data[1][0]
            nb = nb + 1
            print(f'Hot : {V0},   Cold : {V1}')
            return V0, V1
    
    # Affichage et enregistrement des échantillions de tensions continus pour la fonction principale
    
    else:
        V_ref = 0.0
        while V_ref < 2.0:
            data = task.read(number_of_samples_per_channel = 1)                                          
            V0 = data[0][0] ; V1 = data[1][0]
            V_ref = V1
            print(f'Hot : {V0} V,   Cold : {V1} V')
            return V0, V1


    task.stop()
    task.close()
# Fonction pour trouver la résistance
    
def GET_R(R1, VS, channel_list, sample_request, freq):
    V0, V1 =  GET_V(channel_list, sample_request, freq)
    RT0 = R1*(1/((VS/V0)-1.0))
    RT1 = R1*(1/((VS/V1)-1.0))
    return RT0,RT1

# Fonction pour trouver la température

def GET_T(a,b,c, channel_list, sample_request, freq):

    RT0,RT1 = GET_R(115000.0,15.0, channel_list, sample_request, freq)
    T0 = 1/(a+(b*mt.log(RT0)) + (c*(mt.log(RT0))**3))
    T1 = 1/(a+(b*mt.log(RT1)) + (c*(mt.log(RT1))**3))
    print(f'Hot : {T0} °K,   Cold : {T1} °K')

# Test
GET_T(*para.coef_init_guess[:3], ["myDAQ1/ai0", "myDAQ1/ai1"], False, 10.0)
#GET_V(["myDAQ1/ai0", "myDAQ1/ai1"], False, 10.0)
#GET_R(115000.0, 15.0, ["myDAQ1/ai0", "myDAQ1/ai1"], False, 10.0)

# Bug à régler : Comment utiliser autre chose qu'un return car ça brise la boucle