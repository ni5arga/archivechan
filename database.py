import sqlite3
import csv

def export_table_to_csv(db_path, table_name, output_file):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow([i[0] for i in cursor.description])
        writer.writerows(cursor)
    conn.close()
