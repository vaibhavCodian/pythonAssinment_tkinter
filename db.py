import sqlite3
import mysql.connector



class Database:
    def __init__(self):
        self.is_sqlite = False
        try:
            self.conn = mysql.connector.connect(
              host="127.0.0.1",
              user="root",
              password="",
              database="mydatabase"
            )
        except:
            print("****____UNABLE__TO__CONNECT__WITH__MYSQL__Database____****")
            print("Moving forward with sqlite db")
            self.conn = sqlite3.connect("store.db")
            self.is_sqlite = True

        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS students (remark text, name text, rollNo INT, gpa INT)")
        self.cur.execute("ALTER TABLE students ADD COLUMN IF NOT EXISTS id INT AUTO_INCREMENT PRIMARY KEY")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        return rows

    def insert(self, remark, name, rollNo, gpa):
        self.cur.execute("INSERT INTO students (remark, name, rollNo, gpa) VALUES (%s, %s, %s, %s)",
                         (remark, name, rollNo, gpa))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute(f"DELETE FROM students WHERE id={id}")
        self.conn.commit()

    def update(self, id, remark, name, rollNo, gpa):
        try:
            cur = self.cur.execute("UPDATE students SET remark = %s, name = %s, rollNo = %s, gpa = %s WHERE id = %s",
                         (remark, name, rollNo, gpa, id))
            print(f"+_______+{cur}")
            self.conn.commit()
        except Exception as e:
            print("Exception Occured")

    # def update(self, id, remark, name, rollNo, gpa):
    #     res = self.cur.execute("UPDATE FROM students SET remark = %s, name = %s, rollNo = %s, gpa = %s WHERE id = %s",
    #                      (remark, name, rollNo, gpa, id))
    #     print(f"---->  { name, rollNo, gpa, res}")
    #     self.conn.commit()

    def __del__(self):
        self.conn.close()

