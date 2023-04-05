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
    
    coef, cov = optimize.curve_fit(ut.v_to_temp, data["V"], data["T"], p0=param.coef_init_guess, maxfev=1000000)

    print(coef)
    print(param.coef_init_guess)
    
    np.savez(save_path, coef=coef, cov=cov)

    if plot_regression:
        x = np.linspace(0.5, 1.5, 1000)
        plt.plot(x, ut.v_to_temp(x, *coef), label="Régression", color="blue")
        plt.scatter(data["V"], data["T"], label="Données", color="red", s=2)
        plt.legend()
        plt.show()

if __name__ == "__main__":
    find_coef("thermi_ext", True)
