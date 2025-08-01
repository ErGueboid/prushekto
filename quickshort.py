
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random
from matplotlib.animation import FuncAnimation


def quick_sort(arr, start, end, steps):
    if start < end:

        pivot_index = partition(arr, start, end, steps)

        quick_sort(arr, start, pivot_index - 1, steps)
        quick_sort(arr, pivot_index + 1, end, steps)

def partition(arr, start, end, steps):
    pivot = arr[end]  
    i = start - 1
    for j in range(start, end):
        if arr[j] <= pivot:
            i += 1

            arr[i], arr[j] = arr[j], arr[i]

            steps.append((arr.copy(), i, j, end))

    arr[i + 1], arr[end] = arr[end], arr[i + 1]
    steps.append((arr.copy(), i + 1, end, end))
    return i + 1


class QuickSortVisualizer:
    def __init__(self, pasos):
        self.pasos = pasos
        self.index = 0  # Paso actual
        self.is_playing = True  # La animación comienza automáticamente


        self.fig, self.ax = plt.subplots()
        self.fig.subplots_adjust(bottom=0.25)  # Dejo espacio para los botones
        self.bar_rects = self.ax.bar(range(len(pasos[0][0])), pasos[0][0], align="edge", color="skyblue")
        self.texto = self.ax.text(0.02, 0.95, "", transform=self.ax.transAxes)
        self.ax.set_title("Quick Sort - Paso a Paso")
        self.ax.set_ylim(0, max(max(paso[0]) for paso in pasos) * 1.1)


        self.boton_anterior = Button(plt.axes([0.1, 0.05, 0.15, 0.075]), 'Anterior')
        self.boton_play = Button(plt.axes([0.3, 0.05, 0.15, 0.075]), 'Pausar')
        self.boton_siguiente = Button(plt.axes([0.5, 0.05, 0.15, 0.075]), 'Siguiente')
        self.boton_reiniciar = Button(plt.axes([0.7, 0.05, 0.15, 0.075]), 'Reiniciar')


        self.boton_anterior.on_clicked(self.handle_anterior)
        self.boton_siguiente.on_clicked(self.handle_siguiente)
        self.boton_reiniciar.on_clicked(self.handle_reiniciar)
        self.boton_play.on_clicked(self.handle_play_pause)

        self.mostrar_paso()


        self.animation = FuncAnimation(self.fig, self.animate, interval=500)
        plt.show()

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

    def animate(self, _):
        if self.is_playing and self.index < len(self.pasos) - 1:
            self.index += 1
            self.mostrar_paso()
        elif self.index >= len(self.pasos) - 1:
            self.is_playing = False
            self.boton_play.label.set_text('Continuar')

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


    def handle_siguiente(self, event):
        if self.is_playing:
            self.is_playing = False
            self.boton_play.label.set_text('Continuar')
        if self.index < len(self.pasos) - 1:
            self.index += 1
            self.mostrar_paso()


    def handle_anterior(self, event):
        if self.is_playing:
            self.is_playing = False
            self.boton_play.label.set_text('Continuar')
        if self.index > 0:
            self.index -= 1
            self.mostrar_paso()

    def handle_reiniciar(self, event):
        self.is_playing = False
        self.index = 0
        self.boton_play.label.set_text('Continuar')
        self.mostrar_paso()


def main():
    arr = [random.randint(1, 100) for _ in range(10)]  
    pasos = [(arr.copy(), -1, -1, -1)]  
    quick_sort(arr, 0, len(arr) - 1, pasos)  
    QuickSortVisualizer(pasos)  

if __name__ == "__main__":
    main()
