import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="admin",      # Tu contraseña
        database="sistema_analisis"
    )