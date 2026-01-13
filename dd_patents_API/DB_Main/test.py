import psycopg2

try:
    connection = psycopg2.connect(
        dbname="Trademarks_db",
        user="Azhari",
        password="CIPO",
        host="localhost",
        port="5432"
    )
    print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")
finally:
    if connection:
        connection.close()
