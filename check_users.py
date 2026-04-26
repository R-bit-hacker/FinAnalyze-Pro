import sqlite3
import pandas as pd

# Database check karein
conn = sqlite3.connect("users.db")
query = "SELECT id, username, full_name, role FROM users"
df = pd.read_sql_query(query, conn)
conn.close()

print("\n--- DATABASE REPORT ---")
print(df)
print("-----------------------")