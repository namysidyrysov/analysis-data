import os
import numpy as np
import plotly.graph_objects as go

def plot_3d_spectra(
    wave_2D_arr, 
    power_2D_arr, 
    wave_label,
    powers_label, 
    y_label,
    folder_path, 
    file_name,
    title = None
    ):
    """
    Строит интерактивный 3D-график, где у каждой итерации своя сетка длин волн.
    
    :param wave_2D_arr: 2D список/массив длин волн для каждой итерации [[...], [...]]
    :param power_2D_arr: 2D список/массив мощностей для каждой итерации [[...], [...]]
    :param wave_label: Название оси X (например, "Длина волны (нм)")
    :param powers_label: Название для цветовой шкалы (например, "Мощность (мкВт)")
    :param y_label: Название оси Y (например, "Номер итерации")
    :param folder_path: Путь к папке для сохранения HTML-файла
    :param file_name: Имя выходного HTML-файла
    :param title: Заголовок графика (str или None)
    """
    
    fig = go.Figure()
    
    # Находим глобальные минимумы и максимумы по всем массивам для корректного масштаба цвета
    z_min = float(np.min([np.min(p) for p in power_2D_arr]))
    z_max = float(np.max([np.max(p) for p in power_2D_arr]))
    
    # Отрисовка линий
    for idx, (w_arr, p_arr) in enumerate(zip(wave_2D_arr, power_2D_arr)):
        iteration = idx + 1  # Нумерация итераций с 1
        
        x = np.array(w_arr, dtype=float)
        z = np.array(p_arr, dtype=float)
        y = np.full_like(x, iteration)  # Своя ось Y под размер индивидуальной сетки X
        
        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='lines',
            line=dict(
                width=5.0,            # Толстые «горящие» линии
                color=z,              # Шкала привязана к амплитуде мощности Z
                colorscale='turbo',   
                cmin=z_min,
                cmax=z_max,
                showscale=True if iteration == 1 else False, # Шкала только один раз
                colorbar=dict(
                    title=dict(text=f"<b>{powers_label}</b>", font=dict(color="black", size=14)),
                    tickfont=dict(color="#333333", size=12),
                    x=1.05,
                    thickness=20
                )
            ),
            name=f"Итерация {iteration}",
            showlegend=False
        ))

    # Стилизация (Вариант А: Инженерный светло-серый)
    cube_bg = "#D4D3D3"
    grid_color = "#FFFFFF"
    axis_text_color = "black"

    # Настройка отображения (Layout)
    layout_kwargs = {
        "paper_bgcolor": "white",
        "scene": dict(
            xaxis=dict(
                title=dict(text=f"<b>{wave_label}</b>", font=dict(size=14, color=axis_text_color, family="Arial")),
                tickfont=dict(size=12, color="#333333"),
                nticks=5,
                backgroundcolor=cube_bg,     
                gridcolor=grid_color,        
                gridwidth=10,
                showbackground=False,         
                zeroline=False
            ),
            yaxis=dict(
                title=dict(text=f"<b>{y_label}</b>", font=dict(size=14, color=axis_text_color, family="Arial")),
                tickfont=dict(size=12, color="#333333"),
                nticks=5,
                gridcolor=grid_color,
                gridwidth=10,
                showbackground=False,
                zeroline=False
            ),
            zaxis=dict(
                title=dict(text=""),         
                showticklabels=False,        
                gridcolor=grid_color,
                gridwidth=10,
                showbackground=False,
                zeroline=False
            ),
            camera=dict(
                eye=dict(x=1.8, y=1.8, z=1.4)
            )
        ),
        "margin": dict(l=20, r=80, t=60, b=20),
        "autosize": True
    }
    
    if title:
        formatted_title = title.replace("\n", "<br>")
        layout_kwargs["title"] = dict(
            text=f"<b>{formatted_title}</b>",
            x=0.5,
            xanchor="center",
            font=dict(family="Arial, sans-serif", size=22, color="black")
        )
        
    fig.update_layout(**layout_kwargs)

    # Проверка и добавление расширения .html
    name, ext = os.path.splitext(file_name)
    if ext.lower() != '.html':
        file_name = f"{file_name}.html"

    # Сохранение файла
    os.makedirs(folder_path, exist_ok=True)
    full_output_path = os.path.join(folder_path, file_name)
    fig.write_html(full_output_path)
    print(f"Успешно сохранено в файл: {full_output_path}")


if __name__ == '__main__':
    from scripts.read_txt_file import read_txt_xy
    from scripts.convert_dBm_mW import convert_dbm_to_mw
    
    # Теперь собираем индивидуальные данные независимо для каждого шага
    final_wave_2D = []
    final_power_2D = []

    for iteration in range(1, 41):
        osa_txt_file = fr"C:\Users\namys\Documents\DATA_dual_wavelength_laser\LD_set_current_9.83A_September-13-2026_time_10-18-08\OSA\linewidth_2nm\wavelength_1068nm\osa_iteration_{iteration}_wavelength_1068nm_linewidth_2nm_current_9.83A.txt"
        
        wave_arr, power_arr = read_txt_xy(file_path=osa_txt_file)
        power_arr = convert_dbm_to_mw(power_arr_dbm=power_arr)
        
        # Первичная грубая обрезка спектра
        mask = (wave_arr > 1030) & (wave_arr < 1080)
        wave_arr = wave_arr[mask]
        power_arr = power_arr[mask]
        
        # Поиск пика СТРОГО для текущей итерации
        max_index = np.argmax(power_arr)
        max_wave = wave_arr[max_index]
        
        # Фильтрация ± 2 нм вокруг локального пика этой конкретной итерации
        mask_2 = (wave_arr > max_wave - 2) & (wave_arr < max_wave + 2)
        
        # Сохраняем в свои 2D матрицы
        final_wave_2D.append(wave_arr[mask_2])
        final_power_2D.append(power_arr[mask_2])
        
    # Вызов функции — теперь 100% физически корректно
    plot_3d_spectra(
        wave_2D_arr=final_wave_2D, 
        power_2D_arr=final_power_2D, 
        wave_label='Длина волны (нм)',
        powers_label="Мощность<br>(мкВт)", 
        y_label='Номер итерации',
        folder_path='.', 
        file_name='spectra_result',
        title='Оптические спектры по итерациям'
    )
