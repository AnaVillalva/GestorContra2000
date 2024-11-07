import sqlite3

def iniciar_base_datos():
    db = sqlite3.connect("password_vault.db")  # Crear la conexión
    cursor = db.cursor()

    # Crear la tabla 'master' si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS master (
        id INTEGER PRIMARY KEY,
        contraseña TEXT NOT NULL
    );
    """)

    # Crear la tabla 'vault' si no existe (asegurando consistencia en el nombre)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vault (
        id INTEGER PRIMARY KEY,
        plataforma TEXT NOT NULL,
        usuario_id TEXT NOT NULL,
        contraseña TEXT NOT NULL
    );
    """)

    return db, cursor  # Retornar la conexión y el cursor
