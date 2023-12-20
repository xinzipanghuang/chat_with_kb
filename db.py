import sqlite3

class DatabaseHandler:
    def __init__(self, db_name,table_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table_name=table_name
        
    def create_table(self, columns):
        """创建新表"""
        column_str = ", ".join([f"{col_name} {data_type}" for col_name, data_type in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({column_str})"
        self.cursor.execute(query)
        self.conn.commit()

    def insert_data(self, data):
        """插入数据"""
        placeholders = ", ".join(["?"] * len(data))
        column_names = ", ".join(data.keys())
        query = f"INSERT INTO {self.table_name} ({column_names}) VALUES ({placeholders})"
        self.cursor.execute(query, list(data.values()))
        self.conn.commit()

    def query_data(self, columns="*", condition="1"):
        """查询数据"""
        query = f"SELECT {columns} FROM {self.table_name} WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_data(self, data, condition):
        """更新数据"""
        update_str = ", ".join([f"{key} = ?" for key in data])
        query = f"UPDATE {self.table_name} SET {update_str} WHERE {condition}"
        self.cursor.execute(query, list(data.values()))
        self.conn.commit()

    def delete_data(self, condition):
        """删除数据"""
        query = f"DELETE FROM {self.table_name} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        """关闭数据库连接"""
        self.conn.close()
