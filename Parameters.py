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
    "thermi_1": os.path.join(coef_path, "thermi_1"),
    "thermi_2": os.path.join(coef_path, "thermi_2"),
    "thermi_ext": os.path.join(coef_path, "thermi_ext"),
}

coef_init_guess = [
    0.00113,  # a
    0.000235,  # b
    8.57e-8,  # c
    15,  # e
    115e3,  # r
]