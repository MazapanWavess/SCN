import tkinter as tk
import math

def dibujar_poligono():
    num_lados = int(entry_lados.get())

    canvas.delete("all")

    if num_lados < 1:
        label_resultado.config(text="Ingrese un número válido de lados")
    else:
        label_resultado.config(text="Dibujando polígono(s) de {} lados".format(num_lados))
        centro_x, centro_y = 150, 150
        radio = 100
        angulo = 360 / num_lados

        for j in range(1, num_lados + 1):
            puntos = []
            for i in range(j):
                x = centro_x + radio * math.cos(math.radians(i * angulo))
                y = centro_y - radio * math.sin(math.radians(i * angulo))
                puntos.append((x, y))

            canvas.create_polygon(puntos, outline='black')

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Dibujar Polígono")
ventana.geometry("400x400")

# Etiqueta y entrada para el número de lados
label_lados = tk.Label(ventana, text="Número de Lados:")
label_lados.pack()
entry_lados = tk.Entry(ventana)
entry_lados.pack()

# Botón para dibujar el polígono
boton_dibujar = tk.Button(ventana, text="Dibujar", command=dibujar_poligono)
boton_dibujar.pack()

# Canvas para dibujar
canvas = tk.Canvas(ventana, width=300, height=300)
canvas.pack()

# Etiqueta para mostrar el resultado
label_resultado = tk.Label(ventana, text="")
label_resultado.pack()

ventana.mainloop()
