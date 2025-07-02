import sqlite3
from pathlib import Path

class LoginCore:
    def __init__(self):
        current_dir=Path(__file__).resolve().parent
        db_path=current_dir.parent/"todo_db.db"
        db_path_str=str(db_path)
        self.conn=sqlite3.connect(db_path_str)
        self.create_login_table()
        
    def create_login_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS login (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)    
            self.conn.commit()
        except sqlite3.Error as e:
            pass

    def register(self,username,password):
        try:
            cursor=self.conn.execute('SELECT * FROM login WHERE username=?', (username,))
            if cursor.fetchone():
                return 'exist'
            else:
                self.conn.execute('INSERT INTO login (username, password) VALUES (?,?)',(username,password))
                self.conn.commit()
                return 'successful'
        except sqlite3.Error as error:
            return error
    
    def login(self,username,password):
        
        try:
            login_info={'status':'','uid':0}
            cursor=self.conn.execute('SELECT * FROM login WHERE username=? AND password=?',(username,password))
            row=cursor.fetchone()
            
            if row:
                login_info['status']='successful'
                login_info['uid']=row[0]

                return login_info
            
            else:
                login_info['status']='wrong'

                return login_info
            
        except sqlite3.Error as e:
            login_info['status']='error'
            return login_info