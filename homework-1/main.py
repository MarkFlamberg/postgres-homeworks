"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import csv


class DBFiller:
    def __init__(self, filename: object, tablename: object) -> object:
        self.filename = filename
        self.tablename = tablename

        # Создание соединения с БД
        self.conn = psycopg2.connect(host='localhost', database='north', user='postgres', password='12345')
        # Создание курсора для выполнения запросов к БД
        self.cur = self.conn.cursor()

    def fill_table(self):

        try:
            # открытие файла csv и чтение данных
            with open(self.filename, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # считываем наименования заголовков таблицы

                # выполнение sql-запросов для вставки данных в таблицу
                for row in reader:
                    query = f"insert into {self.tablename} ({','.join(headers)}) values ({','.join(['%s'] * len(headers))})"
                    self.cur.execute(query, row)

                    # подтверждение транзакции
                    self.conn.commit()

        finally:
            # закрытие курсора и соединения с базой данных
            self.cur.close()
            self.conn.close()


#employees = DBFiller('north_data/employees_data.csv', 'employees')
#print(employees.fill_table())

#emp = DBFiller('north_data/customers_data.csv', 'customers')
#print(emp.filename)
#emp.fill_table()

orders = DBFiller('north_data/orders_data.csv', 'orders')
orders.fill_table()