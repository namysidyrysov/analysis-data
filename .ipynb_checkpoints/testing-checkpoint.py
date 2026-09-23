import numpy as np
import os
from tqdm import tqdm
import plotly.graph_objects as go  # Нужна библиотека: pip install plotly

from scripts.read_txt_file import read_txt_xy
from scripts.convert_dBm_mW import convert_dbm_to_mw
from scripts.get_formated_time import get_formatted_time

LINEWIDTHS = [2]
CURRENT = 9.83

WAVELENGTH_START = 1056
WAVELENGTH_STOP = 1071
WAVELENGTH_STEP = 1
WAVELENGTHS = np.arange(WAVELENGTH_START, WAVELENGTH_STOP, WAVELENGTH_STEP)

NUMBER_ITERATIONS = 40
WAVE_LABEL = 'Wavelength (nm)'
ITERATION_LABEL = 'Iteration (N)'
POW_LABEL_mW = 'Power (mW)'
time_now = get_formatted_time()

WAVE_START = 1050
WAVE_STOP = 1300

DATA_FOLDER = rf'C:\Users\namys\Documents\DATA_dual_wavelength_laser\LD_set_current_9.83A_September-13-2026_time_10-18-08'

for linewidth in LINEWIDTHS:
    SAVE_FOLDER = rf'{DATA_FOLDER}\OSA_graphs_{time_now}\linewidth_{linewidth}nm'
    
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
       
    for wavelength in tqdm(WAVELENGTHS, desc=f"Processing LW {linewidth}nm"):
        pow_arr_arr = []
        sub_wave_arr = None
        
        # 1. Собираем данные
        for iteration in range(1, NUMBER_ITERATIONS + 1):
            osa_txt_file = rf"{DATA_FOLDER}\OSA\linewidth_{linewidth}nm\wavelength_{wavelength}nm\osa_iteration_{iteration}_wavelength_{wavelength}nm_linewidth_{linewidth}nm_current_9.83A.txt"
            
            if not os.path.exists(osa_txt_file):
                continue
                
            wave_arr, pow_arr = read_txt_xy(path=osa_txt_file)
            # pow_arr = convert_dbm_to_mw(pow_arr_dbm=pow_arr)
            
            mask_freq = (wave_arr >= WAVE_START) & (wave_arr <= WAVE_STOP)
            sub_wave_arr = wave_arr[mask_freq]
            sub_pow_arr = pow_arr[mask_freq]
            
            pow_arr_arr.append(sub_pow_arr)
            
        if not pow_arr_arr or sub_wave_arr is None:
            continue
            
        # 2. Формируем 2D матрицу для Plotly
        Z = np.array(pow_arr_arr)
        X = sub_wave_arr
        Y = np.arange(1, len(pow_arr_arr) + 1)
        
        # 3. Строим высококачественную интерактивную 3D-поверхность
        fig = go.Figure(data=[go.Surface(
            x=X, y=Y, z=Z,
            colorscale='Viridis',  # Стильный современный градиент. Можно заменить на 'Plasma', 'Jet' или 'Hot'
            contours={
                "z": {"show": True, "start": Z.min(), "end": Z.max(), "size": (Z.max()-Z.min())/20, "usecolormap": True, "highlightcolor": "white", "project_z": True}
            },
            lighting=dict(ambient=0.6, diffuse=0.8, roughness=0.1, specular=1.2, fresnel=0.5), # Настройка бликов света
        )])
        
        # 4. Стилизация осей и сцены (делаем стильно, убираем лишний визуальный мусор)
        fig.update_layout(
            title=f"3D Laser Spectrum: LW {linewidth}nm, Center WL {wavelength}nm",
            title_x=0.5,
            scene=dict(
                xaxis_title=WAVE_LABEL,
                yaxis_title=ITERATION_LABEL,
                zaxis_title=POW_LABEL_mW,
                xaxis=dict(backgroundcolor="rgb(240, 240, 240)", gridcolor="white", showbackground=True, zerolinecolor="white"),
                yaxis=dict(backgroundcolor="rgb(240, 240, 240)", gridcolor="white", showbackground=True, zerolinecolor="white"),
                zaxis=dict(backgroundcolor="rgb(230, 230, 230)", gridcolor="white", showbackground=True, zerolinecolor="white"),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)) # Угол обзора по умолчанию
            ),
            margin=dict(l=0, r=0, b=0, t=40),
            width=900,
            height=700
        )
        
        # 5. Сохраняем в интерактивный HTML (файл можно пересылать кому угодно, он откроется везде)
        save_filename = f"Interactive_3D_WL_{wavelength}nm.html"
        fig.write_html(os.path.join(SAVE_FOLDER, save_filename))
