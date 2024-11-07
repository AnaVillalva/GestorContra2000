import hashlib
from tkinter.constants import BOTH, CENTER, END, LEFT, RIGHT, VERTICAL, Y
from tkinter import Button, Canvas, Entry, Frame, Label, Scrollbar, Tk
from functools import partial
from generador import GeneradorContraseñas
from basedatos import iniciar_base_datos
from vault import VaultMethods


class AdministradorContraseñas:
    
    def __init__(self):
        self.db, self.cursor = iniciar_base_datos()
        self.ventana = Tk()
        self.ventana.update()
        self.ventana.title("Administrador de contraseñas")
        self.ventana.geometry("650x350")

    def bienvenida_nuevo_usuario(self):
        self.ventana.geometry("450x200")

        etiqueta1 = Label(self.ventana, text="Crear nueva contraseña maestra")
        etiqueta1.config(anchor=CENTER)
        etiqueta1.pack(pady=10)

        entrada_mp = Entry(self.ventana, width=20, show="*")
        entrada_mp.pack()
        entrada_mp.focus()

        etiqueta2 = Label(self.ventana, text="Ingrese la contraseña nuevamente")
        etiqueta2.config(anchor=CENTER)
        etiqueta2.pack(pady=10)

        entrada_rmp = Entry(self.ventana, width=20, show="*")
        entrada_rmp.pack()

        self.feedback = Label(self.ventana)
        self.feedback.pack()

        boton_guardar = Button(self.ventana, text="Crear Contraseña",
                            command=partial(self.guardar_contraseña_maestra, entrada_mp, entrada_rmp))

        boton_guardar.pack(pady=5)

    def iniciar_sesion_usuario(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

        self.ventana.geometry("450x200")

        etiqueta1 = Label(self.ventana, text="Ingrese su contraseña maestra")
        etiqueta1.config(anchor=CENTER)
        etiqueta1.place(x=150, y=50)

        self.entrada_contraseña = Entry(self.ventana, width=20, show="*")
        self.entrada_contraseña.place(x=160, y=80)
        self.entrada_contraseña.focus()


        self.feedback = Label(self.ventana)
        self.feedback.place(x=170, y=105)

        boton_iniciar_sesion = Button(self.ventana, text="Iniciar Sesión", command=partial(
            self.verificar_contraseña_maestra, self.entrada_contraseña))
        boton_iniciar_sesion.place(x=200, y=130)


    def guardar_contraseña_maestra(self, entrada1, entrada2):
        contraseña1 = entrada1.get()
        contraseña2 = entrada2.get()
        if contraseña1 == contraseña2:
            contraseña_cifrada = self.cifrar_contraseña(contraseña1)
            comando_insertar = """INSERT INTO master(contraseña) VALUES(?) """
            self.cursor.execute(comando_insertar, [contraseña_cifrada])
            self.db.commit()
            self.iniciar_sesion_usuario()
        else:
            self.feedback.config(text="Las contraseñas no coinciden", fg="red")

    def verificar_contraseña_maestra(self, entrada):
        contraseña_cifrada = self.cifrar_contraseña(entrada.get())
        self.cursor.execute(
            "SELECT * FROM master WHERE id = 1 AND contraseña= ?", [contraseña_cifrada])
        if self.cursor.fetchall():
            self.pantalla_vault_contraseñas()
        else:
            self.entrada_contraseña.delete(0, END)
            self.feedback.config(text="Contraseña incorrecta", fg="red")

    def pantalla_vault_contraseñas(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

        metodos_vault = VaultMethods()

        self.ventana.geometry("850x350")
        marco_principal = Frame(self.ventana)
        marco_principal.pack(fill=BOTH, expand=1)

        lienzo_principal = Canvas(marco_principal)
        lienzo_principal.pack(side=LEFT, fill=BOTH, expand=1)

        barra_desplazamiento = Scrollbar(
            marco_principal, orient=VERTICAL, command=lienzo_principal.yview)
        barra_desplazamiento.pack(side=RIGHT, fill=Y)

        lienzo_principal.configure(yscrollcommand=barra_desplazamiento.set)
        lienzo_principal.bind('<Configure>', lambda e: lienzo_principal.configure(
            scrollregion=lienzo_principal.bbox("all")))

        segundo_marco = Frame(lienzo_principal)
        lienzo_principal.create_window((0, 0), window=segundo_marco, anchor="nw")

        boton_generar_contraseña = Button(segundo_marco, text="Generar Contraseña",
                                        command=GeneradorContraseñas)
        boton_generar_contraseña.grid(row=1, column=2, pady=10)

        boton_agregar_contraseña = Button(
            segundo_marco, text="Agregar Nueva Contraseña", command=partial(metodos_vault.agregar_contraseña, self.pantalla_vault_contraseñas))
        boton_agregar_contraseña.grid(row=1, column=3, pady=10)

        etiqueta = Label(segundo_marco, text="Plataforma")
        etiqueta.grid(row=2, column=0, padx=40, pady=10)
        etiqueta = Label(segundo_marco, text="Email/Usuario")
        etiqueta.grid(row=2, column=1, padx=40, pady=10)
        etiqueta = Label(segundo_marco, text="Contraseña")
        etiqueta.grid(row=2, column=2, padx=40, pady=10)

        self.cursor.execute("SELECT * FROM vault")

        if self.cursor.fetchall():
            i = 0
            while True:
                self.cursor.execute("SELECT * FROM vault")
                array = self.cursor.fetchall()

                etiqueta_plataforma = Label(segundo_marco, text=(array[i][1]))
                etiqueta_plataforma.grid(column=0, row=i + 3)

                etiqueta_cuenta = Label(segundo_marco, text=(array[i][2]))
                etiqueta_cuenta.grid(column=1, row=i + 3)

                etiqueta_contraseña = Label(segundo_marco, text=(array[i][3]))
                etiqueta_contraseña.grid(column=2, row=i + 3)

                boton_copiar = Button(segundo_marco, text="Copiar Contraseña",
                                    command=partial(self.copiar_texto, array[i][3]))
                boton_copiar.grid(column=3, row=i + 3, pady=10, padx=10)
                boton_actualizar = Button(segundo_marco, text="Actualizar Contraseña",
                                        command=partial(metodos_vault.actualizar_contraseña, array[i][0], self.pantalla_vault_contraseñas))
                boton_actualizar.grid(column=4, row=i + 3, pady=10, padx=10)
                boton_eliminar = Button(segundo_marco, text="Eliminar Contraseña",
                                        command=partial(metodos_vault.eliminar_contraseña, array[i][0], self.pantalla_vault_contraseñas))
                boton_eliminar.grid(column=5, row=i + 3, pady=10, padx=10)

                i += 1

                self.cursor.execute("SELECT * FROM vault")
                if len(self.cursor.fetchall()) <= i:
                    break


    def cifrar_contraseña(self, contraseña):
        contraseña = contraseña.encode("utf-8")
        texto_cifrado = hashlib.md5(contraseña).hexdigest()
        return texto_cifrado

    def copiar_texto(self, texto):
        self.ventana.clipboard_clear()
        self.ventana.clipboard_append(texto)

if __name__ == '__main__':
    db, cursor = iniciar_base_datos()
    cursor.execute("SELECT * FROM master")
    administrador = AdministradorContraseñas()
    if cursor.fetchall():
        administrador.iniciar_sesion_usuario()
    else:
        administrador.bienvenida_nuevo_usuario()
    administrador.ventana.mainloop()
