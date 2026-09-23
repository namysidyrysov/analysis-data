import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def plot_dense_3d_surface(x_arr, y_arrays, x_label, y_label, z_label, 
                          title=None,
                          elev=30, azim=45, roll=-3, 
                          x_limits=None, y_limits=None, z_limits=None,
                          save_folder_path=None, filename=None, show_plot=True):
    """
    Строит плотную, объемную 3D-поверхность с цветовой шкалой и заголовком.
    """
    if x_arr is None or len(y_arrays) == 0:
        print("Ошибка: Входные данные пусты.")
        return

    # 1. Формируем двумерную матрицу высот Z и сетку координат
    Z = np.array(y_arrays)
    num_iterations = Z.shape[0]
    y_coords = np.arange(1, num_iterations + 1)
    X, Y = np.meshgrid(x_arr, y_coords)
    
    # 2. Инициализируем 3D-окно
    fig = plt.figure(figsize=(12, 7))  # Немного расширили окно под colorbar
    ax = fig.add_subplot(111, projection='3d')
    
    # 3. Отрисовка плотной сплошной поверхности
    surf = ax.plot_surface(X, Y, Z, 
                           cmap=cm.cool, 
                           edgecolor='none', 
                           linewidth=0, 
                           antialiased=True, 
                           alpha=0.95)
    
    # --- ДОБАВЛЕНИЕ ЦВЕТОВОЙ ШКАЛЫ (COLORBAR) ---
    # pad=0.1 отодвигает шкалу вправо, shrink=0.6 уменьшает её высоту под размер 3D куба
    cbar = fig.colorbar(surf, ax=ax, shrink=0.55, aspect=15, pad=0.1)
    cbar.set_label(z_label, fontsize=10, fontweight='bold', labelpad=10)
    
    # --- ДОБАВЛЕНИЕ ЗАГОЛОВКА ---
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # 4. Оформление подписей и шрифтов осей
    ax.set_xlabel(x_label, labelpad=12, fontsize=10, fontweight='bold')
    ax.set_ylabel(y_label, labelpad=12, fontsize=10, fontweight='bold')
    ax.set_zlabel(z_label, labelpad=12, fontsize=10, fontweight='bold')
    
    # Настройка жестких границ осей
    if x_limits is not None:
        ax.set_xlim(*x_limits)
    else:
        ax.set_xlim(x_arr.min(), x_arr.max())
        
    if y_limits is not None:
        ax.set_ylim(*y_limits)
    else:
        ax.set_ylim(1, num_iterations)
        
    if z_limits is not None:
        ax.set_zlim(*z_limits)
        
    # Позиционирование 3D-камеры
    ax.view_init(elev=elev, azim=azim, roll=roll)
    
    # Очистка заднего плана (панели прозрачные)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Тонкая сетка координат
    ax.xaxis._axinfo["grid"]['linewidth'] = 0.5
    ax.yaxis._axinfo["grid"]['linewidth'] = 0.5
    ax.zaxis._axinfo["grid"]['linewidth'] = 0.5
    
    plt.tight_layout()
    
    # 5. Сохранение файла
    if save_folder_path is not None and filename is not None:
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)
        full_path = os.path.join(save_folder_path, filename)
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        
    # 6. Вывод на экран
    if show_plot:
        plt.show()
    else:
        plt.close(fig)
