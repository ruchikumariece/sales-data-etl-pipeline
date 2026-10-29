"""Creates a small, intentionally messy sales dataset (synthetic) for the ETL demo."""
import random
import csv
from datetime import date, timedelta

random.seed(42)
products = {"Laptop": 850, "Mouse": 25, "Keyboard": 45, "Monitor": 210, "Headset": 80, "Webcam": 60}
regions = ["North", "South", "East", "West"]
rows = []
start = date(2026, 1, 1)

for i in range(1, 501):
    product = random.choice(list(products))
    d = start + timedelta(days=random.randint(0, 270))
    rows.append({
        "order_id": 1000 + i,
        "order_date": d.strftime("%Y-%m-%d"),
        "customer_name": random.choice(["Amit Shah", "Priya Nair", "John Smith", "Maria Lopez", "Wei Chen", "Sara Khan"]),
        "region": random.choice(regions),
        "product": product,
        "quantity": random.randint(1, 5),
        "unit_price": f"${products[product]}",
    })

# --- inject realistic problems ---
for r in random.sample(rows, 15):
    r["region"] = r["region"].lower() + "  "          # casing + trailing spaces
for r in random.sample(rows, 12):
    r["customer_name"] = ""                          # missing values
for r in random.sample(rows, 10):
    r["quantity"] = -abs(r["quantity"])              # invalid negative quantity
for r in random.sample(rows, 8):
    r["order_date"] = "31/02/2026"                   # impossible date
for r in random.sample(rows, 10):
    r["product"] = r["product"].upper()              # inconsistent labels
rows += random.sample(rows, 20)                      # duplicate rows

random.shuffle(rows)
with open("data/raw/sales_raw.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"Wrote {len(rows)} raw rows to data/raw/sales_raw.csv")
