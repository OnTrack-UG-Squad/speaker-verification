import pytest
import os
from speaker_verification import enroll_new_user, validate_user
from speaker_verification.sql_utils import get_db_connection,create_db_table
from os.path import join, abspath, dirname
import pathlib

TEST_PATH = join(abspath(dirname(__file__)), "input")
audio_list = [
        pathlib.Path(TEST_PATH, "enrollment.flac"),
        pathlib.Path(TEST_PATH, "validation.flac"),
    ]
class Args:
    def __init__(self, db_table, id,audio_path,database_path):
        self.db_table = db_table
        self.id= id
        self.audio_path=audio_path
        self.database_path=database_path


database_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "input", "test.db"
)
con, _ = get_db_connection(database_path)
con.close()
create_db_table("test", database_path)

arg_enroll=Args("test","219249449",audio_list[0],database_path)
arg_enroll_invalid=Args("test","219449",audio_list[0],database_path)
arg_validate=Args("test","219249449",audio_list[1],database_path)
arg_validate_does_not_exist=Args("test","219249446",audio_list[1],database_path)
arg_validate_invalid_id=Args("test","21946",audio_list[1],database_path)

@pytest.mark.integtest
def test_enroll_new_user():
    '''Enrolls a new user and the valid data is uploaded to the database
    '''
    enroll_new_user(arg_enroll)

@pytest.mark.integtest
def test_validate_user():
    '''Validates the user data exists in the database
    '''    
    validate_user(arg_validate)
    os.remove(database_path)

@pytest.mark.integtest
def test_enroll_new_user_invalid():
    ''' Try to enroll the user data with invalid values in the database,
    assertion error is expected as a result
    '''  
    with pytest.raises(AssertionError):
        enroll_new_user(arg_enroll_invalid)

@pytest.mark.integtest
def test_validate_user_does_not_exist():
    ''' Try to validate the user which does not have it's data in the database
    ''' 
    with pytest.raises(Exception):
        validate_user(arg_enroll_invalid)
        
@pytest.mark.integtest
def test_validate_user_invalid_id():
        ''' Try to validate the user by passing invalid argument for id parameter 
    ''' 
    with pytest.raises(AssertionError):
        validate_user(arg_validate_invalid_id)
        os.remove(database_path)