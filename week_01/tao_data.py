import sqlite3
conn = sqlite3.connect("school.db")
cursor = conn.cursor()

# 2. Tạo bảng học sinh theo đúng tài liệu Tuan1 DataEngineer (1).docx
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id      INTEGER PRIMARY KEY,
        name    TEXT,
        class   TEXT,
        score   REAL,
        city    TEXT
    )
""")

# 3. Chèn 10 học sinh mẫu
students_data = [
    (1,  'Nguyen Van A', '10A', 8.5, 'Hanoi'),
    (2,  'Tran Thi B',   '10B', 4.0, 'HCMC'),
    (3,  'Le Van C',     '10A', 6.5, 'Danang'),
    (4,  'Pham Thi D',   '10C', 3.5, 'Hanoi'),
    (5,  'Hoang Van E',  '10B', 9.0, 'HCMC'),
    (6,  'Nguyen Thi F', '10A', 5.0, 'Hanoi'),
    (7,  'Tran Van G',   '10C', 7.5, 'Danang'),
    (8,  'Le Thi H',     '10B', 2.0, 'HCMC'),
    (9,  'Pham Van I',   '10A', 8.0, 'Hanoi'),
    (10, 'Hoang Thi J',  '10C', 6.0, 'HCMC')
]

cursor.executemany("INSERT OR IGNORE INTO students VALUES (?,?,?,?,?)", students_data)
conn.commit()
conn.close()
print("Đã tạo xong file school.db thành công!")