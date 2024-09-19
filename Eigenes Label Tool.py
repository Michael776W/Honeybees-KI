import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class LabelingTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Labeling Tool")

        # Bildindex und Liste der geladenen Bilder
        self.image_index = 0
        self.image_list = []
        self.labels = []

        # Aktuelle Klasse für die Bounding Box
        self.current_class = None

        # Canvas zum Laden und Markieren von Bildern
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.grid(row=0, column=0, rowspan=5)

        # Buttons für Klassen (Buckfast, Carnica, Pollen, Varroa)
        self.class_buttons = ['Buckfast', 'Carnica', 'Pollen', 'Varroa']
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=0, column=1)

        for i, class_name in enumerate(self.class_buttons):
            button = tk.Button(self.button_frame, text=class_name, bg=self.get_class_color(i),
                               command=lambda c=class_name: self.select_class(c))
            button.pack(fill=tk.X)

        # Label zum Anzeigen der aktuellen Klasse
        self.class_label = tk.Label(self.root, text="Aktuelle Klasse: Keine")
        self.class_label.grid(row=1, column=1)

        # Button zum Laden von Bildern
        self.load_button = tk.Button(self.root, text="Bilder laden", command=self.load_images)
        self.load_button.grid(row=2, column=1)

        # Button zum Generieren des Labels
        self.save_button = tk.Button(self.root, text="Generiere Label", command=self.save_labels)
        self.save_button.grid(row=3, column=1)

        # "Zurück"-Button, um die letzte gezeichnete Box zu entfernen
        self.undo_button = tk.Button(self.root, text="Letzte Box zurück", command=self.undo_last_box)
        self.undo_button.grid(row=4, column=1)

        # Mausereignisse für das Zeichnen der Bounding Boxen
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        # Variablen zum Speichern der Bounding Box Koordinaten
        self.start_x = None
        self.start_y = None
        self.rect = None

        # Liste zum Speichern der gezeichneten Rechtecke (Canvas-Objekte)
        self.rectangles = []

        # Aktuell angezeigtes Bild
        self.image_tk = None

    def load_images(self):
        # Öffnen eines Dialogs, um Bilder auszuwählen
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.png")])
        if file_paths:
            self.image_list = list(file_paths)
            self.show_image(0)

    def show_image(self, index):
        if 0 <= index < len(self.image_list):
            image_path = self.image_list[index]
            self.image_index = index

            # Bild laden und anzeigen
            img = Image.open(image_path)
            img = img.resize((800, 600), Image.Resampling.LANCZOS)
            self.image_tk = ImageTk.PhotoImage(img)

            # Canvas leeren und das neue Bild anzeigen
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

            # Zurücksetzen der Bounding Boxen und Rechtecke
            self.labels = []
            self.rectangles = []

    def select_class(self, class_name):
        self.current_class = class_name
        self.class_label.config(text=f"Aktuelle Klasse: {class_name}")

    def on_mouse_down(self, event):
        if self.current_class is None:
            print("Bitte wähle eine Klasse aus!")
            return

        # Startkoordinaten der Bounding Box
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)

        # Bounding Box während des Ziehens in der Farbe der aktuellen Klasse anzeigen
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y,
                                                 outline=self.get_class_color(self.class_buttons.index(self.current_class)))

    def on_mouse_up(self, event):
        # Endkoordinaten der Bounding Box
        end_x = event.x
        end_y = event.y

        # Normalisieren der Koordinaten auf das Bild
        img_width = self.canvas.winfo_width()
        img_height = self.canvas.winfo_height()

        x_center = (self.start_x + end_x) / 2 / img_width
        y_center = (self.start_y + end_y) / 2 / img_height
        box_width = abs(end_x - self.start_x) / img_width
        box_height = abs(end_y - self.start_y) / img_height

        # Speichern der Bounding Box Koordinaten mit der zugehörigen Klasse und Farbe
        label = (self.current_class, x_center, y_center, box_width, box_height, self.get_class_color(self.class_buttons.index(self.current_class)))
        self.labels.append(label)

        # Bounding Box in der jeweiligen Farbe zeichnen und speichern
        rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, end_x, end_y,
                                               outline=self.get_class_color(self.class_buttons.index(self.current_class)))
        self.rectangles.append(rect_id)

    def save_labels(self):
        # Aktuelles Bild und zugehörige Labels speichern
        image_path = self.image_list[self.image_index]
        label_path = os.path.splitext(image_path)[0] + ".txt"

        with open(label_path, "w") as f:
            for label in self.labels:
                class_name, x_center, y_center, box_width, box_height, _ = label
                class_id = self.class_buttons.index(class_name)  # Klassen ID bestimmen
                f.write(f"{class_id} {x_center} {y_center} {box_width} {box_height}\n")

        print(f"Labels für {image_path} gespeichert.")

    def undo_last_box(self):
        if self.labels:
            # Letzte Bounding Box und Rechteck löschen
            self.labels.pop()  # Entferne das letzte Label
            rect_id = self.rectangles.pop()  # Entferne das letzte Rechteck vom Canvas
            self.canvas.delete(rect_id)  # Lösche das Rechteck vom Canvas
            print("Letzte Box wurde entfernt.")

    def get_class_color(self, class_index):
        # Rückgabe einer Farbe für jede Klasse
        colors = ['red', 'blue', 'green', 'yellow']  # Farben für vier Klassen
        return colors[class_index % len(colors)]  # Wenn mehr Klassen als Farben vorhanden sind

# Erstellen des Tkinter-Fensters
root = tk.Tk()
app = LabelingTool(root)
root.mainloop()
