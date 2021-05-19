import sys
from io import open
from RSAKeyGen import PublicKey
from RSAKeyGen import KeyPair
from itertools import permutations


# Главная функция
def main(argv):
    """
    Формат консольной команды
    > RSAHack.py (-options ...)
    -pubk   файл, содержащий открытый ключ
    -start  начальное простое число
    -amount кол-во простых чисел, начиная со start
    Подсказка:
    [] - опциональный параметр
    () - обязательный параметр с выбором
    Примеры:
    > Подобрать закрытый ключ:  RSAHack.py -pubk public.key -start 17 -amount 100
    """

    start = 17
    end = 100
    public_key_file = None

    # Инициализация параметров sys.argv
    try:
        for arg in argv:
            if arg == "-pubk":
                public_key_file = open(argv[argv.index(arg) + 1], "r", encoding="utf-8")
            elif arg == "-start":
                start = int(argv[argv.index(arg) + 1])
            elif arg == "-amount":
                end = int(argv[argv.index(arg) + 1])

        if public_key_file is None:
            raise Exception("Файл с открытым ключём не указан в аргументах")

    except Exception as e:
        print("Ошибка в ведённых параметрах.", str(e))
        if public_key_file is not None:
            public_key_file.close()
        raise SystemExit(1)

    public_key = PublicKey(from_file=public_key_file)

    print(f"""
    Открытый ключ: {public_key}
    Диапазон простых чисел: [{start}; {end}]""")

    # Диапазон простых чисел
    prime_range = KeyPair.get_prime_range(start=17, amount=100)

    # Комбинации
    perms = list(permutations(prime_range, 2))

    # Перебор
    for perm in perms:
        if perm[0] * perm[1] == public_key.n:
            keys = KeyPair(perm[0], perm[1])
            print(keys.export_public_key())
            print(keys.export_private_key())
            break


# Вход в программу
if __name__ == "__main__":
    main(sys.argv)
