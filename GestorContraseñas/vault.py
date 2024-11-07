from tkinter import simpledialog
from basedatos import iniciar_base_datos


class VaultMethods:

    def __init__(self):
        self.db, self.cursor = iniciar_base_datos()

    def entrada_popup(self, encabezado):
        respuesta = simpledialog.askstring("Ingresar detalles", encabezado)
        return respuesta

    def agregar_contraseña(self, pantalla_boveda):
        plataforma = self.entrada_popup("Plataforma")
        usuario_id = self.entrada_popup("Usuario/Correo")
        contraseña = self.entrada_popup("Contraseña")

        comando_insertar = """INSERT INTO vault(plataforma, usuario_id, contraseña) VALUES (?, ?, ?)"""
        self.cursor.execute(comando_insertar, (plataforma, usuario_id, contraseña))
        self.db.commit()
        pantalla_boveda()

    def actualizar_contraseña(self, id, pantalla_boveda):
        nueva_contraseña = self.entrada_popup("Ingresar nueva contraseña")
        self.cursor.execute(
            "UPDATE vault SET contraseña = ? WHERE id = ?", (nueva_contraseña, id))
        self.db.commit()
        pantalla_boveda()

    def eliminar_contraseña(self, id, pantalla_boveda):
        self.cursor.execute("DELETE FROM vault WHERE id = ?", (id,))
        self.db.commit()
        pantalla_boveda()
