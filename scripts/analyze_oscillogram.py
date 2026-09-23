""" 
Скрипт автоматически анализирует осциллограммы, используя find_peaks для поиска максимумов и минимумов сигнала. 
На основе экстремумов вычисляются амплитуда, период, частота, а 
также статистические показатели: стандартные отклонения и коэффициенты вариации. 
Для каждой осциллограммы строится график с маркировкой пиков и панелью статистики. 
Скрипт поддерживает пакетную обработку данных по диапазонам токов и задержек, фильтрацию
по пороговым критериям и автоматическое сохранение результатов в виде отдельных 
графиков и общей тепловой карты частот. 
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from tqdm import tqdm
from scripts.read_from_txt import read_txt_xy
from scripts.create_folder import create_date_folder
from scripts.create_map_and_save import create_map_and_save
import os








def analyze_oscillogram(time_arr, voltage_arr, height=None, distance=10, prominence=0.015):
    """Анализирует осциллограмму для поиска экстремумов и расчета характеристик сигнала.

    Функция находит локальные максимумы и минимумы в сигнале напряжения, 
    а затем рассчитывает среднюю амплитуду, частоту, периоды, а также 
    статистические показатели (стандартное отклонение и коэффициент вариации).

    Args:
        time_arr (np.ndarray): Массив значений времени (временная шкала).
        voltage_arr (np.ndarray): Массив значений напряжения (амплитуда сигнала).
        height (float, optional): Минимальная высота для поиска максимумов. 
            Если не задана, используется среднее значение `voltage_arr`.
        distance (int, optional): Минимальное расстояние в количестве точек 
            между соседними пиками. По умолчанию 10.
        prominence (float, optional): Минимальная выраженность (проминенс) 
            пиков для фильтрации шума. По умолчанию 0.005.

    Returns:
        dict: Словарь с результатами анализа, содержащий следующие ключи:
            - 'max_idx' (np.ndarray): Индексы локальных максимумов.
            - 'min_idx' (np.ndarray): Индексы локальных минимумов.
            - 'max_values' (np.ndarray): Значения напряжения в максимумах.
            - 'min_values' (np.ndarray): Значения напряжения в минимумах.
            - 'num_max' (int): Количество найденных максимумов.
            - 'num_min' (int): Количество найденных минимумов.
            - 'amplitude' (float): Размах сигнала (разность средних макс. и мин.).
            - 'mean_max' (float): Среднее значение максимумов.
            - 'mean_min' (float): Среднее значение минимумов.
            - 'std_max' (float): Стандартное отклонение максимумов.
            - 'std_min' (float): Стандартное отклонение минимумов.
            - 'cv_max' (float): Модуль коэффициента вариации максимумов.
            - 'cv_min' (float): Модуль коэффициента вариации минимумов.
            - 'periods' (np.ndarray): Массив периодов между соседними максимумами.
            - 'mean_period' (float): Средний период сигнала.
            - 'std_period' (float): Стандартное отклонение периода.
            - 'cv_period' (float): Коэффициент вариации периода.
            - 'frequency' (float): Средняя частота сигнала.
    """

    
    if height is None:
        height=np.mean(voltage_arr)
        
    # Максимумы
    max_idx, _ = find_peaks(x=voltage_arr,height=height,distance=distance, prominence=prominence)
    
    # Минимумы 
    min_idx, _ = find_peaks(x=-voltage_arr, height=-height, distance=distance, prominence=prominence)
    
    max_values = voltage_arr[max_idx]
    min_values = voltage_arr[min_idx]
    
    # Амплитуда
    
    if len(max_values)>0 and len(min_values)>0:
        mean_max = np.mean(max_values)
        mean_min = np.mean(min_values)
        
        amplitude = mean_max - mean_min
        
        std_max = np.std(max_values)
        std_min = np.std(min_values)    
        
        cv_max = std_max/mean_max if mean_max !=0 else np.nan  
        cv_min = std_min/mean_min if mean_min !=0 else np.nan  
        
    else:
        mean_max = np.nan
        mean_min = np.nan
        amplitude = np.nan
        std_max = np.nan
        std_min = np.nan
        cv_max = np.nan
        cv_min = np.nan
        
    # Периоды
    if len(max_idx)>1:
        periods = np.diff(time_arr[max_idx])
        mean_period=np.mean(periods)
        std_period = np.std(periods)
        cv_period = std_period/mean_period if mean_period !=0 else np.nan
        frequency=1/mean_period if mean_period !=0 else np.nan
    else:
        periods = np.array([])
        mean_period=np.nan
        std_period=np.nan
        cv_period = np.nan
        frequency = np.nan
        
    return{
        # пики
        'max_idx': max_idx,
        'min_idx': min_idx,
        
        "max_values": max_values,
        "min_values": min_values,
        
        "num_max": len(max_idx),
        "num_min": len(min_idx),
        
        # амплитуда
        "amplitude": amplitude,
        
        'mean_max': mean_max,
        'mean_min': mean_min,
        
        'std_max': std_max,
        'std_min': std_min,
        
        'cv_max': np.abs(cv_max),
        'cv_min': np.abs(cv_min),
        
        # период
        'periods': periods,
        'mean_period': mean_period,
        'std_period': std_period,
        'cv_period': cv_period,
        
        'frequency': frequency,
    }
        
    
def plot_oscillogram_with_statistics(time_arr, voltage_arr, stats, title="Title", save_path=None, filename=None):
    
    """Строит график осциллограммы с маркировкой экстремумов и выводом статистики.

    Функция визуализирует массив сигналов, отмечает на графике точки 
    максимумов  и минимумов , а также выводит 
    текстовую панель со статистическими данными из словаря `stats` 
    в три колонки в нижней части изображения.

    Args:
        time_arr (np.ndarray): Массив значений времени (временная шкала).
        voltage_arr (np.ndarray): Массив значений напряжения (амплитуда сигнала).
        stats (dict): Словарь с результатами расчета функции `analyze_oscillogram`. 
            Обязательно должен содержать ключи: 'max_idx', 'min_idx', 'num_max', 
            'num_min', 'mean_max', 'mean_min', 'amplitude', 'std_max', 'std_min', 
            'cv_max', 'cv_min', 'mean_period', 'std_period', 'cv_period', 'frequency'.
        title (str, optional): Заголовок графика. По умолчанию "Title".
        save_path (str, optional): Путь к папке для сохранения графика на диск. 
            Используется только совместно с аргументом `filename`. По умолчанию None.
        filename (str, optional): Имя файла (без расширения) для сохранения изображения. 
            Используется только совместно с аргументом `save_path`. По умолчанию None.

    Returns:
        None: Функция не возвращает значений. Она либо сохраняет график в файл 
            (если переданы `save_path` и `filename`), либо возвращает объект вызова 
            окна отображения .
    """

    # --- НАСТРОЙКА РАЗМЕРОВ ШРИФТОВ ---
    TITLE_FONT = 20      # Заголовок графика
    LABEL_FONT = 20       # Подписи осей X и Y
    TICK_FONT = 20        # Числа на осях координат
    LEGEND_FONT = 20      # Легенда (Maxima/Minima)
    STATS_FONT = 20      # Текст статистики в колонках
    # ----------------------------------

    fig = plt.figure(figsize=(16,9))

    
    gs = fig.add_gridspec(2, 1, height_ratios=[5, 1])
    
    # График
    ax1 = fig.add_subplot(gs[0])
    
    ax1.plot(time_arr, voltage_arr, color='black', lw=2)
    
    ax1.scatter(
        time_arr[stats['max_idx']],
        voltage_arr[stats['max_idx']],
        color='red',
        s=100,
        label='Maxima'
    )
    
    ax1.scatter(
        time_arr[stats['min_idx']],
        voltage_arr[stats['min_idx']],
        color='blue',
        s=100,
        label='Minima'
    )
    
    # Применение размеров шрифтов к графику
    ax1.set_title(title, fontsize=TITLE_FONT)
    ax1.set_xlabel("Time, ns", fontsize=LABEL_FONT)
    ax1.set_ylabel("Voltage, V", fontsize=LABEL_FONT)
    ax1.tick_params(axis='both', labelsize=TICK_FONT)
    
    ax1.grid(True)
    ax1.legend(fontsize=LEGEND_FONT)
    
    # Статистика в три колонки
    ax2 = fig.add_subplot(gs[1])
    
    # Колонка 1: Базовая информация о пиках
    col1_text = (
        f"number of max: {stats['num_max']}\n"
        f"number of min: {stats['num_min']}\n"
        f"mean_max: {stats['mean_max']:.6f} V\n"
        f"mean_min: {stats['mean_min']:.6f} V"
    )
    
    # Колонка 2: Амплитуда и отклонения уровней
    col2_text = (
        f"amplitude: {stats['amplitude']:.6f} V\n"
        f"std_max: {stats['std_max']:.6f} V\n"
        f"std_min: {stats['std_min']:.6f} V\n"
        f"cv_max: {stats['cv_max']:.6f}\n"
        f"cv_min: {stats['cv_min']:.6f}"
    )
    
    # Колонка 3: Временные параметры (Период)
    col3_text = (
        f"mean_period: {stats['mean_period']:.6f} ns\n"
        f"std_period: {stats['std_period']:.6f} ns\n"
        f"cv_period: {stats['cv_period']:.6f}\n"
        f"frequency: {stats['frequency']:.6f} GHz"
    )
    
    # Отрисовка трех колонок с применением STATS_FONT
    ax2.text(0.02, 0.5, col1_text, fontsize=STATS_FONT, va='center', ha='left', fontfamily='monospace')
    ax2.text(0.35, 0.5, col2_text, fontsize=STATS_FONT, va='center', ha='left', fontfamily='monospace')
    ax2.text(0.68, 0.5, col3_text, fontsize=STATS_FONT, va='center', ha='left', fontfamily='monospace')
    
    ax2.axis('off')
    
    plt.tight_layout()
    
    # ========================
    # СОХРАНЕНИЕ
    # ========================
    if save_path is not None and filename is not None:
        full_path = os.path.join(save_path, f"{filename}.png")
        plt.savefig(full_path, dpi=50, bbox_inches='tight')
        print(f"График сохранён в: {full_path}")
    else:
        plt.show()
    


if __name__=="__main__":
    
    
    CURRENT_START=100
    CURRENT_STOP=500
    CURRENT_STEP=20
    CURRENTS=np.arange(CURRENT_START, CURRENT_STOP, CURRENT_STEP)

    DELAY_START=0
    DELAY_STOP=331
    DELAY_STEP=5
    DELAYS=np.arange(DELAY_START, DELAY_STOP, DELAY_STEP)
    
    # Пороговые значения
    amplitude_thresh=0.02
    cv_period_thresh = 0.01
    cv_max_thresh=0.01
    cv_min_thresh=0.01
    
    
    save_folder=create_date_folder(base_path='',prefix='analyze_osc')
    
    
    current_data, delay_data, freq_data = [],[],[]
    for current in tqdm(CURRENTS, desc='Прогресс Current'):
        for delay in DELAYS:
            

            current_data.append(current)
            delay_data.append(delay)
        
            time_arr, voltage_arr = read_txt_xy(full_path=f'oscilloscope_measurements\current_{current}mA\osc_average_delay_{delay}ps_current_{current}mA.txt', header=7)
            
            

            stats = analyze_oscillogram(time_arr, voltage_arr)
           
            # Условие фильтрации
            # if stats['cv_max']<cv_max_thresh and stats['cv_min']<cv_min_thresh:
            # if stats['amplitude']>amplitude_thresh:
            
            if 1>0: # нет условия
    
                
            
                freq_data.append(stats['frequency'])
                
                png_filename=f'analyze_osc_delay_{delay}ps_current_{current}mA'
                fig = plot_oscillogram_with_statistics(
                    time_arr,
                    voltage_arr,
                    stats,
                    title=f"Current = {current} mA, Delay = {delay} ps",
                    save_path=save_folder,
                    filename=png_filename
                )

            else:
                freq_data.append(np.nan)
    
    
    current_label='Current, mA'
    delay_label='Delay, ps'
    freq_label='Frequency, GHz'
    map_filename='map'
    map_title='map'

    x_arr = [current_data, current_label]
    y_arr = [delay_data, delay_label]
    z_arr = [freq_data, freq_label]
    
    create_map_and_save(
        x_arr=x_arr, 
        y_arr=y_arr,
        z_arr=z_arr, 
        title=map_title, 
        folder_path=save_folder, 
        filename=map_filename, 
        show_plot=False
    )