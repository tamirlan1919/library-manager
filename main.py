import json
from pathlib import Path


class LibraryManager:
    def __init__(self):
        self.data_file = "library.json"
        self.library_data = {}

        # Загрузка данных из файла при инициализации
        if Path(self.data_file).exists():
            with open(self.data_file) as file:
                try:
                    self.library_data = json.load(file)
                except json.JSONDecodeError:
                    print("Ошибка чтения файла. Файл поврежден.")

    def save_to_file(self):
        """Сохраняет данные в файл."""
        with open(self.data_file, 'w') as file:
            json.dump(self.library_data, file, indent=4)

    def add_book(self, title: str, author: str, year: int) -> str:
        """Добавляет новую книгу в библиотеку."""
        book_id = len(self.library_data) + 1
        new_book = {
            "id": book_id,
            "title": title,
            "author": author,
            "year": int(year),
            "status": "в наличии"
        }
        self.library_data[str(book_id)] = new_book
        self.save_to_file()
        return f"Книга '{title}' успешно добавлена."

    def delete_book(self, book_id: str) -> str:
        """Удаляет книгу по её ID."""
        if str(book_id) in self.library_data:
            del self.library_data[str(book_id)]
            self.save_to_file()
            return f"Книга с ID {book_id} удалена."
        else:
            return f"Нет книги с таким ID: {book_id}"

    def search_books(self, query=None, field="title") -> list[str]:
        """Ищет книги по названию, автору или году."""
        results = []
        for book in self.library_data.values():
            if query is None or str(query).lower() in str(book[field]).lower():
                results.append(book)
        return results

    def display_all_books(self) -> str:
        """Выводит все книги в библиотеке."""
        books = list(self.library_data.values())
        if not books:
            return "Библиотека пуста."
        output = "\n".join([f"{b['id']}. {b['title']} ({b['author']}, {b['year']}) - {b['status']}" for b in books])
        return output

    def change_status(self, book_id: int, new_status: str) -> str:
        """Изменяет статус книги."""
        if str(book_id) in self.library_data:
            self.library_data[str(book_id)]["status"] = new_status
            self.save_to_file()
            return f"Статус книги с ID {book_id} изменён на '{new_status}'."
        else:
            return f"Нет книги с таким ID: {book_id}"


def main():
    library_manager = LibraryManager()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                title = input("Название книги: ").strip()
                author = input("Автор книги: ").strip()
                year = input("Год издания: ").strip()

                result = library_manager.add_book(title, author, int(year))
                print(result)

            elif choice == "2":
                book_id = input("ID книги для удаления: ").strip()
                result = library_manager.delete_book(int(book_id))
                print(result)

            elif choice == "3":
                query = input("Поисковый запрос (оставьте пустым для поиска всех): ").strip().lower()
                field = input("Поле для поиска (title/author/year): ").strip().lower()
                results = library_manager.search_books(query, field)

                if results:
                    for book in results:
                        print(f"{book['id']}. {book['title']} ({book['author']}, {book['year']}) - {book['status']}")
                else:
                    print("Книг не найдено.")

            elif choice == "4":
                all_books = library_manager.display_all_books()
                print(all_books)

            elif choice == "5":
                book_id = input("ID книги для изменения статуса: ").strip()
                new_status = input("Новый статус книги: ").strip()

                result = library_manager.change_status(int(book_id), new_status)
                print(result)

            elif choice == "0":
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

        except ValueError as e:
            print(f"Произошла ошибка: {e}. Проверьте введённые данные и попробуйте снова.")
        except KeyError as e:
            print(f"Произошла ошибка: {e}. Проверьте введённый параметр и попробуйте снова.")
        except Exception as e:
            print(f"Произошла неожиданная ошибка: {e}. Попробуйте ещё раз.")


if __name__ == "__main__":
    main()