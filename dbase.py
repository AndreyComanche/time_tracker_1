from PyQt5 import QtCore, QtSql, QtGui
from datetime import date
from decimal import Decimal
import os


class Storage:
    def __init__(self):
        self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.con.setDatabaseName(os.path.join(os.getcwd(), r'db\timing.sqlite'))
        self.con.open()

        if 'timing' not in self.con.tables():
            query = QtSql.QSqlQuery()
            q_str = """
            CREATE TABLE timing(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                'ts_date' TEXT, 
                'ts_time' TEXT, 
                'te_date' TEXT, 
                'te_time' TEXT, 
                'task_time' TEXT
            )"""
            query.prepare(q_str)
            query.exec_()

    @staticmethod
    def insert(ts, te, tt):
        fmt = '%Y.%m.%d%H:%M:%S'
        query = QtSql.QSqlQuery()
        q_str = f"""
            INSERT INTO timing(
                'ts_date', 
                'ts_time', 
                'te_date', 
                'te_time', 
                'task_time') 
            VALUES(
                '{ts.strftime(fmt[:8])}', 
                '{ts.strftime(fmt[8:])}', 
                '{te.strftime(fmt[:8])}', 
                '{te.strftime(fmt[8:])}', 
                '{str(tt)}')"""
        query.prepare(q_str)
        query.exec_()

    @staticmethod
    def delete(item_id):
        query = QtSql.QSqlQuery()
        q_str = f"""
            DELETE FROM timing
            WHERE
                id = {item_id}"""
        query.prepare(q_str)
        query.exec_()

    @staticmethod
    def get_model(date_):
        result = QtGui.QStandardItemModel()
        query = QtSql.QSqlQuery()
        q_str = f"""
            SELECT ts_date AS date,
                SUM(task_time) AS 'total',
                COUNT(ts_date) AS 'count'
            FROM timing
                WHERE ts_date LIKE '{date_}%'
                GROUP BY ts_date
                ORDER BY id DESC
        """
        query.prepare(q_str)
        query.exec_()
        if query.isActive():
            query.first()
            while query.isValid():
                total = Storage.to_total_time(query.value('total'))
                date_ = Storage.to_date(query.value('date'))
                row = QtGui.QStandardItem(f"{date_}  total: {total}")
                row.setData(query.value('date'), QtCore.Qt.UserRole)
                result.appendRow(row)
                query.next()
            query.finish()
        for i in range(result.rowCount()):
            row = result.item(i)
            q_str = f"""
                    SELECT id AS 'id', ts_time AS 'time', task_time FROM timing
                    WHERE ts_date = '{row.data(QtCore.Qt.UserRole)}'
                    ORDER BY id DESC
                """
            query.prepare(q_str)
            query.exec_()
            if query.isActive():
                query.first()
                while query.isValid():
                    task = QtGui.QStandardItem(
                        f"{query.value('time')}\t{query.value('task_time')}"
                    )
                    task.setData(query.value('id'), QtCore.Qt.UserRole)
                    row.appendRow(task)
                    query.next()
                query.finish()
        return result

    @staticmethod
    def to_total_time(total):
        total = Decimal(str(total)).quantize(Decimal('0.01'))
        hours = str(total // Decimal("60"))
        hours = hours if len(hours) > 1 else f'0{hours}'
        minutes = str(total % Decimal("60"))
        minutes = minutes if len(minutes) > 4 else f'0{minutes}'
        return f'{hours}:{minutes}'

    @staticmethod
    def to_date(raw):
        return date(*[int(x) for x in raw.split('.')]).strftime('%A, %B %d')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()
        super().__exit__(exc_type, exc_val, exc_tb)
