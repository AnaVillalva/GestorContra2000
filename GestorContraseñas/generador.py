from tkinter import Button, Entry, Frame, Label, LabelFrame, Tk
import string
from secrets import choice
from tkinter.constants import END

MAYUSCULAS = list(string.ascii_uppercase)
MINUSCULAS = list(string.ascii_lowercase)
NUMEROS = list(string.digits)
SIMBOLOS = ['@', '#', '$', '%', '&', '_']


class GeneradorContraseñas:

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Generador de Contraseñas")
        self.ventana.geometry("450x300")

        # Label Frame
        self.label_frame = LabelFrame(
            self.ventana, text="Enter the number of characters")
        self.label_frame.pack(pady=20)

        # Entry box for number of characters
        self.caja_longitud = Entry(self.label_frame, width=20)
        self.caja_longitud.pack(padx=20, pady=20)

        # Declaring feedback if no length is found
        self.advertencia = Label(self.ventana)

        self.caja_contraseña = Entry(
            self.ventana, text="", width=50)
        self.caja_contraseña.pack(pady=20)

        # Marco para los botones
        self.marco_botones = Frame(self.ventana)
        self.marco_botones.pack(pady=20)

        # Botón para generar la contraseña
        btn_generar = Button(
            self.marco_botones, text="Generar Contraseña", command=self.generar_contraseña_aleatoria)
        btn_generar.grid(row=0, column=0, padx=10)

        # Botón para copiar la contraseña
        btn_copiar = Button(self.marco_botones,
                            text="Copiar Contraseña", command=self.copiar_contraseña)
        btn_copiar.grid(row=0, column=1, padx=10)

    def generar_contraseña_aleatoria(self):
        # Limpiar caja de contraseña
        self.caja_contraseña.delete(0, END)
        try:
            # Obtener la longitud de la contraseña ingresada por el usuario
            longitud_contraseña = int(self.caja_longitud.get())
            self.advertencia.destroy()  # Destruir advertencia si se ingresó longitud
            # Crear lista de caracteres disponibles
            caracteres = MAYUSCULAS + MINUSCULAS + NUMEROS + SIMBOLOS
            # Generar contraseña aleatoria
            contraseña = ''.join(choice(caracteres) for _ in range(longitud_contraseña))
            self.caja_contraseña.insert(0, contraseña)
        except ValueError:
            # Mostrar advertencia si el usuario no ingresa un número
            self.advertencia = Label(self.ventana, fg="red",
                                    text="Por favor, ingrese el número de caracteres")
            self.advertencia.place(x=130, y=100)

    def copiar_contraseña(self):
        # Copiar la contraseña al portapapeles
        self.ventana.clipboard_clear()
        self.ventana.clipboard_append(self.caja_contraseña.get())


if __name__ == "__main__":
    GeneradorContraseñas().ventana.mainloop()
