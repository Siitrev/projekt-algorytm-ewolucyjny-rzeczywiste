import sqlite3
import numpy as np

class DbController:
    """Klasa służąca do połączenia z bazą danych.\n
    Połączenie z naszą bazą danych jest ustanawiane automatycznie."""
    def __init__(self, db_name = "database/db.sqlite3") -> None:
        self.con = sqlite3.connect(db_name)
        cur = self.con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS dane_populacji(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            najlepszy TEXT, 
            srednia_populacji TEXT, 
            odchylenie_standardowe_populacji TEXT)
            """)
        cur.close()
        
    def insert_values(self, best : float, population_avg : float, population_dev : float):
        cur = self.con.cursor()
        cur.execute(f"""INSERT INTO dane_populacji(`najlepszy`,`srednia_populacji`,`odchylenie_standardowe_populacji`) VALUES(
            '{best}',
            '{population_avg}',
            '{population_dev}')
            """)
        self.con.commit()
        cur.close()
        
    def get_column(self, column : str) -> list[np.float64]:
        """Funkcja zwracająca wartości z danej kolumny w postaci listy.\n
            Mozliwe nazwy kolumn to: 
            najlepszy,
            srednia_populacji
            odchylenie_standardowe_populacji"""
        cur = self.con.cursor()
        res = cur.execute(f"""SELECT {column} FROM dane_populacji""")
        data = []
        for value in res.fetchall():
            data.append(np.float64(value[0]))
        cur.close()
        return data
    
    def clear_data(self):
        cur = self.con.cursor()
        cur.execute("DELETE FROM dane_populacji")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='dane_populacji'")
        self.con.commit()
        cur.close()
        
    def __del__(self):
        self.con.close()
        