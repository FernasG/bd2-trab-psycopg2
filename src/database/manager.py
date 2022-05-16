import psycopg2

from .config import config

class DatabaseManager:
    def __init__(self) -> None:
        self.__connection = psycopg2.connect(**config)
        self.__cursor = self.__connection.cursor()

    def insert(self, query: str, values: tuple) -> tuple:
        try:
            self.__cursor.execute(query, values)

            self.__connection.commit()

            return self.__cursor.fetchone()
        except Exception as error:
            self.__connection.rollback()
            print(f"DatabaseManager -> Error method 'insert': {str(error)}")
            return False

    def find_one(self, query: str) -> tuple:
        try:
            self.__cursor.execute(query)

            return self.__cursor.fetchone()
        except Exception as error:
            print(f"DatabaseManager -> Error method 'find_one': {str(error)}")
            return False

    def find_all(self, query: str, limit: int = None) -> list:
        try:
            self.__cursor.execute(query)

            return self.__cursor.fetchmany(limit) if limit else self.__cursor.fetchall()
        except Exception as error:
            print(f"DatabaseManager -> Error method 'find_all': {str(error)}")
            return False

    def update(self, query: str, values: tuple) -> tuple:
        try:
            self.__cursor.execute(query, values)

            self.__connection.commit()

            return True
        except Exception as error:
            self.__connection.rollback()
            print(f"DatabaseManager -> Error method 'update': {str(error)}")
            return False

    def delete(self, query: str, values: tuple) -> tuple:
        try:
            self.__cursor.execute(query, values)

            self.__connection.commit()

            count = self.__cursor.rowcount

            return count
        except Exception as error:
            self.__connection.rollback()
            print(f"DatabaseManager -> Error method 'delete': {str(error)}")
            return False

    def close(self):
        self.__cursor.close()
        self.__connection.close()