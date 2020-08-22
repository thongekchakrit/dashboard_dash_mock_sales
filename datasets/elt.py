'''
connect with operation database 
create a denormalized dataframe for dataware house
'''

import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from sqlite3 import Error

# ------------------------------------------------------------------------------
def create_connection(db_file):
    '''
    create connection with operation database
    '''
    try:
        conn = sqlite3.connect(db_file)
        return conn
    
    except Error as e:
        return print (e)

# ------------------------------------------------------------------------------        
def create_cursor(conn, sql_query):
    '''
    hold the rows returned by sql query
    '''
    try:
        cursor = conn.cursor()
        
    except:
        print('\nPlease check database path!')
    
    try:  
        return cursor.execute(sql_query)
    
    except UnboundLocalError as u:
        print(u)
        
    else: 
        print('\nTable in database and query does not match!')

# ------------------------------------------------------------------------------
def get_datawarehouse_dataframe():
    '''
    create a dataframe for dataware house
    '''
    
    db_file = 'operation.db'

    order_details_query = '''
    SELECT
        strftime('%Y', OH.OrderDate) as Year,
        CASE
            WHEN strftime('%m', OH.OrderDate) BETWEEN '01' AND '03' THEN 1
            WHEN strftime('%m', OH.OrderDate) BETWEEN '04' AND '06' THEN 2
            WHEN strftime('%m', OH.OrderDate) BETWEEN '07' AND '09' THEN 3
            ELSE '4'
            END AS Quarter,
        ContactName as CustomerName,
        City,
        Country,
        round(OD.Sales, 2) as Sales, 
        round(OD.Discount, 2) as Discount, 
        round(OD.Costs, 2) as Cost, 
        round(OD.Profit, 2) as Profit,
        Quantity,
        CASE 
            WHEN OD.Profit < 75 THEN 'Small'
            WHEN OD.Profit >= 75 AND Profit < 300 THEN 'Medium'
            ELSE 'Large' 
        END AS ProfitType,
        P.ProductName as Products,
        CAT.CategoryName as ProductCategory,
        EmployeeName,
        Latitude,
        Longitude
    FROM 
        ORDER_DETAILS as OD  
    INNER JOIN ORDER_HEADER as OH
        ON OH.OrderID = OD.OrderID
    INNER JOIN CUSTOMERS as C
        ON C.CustomerNumber = OH.CustomerID
    INNER JOIN PRODUCTS as P
        ON P.ProductID = OD.ProductID
    INNER JOIN CATEGORIES as CAT
        ON CAT.CategoryID = P.CategoryID
    INNER JOIN EMPLOYEES as EM
        ON EM.EmployeeID = OH.EmployeeID
    '''

    try:
        conn = create_connection(db_file)
    except:
        print('\nCannot create connection to database!')

    try:
        cursor = create_cursor(conn, order_details_query)
    except:
        print('\nTable cannot be found!')
    
    try:
        master_df = pd.DataFrame(cursor, columns=[i[0] for i in cursor.description])
    except:
        print('\nCannot convert query into dataframe!')
    
    return master_df

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    
    get_datawarehouse_dataframe()


