import sqlite3
import pandas as pd


class LocalDatabase:

    def __init__(self, db_name='./data/database/penny_ai.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, create_table_sql):
        self.cursor.execute(create_table_sql)

    def append_df(self, df, table_name):
        df.to_sql(table_name, self.conn, if_exists='append', index=False)
    
    def replace_df(self, df, table_name):
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)

    def query(self, query):
        return pd.read_sql_query(query, self.conn)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
        
    