import sys
from io import StringIO
from io import open
import matplotlib.pyplot as plt


def int_to_bin(number: int) -> str:
    """Представляет число в строке в двоичной форме"""
    return "".join(f"{number:08b}")


def bin_to_int(binary: str) -> int:
    length = len(binary)
    num = 0
    for j in range(0, length):
        num += 2 ** j if binary[length - 1 - j] == '1' else 0
    return num


def str_to_bin(string: str, sep='') -> str:
    """Конвертация ASCII строки в бинарное представление"""
    return sep.join(int_to_bin(ord(char)) for char in string)


def bin_to_str(binary: str) -> str:
    res = StringIO()
    for i in range(int(len(binary) / 8)):
        # Конвертируем часть последовательности, а именно 8 бит, в число
        number = bin_to_int(binary[i * 8:8 + i * 8])

        # Переводим число в символ кодировки ASCII и дописываем результат
        res.write(chr(number))

    return res.getvalue()


def do_as_scheme(binary: str, scheme: list) -> str:
    """
    Функция перестановки массива согласно указанной схеме (таблице)
    :param binary: переставляемое
    :param scheme: индексы перестановки
    :return: новая строка после перестановки
    """
    return "".join([binary[i] for i in scheme])


INITIAL_PERMUTATION = [
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
    56, 48, 40, 32, 24, 16, 8,  0,
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6
]


FINAL_PERMUTATION = [
    39, 7,  47, 15, 55, 23, 63, 31,
    38, 6,  46, 14, 54, 22, 62, 30,
    37, 5,  45, 13, 53, 21, 61, 29,
    36, 4,  44, 12, 52, 20, 60, 28,
    35, 3,  43, 11, 51, 19, 59, 27,
    34, 2,  42, 10, 50, 18, 58, 26,
    33, 1,  41, 9,  49, 17, 57, 25,
    32, 0,  40, 8,  48, 16, 56, 24,
]


def IP(binary: str) -> str:
    return do_as_scheme(binary, INITIAL_PERMUTATION)


def FP(binary: str) -> str:
    return do_as_scheme(binary, FINAL_PERMUTATION)


def LR(binary: str):
    """
    :param binary: - 64 бит
    :return: Возвращает кортеж из левой и правой частей :param binary:
    """
    return binary[0:32], binary[32:64]


EXPANSION = [
    31, 0,  1,  2,  3,  4,
    3,  4,  5,  6,  7,  8,
    7,  8,  9,  10, 11, 12,
    11, 12, 13, 14, 15, 16,
    15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24,
    23, 24, 25, 26, 27, 28,
    27, 28, 29, 30, 31, 0
]


def E(R: str) -> str:
    """
    Функция расширения
    Расширяет 32-битовый вектор R до 48-битового вектора E(R) путём дублирования некоторых битов вектора R,
    при этом порядок следования битов в E(R) задан в :EXPANSION:
    :return: дополненный вектор
    """
    return do_as_scheme(R, EXPANSION)


S_BLOCKS = {
    1: [
        14, 4,  13, 1,  2,  15, 11, 8,  3,  10, 6,  12, 5,  9,  0,  7,
        0,  15, 7,  4,  14, 2,  13, 1,  10, 6,  12, 11, 9,  5,  3,  8,
        4,  1,  14, 8,  13, 6,  2,  11, 15, 12, 9,  7,  3,  10, 5,  0,
        15, 12, 8,  2,  4,  9,  1,  7,  5,  11, 3,  14, 10, 0,  6,  13
    ],
    2: [
        15, 1,  8,  14, 6,  11, 3,  4,  9,  7,  2,  13, 12, 0,  5,  10,
        3,  13, 4,  7,  15, 2,  8,  14, 12, 0,  1,  10, 6,  9,  11, 5,
        0,  14, 7,  11, 10, 4,  13, 1,  5,  8,  12, 6,  9,  3,  2,  15,
        13, 8,  10, 1,  3,  15, 4,  2,  11, 6,  7,  12, 0,  5,  14, 9
    ],
    3: [
        10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
        13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
        13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
        1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12
    ],
    4: [
        7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
        13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
        10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
        3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14
    ],
    5: [
        2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
        14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
        4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
        11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3
    ],
    6: [
        12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
        10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
        9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
        4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13
    ],
    7: [
        4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
        13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
        1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
        6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12
    ],
    8: [
        13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
        1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
        7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
        2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11
    ]
}


def S(B: str, block_number: int) -> str:
    """
    :param B: вектор 6 бит
    :param block_number: номер S-блока, по которому происходит преобразование вектора B
    :return: вектор 4 бит
    """
    a = bin_to_int(B[0] + B[5])
    b = bin_to_int(B[1:5])

    # Получаем нужный элемент из S-блоков и записываем его в
    # двоичном виде как B'
    S_BLOCK = S_BLOCKS.get(block_number)
    B_ = int_to_bin(S_BLOCK[a*16 + b])

    return B_


PERMUTATION = [
    15, 6,  19, 20,
    28, 11, 27, 16,
    0,  14, 22, 25,
    4,  17, 30, 9,
    1,  7,  23, 13,
    31, 26, 2,  8,
    18, 12, 29, 5,
    21, 10, 3,  24
]


def P(binary: str) -> str:
    """
    Конечная перестановка
    :param binary: вектор 32 бит, состоящий из B' 4-битовых векторов
    :return: результат перестановки
    """
    return do_as_scheme(binary, PERMUTATION)


def f(R: str, k: str) -> str:
    """
    Для вычисления функции шифрования f() используется: функция расширения E();
    преобразование S, составленное из восьми преобразований :S_BLOCKS: S1,S2,...,S8;
    перестановка P.
    :param R: вектор 32 бит
    :param k: вектор 48 бит
    :return: зашифрованный 32-битный вектор
    """

    # Расширяем вектор R до 48 бит
    extended = E(R)

    # Исключающее ИЛИ: E^k
    xored = xor(extended, k)

    # Разделяем на восемь 6-битовых блоков
    B = {}
    for i in range(0, 8):
        B[i + 1] = xored[0 + i*6:6 + i*6]

    # Преобразуем все B векторы в 4-битовые векторы B' преобразованием S()
    B_ = {}
    for i in range(1, 9):
        B_[i] = S(B[i], 1)

    # Сборка результата шифрования
    binary = "".join(B_.get(i) for i in [1, 2, 3, 4, 6, 7, 8])

    # Перестановка битов P
    perm = P(binary)

    return perm


def add_parity_bit(k: str) -> str:
    """
    Функция добавления бита чётности
    :param k: вектор 56 бит (пароль от пользователя)
    :return: возвращает дополненный вектор битом чётности на позхициях 8,16,...,64
    """
    ki = StringIO()
    for i in range(int(len(k)/7)):
        word_7_bit = k[0 + i*7:7 + i*7]
        bit = "1" if word_7_bit.count("1") % 2 == 0 else "0"

        ki.write(word_7_bit)
        ki.write(bit)

    return ki.getvalue()


LEFT_CYCLE_SHIFT = {
    0:  1,  1:  1,  2:  2,  3:  2,
    4:  2,  5:  2,  6:  2,  7:  2,
    8:  1,  9:  2,  10: 2,  11: 2,
    12: 2,  13: 2,  14: 2,  15: 1
}


def left_cycle_shift(binary: str, index: int) -> str:
    """Функция левостороннего сдвига"""
    shift = LEFT_CYCLE_SHIFT.get(index)
    return binary[shift:] + binary[:shift]


KEY_PERMUTATION_1 = [
    56, 48, 40, 32, 24, 16, 8,
    0,  57, 49, 41, 33, 25, 17,
    9,  1,  58, 50, 42, 34, 26,
    18, 10, 2,  59, 51, 43, 35,
    62, 54, 46, 38, 30, 22, 14,
    6,  61, 53, 45, 37, 29, 21,
    13, 5,  60, 52, 44, 36, 28,
    20, 12, 4,  27, 19, 11, 3
]


KEY_PERMUTATION_2 = [
    13, 16, 10, 23, 0,  4,
    2,  27, 14, 5,  20, 9,
    22, 18, 11, 3,  25, 7,
    15, 6,  26, 19, 12, 1,
    40, 51, 30, 36, 46, 54,
    29, 39, 50, 44, 32, 47,
    43, 48, 38, 55, 33, 52,
    45, 41, 49, 35, 28, 31
]


def key_gen(password: str) -> dict:
    k = str_to_bin(password)

    # Добавляет бит чётности
    k = add_parity_bit(k)

    # Выполняем перестановку согласно схеме с уменьшением ключа до 56 бит
    k = do_as_scheme(k, KEY_PERMUTATION_1)

    # Производим левосторонний сдвиг в половинах ключа k
    C = {}
    D = {}
    (C[0], D[0]) = LR(k)
    for i in range(1, 17):
        C[i] = left_cycle_shift(C[i - 1], i)
        D[i] = left_cycle_shift(D[i - 1], i)

    # Вторая перестановка с уменьшением ключа до 48 бит
    key = {}
    for i in range(1, 17):
        key[i] = do_as_scheme(C[i] + D[i], KEY_PERMUTATION_2)

    return key


def xor(arg1: str, arg2: str) -> str:
    """
    :param arg1: строка с битами, напр., 1010
    :param arg2: строка с битами, напр., 1101
    :return: результат побитового исключающего ИЛИ, напр., 1010^1101 = 0111
    """
    return "".join(str((int(arg1[i]) + int(arg2[i])) % 2) for i in range(0, len(arg1)))


def encdec(T: str, k: dict, mode="enc") -> str:
    result = StringIO()

    # Начальная перестановка (по 64 бита)
    initial_perm = IP(T)

    if mode == "enc":
        # Подготовка к шифрованию
        L = {}
        R = {}
        (L[0], R[0]) = LR(initial_perm)

        # Шифрование (спускаемся по словарю с 1 до 16)
        for i in range(1, 17):
            L[i] = R[i - 1]
            R[i] = xor(L[i - 1], f(R[i - 1], k[i]))

        # Конечная перестановка
        final_perm = FP(L[16] + R[16])
        # Дописываем результат шифрования 64-битного блока
        result.write(final_perm)

    elif mode == "dec":

        # Разделяем на левую и правую половины
        L = {}
        R = {}
        (L[16], R[16]) = LR(initial_perm)

        # Дешифровка (спускаемся по словарю с 16 до 0)
        for i in range(16, 0, -1):
            R[i - 1] = L[i]
            L[i - 1] = xor(R[i], f(L[i], k[i]))

        # Конечная перестановка
        final_perm = FP(L[0] + R[0])
        # Дописываем результат шифрования 64-битного блока
        result.write(final_perm)

    return result.getvalue()


def make_dict_freqs(source: str) -> dict:
    alph = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    dict_freqs = {char: 0 for char in alph}
    source = sorted(source)
    for c in source:
        c = c.upper()  # Перевод всех символов в uppercase, чтобы учитывались в статистике
        if c in alph:
            dict_freqs[c] = dict_freqs.get(c, 0) + 1
        else:
            dict_freqs["Other"] = dict_freqs.get("Other", 0) + 1
    return dict_freqs


# Главная функция
def main(argv):
    """
    Формат консольной команды
    > DES.py (-options ...)
    -i      файл, данные которого будут зашифрованы
    -o      файл, в который будет дешифрован
    -mode   режим работы (enc=шифрование, dec=дешифрование)
    Подсказка:
    [] - опциональный параметр
    () - обязательный параметр с выбором
    Примеры:
    > Зашифровать:  DES.py -i входной_файл.txt -o encrypted.txt -mode enc
    > Дешифровать:  DES.py -i encrypted.txt -o decrypted.txt -mode dec
    """

    input_file = None
    output_file = None
    mode = "enc"

    # Инициализация параметров sys.argv
    try:
        for arg in argv:
            if arg == "-i":
                input_file = open(argv[argv.index(arg) + 1], "r", encoding="utf-8")
            elif arg == "-o":
                output_file = open(argv[argv.index(arg) + 1], "w+", encoding="utf-8")
            elif arg == "-mode":
                mode = argv[sys.argv.index(arg) + 1]

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

    # Запрос и генерация ключа
    password = input("Введите пароль (7 символов): ")
    k = key_gen(password[0:7])

    input_string = input_file.read()
    output_string = StringIO()

    for i in range(int(len(input_string) / 8)):
        # Исходный текст
        T = str_to_bin(input_string[0 + i*8:8 + i*8])
        input_file.close()

        # Шифрование/Дешифрование
        result = encdec(T, k, mode)

        # Двоичную запись приводим в "читабельный" вид
        output_string.write(bin_to_str(result))

    # Вывод в файл
    output_file.write(output_string.getvalue())
    output_file.close()

    # Вывод в консоль
    # print("╒══════════════════════Исходная строка═════════════════════╕")
    # print("\t".join([c.encode("utf-8").hex() for c in bin_to_str(T)]))
    # print("╒═══════════════════", "Зашифрованная" if mode != "dec" else "Дешифрованная", " строка═══════════════════╕", sep="")
    # print("\t".join([c.encode("utf-8").hex() for c in result]))

    # Гистограммы
    source = make_dict_freqs(input_string)
    result = make_dict_freqs(output_string.getvalue())

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
    ax2.set_title(f"{'Зашифрованный' if mode == 'enc' else 'Дешифрованный'} файл")
    ax2.set_xlabel("Символ")
    ax2.set_ylabel("Частота появления символа")

    plt.show()

# Вход в программу
if __name__ == "__main__":
    main(sys.argv)
