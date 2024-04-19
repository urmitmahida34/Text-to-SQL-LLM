import sqlite3
from datetime import datetime, timedelta
import random
import string

# Function to generate random alphanumeric coupon code
def generate_coupon_code(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# Connect to SQLite database
connection = sqlite3.connect("subscription.db")
cursor = connection.cursor()

# Create the table if it doesn't exist
subscription_table = """
CREATE TABLE IF NOT EXISTS SUBSCRIPTION (
    userid VARCHAR(25),
    Plan_amount INT,
    country VARCHAR(25),
    subscription_start_date DATE,
    subscription_end_date DATE,
    coupon_code VARCHAR(25)
);
"""
cursor.execute(subscription_table)

# Insert entries into the table
for _ in range(100):
    userid = 'ux' + str(random.randint(1000, 9999))
    plan_amount = random.randint(500, 1500)
    country = random.choice(['INDIA', 'USA', 'UK', 'CANADA'])
    
    # Generate random subscription start date within the last 5 years
    start_date = datetime.now() - timedelta(days=random.randint(1, 365) * 5)
    
    # Generate random subscription duration between 1 and 12 months
    subscription_duration_months = random.randint(1, 12)
    end_date = start_date + timedelta(days=subscription_duration_months * 30)
    
    # Generate random alphanumeric coupon code
    coupon_code = generate_coupon_code(10)
    
    # Insert the record into the table using parameters
    insert_query = """
    INSERT INTO SUBSCRIPTION VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insert_query, (userid, plan_amount, country, start_date.date(), end_date.date(), coupon_code))

# Commit the transaction to save changes
connection.commit()

# Display inserted records
print("The inserted records are:")
data = cursor.execute('''SELECT * FROM SUBSCRIPTION''')
for row in data:
    print(row)

# Close the cursor and the connection
cursor.close()
connection.close()
