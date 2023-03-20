import math as mt
print(mt.log(2.71,10.0))

"""from tkinter import Tk

window = Tk()

def do_something():
    print("doing something!")
    window.after(1000, do_something)  # every 1000 milliseconds

# start the do_something function immediately when the window starts
window.after(0, do_something)

window.mainloop()"""













"""def analog_setup(freq_0 = float, freq_1 = float, id_ai0 = str, id_ai1 = str, bool_ai0 = bool,
                  bool_ai1 = bool, T_max = float):

    task_ai0 = nidaqmx.Task()
    task_ai1 = nidaqmx.Task()
    cas1 = None ; cas2 = None ; cas3 = None
    if (bool_ai0 == True) and (bool_ai1 == True):
        task_ai0.ai_channels.add_ai_voltage_chan(
            physical_channel=id_ai0, min_val=0.0,max_val=2.0,units=VoltageUnits.VOLTS) #init. AI0
        task_ai1.ai_channels.add_ai_voltage_chan(
            physical_channel=id_ai1, min_val=0.0,max_val=2.0,units=VoltageUnits.VOLTS) #init. AI1
        cas1 = True
    elif (bool_ai0 == True) and (bool_ai1 == False):
        task_ai0.ai_channels.add_ai_voltage_chan(
            physical_channel=id_ai0, min_val=0.0,max_val=2.0,units=VoltageUnits.VOLTS) #init. AI0
        cas2 = True
    elif (bool_ai0 == False) and (bool_ai1 == True):
        task_ai1.ai_channels.add_ai_voltage_chan(
            physical_channel=id_ai1, min_val=0.0,max_val=2.0,units=VoltageUnits.VOLTS) #init. AI1
        cas3 = True
        
    task_ai0.timing.cfg_samp_clk_timing(freq_0, sample_mode = AcquisitionType.CONTINUOUS)
    task_ai1.timing.cfg_samp_clk_timing(freq_1, sample_mode = AcquisitionType.CONTINUOUS)     #Cette ligne doit être après l'init. des AI

    task_ai0.start()
    task_ai1.start()

    T = 0
    while T < 1000:                                 # Modifier 1000 pour T_max
        data_0 = task_ai0.read(number_of_samples_per_channel = 1)     #Afficher data sur GUI
        data_1 = task_ai1.read(number_of_samples_per_channel = 1)
        #convertir les tensions list en float
        if cas1 == True:
            V0 = data_0[0]
            V1 = data_1[0]
            print(V0,"v   ",V1,"v")
        elif cas2 == True:
            V0 = data_0[0]
            print(V0,"V")
        elif cas3 == True:
            V1 = data_1[0]
            print(V1,"V")
        #Insérer équation de température en fonction de voltage provenant de l'étallonnage
        T = T + 1

    task_ai0.stop() ; task_ai1.stop()
    task_ai0.close() ; task_ai1.close()"""