from pathlib import Path
import sqlite3 as SQL

dIr = Path()
#--------------------------------------------------------
DB_DIR = (f"{dIr}\\units.db")                           
DB_CONN = SQL.connect(DB_DIR, check_same_thread=False)
CURSOR_DB = DB_CONN.cursor()
#--------------------------------------------------------

def db_status(data): #DB para uso da API 
    for item in data:
        CURSOR_DB.execute(f"SELECT * FROM status WHERE ex_id={item[0]}")
        unit = CURSOR_DB.fetchall()

        if len(unit) == 0: 
            CURSOR_DB.execute("""INSERT INTO status (nick, unit_tip, acronym, stats, ex_id) VALUES (?,?,?,?,?)""", (item[1], item[2], item[3], item[4], item[0]))
            DB_CONN.commit()
        else:
            CURSOR_DB.execute(f"UPDATE status SET stats='{item[4]}' WHERE ex_id={item[0]}")
            DB_CONN.commit()