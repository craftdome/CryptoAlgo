import sys
from io import open
from Crypto.Random import random
import hashlib


class PrivateKey:

    n = None
    p = None
    q = None
    d = None
    inited = True

    def __init__(self, key=None, from_file=None):
        """
        :param key: ключ вида k(n, p, q, e, d), из колторого будет извлечена секретная часть
        :param from_file: файл, в котором хранится закрытый ключ в виде "n,p,q,d"
        """
        if from_file is not None:
            args = from_file.read().split(",")
            self.n, self.p, self.q, self.d = [int(arg) for arg in args]
        elif key is not None:
            self.n, self.p, self.q, self.d = key[0], key[1], key[2], key[3]
        else:
            self.inited = False

    def write_to_file(self, file):
        if self.inited:
            file.write(",".join(str(item) for item in [self.n, self.p, self.q, self.d]))

    # Электронная цифровая подпись
    def make_digital_sign(self, from_file=None) -> str:
        """
        Создание цифровой подписи по хэшу входного файла
        :return: результат применение закрутого ключа (т. е. ЭЦП)
        """
        sha1_hash = hashlib.sha1(from_file.read().encode("utf-8")).digest()
        res = self.apply(sha1_hash, bytes_read=1, bytes_write=3).hex()
        return res

    # Решил не умничать с наследованием, поэтому эта функция продублирована для удобства
    def apply(self, byte_array: bytes, bytes_read=3, bytes_write=1) -> bytes:
        """
        Применяет действие ключа над набором байт
        :param byte_array: входной файл в виде байтов
        :param bytes_write: сколькими байтами будет записано число после формирования
        :param bytes_read: сколько байт будут считаны с файла перед тем как сформировать число,
        например, для числа от 255 и до 65536 нужно 2 байта, т. к. это == [2^8, 2^16)
        :return: байты после преобразования
        """
        result = bytearray()

        if self.inited:
            # Буфер для записи bytes_read_at_once байт из byte_array
            # Нужно когда считываем число из файла весит больше 1 байта
            buff = bytearray()

            i = 1
            for byte in byte_array:
                # Добавляем в буфер считанный байт
                buff.append(byte)

                # Если в буфере накопилось bytes_read_at_once байт
                if i % bytes_read == 0:
                    # Конвертируем number_length байт в int и применяем
                    # формулу дешифровки D = C^d mod n
                    x = (int.from_bytes(buff, byteorder='big', signed=False) ** self.d) % self.n

                    # Записываем полученное int-число байтами
                    # Запись в bytes_write_at_once байт накладывает ограничение на генерацию ключей
                    # по размеру простых чисел
                    result.extend(x.to_bytes(bytes_write, byteorder='big', signed=False))
                    # if x > 255:
                    #     # Запись в 3 байта накладывает ограничение на генерацию ключей
                    #     # по размеру простых чисел
                    #     result.extend(x.to_bytes(3, byteorder='big', signed=False))
                    # else:
                    #     # Запись одним байтом не требует extend()
                    #     result.append(x)

                    # Очистка буфера
                    buff.clear()

                i += 1

        return result

    def __repr__(self):
        return f"PrivateKey(n={self.n}, p={self.p}, q={self.q}, d={self.d})"


class PublicKey:

    n = None
    e = None
    inited = True

    def __init__(self, key=None, from_file=None):
        """
        :param key: ключ вида k(n, p, q, e, d), из колторого будет извлечена секретная часть
        :param from_file: файл, в котором хранится закрытый ключ в виде "n,p,q,d"
        """
        if from_file is not None:
            args = from_file.read().split(",")
            self.n, self.e = [int(arg) for arg in args]
        elif key is not None:
            self.n, self.e = key[0], key[1]
        else:
            self.inited = False

    def write_to_file(self, file):
        if self.inited:
            file.write(",".join(str(item) for item in [self.n, self.e]))

    def validate_digital_sign(self, validate_file=None, sign_file=None):
        """
        Проверка цифровой подписи по алгоритму SHA1
        :param validate_file: файл, который подвергается проверке
        :param sign_file: подпись в hex-формате
        :return: True если документ не изменён, иначе False
        """
        # Считаем хэш файла, который собираемся проверять на целосность
        sha1_hash = hashlib.sha1(validate_file.read().encode("utf-8")).digest()

        # Считываем строку из файла с ЭЦП и переводим хекс в байты
        digest = bytes.fromhex(sign_file.read())

        # Считываем наш дайджест по 3 байта и применяем действие открытого ключа
        eds = self.apply(digest, bytes_read=3, bytes_write=1)
        return eds == sha1_hash

    # Решил не умничать с наследованием, поэтому эта функция продублирована для удобства
    def apply(self, byte_array: bytes, bytes_read=1, bytes_write=3) -> bytes:
        """
        Применяет действие ключа над набором байт
        :param byte_array: входной файл в виде байтов
        :param bytes_write: сколькими байтами будет записано число после формирования
        :param bytes_read: сколько байт будут считаны с файла перед тем как сформировать число,
        например, для числа от 255 и до 65536 нужно 2 байта, т. к. это == [2^8, 2^16)
        :return: байты после преобразования
        """
        result = bytearray()

        if self.inited:
            # Буфер для записи bytes_read_at_once байт из byte_array
            buff = bytearray()

            i = 1
            for byte in byte_array:
                # Добавляем в буфер считанный байт
                buff.append(byte)

                # Если в буфере накопилось bytes_read_at_once байт
                if i % bytes_read == 0:
                    # Шифруем символ по формуле: C = M^e mod n
                    x = (int.from_bytes(buff, byteorder='big', signed=False) ** self.e) % self.n

                    # Записываем полученное int-число байтами
                    # Запись в bytes_write_at_once байт накладывает ограничение на генерацию ключей
                    # по размеру простых чисел
                    result.extend(x.to_bytes(bytes_write, byteorder='big', signed=False))
                    # if x > 255:
                    #     # Запись в 3 байта накладывает ограничение на генерацию ключей
                    #     # по размеру простых чисел
                    #     result.extend(x.to_bytes(3, byteorder='big', signed=False))
                    # else:
                    #     # Запись одним байтом не требует extend()
                    #     result.append(x)

                    # Очистка буфера
                    buff.clear()

                i += 1

        return result

    def __repr__(self):
        return f"PublicKey(n={self.n}, e={self.e})"


class KeyPair:

    def __init__(self, p=1, q=1):
        self.__n = None
        self.__p = None
        self.__q = None
        self.__e = None
        self.__d = None
        if p == 1 or q == 1:
            self.p, self.q = KeyPair.create_2_prime_number()
        else:
            self.p = p
            self.q = q
        self.__generate()

    @staticmethod
    def gcd(a: int, b: int) -> int:
        if b == 0:
            return a
        else:
            return KeyPair.gcd(b, a % b)

    @staticmethod
    def gcd_extended(num1, num2):
        if num1 == 0:
            return num2, 0, 1
        else:
            div, x, y = KeyPair.gcd_extended(num2 % num1, num1)
        return div, y - (num2 // num1) * x, x

    @staticmethod
    def is_prime(num: int) -> bool:
        """
        :return: Возвращает True, если число :param num: простое, иначе False
        """
        return all(num % i != 0 for i in range(2, num))

    @staticmethod
    def get_prime_range(start=2, amount=100) -> list:
        """
        Генерация списка простых чисел в прямой последовательность от :param start: до кол-ва :param amount:
        :return: Список простых чисел
        """
        primes = list()
        start = 2 if start < 2 else start
        amount = 1 if amount < 1 else amount

        if start == 2:
            primes.append(2)
            start += 1

        while len(primes) < amount:
            if KeyPair.is_prime(start):
                primes.append(start)
            start += 1

        return primes

    @staticmethod
    def rand_prime_range(start: int, amount: int) -> list:
        """
        Генерация списка случайных простых чисел в диапазоне от :param start: до кол-ва :param amount:
        :return: список случайных простых чисел
        """
        prime_range = KeyPair.get_prime_range(start, amount)
        return [random.choice(prime_range) for _ in range(amount)]

    @staticmethod
    def __e_gen(fi: int) -> int:
        """
        :param fi: fi(n) = (p - 1) * (q - 1)
        :return: нечётное число e, которое не имеет общих делителей с fi(n)
        """
        e = 3
        while True:
            if KeyPair.gcd(fi, e) == 1:
                return e
            e += 2

    @staticmethod
    def __d_gen(fi: int, e: int) -> int:
        """
        :return: секретное число d, которое используется в дешифровании
        """
        div, v, u = KeyPair.gcd_extended(fi, e)
        return u % fi

    @staticmethod
    def create_2_prime_number():
        """Генерация двух случайных простых чисел"""
        primes = KeyPair.rand_prime_range(start=17, amount=100)

        p = random.choice(primes)
        q = random.choice(primes)

        return p, q

    def __generate(self):
        """Функция генерации ключа, состоящего из открытого и закрытого ключей"""

        self.n = self.p * self.q
        fi = (self.p - 1) * (self.q - 1)
        self.e = KeyPair.__e_gen(fi)
        self.d = KeyPair.__d_gen(fi, self.e)

        print("Key test:", "OK" if (self.e*self.d) % fi == 1 else "NOT OK")

    def export_private_key(self):
        return PrivateKey(key=[self.n, self.p, self.q, self.d])

    def export_public_key(self):
        return PublicKey(key=[self.n, self.e])


# Главная функция
def main(argv):
    """
    Формат консольной команды
    > RSAKeyGen.py (-options ...)
    -pubk   файл, в который будет помещён открытый ключ RSA
    -prik   файл, в который будет помещён закрытый ключ RSA
    Подсказка:
    [] - опциональный параметр
    () - обязательный параметр с выбором
    Примеры:
    > Создать ключи:    RSAKeyGen.py -pubk public.key -prik private.key
    """

    public_key_file = None
    private_key_file = None

    # Инициализация параметров sys.argv
    try:
        for arg in argv:
            if arg == "-pubk":
                public_key_file = open(argv[argv.index(arg) + 1], "w+", encoding="utf-8")
            elif arg == "-prik":
                private_key_file = open(argv[argv.index(arg) + 1], "w+", encoding="utf-8")

        if public_key_file is None:
            raise Exception("Файл открытого ключа не указан в аргументах")
        if private_key_file is None:
            raise Exception("Файл закрытого ключа не указан в аргументах")
    except Exception as e:
        print("Ошибка в ведённых параметрах.", str(e))
        if public_key_file is not None:
            public_key_file.close()
        if private_key_file is not None:
            private_key_file.close()
        raise SystemExit(1)

    # Генерация ключей
    key_pair = KeyPair()

    # Экспорт открытого и закрытого ключей
    public_key = key_pair.export_public_key()
    private_key = key_pair.export_private_key()

    # Запись ключей в файлы
    public_key.write_to_file(public_key_file)
    private_key.write_to_file(private_key_file)

    public_key_file.close()
    private_key_file.close()

    print(f"""
    Файл открытого ключа: {public_key_file.name}
    Файл закрытого ключа: {private_key_file.name}
    Ключи:
     {public_key}
     {private_key}
    """)


# Вход в программу
if __name__ == "__main__":
    main(sys.argv)
