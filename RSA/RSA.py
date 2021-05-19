import sys
from io import open
from RSAKeyGen import PublicKey
from RSAKeyGen import PrivateKey


# Главная функция
def main(argv):
    """
    Формат консольной команды
    > RSA.py (-options ...)
    -i      файл, содержащий исходный или шифротекст
    -o      файл, куда происходит запись результата
    -pubk   файл, содержащий открытый ключ
    -prik   файл, содержащий закрытый ключ
    Подсказка:
    [] - опциональный параметр
    () - обязательный параметр с выбором
    Примеры:
    > Зашифровать:      RSA.py -i входной_файл.txt -o encrypted.txt -pubk public.key
    > Расшифровать:     RSA.py -i encrypted.txt -o decrypted.txt -prik private.key
    """

    input_file = None
    output_file = None
    public_key_file = None
    private_key_file = None

    # Инициализация параметров sys.argv
    try:
        for arg in argv:
            if arg == "-i":
                input_file = open(argv[argv.index(arg) + 1], "rb")
            elif arg == "-o":
                output_file = open(argv[argv.index(arg) + 1], "wb+")
            elif arg == "-pubk":
                public_key_file = open(argv[argv.index(arg) + 1], "r", encoding="utf-8")
            elif arg == "-prik":
                private_key_file = open(argv[argv.index(arg) + 1], "r", encoding="utf-8")

        if input_file is None:
            raise Exception("Входной файл не указан в аргументах")
        if output_file is None:
            raise Exception("Выходной файл не указан в аргументах")
        if public_key_file is None and private_key_file is None:
            raise Exception("Файл с ключём не указан в аргументах")

        mode = "enc" if private_key_file is None else "dec"

    except Exception as e:
        print("Ошибка в ведённых параметрах.", str(e))
        if input_file is not None:
            input_file.close()
        if output_file is not None:
            output_file.close()
        if public_key_file is not None:
            public_key_file.close()
        if private_key_file is not None:
            private_key_file.close()
        raise SystemExit(1)

    print(f"""
    Входной файл: {input_file.name}
    Выходной файл: {output_file.name}
    Режим: {mode}""")

    input_bytes = input_file.read()

    if mode == "enc":
        # Создаём объект открытого ключа из файла
        public_key = PublicKey(from_file=public_key_file)
        print(f"""    Открытый ключ: {public_key}""")

        # Шифруем текст открытым ключом
        encrypted_text = public_key.apply(input_bytes)

        # Записываем результат шифрования в файл
        output_file.write(encrypted_text)
        public_key_file.close()
    elif mode == "dec":
        # Создаём объект закрытого ключа из файла
        private_key = PrivateKey(from_file=private_key_file)
        print(f"""    Закрытый ключ: {private_key}""")

        # Дешифруем шифротекст закрытым ключом
        decrypted_text = private_key.apply(input_bytes)

        # Записываем результат дешифрования в файл
        output_file.write(decrypted_text)
        private_key_file.close()

    input_file.close()
    output_file.close()


# Вход в программу
if __name__ == "__main__":
    main(sys.argv)
