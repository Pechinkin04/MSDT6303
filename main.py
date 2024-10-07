import csv
import re

patterns = {
    'telephone': r'^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$',
    'height': r'^[1-2]\.\d{2}$',
    'inn': r'^\d{12}$',
    'identifier': r'^\d{2}-\d{2}/\d{2}$',
    'occupation': r'^[A-Za-zА-Яа-я\s\-]+$',
    'latitude': r'^-?\d{1,2}\.\d+$',
    'blood_type': r'^(A|B|AB|O)([+-]|[\u2212])$',
    'issn': r'^\d{4}-\d{4}$',
    'uuid': r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',
    'date': r'^\d{4}-\d{2}-\d{2}$'
}

# Функция для проверки валидности строки
def is_valid(row):
    for field, pattern in patterns.items():
        if not re.match(pattern, row[field]):
            return False
    return True

# Массив для хранения невалидных строк
invalid_rows = []
# Массив для хранения номеров невалидных строк
invalid_rowsNum = []

i = 1
# Открываем и проверяем файл
with open('80.csv', newline='', encoding='utf-16') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        i += 1
        if not is_valid(row):
            invalid_rows.append(row)
            invalid_rowsNum.append(i - 2)
            # if i < 30:
            #     print(row)
            #     i += 1

# Выводим количество невалидных строк
print(f"Количество невалидных строк: {len(invalid_rows)}")
first_30_elements = invalid_rowsNum[:30]
print(first_30_elements)

# Вывод суммы
sum = 0
for rowNum in invalid_rowsNum:
    sum = sum + rowNum

print(sum)

import json
import hashlib
from typing import List

"""
В этом модуле обитают функции, необходимые для автоматизированной проверки результатов ваших трудов.
"""


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Метод для сериализации результатов лабораторной.
    Записывает номер варианта и контрольную сумму в файл result.json.

    :param variant: номер вашего варианта
    :param checksum: контрольная сумма, вычисленная через calculate_checksum()
    """
    result = {
        "variant": variant,
        "checksum": checksum
    }

    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


variant_number = 80  # Укажите ваш номер варианта
invalid_row_numbers = invalid_rowsNum  # Пример номеров невалидных строк

checksum = calculate_checksum(invalid_row_numbers)
print(checksum)
serialize_result(variant_number, checksum)