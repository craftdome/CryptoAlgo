import sys
import hashlib
from VerticalPermutation import decrypt
from threading import Thread
from itertools import permutations
import matplotlib.pyplot as plt
import time


found_perm_key = None


def try_decode(input_string: str, perm_key: list, source_hash: str):
    t = time.time()
    global found_perm_key

    decoded_string = decrypt(input_string, perm_key)
    decoded_hash = hashlib.sha1(decoded_string.encode("windows-1251")).hexdigest()

    # print(" SHA1 => src", source_hash, "?= in", decoded_hash, ": ", decoded_hash == source_hash)

    if decoded_hash == source_hash:
        found_perm_key = perm_key.copy()

    print(round(time.time() - t, 3), "с")


def main(argv):
    """
    Формат консольной команды
    > VerticalPermHack.py (-options ...)
    -src            исходный файл
    -i              зашифрованный файл
    -maxKeyLength   максимальная длина ключа, до которой следует вести перебор
    -threads        режим работы (enc=шифрование, dec=дешифрование)
    Подсказка:
    [] - опциональный параметр
    () - обязательный параметр с выбором
    Примеры:
    > Подобрать ключ:  VerticalPermHack.py -src исходный_текст.txt -i encrypted.txt -maxKeyLength 7 -threads 8
    """

    source_file = None
    input_file = None
    threshold_key_length = 4
    num_threads = 4

    # Инициализация параметров argv
    try:
        for arg in sys.argv:
            if arg == "-src":
                source_file = open(argv[argv.index(arg) + 1], "r")
            if arg == "-i":
                input_file = open(argv[argv.index(arg) + 1], "r")
            if arg == "-maxKeyLength":
                threshold_key_length = int(argv[argv.index(arg) + 1])
            if arg == "-threads":
                num_threads = int(argv[argv.index(arg) + 1])

        if input_file is None:
            raise Exception("Входной файл не указан в аргументах")
        if source_file is None:
            raise Exception("Исходный файл не указан в аргументах")
        if threshold_key_length < 2:
            raise Exception("Длина ключа не может быть меньше 2")
        if 1 > num_threads > 100:
            raise Exception("Кол-во потоков не может быть меньше 1 и больше 100")
    except Exception as e:
        print("Ошибка в ведённых параметрах.", str(e))
        if input_file is not None:
            input_file.close()
        if source_file is not None:
            source_file.close()
        raise SystemExit(1)

    input_string = input_file.read()
    input_file.close()
    source_string = source_file.read()
    source_file.close()

    source_hash = hashlib.sha1(source_string.encode("windows-1251")).hexdigest()
    input_hash = hashlib.sha1(input_string.encode("windows-1251")).hexdigest()

    print(f"""
    Хэш исходного файла SHA1: {source_hash}
    Хэш зашифрованного файла SHA1: {input_hash}
    """)

    if source_hash == input_hash:
        print("Файлы идентичны")
        raise SystemExit(0)

    # Использование нескольких потоков не сказывается на скорости перебора ключей, лучше использовать
    # многопроцессорность Декларация пула потоков
    pull = {}
    for i in range(num_threads):
        pull[i] = None

    # Статистика по использованию потоков
    thread_stat = {i: 0 for i in range(num_threads)}

    # Старт перебора ключей
    for it in range(threshold_key_length - 1):

        # Выход из цикла, если какой-то поток нашёл нужный ключ
        if found_perm_key is not None:
            break

        # Генерация списка с элементами ключа
        key_elems = [str(i + 1) for i in range(it + 2)]
        # Комбинирование
        perms = list(permutations(key_elems))

        # Runtime статистика по прогрессу подбора в текущей длине ключа
        iter_progress = 0

        # Старт перебора комбинаций ключей
        for perm in perms:
            perm_key = list(perm)

            # Выход из цикла, если какой-то поток нашёл нужный ключ
            if found_perm_key is not None:
                break

            i = 0
            while True:

                # Вычисление номера потока
                # Нужен для выбора другого потока, когда текущий занят
                thread_number = i % num_threads
                thread = pull.get(thread_number)

                if thread is None or not thread.is_alive():

                    thread = Thread(target=try_decode, args=(input_string, perm_key, source_hash), daemon=True)
                    thread.start()
                    pull[thread_number] = thread

                    # Статистика
                    thread_stat[thread_number] = thread_stat.get(thread_number) + 1

                    print(">>> [", thread_number, "] Длина ключа\t", it + 2, "\tПрогресс\t",
                          round(iter_progress / len(perms) * 100, 2), "%\tКлюч\t", ",".join(perm_key), sep="")
                    break

                if thread_number == num_threads - 1:
                    print("ВСЕ ПОТОКИ ЗАНЯТЫ, ЖДЁМ ОСВОБОЖДЕНИЯ")

                i += 1

            iter_progress += 1

    print("Ключ не найден" if found_perm_key is None else f"Найденный ключ: {found_perm_key}")

    # Вывод статистики по использованым потокам
    fig, ax1 = plt.subplots(
        nrows=1, ncols=1,
        figsize=(18, 6)
    )

    ax1.grid(axis="y")
    ax1.bar(
        list(thread_stat.keys()),
        thread_stat.values(),
        color='g'
    )
    ax1.set_title(f"Статистика по использованию потоков\n"
                  f"Ключ: {','.join(found_perm_key if found_perm_key is not None else 'None')}")
    ax1.set_xlabel("Номер потока")
    ax1.set_ylabel("Кол-во обработанных операций от общего объёма")
    plt.show()


# Вход в программу
if __name__ == "__main__":
    main(sys.argv)
