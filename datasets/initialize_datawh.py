'''
create denormalized table for data warehouse
change the table according to business needs
'''
import sqlite3 
import pandas as pd
from  sqlite3 import Error

# ------------------------------------------------------------------------------
def create_connection(dw_file):
    '''
    create connection with data warehouse
    '''
    try:
        conn = sqlite3.connect(dw_file)
        return conn

    except Error as e:
        print(e)

# ------------------------------------------------------------------------------
def create_table_sql(conn, sql_query):
    '''
    create denormalized table from sql_query
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)

    except Error as e:
        print(e)

# ------------------------------------------------------------------------------
def main():
    '''
    create denormolized framework for data
    '''
    database = 'data_warehouse.db'

    data_warehouse = '''
    
    CREATE TABLE IF NOT EXISTS MASTER_FILE(
        Year INT NOT NULL CHECK(length(Year) = 4),
        Quarter INT NOT NULL CHECK(Quarter <= 4 AND Quarter >= 1),
        CustomerName CHAR(30) NOT NULL,
        City CHAR(30) NOT NULL,
        Country CHAR(30) NOT NULL,
        Sales DECIMAL(10,2) NOT NULL,
        Discount DECIMAL(10,2) NOT NULL,
        Cost DECIMAL(10,2) NOT NULL,
        Profit DECIMAL(15,2) NOT NULL CHECK(Profit > 0),
        ProfitType CHAR(6) NOT NULL,
        Quantity INT NOT NULL,
        Products CHAR(30) NOT NULL,
        ProductCategory CHAR(30) NOT NULL,
        EmployeeName CHAR(30) NOT NULL,
        Latitude FLOAT NOT NULL,
        Longitude FLOAT NOT NULL
    );
    '''

    # create a database connection
    conn = create_connection(database)

    if conn is not None:

        # create 
        create_table_sql(conn, data_warehouse)

        conn.commit()

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    
    try:
        main()
    except:
        print('Database exists!')