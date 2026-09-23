import os
import numpy as np


def write_txt_xy(
        x_arr,
        x_label,
        y_arr,
        y_label,
        header=None,
        folder_path="test_folder",
        filename="output.txt",
    ):
    """
    Функция записывает два массива x_arr, y_arr в txt файл.
    header: str- это шапка. Сюда можно записать дополнительную информацию.
    """

    # Создание папки
    os.makedirs(folder_path, exist_ok=True)
    if not filename.lower().endswith(".txt"):
        filename = f"{filename}.txt"

    filepath = os.path.join(folder_path, filename)

    # Объединяем X и Y в двумерный массив (столбцы)
    data = np.column_stack((x_arr, y_arr))

    # Формируем заголовок для таблицы (названия колонок)
    columns_header = f"{x_label}\t{y_label}"
    if header:
        full_header = f"{header}\n{columns_header}"
    else:
        full_header = columns_header

    # Сохраняем данные с помощью numpy
    np.savetxt(
        filepath,
        data,
        fmt="%s",  # Универсальный формат (поддерживает числа и текст)
        delimiter="\t",
        header=full_header,
        comments="",  # Убираем дефолтный символ '#' перед заголовком
        encoding="utf-8",
    )

    print(f"Данные успешно сохранены")


# Пример использования:
if __name__ == "__main__":
    x = [1, 2, 3]
    y = [10, 20, 30]

    x_label = "Current (mA)"
    y_label = "Voltage (mV)"

    test_header = "Информация об эскприменте. Например, настройки, дата и так далее."


    write_txt_xy(
        x_arr=x,
        x_label=x_label,
        y_arr=y,
        y_label=y_label,
        header=test_header,
        folder_path="test_folder",
        filename="output.txt",
    )
