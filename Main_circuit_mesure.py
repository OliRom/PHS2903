import numpy as np ; import math as mt
import time ;
import nidaqmx
from nidaqmx.stream_readers import AnalogSingleChannelReader, AnalogMultiChannelReader
from nidaqmx.constants import (BridgeConfiguration, VoltageUnits,
                               BridgeUnits, AcquisitionType)
import Parameters as para
###############################################################################################################################################



###############################################################################################################################################
#CONSTANTE
Tmax = 40

#PROGRAMME PRINCIPAL
def main():
    #Note le temps de départ dans la variable temps_debut#
    temps_debut = time.time_ns()

    #TODO mesurer la température initiale
    Température = 0

    #On fixe la puissance fournie à l'élément chauffant
    'set_power(puissance)'

    while Temperature <= Tmax:

        #Mesurer tension des thermistances
        'V1,V2 = mesurer_V(port1), mesurer_V(port2)'

        #Convertir tension en température
        'T1, T2 = v_to_temp(V1,a,b,c),v_to_temp(V2,a,b,c)'

        #Prendre en note la valeur du temps lors de la mesure
        temps = time.time_ns() - temps_debut

        #Mesure de la température moyenne
        'Tmoyen = (T1+T2)/2'

        #Mesurer la tension de l'élément chauffant
        'Vp = mesurer_V(port3)'

        #Calculer la puissance fournie
        'P = V_to_power(Vp,R)'

        #Ajoute les valeurs à notre liste de données
        'data.append(temps,T1,T2,Tmoyen,P)'

        #Envoyer la température moyenne au Arduino
        'send(Tmoyen)'

        #On attend 0.1 secondes entre chaque mesure
        time.sleep(0.1)

    #Calculer l'enthalpie de fusion avec toutes les température moyenne et la puissance
    'enthalpie = Calculer_enthalpie(Tmoyen,P,t)'

    #Calculer la capacité thermique
    'capacité = Calculer_capacité(Tmoyen,P,t)'

    #Enregistrer les données
    'Enregistrer(data)'

    #Afficher la courbe de température en fonction du temps
    'plot_data()'

#Todo FONCTION QUI RETOURNE LA VALEUR DE VOLTAGE AU PORT SELECTIONNÉ
def mesurer_V(Port):

    voltage = 0

    return voltage















