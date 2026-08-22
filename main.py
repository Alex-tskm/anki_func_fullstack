import time
import sys
import random
from typing import Dict, Tuple

WORDS_FILE = "words.txt"


def load_words(filename: str = WORDS_FILE) -> Dict[str, str]:
    """
    Загружает пары «слово, перевод» из файла и формирует словарь.

    :param filename: имя файла (по умолчанию 'words.txt')
    :return: словарь Dict[str, str] (ключ — слово, значение — перевод)
    """
    words: Dict[str, str] = {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",", 1)
                if len(parts) == 2:
                    word, translation = parts
                    words[word] = translation
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден. Создан пустой словарь.")
        return words

    return words


def save_words(words: Dict[str, str], filename: str = WORDS_FILE) -> None:
    """
    Сохраняет пары «слово, перевод» из словаря в текстовый файл.

    :param words: словарь пар «слово: перевод»
    :param filename: имя файла для сохранения (по умолчанию 'words.txt')
    """
    count = 0
    with open(filename, "w", encoding="utf-8") as f:
        for word, translation in words.items():
            f.write(f"{word},{translation}\n")
            count += 1

    print(f"Было сохранено {count} слов в файл {filename}")


def add_words(words: Dict[str, str]) -> None:
    """
    Добавляет пары «слово — перевод» в словарь в интерактивном режиме.

    Ввод завершается при вводе слова «СТОП»
    (независимо от регистра и пробелов).1
    Словарь изменяется по месту.

    :param words: словарь пар «слово: перевод», который дополняется
    """
    stop_word = "стоп"
    print("Для завершения ввода введите СТОП в качестве слова или перевода.\n")

    while True:
        word = input("Введите слово: ").strip()
        if word.lower() == stop_word:
            break

        translation = input("Введите перевод: ").strip()
        if translation.lower() == stop_word:
            break

        if not word or not translation:
            print("Слова не могут быть пустыми. Попробуйте снова.\n")
            continue

        words[word] = translation
        print(f"Пара '{word} — {translation}' добавлена.\n")


def ask_and_check(word: str, correct: str) -> Tuple[bool, bool, float]:
    """
    Спрашивает у пользователя перевод заданного слова.

    :param word: слово для перевода (выводится пользователю)
    :param correct: правильный перевод
    :return: (need_exit, is_correct, answer_time)
        need_exit: True, если пользователь ввёл СТОП
        is_correct: True при верном ответе (регистр и пробелы не важны)
        answer_time: время ответа в секундах
    """
    print(f"Ваше слово: {word}")

    start = time.time()
    user_answer = input("Ваш перевод: ").strip()
    elapsed = time.time() - start

    stop_word = "стоп"
    if user_answer.lower() == stop_word:
        return True, False, 0.0

    is_correct = user_answer.lower() == correct.lower()
    return False, is_correct, elapsed


def print_statistics(score: int, total_time: float) -> None:
    """
    Выводит итоговую статистику игры.

    :param score: количество правильных ответов
    :param total_time: общее время игры в секундах
    """
    if score > 0:
        avg_time = total_time / score
        avg_display = f"{avg_time:.2f}"
    else:
        avg_display = "—"

    print()
    print(f"Ваш итоговый счёт: {score}")
    print(
        f"Время игры: {total_time:.2f} секунд "
        f"(среднее время: {avg_display} сек.)"
    )


def train_until_mistake(words: Dict[str, str]) -> None:
    """
    Режим «до первой ошибки»: случайные слова, выход при ошибке или СТОП.

    :param words: словарь пар «слово: перевод»
    """
    if not words:
        print("Словарь пуст. Сначала добавьте слова.\n")
        return

    print("Режим: Игра до первой ошибки! Чтобы выйти вручную, введите СТОП\n")

    keys = list(words.keys())
    score = 0
    total_time = 0.0

    while True:
        word = random.choice(keys)
        correct_answer = words[word]

        result = ask_and_check(word, correct_answer)
        need_exit, is_correct, answer_time = result

        if need_exit:
            print("Выход из режима по запросу пользователя.")
            break

        total_time += answer_time

        if not is_correct:
            print(f"Ошибка! Неверно. Правильный ответ: {correct_answer}")
            break

        score += 1
        print(
            f"Верно! Всего очков: {score} "
            f"(ответ за {answer_time:.2f} секунд)"
        )

    print_statistics(score, total_time)


def start_game(words: Dict[str, str]) -> None:
    """
    Запускает игровой режим, в котором пользователь переводит случайные слова.

    Игра продолжается, пока пользователь не введёт СТОП.
    При неверном ответе игра не завершается — продолжается дальше.

    :param words: словарь пар «слово: перевод»
    """
    if not words:
        print("Словарь пуст. Сначала добавьте слова.\n")
        return

    print("Чтобы закончить, введите СТОП\n")

    keys = list(words.keys())
    score = 0
    total_time = 0.0

    while True:
        word = random.choice(keys)
        correct_answer = words[word]

        result = ask_and_check(word, correct_answer)
        need_exit, is_correct, answer_time = result

        if need_exit:
            break

        total_time += answer_time

        if is_correct:
            print(f"Верно! Время на ответ: {answer_time:.2f} секунд")
            score += 1
        else:
            print(
                f"Неправильно, правильный ответ: {correct_answer} "
                f"(Время на ответ: {answer_time:.2f} секунд)"
            )

    print("Спасибо за игру!")
    print_statistics(score, total_time)


def show_all_words(words: dict[str, str]) -> None:
    """
    Выводит все пары «слово — перевод» в одну строку.
    Пары разделены точкой с запятой и пробелом.
    Формат: «слово - перевод; слово - перевод».
    Если словарь пуст — выводится пустая строка.

    :param words: словарь пар «слово: перевод»
    """
    if not words:
        print()
        return

    pairs = [f"{ru} - {en}" for ru, en in words.items()]
    print("; ".join(pairs))


def main() -> None:
    """
    Главное меню: запускает основной цикл работы программы-тренажёра.

    Реализует меню выбора режимов.
    Обеспечивает взаимодействие пользователя с программой.
    Не принимает входных аргументов.
    """
    words = load_words()
    print(f"Было загружено {len(words)} слов из файла {WORDS_FILE}\n")

    while True:
        print("Меню:")
        print("    1. Начать игру")
        print("    2. Добавить слова")
        print("    3. Тренировка до первой ошибки")
        print("    4. Вывод всех слов")
        print("    5. Выход")
        choice = input("Пункт меню: ").strip()
        print()

        if choice == "1":
            start_game(words)
        elif choice == "2":
            add_words(words)
        elif choice == "3":
            train_until_mistake(words)
        elif choice == "4":
            show_all_words(words)
        elif choice == "5":
            save_words(words)
            print("Словарь сохранён. До свидания!")
            sys.exit(0)
        else:
            print("Неизвестный пункт меню. Попробуйте снова.\n")


if __name__ == "__main__":
    main()
