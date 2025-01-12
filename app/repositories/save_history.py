from app import mysql

class History(object):
    def __init__(self):
        self.write = mysql.write_client()
        self.read = mysql.read_client()
        
    def save_history(self):
        pass