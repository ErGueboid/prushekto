# importamos las librerías necesarias para poder visualizar y animar el algoritmo
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random
from matplotlib.animation import FuncAnimation

# Esta es la función principal del algoritmo QuickSort, que recibe el arreglo y usa recursividad para ordenarlo
def quick_sort(arr, start, end, steps):
    if start < end:
        # Aquí encontramos la posición correcta del pivote
        pivot_index = partition(arr, start, end, steps)
        # Luego aplicamos el mismo algoritmo a los subarreglos izquierdo y derecho
        quick_sort(arr, start, pivot_index - 1, steps)
        quick_sort(arr, pivot_index + 1, end, steps)

# Esta función organiza los elementos menores que el pivote a la izquierda y los mayores a la derecha
# También se encarga de guardar cada paso para poder visualizarlo luego
def partition(arr, start, end, steps):
    pivot = arr[end]  # El pivote es el último elemento del subarreglo
    i = start - 1
    for j in range(start, end):
        if arr[j] <= pivot:
            i += 1
            # Intercambiamos elementos si están en la posición incorrecta
            arr[i], arr[j] = arr[j], arr[i]
            # Guardamos el estado actual del arreglo con los índices involucrados
            steps.append((arr.copy(), i, j, end))
    # Colocamos el pivote en su lugar final
    arr[i + 1], arr[end] = arr[end], arr[i + 1]
    steps.append((arr.copy(), i + 1, end, end))
    return i + 1

# Esta clase es responsable de toda la visualización interactiva del algoritmo
class QuickSortVisualizer:
    def __init__(self, pasos):
        self.pasos = pasos
        self.index = 0  # Paso actual
        self.is_playing = True  # La animación comienza automáticamente

        # Configuramos la gráfica
        self.fig, self.ax = plt.subplots()
        self.fig.subplots_adjust(bottom=0.25)  # Dejo espacio para los botones
        self.bar_rects = self.ax.bar(range(len(pasos[0][0])), pasos[0][0], align="edge", color="skyblue")
        self.texto = self.ax.text(0.02, 0.95, "", transform=self.ax.transAxes)
        self.ax.set_title("Quick Sort - Paso a Paso")
        self.ax.set_ylim(0, max(max(paso[0]) for paso in pasos) * 1.1)

        # Aquí creamos los botones para controlar la visualización
        self.boton_anterior = Button(plt.axes([0.1, 0.05, 0.15, 0.075]), 'Anterior')
        self.boton_play = Button(plt.axes([0.3, 0.05, 0.15, 0.075]), 'Pausar')
        self.boton_siguiente = Button(plt.axes([0.5, 0.05, 0.15, 0.075]), 'Siguiente')
        self.boton_reiniciar = Button(plt.axes([0.7, 0.05, 0.15, 0.075]), 'Reiniciar')

        # Asignamos funciones a cada botón
        self.boton_anterior.on_clicked(self.handle_anterior)
        self.boton_siguiente.on_clicked(self.handle_siguiente)
        self.boton_reiniciar.on_clicked(self.handle_reiniciar)
        self.boton_play.on_clicked(self.handle_play_pause)

        # Mostramos el primer paso del algoritmo
        self.mostrar_paso()

        # Creamos la animación continua que depende del estado de is_playing
        self.animation = FuncAnimation(self.fig, self.animate, interval=500)
        plt.show()

    # Esta función actualiza la gráfica según el paso actual
    def mostrar_paso(self):
        arr, i, j, pivot = self.pasos[self.index]
        for rect, val in zip(self.bar_rects, arr):
            rect.set_height(val)
            rect.set_color("skyblue")
        if 0 <= i < len(arr):
            self.bar_rects[i].set_color("orange")  # Elemento i (intercambiado)
        if 0 <= j < len(arr):
            self.bar_rects[j].set_color("green")   # Elemento j (comparado)
        if 0 <= pivot < len(arr):
            self.bar_rects[pivot].set_color("red")  # Pivote actual
        self.texto.set_text(f"Paso {self.index + 1} de {len(self.pasos)}")
        self.fig.canvas.draw_idle()

    # Esta función avanza automáticamente en la animación si está en modo "play"
    def animate(self, _):
        if self.is_playing and self.index < len(self.pasos) - 1:
            self.index += 1
            self.mostrar_paso()
        elif self.index >= len(self.pasos) - 1:
            self.is_playing = False
            self.boton_play.label.set_text('Continuar')

    # Al presionar el botón, se pausa o continúa la animación
    def handle_play_pause(self, event):
        if self.is_playing:
            self.is_playing = False
            self.boton_play.label.set_text('Continuar')
        else:
            if self.index >= len(self.pasos) - 1:
                self.index = 0
                self.mostrar_paso()
            self.is_playing = True
            self.boton_play.label.set_text('Pausar')

    # Permite avanzar un paso manualmente
    def handle_siguiente(self, event):
        if self.is_playing:
            self.is_playing = False
            self.boton_play.label.set_text('Continuar')
        if self.index < len(self.pasos) - 1:
            self.index += 1
            self.mostrar_paso()

    # Permite retroceder un paso
    def handle_anterior(self, event):
        if self.is_playing:
            self.is_playing = False
            self.boton_play.label.set_text('Continuar')
        if self.index > 0:
            self.index -= 1
            self.mostrar_paso()

    # Reinicia la animación desde el primer paso
    def handle_reiniciar(self, event):
        self.is_playing = False
        self.index = 0
        self.boton_play.label.set_text('Continuar')
        self.mostrar_paso()

# Función principal donde se genera el arreglo aleatorio y se llama a la visualización
def main():
    arr = [random.randint(1, 100) for _ in range(10)]  # Lista aleatoria
    pasos = [(arr.copy(), -1, -1, -1)]  # Guardamos el primer estado inicial
    quick_sort(arr, 0, len(arr) - 1, pasos)  # Ejecutamos el algoritmo
    QuickSortVisualizer(pasos)  # Llamamos a la clase para mostrar la animación

# Este if asegura que se ejecute el main si este archivo es el principal
if __name__ == "__main__":
    main()
