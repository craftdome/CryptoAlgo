import sys
from io import StringIO
import matplotlib.pyplot as plt


availableSymbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encdec(source: str, pad: str, typ="enc") -> str:
    # Если encode, то сложение по модулю 26, иначе вычитание по модулю 26
    operation = -1 if typ == "dec" else 1

    result = StringIO()
    for i in range(len(source)):
        if source[i] not in availableSymbols:
            continue
        result.write(
            chr(
                (
                    ord(source[i].upper()) - 65
                    + operation  # Encode или Decode
                    * (ord(pad[i % len(pad)]) - 65)
                )
                % 26  # Выравнивание символа в диапазоне [0, 25]
                + 65  # Восстановление номера символа в таблице ASCII
            )
        )

    return result.getvalue()


def make_dict_freqs(source: str) -> dict:
    alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    dict_freqs = {char: 0 for char in alph}
    source = sorted(source)
    for c in source:
        c = c.upper()  # Перевод всех символов в uppercase, чтобы учитывались в статистике
        if c not in alph:
            continue
        dict_freqs[c] = dict_freqs.get(c, 0) + 1
    return dict_freqs


# Вход в программу
if __name__ == "__main__":

    # Оформление кода: тут не доплатили

    iFile = None
    oFile = None
    typ = "enc"
    oneTimePad = None

    # Инициализация параметров sys.argv
    try:
        for arg in sys.argv:
            if arg == "-i":
                iFile = open(sys.argv[sys.argv.index(arg) + 1], "r")
            if arg == "-pad":
                oneTimePad = open(sys.argv[sys.argv.index(arg) + 1], "r+")
            elif arg == "-o":
                oFile = open(sys.argv[sys.argv.index(arg) + 1], "w+")
            elif arg == "-t":
                typ = sys.argv[sys.argv.index(arg) + 1]

        if iFile is None:
            raise Exception("Входной файл не указан в аргументах")
        if oFile is None:
            raise Exception("Выходной файл не указан в аргументах")
        if oneTimePad is None:
            raise Exception("Одноразовый блокнот не указан в аргументах не указан в аргументах")
    except Exception as e:
        print("Ошибка в ведённых параметрах.", str(e))
        if iFile is not None:
            iFile.close()
        if oFile is not None:
            oFile.close()
        if oneTimePad is not None:
            oneTimePad.close()
        raise SystemExit(1)

    print(f"""
        Входной файл: {iFile.name}
        Выходной файл: {oFile.name}
        Одноразовый блокнот: {oneTimePad.name}
        Действие: {"Encode" if typ == "enc" else "Decode"}""")

    padString = oneTimePad.read()
    oneTimePad.close()

    inputString = iFile.read().replace(" ", "").replace(",", "").replace(".", "").replace("\n", "")
    iFile.close()
    outputString = encdec(inputString, padString, typ=typ)
    oFile.write(outputString)
    oFile.close()

    # Очистка файла от содержимого
    oneTimePad = open(oneTimePad.name, "w")
    oneTimePad.close()

    # Гистограммы
    source = make_dict_freqs(inputString)
    result = make_dict_freqs(outputString)

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
    ax2.set_title(f"{'Зашифрованный' if typ == 'enc' else 'Дешифрованный'} файл")
    ax2.set_xlabel("Символ")
    ax2.set_ylabel("Частота появления символа")

    plt.show()
