import sqlite3
import eel

eel.init('C:\\Friday\\www')

@eel.expose
def retrieve_data_from_database():
    return 'hello'

eel.start('System_cms.html')
