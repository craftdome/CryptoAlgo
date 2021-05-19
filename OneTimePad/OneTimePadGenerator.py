import sys
from Crypto.Random.random import randrange

# Вход в программу
if __name__ == "__main__":

    pad1 = None
    pad2 = None
    n = 16

    # Инициализация параметров sys.argv
    try:
        for arg in sys.argv:
            if arg == "-pad1":
                pad1 = open(sys.argv[sys.argv.index(arg) + 1], "w")
            if arg == "-pad2":
                pad2 = open(sys.argv[sys.argv.index(arg) + 1], "w")
            elif arg == "-n":
                n = int(sys.argv[sys.argv.index(arg) + 1])

        if pad1 is None or pad2 is None:
            raise Exception("Файл(ы) для выгрузки ключа не указаны в аргументах (-pad1 и/или -pad2)")
    except Exception as e:
        print("Ошибка в ведённых параметрах.", str(e))
        if pad1 is not None:
            pad1.close()
        if pad2 is not None:
            pad2.close()
        raise SystemExit(1)

    print(f"""
        Длина ключа: {n}
        Одноразовый блокнот #1: {pad1.name}
        Одноразовый блокнот #2: {pad1.name}
        """)

    session_key = "".join([chr(randrange(65, 90)) for i in range(n)])
    pad1.write(session_key)
    pad1.close()
    pad2.write(session_key)
    pad2.close()
    print("Ключи сгенерированы")

