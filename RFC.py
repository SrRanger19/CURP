import re
import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

rfc_first_four_pattern = re.compile(r'^[TtUuSsJj]{4}')

current_canvas = None

def show_automaton(rfc_start):
    global current_canvas

    Graff = nx.DiGraph()

    for i, letter in enumerate(rfc_start):
        Graff.add_edge(f'q{i}', f'q{i+1}', label=letter)

    fig, ax = plt.subplots()

    pos = nx.spring_layout(Graff)
    nx.draw(Graff, pos, ax=ax, with_labels=True, node_size=3000,
            node_color="lightblue", linewidths=2, font_size=18)

    nx.draw_networkx_nodes(Graff, pos, nodelist=['q0'], node_color="blue")
    nx.draw_networkx_nodes(
        Graff, pos, nodelist=[f'q{len(rfc_start)}'], node_color="red")

    edge_labels = {(u, v): d['label'] for u, v, d in Graff.edges(data=True)}
    nx.draw_networkx_edge_labels(
        Graff, pos, edge_labels=edge_labels, font_color='red')

    if current_canvas is not None:
        current_canvas.get_tk_widget().destroy()

    current_canvas = FigureCanvasTkAgg(fig, master=window)
    current_canvas.draw()
    current_canvas.get_tk_widget().pack()

def on_submit():
    rfc_input = simpledialog.askstring(
        "Input", "Ingresa tu RFC:", parent=window)

    if rfc_input:
        match = rfc_first_four_pattern.match(rfc_input)
        if match:
            rfc_start = match.group(0).upper()
            show_automaton(rfc_start)
        else:
            messagebox.showerror(
                "Error", "RFC Invalido. Por favor ingresa como minimo los primeros 4 digitos.")
    else:
        messagebox.showinfo("Cancelado", "Operación cancelada por el usuario.")

window = tk.Tk()
window.title("Generador de Autómata RFC")

submit_button = tk.Button(window, text="Ingresar RFC", command=on_submit)
submit_button.pack()

window.mainloop()