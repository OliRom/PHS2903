import os


data_path = os.path.join("data")

etalon_path = os.path.join(data_path, "etalonnage_v_t")
etal_data_file_paths = {
    "thermi_1": os.path.join(etalon_path, "thermi_1.csv"),
    "thermi_2": os.path.join(etalon_path, "thermi_2.csv"),
    "thermi_ext": os.path.join(etalon_path, "thermi_ext.csv"),
}

coef_path = os.path.join(data_path, "coefficients")
coef_file_paths = {
    "thermi_1": os.path.join(coef_path, "thermi_1.npz"),
    "thermi_2": os.path.join(coef_path, "thermi_2.npz"),
    "thermi_ext": os.path.join(coef_path, "thermi_ext.npz"),
}

meas_path = os.path.join(data_path, "measurement")
meas_file_paths = {
    "data": os.path.join(meas_path, "data.csv"),
    "results": os.path.join(meas_path, "results.npz"),
}

daq_ports = {
    "thermi_1": "mydaq1/ai0",
    "thermi_2": "myDAQ1/ai1",
    "power": 3,
}

coef_init_guess = [
    0.00113,  # a
    0.000235,  # b
    8.57e-8,  # c
    15,  # e
    115e3,  # r
]

T_max = 40  # Température maximale
m_Ga = 50  # Masse du gallium
c_recipient = 10  # Capacité thermique du récipient [J/(g K)]
