from scipy import optimize
import Utils as ut
import pandas as pd
import Parameters as param
import numpy as np
import matplotlib.pyplot as plt


def find_coef(therm, plot_regression=False):
    data_path = param.etal_data_file_paths[therm]
    save_path = param.coef_file_paths[therm]

    data = pd.read_csv(data_path)
    
    coef, cov = optimize.curve_fit(ut.v_to_temp, data["V"], data["T"], param.coef_init_guess)
    
    np.savez(save_path, coef=coef, cov=cov)

    if plot_regression:
        x = np.arange(1, 11)
        plt.plot(x, ut.v_to_temp(x, *coef), label="Régression")
        plt.scatter(data["V"], data["T"], label="Données")
        plt.legend()
        plt.show()

2 weeks ago2 weeks ago2 weeks ago
if __name__ == "__main__":
    find_coef("thermi_1", True)
