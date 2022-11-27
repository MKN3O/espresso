import sqlite3


con = sqlite3.connect("coffee.sqlite")
cur = con.cursor()
cur.execute(f"""INSERT INTO coffee(sort, grade, condition, descriptor, price, mass)
                             VALUES('Робуста','Тёмная','True','Табачный',
                             '1000', '1000')""")
con.commit()