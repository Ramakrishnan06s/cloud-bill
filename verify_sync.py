import sqlite3
import os

def verify_sync():
    db_path = 'instance/cloud_bill.db'
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    tables = ['customers', 'service_plans', 'resources', 'usage_logs', 'invoices']
    
    print("="*60)
    print("HYPERCLOUD DATABASE SYNCHRONIZATION AUDIT")
    print("="*60)

    for table in tables:
        print(f"\n[TABLE: {table.upper()}]")
        try:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            
            # Get column names
            cursor.execute(f"PRAGMA table_info({table})")
            cols = [c[1] for c in cursor.fetchall()]
            print(f"{' | '.join(cols)}")
            print("-" * (len(' | '.join(cols)) + 10))
            
            for row in rows:
                print(f"{' | '.join(map(str, row))}")
        except Exception as e:
            print(f"Error reading table {table}: {e}")

    conn.close()
    print("\n" + "="*60)
    print("AUDIT COMPLETE")
    print("="*60)

if __name__ == '__main__':
    verify_sync()
