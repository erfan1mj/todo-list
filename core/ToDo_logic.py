# class ToDoListCore:
#     def __init__(self):
#         self.tasks=[]

#     def add_task(self,subject,description):
#         task={
#             "subject":subject.strip(),
#             "description":description.strip()
#         }
#         self.tasks.append(task)

#     def remove_task(self,index):
#         try:
#             self.tasks.pop(index)
#         except:
#             return "not found"
    
#     def get_tasks(self):
#         return self.tasks
    
#     def edit_task(self,index,newsub,newdes):
#         try:
#             self.tasks[index]['subject']=newsub.strip()
#             self.tasks[index]['description']=newdes.strip()
#         except:
#             return 'not found'
    
import sqlite3

class ToDoListCore:
    def __init__(self, user_id):
        self.user_id = user_id
        self.conn = sqlite3.connect("todo_db.db")
        self.cursor = self.conn.cursor()
        self.tasks = []
        self.create_table()
        self.load_tasks()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS task(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                user_id INTEGER,
                is_done INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def load_tasks(self):
        self.cursor.execute("SELECT id, title, description FROM task WHERE user_id = ?", (self.user_id,))
        rows = self.cursor.fetchall()
        self.tasks = []
        for row in rows:
            task = {
                "id": row[0],
                "subject": row[1],
                "description": row[2]
            }
            self.tasks.append(task)

    def add_task(self, subject, description):
        subject = subject.strip()
        description = description.strip()
        self.cursor.execute("INSERT INTO task (title, description, user_id, is_done) VALUES (?, ?, ?, 0)",
                            (subject, description, self.user_id))
        self.conn.commit()
        self.load_tasks()  # لیست را دوباره آپدیت می‌کنیم

    def remove_task(self, index):
        try:
            task_id = self.tasks[index]['id']
            self.cursor.execute("DELETE FROM task WHERE id = ?", (task_id,))
            self.conn.commit()
            self.load_tasks()
        except IndexError:
            return "not found"

    def get_tasks(self):
        return self.tasks

    def edit_task(self, index, newsub, newdes):
        try:
            task_id = self.tasks[index]['id']
            self.cursor.execute("UPDATE task SET title = ?, description = ? WHERE id = ?",
                                (newsub.strip(), newdes.strip(), task_id))
            self.conn.commit()
            self.load_tasks()
        except IndexError:
            return "not found"

    def __del__(self):
        self.conn.close()  # بستن اتصال دیتابیس هنگام پایان کار