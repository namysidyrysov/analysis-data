import os
import matplotlib.pyplot as plt
import numpy as np


def plot_multiple_curves(
    x_arrays,
    y_arrays,
    labels=None,
    title="Multiple Curves",
    xlabel="X Axis",
    ylabel="Y Axis",
    folder_path=".",
    filename="combined_plot",
    show_plot=False,
):
    """Строит несколько графиков (кривых) на одном общем рисунке и сохраняет его.

    Параметры:
    ----------
    x_arrays : list of lists/arrays
        Список массивов с данными для оси X (по одному массиву на каждую кривую).
    y_arrays : list of lists/arrays
        Список массивов с данными для оси Y (по одному массиву на каждую кривую).
    labels : list of str, optional
        Список названий для легенды. Если None, графики будут пронумерованы: Curve
        1, Curve 2...
    title : str, optional
        Заголовок графика.
    xlabel : str, optional
        Подпись оси X.
    ylabel : str, optional
        Подпись оси Y.
    folder_path : str, optional
        Путь к папке для сохранения графика (по умолчанию текущая директория '.').
    filename : str, optional
        Имя сохраняемого файла (без расширения).
    show_plot : bool, optional
        Если True, отобразит график на экране. По умолчанию False.
    """
    # Проверка на корректность переданных данных
    if len(x_arrays) != len(y_arrays):
        raise ValueError(
            "Количество массивов по X должно совпадать с количеством массивов по Y!"
        )

    # Создаем объект графика
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)

    # Поочередно наносим каждую кривую на график
    for i in range(len(x_arrays)):
        x_data = x_arrays[i]
        y_data = y_arrays[i]

        # Назначаем имя для легенды
        if labels and i < len(labels):
            curve_label = labels[i]
        else:
            curve_label = f"Curve {i + 1}"

        # Отрисовка линии с маркерами
        ax.plot(
            x_data,
            y_data,
            marker="o",
            linestyle="-",
            markersize=4,
            linewidth=1.5,
            label=curve_label,
        )

    # Сетка и оформление осей
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.6)

    # Настройка легенды (вынесена вправо, чтобы не перекрывать экспериментальные точки)
    ax.legend(
        bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0.0, fontsize=10
    )

    plt.tight_layout()

    # Проверка и создание папки для сохранения
    if folder_path != "." and not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    # Сохранение файла
    full_path = os.path.join(folder_path, f"{filename}.png")
    plt.savefig(full_path, bbox_inches="tight")

    # Показ или закрытие графика
    if show_plot:
        plt.show()
    else:
        plt.close(fig)

    print(f"График успешно сохранен")


# ==============================================================================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ С КРИВЫМИ РАЗНОЙ ДЛИНЫ
# ==============================================================================
if __name__ == "__main__":
    print("Генерация тестовых данных...")

    # Кривая 1: Синусоида (15 точек)
    x1 = np.linspace(0, 10, 15)
    y1 = np.sin(x1) * 10

    # Кривая 2: Линейный тренд с шумом (20 точек)
    x2 = np.linspace(0, 12, 20)
    y2 = 1.5 * x2 + np.random.normal(0, 1, size=len(x2))

    # Кривая 3: Экспоненциальное затухание (10 точек - пример разной длины данных)
    x3 = np.linspace(1, 8, 10)
    y3 = 25 * np.exp(-0.4 * x3)

    # Упаковываем массивы в списки
    test_x_data = [x1, x2, x3]
    test_y_data = [y1, y2, y3]
    test_labels = ["Сигнал А (Sin)", "Сигнал Б (Linear)", "Сигнал В (Exp)"]

    # Папка для сохранения (создастся автоматически рядом со скриптом)
    output_dir = "./test_results"

    # Вызов универсальной функции
    plot_multiple_curves(
        x_arrays=test_x_data,
        y_arrays=test_y_data,
        labels=test_labels,
        title="Сравнение различных физических процессов",
        xlabel="Время / Итерации (ед.)",
        ylabel="Амплитуда / Частота (ед.)",
        folder_path=output_dir,
        filename="multicurve_test_report",
        show_plot=True,  # Поменяйте на True, если хотите сразу увидеть график на экране
    )
