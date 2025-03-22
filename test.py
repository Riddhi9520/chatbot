import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="chatbot"
    )
    if conn.is_connected():
        print("✅ Successfully connected to the MySQL database!")
    else:
        print("❌ Connection failed!")

    conn.close()
except mysql.connector.Error as e:
    print(f"Database Error: {e}")
