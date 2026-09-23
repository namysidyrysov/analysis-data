""" Скрипт для построения 3d карты. 
Анализируется osa спектры двухволного лазера.

    """

import numpy as np
import os
from tqdm import tqdm
from scripts.read_txt_file import read_txt_xy
from scripts.plot_3d_spectra import plot_3d_spectra
from scripts.convert_dBm_mW import convert_dbm_to_mw




LINEWIDTHS = [2,1,3]
WAVELENGTH_START = 1056
WAVELENGTH_STOP = 1071  # Последний элемент не включается
WAVELENGTH_STEP = 1
WAVELENGTHS = np.arange(WAVELENGTH_START, WAVELENGTH_STOP, WAVELENGTH_STEP)

NUMBER_ITERATIONS = 40
# MEGA=1e+6
ITERATION_LABEL="Iteration (N)"
# FREQ_LABEL_MHZ='Frequency (MHz)'
WAVE_LABEL='Wavelength (nm)'
# POWER_LABEL_DBM = 'Power (dBm)'
# POWER_LABEL_MILLI_W= "Power (mW)"
POWER_LABEL_MICRO_W = "Power (μW)"

# Папка, где лежат данные 
DATA_FOLDER=rf'C:\Users\namys\Documents\DATA_dual_wavelength_laser\ВАЖНО_LD_set_I_9.83A_Sep-19-2026_time_12-44-22'

PEAK_CONFIG = {
    'Yb':   dict(wave_start=1000, wave_stop=1100, fwhm=1.4),
    'P205': dict(wave_start=1200, wave_stop=1300, fwhm=3.1),
}
PEAK = 'Yb'




def crop_wavelength_range(wave_arr, power_arr, wave_start, wave_stop):
    
    mask = (wave_arr >= wave_start) & (wave_arr <= wave_stop)
    new_power_arr = power_arr[mask]
    new_wave_arr = wave_arr[mask]
    
    return new_wave_arr, new_power_arr

def main():
    for linewidth in LINEWIDTHS:
        
        wave_start = PEAK_CONFIG[PEAK]['wave_start']
        wave_stop  = PEAK_CONFIG[PEAK]['wave_stop']
        wave_fwhm  = PEAK_CONFIG[PEAK]['fwhm']
        
        SAVE_FOLDER=rf'{DATA_FOLDER}\OSA-3D-Graphs-{PEAK}\{linewidth}nm'
        
        for wavelength in tqdm(WAVELENGTHS, desc=f"Processing LW {linewidth}nm"):
            
            power_2d_arr = []
            wave_2D_arr = []
            amplitude_data, wave_data = [], []
                
            for iteration in range(1, NUMBER_ITERATIONS+1):
                
                osa_txt_file = fr'{DATA_FOLDER}\OSA_lin_port_3\{linewidth}nm\{wavelength}nm\OSA_lin_{iteration}_{wavelength}nm_{linewidth}nm.txt'
                
                wave_arr, power_arr = read_txt_xy(file_path=osa_txt_file)
                
                
                wave_arr = np.array(wave_arr)
                power_arr = np.array(power_arr)
                # Перевод на линейный масштаб
                # power_arr = convert_dbm_to_mw(power_arr_dbm=power_arr)
                
                # Перевод на мкВт
                power_arr = power_arr*1000
                
                # Фильтруем по первичному диапазону
                wave_arr_2, power_arr_2 = crop_wavelength_range(wave_arr=wave_arr, 
                                                    power_arr=power_arr, 
                                                    wave_start=wave_start, 
                                                    wave_stop=wave_stop)
                
                # Находим глобальный пик внутри этого диапазона
                max_index = np.argmax(power_arr_2)
                max_wave = wave_arr_2[max_index]
                max_pow = power_arr_2[max_index]
                
                new_wave_start = max_wave - wave_fwhm
                new_wave_stop = max_wave + wave_fwhm
                
                wave_arr_3, power_arr_3 = crop_wavelength_range(wave_arr=wave_arr_2, 
                                                    power_arr=power_arr_2, 
                                                    wave_start=new_wave_start, 
                                                    wave_stop=new_wave_stop)

                # Добавляем в итоговый список
                power_2d_arr.append(power_arr_3)
                wave_2D_arr.append(wave_arr_3)
                
                amplitude_data.append(max_pow)
                wave_data.append(max_wave)
                
            # Вычисление статистики
            avg_center_wave = np.average(wave_data)
            std_center_wave = np.std(wave_data)
            cv_center_wave = std_center_wave/avg_center_wave
            
            avg_max_ampl = np.average(amplitude_data)
            std_max_ampl = np.std(amplitude_data)
            cv_max_ampl = std_max_ampl/avg_max_ampl
            
            plot_title = '\n'.join([
                        f"LW filter: {linewidth}nm, WL filter: {wavelength}nm,",
                        f'AVG WL: {avg_center_wave:.3f}, STD WL: {std_center_wave:.3f} CV: {cv_center_wave*100:.4f}%,',
                        f"AVG Ampl: {avg_max_ampl:.3f}, STD Ampl: {std_max_ampl:.3f}, CV: {cv_max_ampl*100:.4f}%"
                        ])

            file_name = f'{wavelength}nm_{linewidth}nm'
            
            plot_3d_spectra(
                wave_2D_arr=wave_2D_arr, 
                power_2D_arr=power_2d_arr, 
                wave_label=WAVE_LABEL,
                powers_label=POWER_LABEL_MICRO_W, 
                y_label=ITERATION_LABEL,
                folder_path=SAVE_FOLDER, 
                file_name=file_name,
                title = plot_title
            )
                
                
if __name__=="__main__":
    main()