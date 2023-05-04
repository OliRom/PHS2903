import numpy as np
import Parameters as para
import pandas as pd


def compute_c(data, m, c_r):
    """
    Calcule la capacité thermique en fonction de la température.

    :param data: données prises lors de la mesure
    :param m: masse du gallium (g)
    :param c_r: capacité thermique du récipient [J/(g K)]
    :return: matrice contenant la capacité thermique pour différentes températures
    """

    t, T, p, T1, T2 = data["t"].to_numpy(), data["T1"].to_numpy(), data["T2"].to_numpy(), data["T"].to_numpy(), data[
        "p"].to_numpy()
    dT_dt = np.diff(T) / np.diff(t)
    c = (p[:-1] / dT_dt - c_r) / m

    p_shifted = p[1:-1]  # Ajustement de la taille de p, car np.diff(2) réduit la taille de la matrice par 2
    dT_dt_shifted = (dT_dt[:-1] + dT_dt[
                                  1:]) / 2  # Ajustement de la taille de dT-dt, car np.diff() réduit la taille de la matrice par 1
    T1_shifted = T1[1:-1]  # Ajustement de la taille de T1, car np.diff(2) réduit la taille de la matrice par 2
    T2_shifted = T2[1:-1]  # Ajustement de la taille de T2, car np.diff(2) réduit la taille de la matrice par 2
    T_shifted = T[1:-1]  # Ajustement de la taille de T, car np.diff(2) réduit la taille de la matrice par 2
    c_shifted = (c[:-1] + c[
                1:]) / 2  # Ajustement de la taille de c, car np.diff() réduit la taille de la matrice par 1

    alpha_c = c_shifted * ((para.a_p(p_shifted) / p_shifted) ** 2 + (
                para.a_T(T1_shifted, T2_shifted) * np.diff(T, 2) / (dT_dt_shifted) ** 2) * 2 + (
                               para.a_m / m) ** 2) ** 0.5
    #alpha_c = c_shifted * ((para.a_p(p_shifted) / p_shifted) ** 2 + (
            #para.a_T(T1_shifted, T2_shifted) * np.diff(T, 2) / (dT_dt_shifted) ** 2) * 2 + (
                           #para.a_m / m) ** 2) ** 0.5

    return np.c_[T_shifted, c_shifted, alpha_c]


def compute_t_h_fusion(data, m):
    """
    Calcule la Température de fusion ainsi que l'enthalpie de fusion.

    :param data: données prises lors de la mesure
    :param m: masse de gallium
    :return: tuple contenant la température de fusion et l'enthalpie de fusion
    """

    t, T, p = data["t"].to_numpy(), data["T"].to_numpy(), data["p"].to_numpy()
    E = np.cumsum(p[:-1] * np.diff(t))  # P = dE/dt => dE = P * dt => E = cumsum(dE)

    dT_dE = np.diff(T[:-1]) / np.diff(E)
    courbure_dT_dE = np.diff(dT_dE, n=2) / np.diff(E[:-1], n=2)  # Courbure de dT_dE

    mini, maxi = np.argmin(courbure_dT_dE) + 2, np.argmax(courbure_dT_dE) + 2  # Extrémités du plateau de température
    h_fusion = (E[maxi] + E[maxi - 1] - E[mini] - E[mini - 1]) / (2 * m)  # (h_max_moyen - h_min_moyen) / m, h = E

    T_fusion_arr = T[mini: maxi + 1]
    T_fusion = np.mean(T_fusion_arr)

    return T_fusion, h_fusion


def compute_all_results(data_path, saving_path, m, c_r):
    """
    Calcule tous les résultats souhaités et les enregistre dans un fichier .npz.

    :param data_path: path vers le fichier des mesures prises
    :param saving_path: path où enregistrer les résultats
    :param m: masse du gallium
    :param c_r: capacité thermique du récipient [J/(g K)]
    :return: None
    """

    data = pd.read_csv(data_path)
    c_selon_T = compute_c(data, m, c_r)
    T_fusion, h = compute_t_h_fusion(data, m)

    np.savez_compressed(saving_path, c_selon_T=c_selon_T, T_fusion=T_fusion, h_fusion=h)


if __name__ == "__main__":
    m, c_r = para.m_Ga, para.c_recipient
    data_path, saving_path = para.meas_file_paths["data"], para.meas_file_paths["results"]

    compute_all_results(data_path, saving_path, m, c_r)
