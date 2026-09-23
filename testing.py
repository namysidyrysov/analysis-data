import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.ticker import MaxNLocator

def plot_waterfall(
    x_arr,                
    y_arrays,               
    offsets=None,     
    x_label="X",
    y_label="Y",
    z_label="Z",
    title=None,
    elev=30,          
    azim=45,         
    roll=0,
    save_folder=None,
    file_name=None,
    show_plot=True            
):
    """
    Улучшенная функция для построения 3D Waterfall графика со сплошными полигонами.
    """
    n = len(y_arrays)
    if offsets is None:
        offsets = np.arange(n)

    fig = plt.figure(figsize=(11, 9), dpi=120)  # Слегка прямоугольная форма для 3D
    ax = fig.add_subplot(111, projection='3d')

    # Настройка цветовой палитры (плавный переход от первой итерации к последней)
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, n))

    verts = []
    # Минимальный уровень по Z, до которого будет опускаться заливка «гребня»
    z_min = 0 

    for z_array in y_arrays:
        # Для создания сплошного полигона добавляем крайние точки, опущенные к z_min
        xs = np.concatenate([[x_arr[0]], x_arr, [x_arr[-1]]])
        zs = np.concatenate([[z_min], z_array, [z_min]])
        verts.append(list(zip(xs, zs)))

    # Создаем коллекцию 3D полигонов
    poly = PolyCollection(verts, facecolors=colors, edgecolors='black', linewidths=0.5, alpha=0.85)
    
    # Добавляем полигоны на график, указывая их позиции на оси Y (offsets)
    ax.add_collection3d(poly, zs=offsets, zdir='y')

    # Настройка лимитов осей (для PolyCollection их нужно выставлять вручную)
    ax.set_xlim(x_arr.min(), x_arr.max())
    ax.set_ylim(offsets.min() - 0.5, offsets.max() + 0.5)
    
    max_z = max([max(z) for z in y_arrays]) * 1.1
    ax.set_zlim(z_min, max_z)

    # Красивое оформление подписей и шрифтов
    font_labels = {'fontsize': 12, 'labelpad': 12}
    ax.set_xlabel(x_label, **font_labels)
    ax.set_ylabel(y_label, **font_labels)
    ax.set_zlabel(z_label, **font_labels)
    
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    
    # Сетка и деления
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.zaxis.set_major_locator(MaxNLocator(nbins=5))
    
    # Делаем фоновые панели прозрачными/белыми для минималистичного вида
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Установка углов обзора и приближения (убираем пустые поля)
    ax.view_init(elev=elev, azim=azim)
    try:
        ax.view_init(elev=elev, azim=azim, roll=roll)
        ax.set_box_aspect(None, zoom=1.15)  # Приближение для новых версий matplotlib
    except TypeError:
        ax.dist = 8.0  # Для старых версий
        
    # Сжатие полей фигуры
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.95)

    if save_folder is not None and file_name is not None:
        if not save_folder or not save_folder.strip():
            save_folder = '.'
        os.makedirs(save_folder, exist_ok=True)
        full_path = os.path.join(save_folder, f"{file_name}.png")
        plt.savefig(full_path, dpi=150, bbox_inches='tight')
        print(f"График сохранён: {full_path}")
        
    if show_plot:
        plt.show()

    plt.close(fig)

if __name__ == '__main__':
    # 1. Генерируем общую ось X (например, длины волн или время)
    # Имитируем диапазон длин волн, близкий к вашему графику
    x_data = np.linspace(1225.0, 1231.0, 200)
    
    # 2. Создаем несколько серий данных (массивов Y) для оси Z
    # Каждая линия будет иметь небольшой сдвиг пика и разную амплитуду
    y_list = []
    num_lines = 35  # Количество линий на графике
    
    for i in range(num_lines):
        # Центр пика плавно смещается от линии к линии
        center = 1228.0 + 0.02 * (i - num_lines / 2)
        # Интенсивность (высота пика)
        amplitude = 3000 + 2500 * np.sin(i / 5.0)
        # Ширина пика
        width = 0.8
        
        # Генерируем гауссовский пик (похожий на спектр из вашего примера)
        y_line = amplitude * np.exp(-((x_data - center) / width) ** 2)
        # Добавляем немного случайного шума для реалистичности
        y_line += np.random.normal(0, 50, size=x_data.shape)
        
        y_list.append(y_line)
        
    # 3. Задаем смещения для каждой линии по оси Y (например, шаги по времени или номерам)
    y_offsets = np.arange(num_lines)
    
    # 4. Вызываем вашу функцию plot_waterfall
    print("Запуск построения 3D Waterfall графика...")
    plot_waterfall(
        x_arr=x_data,
        y_arrays=y_list,
        offsets=y_offsets,
        x_label="Wavelength (nm)",
        y_label="Time / Step",
        z_label="Power (mW)",
        title=None,
        elev=20,          # Угол возвышения
        azim=53,          # Азимут
        roll=0,          # Крен
        save_folder="plots",    # Папка для сохранения
        file_name="waterfall_test", # Имя файла
        show_plot=True    # Показать интерактивное окно
    )