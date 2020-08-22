'''
extract and load source files into operation database
'''
# Importing required libraries
import pandas as pd
import sqlite3
from sqlite3 import Error
import glob
import os

# ------------------------------------------------------------------------------
def main(folder_of_files):
    
    conn = sqlite3.connect('operation.db')

    files = glob.glob(os.path.join(folder_of_files,"*.xls"))

    if files == []:
        raise Exception('\nNo datasets found in DATASETS folder!')

    for file in files:
        
        # read xls files
        xls_file = file
        xl = pd.ExcelFile(xls_file)
        
        # loop through sheets in xls file
        # populate database based on tablename
        for sheet in xl.sheet_names:
            # getting tablename
            table_name = sheet.replace(' ', '_').upper()
            # getting dataframes
            df_tmp = xl.parse(sheet)
            df_tmp.to_sql(table_name, conn, if_exists='append', index = False)
    
        conn.commit()
    conn.close()

# ------------------------------------------------------------------------------   
if __name__ == '__main__':

    try:
        main(r'..\datasets\sources')
    except Error as e:
        print(str(e) + ': Primary keys exists!')
        pass 