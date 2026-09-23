import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import AutoMinorLocator

def plot_xy(
        x_arr, 
        y_arr, 
        title, 
        x_label, 
        y_label, 
        folder_path=None, 
        filename=None, 
        show_plot=False,
        
    ):
    """
    Построить график с опциями показа и сохранения.
    
    Параметры:
    - x, y: данные для графика
    - title, xlabel, ylabel: подписи
    - folder_path: папка для сохранения (None = не сохранять)
    - filename: имя файла (None = не сохранять)
    - show_plot: показывать ли график (True/False)
    """
    # перевод в numpy
    x_arr=np.array(x_arr)
    y_arr=np.array(y_arr)
    
    
    # НАСТРОЙКИ ШРИФТОВ
    FONT_FAMILY = 'serif'
    FONT_SIZE_BASE = 16          # Базовый размер шрифта
    FONT_SIZE_TITLE = 16      # Заголовок осей (axes title)
    FONT_SIZE_LABEL = 20         # Подписи осей (X, Y)
    FONT_SIZE_TICK = 16          # Деления осей
    FONT_SIZE_TITLE_TEXT = 22   # Заголовок графика (plt.title)
    FIGSIZE = (16, 9) 
    DPI = 100
    
    
    # ПОДГОТОВКА ПУТЕЙ
    full_path = None
    
    if folder_path is not None and filename is not None:
        # Защита от пустого пути
        if not folder_path or not folder_path.strip():
            folder_path = '.'
        
        # Убедимся, что папка существует
        os.makedirs(folder_path, exist_ok=True)

    
    # НАСТРОЙКА СТИЛЯ
    rcParams['font.family'] = FONT_FAMILY
    rcParams.update({
        'font.size': FONT_SIZE_BASE,
        'axes.titlesize': FONT_SIZE_TITLE,
        'axes.labelsize': FONT_SIZE_LABEL,
        'xtick.labelsize': FONT_SIZE_TICK,
        'ytick.labelsize': FONT_SIZE_TICK,
        'figure.autolayout': True  # автоматическая подгонка макета
    })

    
    # ПОСТРОЕНИЕ ГРАФИКА
    plt.figure(figsize=FIGSIZE)
    plt.plot(x_arr, y_arr, linewidth=2)
    if title is not None:
        plt.title(title, fontsize=FONT_SIZE_TITLE_TEXT, fontname=FONT_FAMILY)
    plt.xlabel(x_label, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
    plt.ylabel(y_label, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
    
    # Основная сетка
    plt.grid(True, which='major', linestyle='-', linewidth=1, alpha=1)
    
    
    # Настройка осей для автоматического отображения мелких делений
    ax = plt.gca()
    ax.xaxis.set_minor_locator(AutoMinorLocator())  
    ax.yaxis.set_minor_locator(AutoMinorLocator())  

    
    # СОХРАНЕНИЕ
    if folder_path is not None and filename is not None:
        full_path = os.path.join(folder_path, f"{filename}.png")
        plt.savefig(full_path, dpi=DPI, bbox_inches='tight')
        print(f"График сохранён в: {full_path}")

    
    # ПОКАЗ ИЛИ ЗАКРЫТИЕ
    if show_plot:
        plt.show()
    else:
        plt.close()  # Освобождаем память
    
    return full_path

def plot_xy_markers(
        x, 
        y, 
        title, 
        xlabel, 
        ylabel, 
        folder_path=None, 
        filename=None, 
        show_plot=False
    ):
    """
    Построить график с линиями и точками (маркерами) с опциями показа и сохранения.
    
    Параметры:
    - x, y: данные для графика
    - title, xlabel, ylabel: подписи
    - folder_path: папка для сохранения (None = не сохранять)
    - filename: имя файла (None = не сохранять)
    - show_plot: показывать ли график (True/False)
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    from matplotlib.ticker import AutoMinorLocator
    import os

    # перевод в numpy
    x = np.array(x)
    y = np.array(y)
    
    # ========================
    # НАСТРОЙКИ ШРИФТОВ
    # ========================
    FONT_FAMILY = 'serif'
    FONT_SIZE_BASE = 16
    FONT_SIZE_TITLE = 16
    FONT_SIZE_LABEL = 20
    FONT_SIZE_TICK = 16
    FONT_SIZE_TITLE_TEXT = 22
    
    # ========================
    # ПОДГОТОВКА ПУТЕЙ
    # ========================
    full_path = None
    
    if folder_path is not None and filename is not None:
        if not folder_path or not folder_path.strip():
            folder_path = '.'
        os.makedirs(folder_path, exist_ok=True)

    # ========================
    # НАСТРОЙКА СТИЛЯ
    # ========================
    rcParams['font.family'] = FONT_FAMILY
    rcParams.update({
        'font.size': FONT_SIZE_BASE,
        'axes.titlesize': FONT_SIZE_TITLE,
        'axes.labelsize': FONT_SIZE_LABEL,
        'xtick.labelsize': FONT_SIZE_TICK,
        'ytick.labelsize': FONT_SIZE_TICK,
        'figure.autolayout': True
    })

    # ========================
    # ПОСТРОЕНИЕ ГРАФИКА (ЛИНИИ + ТОЧКИ)
    # ========================
    plt.figure(figsize=(16, 9))
    
    # Линии + маркеры одновременно
    plt.plot(x, y, 
             marker='o',           # форма маркера (кружок)
             linestyle='-',        # сплошная линия
             linewidth=2,          # толщина линии
             markersize=8,         # размер точек
             markerfacecolor='blue',
             markeredgecolor='blue',
             markeredgewidth=1,
             color='blue')         # цвет линии
    
    if title is not None:
        plt.title(title, fontsize=FONT_SIZE_TITLE_TEXT, fontname=FONT_FAMILY)
    plt.xlabel(xlabel, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
    plt.ylabel(ylabel, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
    
    plt.grid(True, which='major', linestyle='-', linewidth=1, alpha=1)
    
    ax = plt.gca()
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    # ========================
    # СОХРАНЕНИЕ
    # ========================
    if folder_path is not None and filename is not None:
        full_path = os.path.join(folder_path, f"{filename}.png")
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        print(f"\nГрафик сохранён")

    # ========================
    # ПОКАЗ ИЛИ ЗАКРЫТИЕ
    # ========================
    if show_plot:
        plt.show()
    else:
        plt.close()
    
    return full_path


# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ

if __name__ == "__main__":
    # Пример данных
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 1, 5, 3]
   
    
    # ТОЛЬКО ПОКАЗАТЬ (без сохранения)
    plot_xy(
        x_arr=x,
        y_arr=y,
        title='График',
        x_label="Ось X",
        y_label="Ось Y",
        folder_path='graph',
        filename='example',
        show_plot=True #по умолчанию → показываем
    )
    
   