import numpy as np

def convert_mw_to_dbm(pow_arr_mw):
    """ Функция переводит массив из mW в массив dBm.

    Args:
        pow_arr_mw (array): Массив мощности в mW

    Returns:
        array: Массив мощности в dBm
    """
    return 10 * np.log10(pow_arr_mw)
    

def convert_dbm_to_mw(pow_arr_dbm):
    """ Функция переводит массив из dBm в массив mW.

    Args:
        pow_arr_dbm (array): Массив мощности в dBm

    Returns:
        array: Массив мощности в mW
    """
    return 10 ** (pow_arr_dbm / 10)