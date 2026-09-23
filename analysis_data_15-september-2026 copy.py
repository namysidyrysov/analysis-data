import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import os
from tqdm import tqdm

from scripts.read_txt_file import read_txt_xy
from scripts.plot_xy import plot_xy_markers
from scripts.write_data_txt import write_txt_xy
from scripts.plot_multiple_curves import plot_multiple_curves
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


full_path=r"D:\ВАЖНО_laser_with_btf_cir_SN_26736318_after_coupler_April-25-2026_time_15-47-22\yokogawa_measurements\linewidth_1nm\wavelength_1550nm\current_300mA\yokogawa_delay_300ps_current_300mA_wavelength_1550nm_linewidth_1nm.txt"
# Настройка шрифтов (чтобы выглядело профессионально и без засечек)
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 14,          # Размер шрифта для цифр на осях
    'axes.labelsize': 16,     # Размер шрифта для подписей осей
    'xtick.direction': 'in',  # Засечки смотрят внутрь графика
    'ytick.direction': 'in',
    'xtick.major.size': 6,    # Длина основных засечек
    'ytick.major.size': 6
})

# 1. Загрузка данных
x_arr, y_arr = read_txt_xy(full_path)
x_arr = np.array(x_arr, dtype=float)
y_arr = np.array(y_arr, dtype=float)

# 2. Находим пик и обрезаем данные
global_max_idx = np.argmax(y_arr)
max_wave = x_arr[global_max_idx]
x_a = max_wave - 0.2
x_b = max_wave + 0.2

crop_mask = (x_arr >= x_a) & (x_arr <= x_b)
x_crop = x_arr[crop_mask]
y_crop = y_arr[crop_mask]

# 3. Нормируем отсеченные данные от 0 до 1
y_min_local = np.min(y_crop)
y_max_local = np.max(y_crop)
y_crop_norm = (y_crop - y_min_local) / (y_max_local - y_min_local)

# 4. Расчет ширины на уровне 0.5 (с линейной интерполяцией)
max_index = np.argmax(y_crop_norm)
level = 0.5

left_idx = np.where(y_crop_norm[:max_index] <= level)[0]
if len(left_idx) > 0:
    i = left_idx[-1]
    x_left = x_crop[i] + (level - y_crop_norm[i]) * (x_crop[i+1] - x_crop[i]) / (y_crop_norm[i+1] - y_crop_norm[i])
else:
    x_left = x_a

right_idx = np.where(y_crop_norm[max_index:] <= level)[0]
if len(right_idx) > 0:
    j = max_index + right_idx[0]
    x_right = x_crop[j-1] + (level - y_crop_norm[j-1]) * (x_crop[j] - x_crop[j-1]) / (y_crop_norm[j] - y_crop_norm[j-1])
else:
    x_right = x_b

line_width = x_right - x_left

# 5. СОЗДАНИЕ И НАСТРОЙКА ГРАФИКА
fig, ax = plt.subplots(figsize=(5, 4.5)) # Задаем квадратные пропорции как на рисунке

# Рисуем спектр (чуть толще линию)
ax.plot(x_crop, y_crop_norm, color='#1f77b4', linewidth=2)

# Отрисовка красной линии ширины и значения W
# ax.plot([x_left, x_right], [level, level], color='red', linewidth=2, marker='|', markersize=8)
# ax.text(max_wave, level + 0.03, f'W = {line_width:.4f} нм', 
        # color='red', fontsize=12, ha='center', va='bottom', weight='bold')

# Настройка подписей осей на русском языке
ax.set_xlabel('Длина волны (нм)', labelpad=8)
ax.set_ylabel('Интенсивность (отн. ед.)', labelpad=8)

# Строгие границы осей
ax.set_xlim(x_a, x_b)
ax.set_ylim(-0.05, 1.05)

# Форматирование шага засечек (точно как на картинке)
ax.set_yticks([0.00, 0.25, 0.50, 0.75, 1.00])
ax.set_yticklabels(['0.00', '0.25', '0.50', '0.75', '1.00'])

# Настройка засечек по X (оставляем только несколько значений)
# Автоматически ставит 2-3 крупных значения, чтобы не перегружать ось
ax.xaxis.set_major_locator(plt.MaxNLocator(3)) 

# Добавляем букву (а) в левый верхний угол над графиком
# ax.text(-0.12, 1.06, '(a)', transform=ax.transAxes, fontsize=18, weight='normal', ha='left')

plt.tight_layout() # Чтобы подписи не обрезались при сохранении
plt.show()