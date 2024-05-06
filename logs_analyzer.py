from datetime import datetime
import sys
from tabulate import tabulate
from colorama import Fore

# Кортеж з відомих нам рівнів логування
KNOWN_LOG_LEVELS = ('INFO', 'DEBUG', 'ERROR', 'WARNING')

# Кольори для кожного з рівнів логування
LOG_LEVEL_COLORS = {'INFO': Fore.GREEN, 'DEBUG': Fore.BLUE, 'ERROR': Fore.RED, 'WARNING': Fore.YELLOW}

# Функція відкриває файл та парсить його построково
def load_logs(file_path: str) -> list:
    log_records = []

    try:
        with open(file_path, 'r') as log_file:
            while True:
                log_line = log_file.readline()
                
                if not log_line:
                    break
                
                # У випадку неможливості розпарсити рядок логу, parse_log_line повертає None
                parsed_record = parse_log_line(log_line)

                if parsed_record != None:
                    log_records.append(parsed_record)
        
    except FileNotFoundError:
        print('Не вдалося відкрити файл логу. Перевірте правильність шляху.')
    except:
        print('Не вдалося завантажити файл логу.')

    # якщо файл порожній, або не вдалося розпарсити жодного рядка
    if len(log_records) == 0:
        print('Записів не виявлено')

    return log_records

def parse_log_line(line: str) -> dict:
    # Розділяємо рядок логу на частини за пробілами
    chunks = line.split(' ')

    # Якщо рядок містить менше необхідної кількості частин (дата, час, рівень та повідомлення)
    if len(chunks) < 4:
        print(f'Рядок логу має помилковий формат: {line}')

        return None
    
    # Обʼєднуємо дату та час
    str_datetime = chunks[0] + ' ' + chunks[1]

    record_datetime = None

    try:
        # парсимо дату та час у змінну datetime
        record_datetime = datetime.strptime(str_datetime, '%Y-%m-%d %H:%M:%S')
    except:
        print(f'Рядок логу має помилковий формат дати: {str_datetime}')

        return None
    
    # беремо частину, що повинна відповідати рівню логування
    log_level = chunks[2]

    # перевіряємо, чи існує такий рівень
    if not log_level in KNOWN_LOG_LEVELS:
        print(f'Невідомий рівень логування: {log_level}')

        return None
    
    #Створюємо повідомлення з усіх чанків, що йдуть після рівня
    # за допомогою list comprehensions
    message = ' '.join([chunks[i] for i in range(3, len(chunks))])

    # Видаляємо символ кінця рядка у кінці
    message = message.removesuffix('\n')

    # повертаємо словник запису логу
    return {'time': record_datetime, 'level': log_level, 'message': message}

# функція фільтрування списку словників логів за рівнем
def filter_logs_by_level(logs: list, level: str) -> list:
    # фільтруємо елементи, лишаючи ті, що мають ключ 'level' та рівень, що співпадає з заданим
    return filter(lambda log: 'level' in log and log['level'] == level.upper(), logs)

# функція підрахунку кількості записів кожного рівня
def count_logs_by_level(logs: list) -> dict:
    # створюємо словник за допомогою dictionary comprehensions де
    # ключі - це відомі нам рівні логування
    # значення - число нуль
    result = {l: 0 for l in KNOWN_LOG_LEVELS}

    # оскільки ми вже відкинули усі рядки з невідомими нам рівнями під час парсингу файлу,
    # тут ми просто інкрементуємо рівень логування для кожного рядку
    for log in logs:
        result[log['level']] += 1

    return result


def main():
    # перевіряємо кількість аргументів командного рядка
    if len(sys.argv) < 2:
        print('Ви забули передати шлях до файлу логу')

        return

    # беремо шлях до файлу логів з аргументів командного рядка
    log_path = sys.argv[1]

    # сповіщаємо користувача, що ми почали працювати над файлом
    print('Аналіз файлу...')

    # відкриття та парсинг файлу
    logs = load_logs(log_path)

    # якщо файл порожній, або не вдалося розпарсити жодного рядка
    if len(logs) == 0:
        return

    # рахуємо статистику рівнів
    log_stats = count_logs_by_level(logs)

    print('\n')
    
    # виводимо статистику рівнів у вигляді таблиці, розфарбовуючи рівні відповідними кольорами
    # для цього ми використовуємо list comprehensions, щоб створити список із даними у форматі,
    # необхідному для модуля tabulate
    # дуже цікаво, що list comprehensions тут використано для створення двовимірного списку
    table_data = [[LOG_LEVEL_COLORS[level] + level + Fore.RESET, count] for level, count in log_stats.items()]

    print(tabulate(table_data, headers=['Рівень логування', 'Кількість'], tablefmt='orgtbl'))

    print('\n')

    # далі, якщо аргументи командного рядка мають ще й рівень логування
    if len(sys.argv) > 2:
        log_level = sys.argv[2]

        # перевіряємо, чи знаємо ми про існування цього рівня
        if not log_level.upper() in KNOWN_LOG_LEVELS:
            print(f'Невідомий рівень логування: {log_level}')

            return

        # викликаємо функцію фільтрування записів за рівнем
        filtered_logs = filter_logs_by_level(logs, log_level)

        # красиво виводимо наші записи
        for log in filtered_logs:
            print(log['time'].strftime('%Y-%m-%d %H:%M:%S') + ' ' + LOG_LEVEL_COLORS[log['level']] + log['level'] + Fore.RESET + ' ' + log['message'])

if __name__ == '__main__':
    main()