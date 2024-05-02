import re
from typing import Callable

# Функція-генератор, що повертає дійсні числа
def generator_numbers(text: str):
    # Шукаємо число з крапкою або без, не забуваючи про відʼємні
    regexp = r'\s-?\d*\.?\d*\s'

    # 
    for raw_num in re.findall(regexp, text):
        # 
        yield(float(raw_num.strip()))

# Функція підрахунку профіту, що приймає рядок та функцію-генератор
def sum_profit(text: str, func: Callable[[str], float]):
    
    sum = 0
    
    # Отримуємо дійсні числа з рядку по одному
    for number in func(text):
        sum += number

    return sum