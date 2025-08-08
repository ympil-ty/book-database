import sqlite3


class BookDatabase:
    def __init__(self, db_name="book.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """соединение с БД"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """Закрывает соединение с БД"""
        if self.conn:
            self.conn.close()

    def add_book(self):
        try:
            title = input("Введите название книги: ").strip()
            author = input("Введите автор книги: ").strip()
            year = input("Введите год выпуска книги: ").strip()

            if not title or not author:
                print("Ошибка: название или автор не могут быть пустыми!")
                return
            try:
                year = int(year)
            except ValueError:
                print("Ошибка: год должен быть числом!")
                return

            self.connect()

            self.cursor.execute(
                "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
                (title, author, year)
            )
            self.conn.commit()
            print(f"Книга '{title}' успешно добавлена!")
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
        finally:
            self.close()

    def show_books(self):
        self.connect()
        self.cursor.execute("SELECT * FROM books ORDER BY title")
        books = self.cursor.fetchall()
        self.close()

        if not books:
            print("\nВ библиотеке пока нет книг! ")
            return
        print("\n=== Список книг ===")
        for book in books:
            id, title, author, year = book
            print(f"{id}. {title}")
            print(f"   Автор: {author}")
            print(f"   Год: {year}")
            print("-------------------")

    def delete_books(self):
        try:
            self.show_books()

            id_delete = int(input("Введите ID книги для удаления: "))

            self.connect()
            self.cursor.execute("SELECT id FROM books WHERE id = ?",
                                (id_delete,))
            if not self.cursor.fetchone():
                print("Ошибка: такого ID нет!")
                return
            sol = input("Удалить книгу? (да/нет): ").lower()
            if sol != "да":
                print("Отменено!")
                return

            self.cursor.execute("DELETE FROM books WHERE id = ?",
                                (id_delete,))
            self.conn.commit()
            print("Книга удалена!")

        except ValueError:
            print("Ошибка: ID должен быть числом!")
        except sqlite3.Error as e:
            print(f"Ошибка БД: {e}")
        finally:
            self.close()

    def search_books(self):
        keyword = input("Введите название книги или автора для поиска: ").strip()
        if not keyword:
            print("Ошибка: поисковый запрос не может быть пустым!")
            return

        try:
            self.connect()
            self.cursor.execute("""
                SELECT * FROM books 
                WHERE title LIKE ? OR author LIKE ?
                ORDER BY title""",
                (f"%{keyword}%", f"%{keyword}%"))

            books = self.cursor.fetchall()

            if not books:
                print("\nКниги не найдены")
                return

            print(f"\n=== Результаты поиска ({len(books)}): ===")
            for book in books:
                id, title, author, year = book
                print(f"{id}. {title}")
                print(f"   Автор: {author}")
                print(f"   Год: {year}")
                print("-------------------")

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
        finally:
            self.close()

    def menu(self):
        while True:
            print("\n=== Меню управления библиотекой ===")
            print("1. Добавить книгу")
            print("2. Показать все книги")
            print("3. Удалить книгу")
            print("4. Найти книгу")  # Новый пункт
            print("5. Выйти")
            print("\n")

            choice = input("Выберите действие (1-5): ").strip()

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.show_books()
            elif choice == "3":
                self.delete_books()
            elif choice == "4":  # Обработка поиска
                self.search_books()
            elif choice == "5":
                print("Выход из программы...")
                break
            else:
                print("Неверный ввод! Пожалуйста, выберите 1-5.")


if __name__ == "__main__":
    db = BookDatabase()

    # Создаем таблицу при первом запуске
    try:
        db.connect()
        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL
            )
        """)
        db.conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        db.close()

    # Запускаем меню
    db.menu()

