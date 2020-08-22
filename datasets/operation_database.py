'''
Setting up tables for operation database
'''
import sqlite3
from sqlite3 import Error

# ------------------------------------------------------------------------------
def create_connection(db_file):
    '''
    create a database connection to sqlite database
    '''
    try:
        conn = sqlite3.connect(db_file)
        return conn

    except Error as e:
        print(e)

    return conn

# ------------------------------------------------------------------------------
def create_table(conn, create_table_sql):
    '''
    create a table from the create_table_sql statement
    ''' 
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)

    except Error as e:
        print(e)

# ------------------------------------------------------------------------------
def main():
    '''
    create all tables
    '''
    database = 'operation.db'

    products = '''
    
    CREATE TABLE IF NOT EXISTS PRODUCTS(
        ProductID INTEGER NOT NULL UNIQUE PRIMARY KEY,
        ProductName CHAR(50),
        CategoryID INTEGER NOT NULL,
        SupplierID INTEGER NOT NULL
    );
    '''

    categories = '''

    CREATE TABLE IF NOT EXISTS CATEGORIES(
        CategoryID INTEGER NOT NULL UNIQUE PRIMARY KEY,
        CategoryName CHAR(50),
        Description CHAR(50)
    );
    '''

    suppliers = '''

    CREATE TABLE IF NOT EXISTS SUPPLIERS(
        SupplierID INTEGER NOT NULL UNIQUE PRIMARY KEY,
        Supplier CHAR(50),
        SupplierContact CHAR(50),
        SupplierCountry CHAR(50)
    );
    '''

    order_header = '''

    CREATE TABLE IF NOT EXISTS ORDER_HEADER(
        OrderID INTEGER NOT NULL UNIQUE PRIMARY KEY,
        OrderDate DATETIME,
        CustomerID INTEGER,
        EmployeeID INTEGER,
        FOREIGN KEY(CustomerID) REFERENCES CUSTOMERS(CustomerNumber),
        FOREIGN KEY(EmployeeID) REFERENCES EMPLOYEES(EmployeeID)
    );
    '''

    employees = '''

    CREATE TABLE IF NOT EXISTS EMPLOYEES(
        EmployeeID INTEGER NOT NULL UNIQUE PRIMARY KEY,
        EmployeeName CHAR(30) NOT NULL
    );
    '''

    customers = '''

    CREATE TABLE IF NOT EXISTS CUSTOMERS(
        CustomerNumber INTEGER NOT NULL UNIQUE PRIMARY KEY,
        ContactName CHAR(30),
        City CHAR(25),
        Country CHAR(50),
        Fax CHAR(15),
        Phone CHAR(15),
        Latitude FLOAT,
        Longitude FLOAT,
        Region CHAR(15),
        EmployeeID INTEGER  
    );
    '''

    order_details = '''

    CREATE TABLE IF NOT EXISTS ORDER_DETAILS(
        ProductID INTEGER NOT NULL,
        OrderID INTEGER NOT NULL,
        Quantity INTEGER,
        Sales DECIMAL (15, 2),
        Discount DECIMAL(8,2),
        Costs DECIMAL(8,2),
        Profit DECIMAL(8,2),
        FOREIGN KEY(ProductID) REFERENCES PRODUCTS(ProductID),
        FOREIGN KEY(OrderID) REFERENCES ORDER_HEADER(OrderID),
        PRIMARY KEY(ProductID, OrderID)
    );
    '''

    # create a database connection
    conn = create_connection(database)

    # create Tables

    if conn is not None:
       
        # create products table
        create_table(conn, products)

        # create categories table
        create_table(conn, categories)

        # create supplier table
        create_table(conn, suppliers)

         # create order_header table
        create_table(conn, order_header)

        # create employee table
        create_table(conn, employees)

        # create customers table
        create_table(conn, customers)

        # create order_details table
        create_table(conn, order_details)


        conn.commit()
       
    else:
        print('\nError cannot create database connection.')

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    try: 
        main()
    except:
        print('\nDatabase exists!')
    
