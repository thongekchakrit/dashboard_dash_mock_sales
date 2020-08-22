# -*- coding: utf-8 -*-
'''
if operation database does not exist,
create operation database and populate database 
with data from xls files.

next, create data warehouse
create data warehouse tables
extract transformed data from operation.db
populate the data warehouse with extracted data
'''

import elt
import extract_load
import glob
import initialize_datawh
import operation_database
import os
import sqlite3
from sqlite3 import Error

# ------------------------------------------------------------------------------
# locating operation database
file_path = r'../datasets/sources'

def create_operation_database(file_path):
    '''
    create operation database 
    populate operation database
    '''
    # setting up tables for operation database
    operation_database.main()

    try:
        # extract and load source files into operation database
        extract_load.main(file_path)
        print('\nDatabase created and table populated!')

    except Error as e:
        print(str(e) + ': Primary key exists!')
        pass

# ------------------------------------------------------------------------------
def get_master_data_file():
    '''
    create connection with operation database 
    create a denormalized dataframe for dataware house
    '''

    try:
        return elt.get_datawarehouse_dataframe()

    except Error as e:
        print(e)

# ------------------------------------------------------------------------------
def check_operation_exists():
    '''
    check if operation.db exists in database_management folder
    '''
    
    # pointing to database_management folder
    folder_of_files = r'..\datasets'

    # search if 'operation.db' exists in folder
    files = glob.glob(os.path.join(folder_of_files, 'operation.db'))

    # return true if exists
    return True if files != [] else False

# ------------------------------------------------------------------------------
def check_datawh_exists():
    '''
    check if data_warehouse.db exists
    '''

    #pointing to dashboard folder
    folder_of_files = r'..\datasets'

    #search if data warehouse exists
    files = glob.glob(os.path.join(folder_of_files, 'data_warehouse.db'))

    # return true if exists
    return True if files != [] else False

# ------------------------------------------------------------------------------
def main():

    checker_operation = check_operation_exists()
    checker_warehouse = check_datawh_exists()

    if checker_operation != True:

        print('\nCreating operation database!')
        # set up operation database
        create_operation_database(file_path)
        # get master df
        # used for dataware house insertion
        master_df = get_master_data_file()
        print('\nGenerating dataframe for data warehouse!')

    else:
        print('\nOperation database exists, skipping to dataframe generation!')
        # perform dataframe extraction for data warehouse
        # if operation.db is detected
        master_df = get_master_data_file()
        print('\nDataframe for data warehouse generated successfully')

    if checker_warehouse != True:

        # set up data warehouse frame
        initialize_datawh.main()
        # insert master_df into data_warehouse
        try:
            conn = sqlite3.connect('data_warehouse.db')
            master_df.to_sql('MASTER_FILE' ,conn, if_exists='append', index = False)
            print('\nData warehouse has been populated!')
            conn.commit()
        
        except Error as e:
            print(e)

    else:
        # PROBLEM STATMENT
        # THE DATA WAREHOUSE FORMAT GETS RESET
        # FIND A WORK AROUND WAY FOR THIS
        try:
            # insert master_df into data_warehouse
            conn = sqlite3.connect('data_warehouse.db')
            master_df.to_sql('MASTER_FILE' ,conn, if_exists='append', index = False)
            print('\nData warehouse has been updated!')
            conn.commit()

        except Error as e:
            print(e)

# ------------------------------------------------------------------------------       
if __name__ == '__main__':
    
    # run tasks
    main()

    
    