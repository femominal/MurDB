import sqlite3
from io import StringIO
def export_sqlite_db(db_path: str) -> bytes:
    conn = sqlite3.connect(db_path)
    dump_buffer = StringIO()
    for line in conn.iterdump():
        dump_buffer.write(f"{line}\n")
    conn.close()
    return dump_buffer.getvalue().encode("utf-8")
