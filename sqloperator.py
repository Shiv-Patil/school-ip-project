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
        self._create_tables()

    def _create_tables(self):
        students = """
        CREATE TABLE IF NOT EXISTS students (
            gr_no INTEGER PRIMARY KEY NOT NULL,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            last_name TEXT,
            class TEXT NOT NULL,
            division TEXT,
            start_academic_year INTEGER NOT NULL
        )
        """
        exam = """
        CREATE TABLE IF NOT EXISTS exam (
            id INTEGER PRIMARY KEY NOT NULL,
            student INTEGER NOT NULL,
            name TEXT NOT NULL,
            month BOOLEAN,
            FOREIGN KEY (student) REFERENCES students (gr_no) ON DELETE CASCADE
        )
        """
        marks = """
        CREATE TABLE IF NOT EXISTS marks (
            exam INTEGER NOT NULL,
            mathematics INTEGER,
            english INTEGER,
            phyiscs INTEGER,
            chemistry INTEGER,
            informatics_practices INTEGER,
            FOREIGN KEY (exam) REFERENCES exam (id) ON DELETE CASCADE
        )
        """

        self.execute_query(students)
        self.execute_query(exam)
        self.execute_query(marks)

        columns = [i[1] for i in self.execute_query("PRAGMA table_info (students)")]
        if columns != [
            "gr_no",
            "first_name",
            "middle_name",
            "last_name",
            "class",
            "division",
            "start_academic_year",
        ]:
            app.logger.error("App: Table 'students' invalid! Recreating...")
            self.execute_query("DROP TABLE IF EXISTS students")
            return self._create_tables()

        columns = [i[1] for i in self.execute_query("PRAGMA table_info (exam)")]
        if columns != ["id", "student", "name", "month"]:
            app.logger.error("App: Table 'exam' invalid! Recreating...")
            self.execute_query("DROP TABLE IF EXISTS exam")
            return self._create_tables()

        columns = [i[1] for i in self.execute_query("PRAGMA table_info (marks)")]
        if columns != [
            "exam",
            "mathematics",
            "english",
            "phyiscs",
            "chemistry",
            "informatics_practices",
        ]:
            app.logger.error("App: Table 'marks' invalid! Recreating...")
            self.execute_query("DROP TABLE IF EXISTS marks")
            return self._create_tables()

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
