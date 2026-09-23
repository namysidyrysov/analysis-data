from datetime import datetime

def get_formatted_time():
    # Получаем текущую дату и время
    now = datetime.now()
    
    # Форматируем по шаблону
    return now.strftime("%b-%d-%Y_time_%H-%M-%S")

# Пример использования
if __name__=='__main__':
    current_timestamp = get_formatted_time()
    print('Текущее время и дата:',current_timestamp)
