# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 21:41:37 2022

@author: marca
"""
import sys
from ETLprojectExtract import extract_NZ_ag_files
from ETLprojectExtract import delete_old_test_files
from ETLprojectTransform import transform_data
from ETLprojectLoad import load_data
from pandasPostgresHelpersNZ import delete_test_tables




if __name__ == '__main__':

    if len(sys.argv) == 0:
        print(""""Enter desired folder path (inluding r prefix) as one arg,
              desired path and 'deleteTest' as two args
              or run script from IDE""")
    
    elif len(sys.argv) > 2 and sys.argv[2] == 'deleteTest':
        
        home_folder = sys.argv[1]
            
        delete_test_tables()

        delete_old_test_files(home_folder)
            
    else:
            
        try:
        
            home_folder = sys.argv[1]
            
            assert isinstance(home_folder, str), "Please enter desired folder path as arguement"
            
            df_extracted = extract_NZ_ag_files(home_folder)
            #print(df_extracted)
        
            df_transformed = transform_data(df_extracted)
            #print(df_transformed)
        
            load_data(df_transformed, home_folder)

        
        except:
            print("Something went wrong")


