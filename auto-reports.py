import csv
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

# 1. Create table matching the CSV columns
cur.execute("""
CREATE TABLE orders (
    order_id INT,
    city TEXT,
    category TEXT,
    amount REAL,
    status TEXT
)
""")

# 2. Read raw_orders.csv and load every row into SQLite
with open("raw_orders.csv", "r") as infile:
  reader = csv.reader(infile)
  next(reader)  # Skips the first header row
  cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", reader)

# 3. Run SQL analysis on the loaded CSV data
query = """
SELECT 
    city,
    COUNT(order_id) AS total_orders,
    SUM(amount) AS total_revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY city
ORDER BY total_revenue DESC
"""

results = cur.execute(query).fetchall()

# 4. Export clean report to a new CSV
with open("final_city_summary.csv", "w", newline="") as outfile:
  writer = csv.writer(outfile)
  writer.writerow(["City", "Total_Orders", "Total_Revenue"])
  writer.writerows(results)

print("Success! Read raw_orders.csv and saved final_city_summary.csv")
conn.close()
