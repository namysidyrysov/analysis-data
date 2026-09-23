import numpy as np

def convert_mw_to_dbm(power_arr_mw):
    """ Функция переводит массив из mW в массив dBm.

    Args:
        power_arr_mw (array): Массив мощности в mW

    Returns:
        array: Массив мощности в dBm
    """
    return 10 * np.log10(power_arr_mw)
    

def convert_dbm_to_mw(power_arr_dbm):
    """ Функция переводит массив из dBm в массив mW.

    Args:
        power_arr_dbm (array): Массив мощности в dBm

    Returns:
        array: Массив мощности в mW
    """
    return 10 ** (power_arr_dbm / 10)
