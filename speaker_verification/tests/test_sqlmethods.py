import unittest

import pytest
import numpy as np
from os.path import join, abspath, dirname
import pathlib
import sqlite3

from speaker_verification.sql_utils import(
    create_db_table,
    insert_db_row,
    select_db_row,
    remove_db_row
)

table_id = 219944922
mfcc=np.array([1,2,3])
create_db_table("unit_test")
insert_db_row("unit_test", table_id, mfcc)
table_id = 219941122
mfcc=np.array([1,2,4,5,3])
insert_db_row("unit_test", table_id, mfcc)
  

def test_select_db_row_returns_expected_row():
    '''Method test to check by trying to select the row passing in 
      valid values for each of the columns
    '''
    #Arange
    expected=(219944922,np.array([1,2,3]))
    #act
    rows=select_db_row("unit_test", 219944922)
    
    #assert
    assert rows[0]==expected[0] 
    assert all ([a == b for a,b in zip(rows[1],expected[1])])

def test_select_db_row_returns_no_value():
    '''Method test to check by trying to select the row passing in 
      invalid values for student id that does not exist in the table
    '''
    #Arange 
    expected = None
    #Act
    rows=select_db_row("unit_test", 219942322)
    #Assert
    assert expected == rows

def test_insert_db_row_valid():
    '''Method test to check by trying to insert the row passing in 
    valid values for student id and select that row using relevant method
    '''
    #Arange
    expected = (218008432,np.array([2,3,4]))
    #Act
    insert_db_row("unit_test", 218008432, np.array([2,3,4]))
    rows = select_db_row("unit_test", 218008432)
    #Assert
    assert rows[0] == expected[0] 
    assert all ([a == b for a,b in zip(rows[1],expected[1])])

def test_insert_db_row_invalid():
    '''Method test to insert data to the table with invalid 
    value for the column 
    '''
    #Arange
    expected = None
    #Act
    #try to insert a data record with invalid student ID
    insert_db_row("unit_test","string",np.array([2,3,4]))
    #check whether the data record was inserted or not
    rows=select_db_row("unit_test","string")
    #Assert
    assert expected == rows

def test_removes_db_row():
    ''' Method test to remove the data from table with valid 
    values for each of the column names
    '''
    #Arange
    expected = None
    #Act: remove an existing row
    remove_db_row("unit_test",219941122)
    #select the deleted row, should return null
    rows=select_db_row("unit_test",219941122)
    #Assert
    assert rows == expected
    
