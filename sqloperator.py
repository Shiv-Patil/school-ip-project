import sqlite3
import os
from kivymd.app import MDApp

app = MDApp.get_running_app()


class SqlOperator:
    def __init__(self):
        self.storage_dir = os.path.join(getattr(app, "user_data_dir"), "database")
        if not os.path.isdir(self.storage_dir):
            os.makedirs(self.storage_dir)
        self.PATH = os.path.join(self.storage_dir, "user_db.dQw4w9WgXcQ")
        self._check_tables()

    def _check_tables(self):
        get_tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        for table in self.execute_query(get_tables_query):
            if table not in (("students",), ("academic_year",), ("marks",)):
                app.logger.error("App: Dropping table " + table[0] + " as not used.")
                self.execute_query("DROP TABLE IF EXISTS " + table[0])

        columns = [i[1] for i in self.execute_query("PRAGMA table_info (students)")]
        if columns != [
            "id",
            "first_name",
            "middle_name",
            "last_name",
        ]:
            app.logger.error("App: Table 'students' invalid! Creating...")
            self.execute_query("DROP TABLE IF EXISTS students")
            self._create_tables()

        columns = [
            i[1] for i in self.execute_query("PRAGMA table_info (academic_year)")
        ]
        if columns != ["id", "student", "class", "division", "year_start"]:
            app.logger.error("App: Table 'academic_year' invalid! Creating...")
            self.execute_query("DROP TABLE IF EXISTS academic_year")
            self._create_tables()

        columns = [i[1] for i in self.execute_query("PRAGMA table_info (marks)")]
        if columns != [
            "id",
            "academic_year",
            "exam",
            "month",
            "mathematics",
            "english",
            "phyiscs",
            "chemistry",
            "informatics_practices",
        ]:
            app.logger.error("App: Table 'marks' invalid! Creating...")
            self.execute_query("DROP TABLE IF EXISTS marks")
            self._create_tables()

    def _create_tables(self):
        students = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY NOT NULL,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            last_name TEXT
        )
        """
        academic_year = """
        CREATE TABLE IF NOT EXISTS academic_year (
            id INTEGER PRIMARY KEY NOT NULL,
            student INTEGER NOT NULL,
            class TEXT NOT NULL,
            division BOOLEAN,
            year_start INTEGER NOT NULL,
            FOREIGN KEY (student) REFERENCES students (id) ON DELETE CASCADE
        )
        """
        marks = """
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY NOT NULL,
            academic_year INTEGER NOT NULL,
            exam TEXT NOT NULL,
            month TEXT,
            mathematics INTEGER,
            english INTEGER,
            phyiscs INTEGER,
            chemistry INTEGER,
            informatics_practices INTEGER,
            FOREIGN KEY (academic_year) REFERENCES academic_year (id) ON DELETE CASCADE
        )
        """

        self.execute_query(students)
        self.execute_query(academic_year)
        self.execute_query(marks)

        app.logger.info("App: Database initialized")

    def _create_connection(self):
        if not os.path.isdir(self.storage_dir):
            os.makedirs(self.storage_dir)
        connection = None
        try:
            connection = sqlite3.connect(self.PATH, timeout=10)
        except Exception as e:
            app.logger.error("App: " + str(e))
        return connection

    def execute_query(self, query, values=()):
        connection = self._create_connection()
        cursor = connection.cursor()
        result = False
        try:
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(query, values)
            result = cursor.fetchall() or True
            connection.commit()
            connection.close()
        except Exception as e:
            app.logger.error("App: " + str(e))
            connection.close()
        finally:
            return result
