import numpy as np
from tqdm import tqdm

from scripts.read_txt_file import read_txt_xy
from scripts.plot_xy import plot_xy_markers
from scripts.write_data_txt import write_txt_xy
LINEWIDTHS = [2]
CURRENT = 9.83

WAVELENGTH_START = 1056
WAVELENGTH_STOP = 1071  # Последний элемент не включается
WAVELENGTH_STEP = 1
WAVELENGTHS = np.arange(WAVELENGTH_START, WAVELENGTH_STOP, WAVELENGTH_STEP)

NUMBER_ITERATIONS=40
MEGA=1e+6
x_label="Iteration (N)"
y_label='Frequency (MHz)'

# Диапазон поиска пика (в МГц)
MAX_FREQ_START = 150 
MAX_FREQ_STOP = 650





# Папка, где лежат данные   
DATA_FOLDER=rf'C:\Users\namys\Documents\DATA_dual_wavelength_laser\LD_set_current_9.83A_September-13-2026_time_10-18-08'

for linewidth in LINEWIDTHS:
    SAVE_FOLDER=rf'{DATA_FOLDER}\graphs\linewidth_{linewidth}nm'
    for wavelength in tqdm(WAVELENGTHS, desc=f"Processing LW {linewidth}nm"):
        
        # Формирование имя файлов
        filename=f'freq_vs_time_linewidth_{linewidth}nm_wavelength_{wavelength}nm'
        png_title=f'LW={linewidth}nm, WL={wavelength}nm, I={CURRENT}A'
                
        iteration_arr, max_freq_arr = [], []
        
        for iteration in range(1, NUMBER_ITERATIONS+1):
                
            rf_txt_file=rf"{DATA_FOLDER}\RF\linewidth_{linewidth}nm\wavelength_{wavelength}nm\span_6000.0MHz\rf_iteration_{iteration}_wavelength_{wavelength}nm_linewidth_{linewidth}nm_current_{CURRENT}A_span_6000.0MHz.txt"
        
            freq_arr, pow_arr = read_txt_xy(file_path=rf_txt_file)
            
            
            # ЛОГИКА ОГРАНИЧЕНИЯ ДИАПАЗОНА ПОИСКА
            # Переводим границы поиска из МГц обратно в Гц (как в исходном файле)
            start_hz = MAX_FREQ_START * MEGA
            stop_hz = MAX_FREQ_STOP * MEGA
            
            # Создаем маску: True для элементов, попавших в диапазон
            mask = (freq_arr >= start_hz) & (freq_arr <= stop_hz)
            
            # Проверяем, есть ли вообще точки в этом диапазоне, чтобы не упасть с ошибкой
            if not np.any(mask):
                print(f"\n[Warning] No data points found in range {MAX_FREQ_START}-{MAX_FREQ_STOP} MHz for iteration {iteration}")
                continue
            
            # Фильтруем массивы по маске
            sub_freq = freq_arr[mask]
            sub_pow = pow_arr[mask]
            
            # Ищем пик только внутри обрезанного диапазона мощности
            max_sub_index = np.argmax(sub_pow)
            
            # Берем частоту, соответствующую этому пику
            max_freq = sub_freq[max_sub_index] / MEGA
            
            max_freq_arr.append(max_freq)
            iteration_arr.append(iteration)
            

        
        plot_xy_markers(
            x=iteration_arr, 
            y=max_freq_arr, 
            title=png_title, 
            xlabel=x_label, 
            ylabel=y_label, 
            folder_path=SAVE_FOLDER, 
            filename=filename, 
            show_plot=False
        )

        write_txt_xy(
            x_arr=iteration_arr,
            x_label=x_label,
            y_arr=max_freq_arr,
            y_label=y_label,
            header=None,
            folder_path=SAVE_FOLDER,
            filename=filename,
        )
        
        iteration_arr, max_freq_arr = [], []
    
        
        
