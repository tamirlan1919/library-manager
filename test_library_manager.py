import unittest
from main import LibraryManager


class TestLibraryManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass  # Оставляем этот метод пустым, так как его роль теперь выполняет setUp

    def setUp(self):
        self.manager = LibraryManager()
        self.book_1 = {"id": 1, "title": "Книга 1", "author": "Автор 1", "year": 2020, "status": "в наличии"}
        self.book_2 = {"id": 2, "title": "Книга 2", "author": "Автор 2", "year": 2019, "status": "в наличии"}
        self.manager.library_data = {'1': self.book_1, '2': self.book_2}

    def test_add_book(self):
        # Проверка добавления новой книги
        result = self.manager.add_book('Новая книга', 'Новый автор', 2021)
        self.assertEqual(result, "Книга 'Новая книга' успешно добавлена.")
        self.assertIn('3', self.manager.library_data)
        self.assertDictEqual(
            self.manager.library_data['3'],
            {"id": 3, "title": "Новая книга", "author": "Новый автор", "year": 2021, "status": "в наличии"}
        )

    def test_delete_book(self):
        # Проверка удаления существующей книги
        result = self.manager.delete_book('1')
        self.assertEqual(result, "Книга с ID 1 удалена.")
        self.assertNotIn('1', self.manager.library_data)

        # Проверка попытки удалить несуществующую книгу
        result = self.manager.delete_book('10')
        self.assertEqual(result, "Нет книги с таким ID: 10")

    def test_search_books(self):
        # Поиск по названию
        results = self.manager.search_books('Книга 1', 'title')
        self.assertListEqual(results, [self.book_1])

        # Поиск по автору
        results = self.manager.search_books('Автор 2', 'author')
        self.assertListEqual(results, [self.book_2])

        # Поиск по году
        results = self.manager.search_books(2020, 'year')
        self.assertListEqual(results, [self.book_1])

        # Поиск всех книг
        results = self.manager.search_books()
        self.assertListEqual(results, [self.book_1, self.book_2])

    def test_display_all_books(self):
        # Проверка отображения всех книг
        expected_output = "1. Книга 1 (Автор 1, 2020) - в наличии\n2. Книга 2 (Автор 2, 2019) - в наличии"
        actual_output = self.manager.display_all_books()
        self.assertEqual(actual_output, expected_output)

    def test_change_status(self):
        # Проверка изменения статуса существующей книги
        result = self.manager.change_status(1, 'выдана')
        self.assertEqual(result, "Статус книги с ID 1 изменён на 'выдана'.")
        self.assertEqual(self.manager.library_data['1']['status'], 'выдана')

        # Проверка попытки изменить статус несуществующей книги
        result = self.manager.change_status(10, 'выдана')
        self.assertEqual(result, "Нет книги с таким ID: 10")


if __name__ == '__main__':
    unittest.main()