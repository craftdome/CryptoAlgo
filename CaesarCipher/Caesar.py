import sys
import matplotlib.pyplot as plt

ruL = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
enL = "abcdefghijklmnopqrstuvwxyz"

ruenL = ruL + enL  # Нужно для вывода только lower символов на гистограмме

ruU = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
enU = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

alph = enU + enL + ruU + ruL  # весь алфавит, последовательность должна быть как в CaesarEncDec()


def caesar_encdec(mode="enc", shift=3):
    """Функция транслитерации символов строки с помощью метода .translate()"""

    # Берём shift элементов с конца и добавляем все элементы с начала до shift
    en2U = enU[-shift:] + enU[:-shift]
    en2L = enL[-shift:] + enL[:-shift]
    ru2U = ruU[-shift:] + ruU[:-shift]
    ru2L = ruL[-shift:] + ruL[:-shift]

    # maketrans возвращает словарь с заменами символов
    return str.maketrans(alph, en2U+en2L+ru2U+ru2L) if mode == "dec" else str.maketrans(en2U+en2L+ru2U+ru2L, alph)


def make_dict_freqs(input_text: str) -> dict:
    source = {char: 0 for char in ruenL}
    input_text = sorted(input_text)
    for c in input_text:
        c = c.lower()
        if c not in ruenL:
            continue
        source[c] = source.get(c, 0) + 1
    return source


def main(argv):
    """
    Формат консольной команды
    > Caesar.py (-options ...)
    -i      файл, данные которого будут зашифрованы
    -o      файл, в который будет дешифрован
    -mode   режим работы (enc=шифрование, dec=дешифрование)
    -s      ключ, смещения
    Подсказка:
    [] - опциональный параметр
    () - обязательный параметр с выбором
    Примеры:
    > Зашифровать:  Caesar.py -i входной_файл.txt -o encrypted.txt -mode enc -s 3
    > Дешифровать:  Caesar.py -i encrypted.txt -o decrypted.txt -mode dec -s 3
    """

    input_file = None
    output_file = None
    shift = 3
    mode = "enc"

    try:
        for arg in argv:
            if arg == "-i":
                input_file = open(argv[argv.index(arg) + 1], "r")
            elif arg == "-o":
                output_file = open(argv[argv.index(arg) + 1], "w+")
            elif arg == "-mode":
                mode = argv[argv.index(arg) + 1]
            elif arg == "-s":
                shift = int(argv[argv.index(arg) + 1]) % 26

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

    print(f"""
        Входной файл: {input_file.name}
        Выходной файл: {output_file.name}
        Действие: {"Encode" if mode == "enc" else "Decode"}
        Сдвиг: {shift}""")

    # Ввод и вывод из файла
    input_text = input_file.read()
    output_text = input_text.translate(caesar_encdec(shift=shift, mode=mode))
    output_file.write(output_text)

    input_file.close()
    output_file.close()

    # Гистограммы (криптоанализ)
    source = make_dict_freqs(input_text)
    result = make_dict_freqs(output_text)

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
    ax2.set_title(f"{'Зашифрованный' if mode == 'enc' else 'Дешифрованный'} файл (shift={shift})")
    ax2.set_xlabel("Символ")
    ax2.set_ylabel("Частота появления символа")

    plt.show()


if __name__ == '__main__':
    main(sys.argv)
