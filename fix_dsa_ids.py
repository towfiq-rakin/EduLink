import sqlite3
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'student.db'))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Read all data except the ID column
cursor.execute("SELECT * FROM DSA")
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

# Find the index of the ID column (assume it's named 'id' or 'ID')
id_col = None
for i, col in enumerate(columns):
    if col.lower() == 'id':
        id_col = i
        break
if id_col is None:
    raise Exception("No 'id' column found in DSA table.")

# Prepare new rows with new IDs starting from 1
new_rows = []
for new_id, row in enumerate(rows, start=1):
    row = list(row)
    row[id_col] = new_id
    new_rows.append(tuple(row))

# Start transaction
conn.execute("BEGIN TRANSACTION;")
try:
    # Remove all rows
    cursor.execute("DELETE FROM DSA")
    # Insert rows with new IDs
    placeholders = ','.join(['?'] * len(columns))
    cursor.executemany(f"INSERT INTO DSA VALUES ({placeholders})", new_rows)
    # Reset the sqlite_sequence for AUTOINCREMENT to the current max id
    cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM DSA) WHERE name = 'DSA'")
    conn.commit()
    print("DSA table IDs renumbered and AUTOINCREMENT reset successfully.")
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")
finally:
    conn.close()
