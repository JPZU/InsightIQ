import pymysql

try:
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="password",
        database="insightiq",
        port=3306
    )
    print("Conexión exitosa a la base de datos.")
    connection.close()
except pymysql.Error as e:
    print(f"Error al conectar a la base de datos: {e}")