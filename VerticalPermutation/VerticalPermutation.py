import math
import sys
from io import StringIO
import matplotlib.pyplot as plt


def decrypt(source: str, perm_key: list) -> str:
    table = {}
    size = len(source)
    table_width = len(perm_key)
    long_columns = size % table_width
    long_column_length = math.ceil(size/table_width)
    # print(f"Кол-во больших колонок: {long_columns}")
    # print(f"Длина большой колонки: {long_column_length}")

    # Проходим ключ в заданном порядке
    for i in range(len(perm_key)):
        key = str(i + 1)
        # Если номер столбца является большим столбцом
        # 10.03.2021 fix:   добавил проверку если больших столбцов 0, то все столбцы считаются большими
        #                   именно этого условия не было в методичке (о нём умолчали)
        if perm_key.index(key) + 1 <= long_columns or long_columns == 0:
            table[key] = source[0:long_column_length]
            source = source[long_column_length:]  # обрезаем строку
        # Если номер столбца НЕ является большим столбцом
        else:
            table[key] = source[0:long_column_length-1]
            source = source[long_column_length-1:]  # обрезаем строку

    # Создаём объект билдера строки (конкатенация строк в виде ссылок, без объявления новый переменных)
    # StringIO в разы быстрее стандартного форматирования строк
    result = StringIO()
    for i in range(long_column_length):

        for key in perm_key:
            try:
                result.write(table.get(key)[i])
            # Ловим исключение на последних пустых ячейках, тк их нет в строке при обращении через [i]
            except IndexError:
                break

    # Формируем результат
    return result.getvalue()


def encrypt(source: str, perm_key: list) -> str:
    table = {}
    table_width = len(perm_key)

    # спарсить данные по ключу перестановки в словарь
    index = 0
    for c in source:
        # Номер в ключе перестановок
        # Сдвиг индекса в начало обеспечивается делением по модулю
        key = index % table_width + 1
        # Получаем текущую строку из словаря
        column = table.get(key, StringIO())
        # Добавляем к строке следующий символ входного файла
        column.write(c)
        # Кладём ссылку обратно в словарь, тк изначально её там могло не быть
        table[key] = column
        index += 1

    # Сборка строки с учётом ключа перестановок из всех элементов словаря
    result = StringIO()
    for i in range(len(perm_key)):
        result.write(table.get(perm_key.index(str(i + 1)) + 1, StringIO()).getvalue())

    return result.getvalue()


def make_dict_freqs(source: str) -> dict:
    # Нужно для вывода только lower символов на гистограмме
    alph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" \
           "abcdefghijklmnopqrstuvwxyz"
    dict_freqs = {char: 0 for char in alph}
    source = sorted(source)
    for c in source:
        c = c.lower()  # Перевод всех символов в lowercase, чтобы учитывались в статистике
        if c not in alph:
            continue
        dict_freqs[c] = dict_freqs.get(c, 0) + 1
    return dict_freqs


def main(argv):
    """
    Формат консольной команды
    > VerticalPermutation.py (-options ...)
    -i      файл, данные которого будут зашифрованы
    -o      файл, в который будет дешифрован
    -mode   режим работы (enc=шифрование, dec=дешифрование)
    Подсказка:
    [] - опциональный параметр
    () - обязательный параметр с выбором
    Примеры:
    > Зашифровать:  VerticalPermutation.py -i входной_файл.txt -o encrypted.txt -mode enc
    > Дешифровать:  VerticalPermutation.py -i encrypted.txt -o decrypted.txt -mode dec
    """

    input_file = None
    output_file = None
    mode = "enc"

    # Инициализация параметров sys.argv
    try:
        for arg in argv:
            if arg == "-i":
                input_file = open(argv[argv.index(arg) + 1], "r")
            elif arg == "-o":
                output_file = open(argv[argv.index(arg) + 1], "w+")
            elif arg == "-mode":
                mode = argv[argv.index(arg) + 1]

        if input_file is None:
            raise Exception("Входной файл не указан в аргументах")
        if output_file is None:
            raise Exception("Выходной файл не указан в аргументах")
    except Exception as e:
        print("Ошибка в ведённых параметрах.", str(e))
        if input_file is not None:
            input_file.close()
        if output_file is not None:
            output_file.close()
        raise SystemExit(1)

    # Запрос ключа перестановок
    print("Введите ключ перестановки в формате: 5,1,4,7,2,6,3")
    perm_key = input("Ключ: ").split(",")

    print(f"""
            Входной файл: {input_file.name}
            Выходной файл: {output_file.name}
            Действие: {"Encrypt" if mode == "enc" else "Decrypt"}
            Ключ перестановки: {perm_key}""")

    input_string = input_file.read()
    input_file.close()
    output_string = decrypt(input_string, perm_key) if mode == "dec" else encrypt(input_string, perm_key)
    output_file.write(output_string)
    output_file.close()

    # Гистограммы (криптоанализ)
    source = make_dict_freqs(input_string)
    result = make_dict_freqs(output_string)

    fig, (ax1, ax2) = plt.subplots(
        nrows=1, ncols=2,
        figsize=(18, 6)
    )

    ax1.grid(axis="y")
    ax1.bar(
        list(source.keys()),
        source.values(),
        color='g'
    )
    ax1.set_title("Исходный файл")
    ax1.set_xlabel("Символ")
    ax1.set_ylabel("Частота появления символа")

    ax2.grid(axis="y")
    ax2.bar(
        list(result.keys()),
        result.values(),
        color='r'
    )
    ax2.set_title(f"{'Зашифрованный' if mode == 'enc' else 'Дешифрованный'} файл (key={perm_key})")
    ax2.set_xlabel("Символ")
    ax2.set_ylabel("Частота появления символа")

    plt.show()


# Вход в программу
if __name__ == "__main__":
    main(sys.argv)
