import sys
from io import open
from RSAKeyGen import PublicKey
from RSAKeyGen import PrivateKey


# Главная функция
def main(argv):
    """
    Формат консольной команды
    > RSAEDS.py (-options ...)
    -i      входной файл
    -sign   файл цифровой подписи
    -prik   файл закрытого ключа
    -pubk   файл открытого ключа
    Подсказка:
    [] - опциональный параметр
    () - обязательный параметр с выбором
    Примеры:
    > Создать ЭЦП:      RSAEDS.py -i i.txt -sign sign.txt -prik private.key
    > Проверить ЭЦП:    RSAEDS.py -i i.txt -sign sign.txt -pubk public.key
    """

    input_file = None
    digital_sign_file = None
    digital_sign_file_name = ""
    public_key_file = None
    private_key_file = None

    # Инициализация параметров sys.argv
    try:
        for arg in argv:
            if arg == "-i":
                input_file = open(argv[argv.index(arg) + 1], "r", encoding='utf-8')
            elif arg == "-sign":
                digital_sign_file_name = argv[argv.index(arg) + 1]
            elif arg == "-pubk":
                public_key_file = open(argv[argv.index(arg) + 1], "r", encoding="utf-8")
            elif arg == "-prik":
                private_key_file = open(argv[argv.index(arg) + 1], "r", encoding="utf-8")

        if input_file is None:
            raise Exception("Входной файл не указан в аргументах")
        if digital_sign_file_name == "":
            raise Exception("Файл цифровой подписи не указан в аргументах")
        if public_key_file is None and private_key_file is None:
            raise Exception("Файл с ключём не указан в аргументах")

        mode = "create" if public_key_file is None else "validate"

        digital_sign_file = open(digital_sign_file_name, "w" if mode == "create" else "r")

    except Exception as e:
        print("Ошибка в ведённых параметрах.", str(e))
        if input_file is not None:
            input_file.close()
        if digital_sign_file is not None:
            digital_sign_file.close()
        if public_key_file is not None:
            public_key_file.close()
        if private_key_file is not None:
            private_key_file.close()
        raise SystemExit(1)

    print(f"""
    Входной файл: {input_file.name}
    Режим: {mode}""")

    if mode == "validate":
        # Создаём объект открытого ключа из файла
        public_key = PublicKey(from_file=public_key_file)
        print(f"""    Открытый ключ: {public_key}\n""")

        # Проверяем ЭЦП
        verdict = public_key.validate_digital_sign(validate_file=input_file, sign_file=digital_sign_file)

        print("Проверка цифровой подписи:", "OK" if verdict else "NOT OK")

    elif mode == "create":
        # Создаём объект закрытого ключа из файла
        private_key = PrivateKey(from_file=private_key_file)
        print(f"""    Закрытый ключ: {private_key}""")

        # Создаём ЭЦП
        digital_sign = private_key.make_digital_sign(from_file=input_file)
        print(f"""    Цифровая подпись: {digital_sign}\n""")

        # Перемещаем указатель в начало файла
        # digital_sign_file.seek(0)  # не хотел делать очистку файла, поэтому записываем поверх

        # Записываем ЭЦП в файл
        digital_sign_file.write(digital_sign)
        private_key_file.close()

    input_file.close()
    digital_sign_file.close()


# Вход в программу
if __name__ == "__main__":
    main(sys.argv)
