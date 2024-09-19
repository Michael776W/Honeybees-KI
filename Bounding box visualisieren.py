import os
import cv2
import matplotlib.pyplot as plt

# Funktion, um YOLO-Bounding-Boxen zu lesen und auf das Bild zu projizieren
def draw_bounding_boxes(image_path, label_path):
    # Bild laden
    image = cv2.imread(image_path)
    image_height, image_width = image.shape[:2]

    # Bounding Box-Daten aus der .txt Datei lesen
    with open(label_path, 'r') as file:
        lines = file.readlines()

    # Jede Zeile der Label-Datei durchgehen
    for line in lines:
        data = line.strip().split()

        # Klasse runden, falls sie als Gleitkommazahl vorliegt
        class_id = int(float(data[0]))  # Verwandle in float und dann in int (entfernt .0)
        x_center, y_center, width, height = map(float, data[1:])

        # Berechne absolute Bounding Box-Koordinaten
        x_center_abs = int(x_center * image_width)
        y_center_abs = int(y_center * image_height)
        width_abs = int(width * image_width)
        height_abs = int(height * image_height)

        # Berechne die obere linke Ecke der Bounding Box
        x1 = int(x_center_abs - width_abs / 2)
        y1 = int(y_center_abs - height_abs / 2)
        # Berechne die untere rechte Ecke der Bounding Box
        x2 = int(x_center_abs + width_abs / 2)
        y2 = int(y_center_abs + height_abs / 2)

        # Zeichne das Rechteck auf das Bild
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Grün für Bounding Boxen
        # Optional: Zeichne die Klassen-ID auf das Bild
        cv2.putText(image, f'Class {class_id}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Bild mit Bounding Boxes anzeigen
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

# Hauptfunktion, um durch alle Bilder und Labels zu gehen
def visualize_yolo_annotations(image_dir, label_dir):
    # Durch alle Bilder im Bildverzeichnis gehen
    for image_file in os.listdir(image_dir):
        if image_file.endswith(('.jpg', '.png')):
            image_path = os.path.join(image_dir, image_file)
            label_path = os.path.join(label_dir, image_file.replace('.jpg', '.txt').replace('.png', '.txt'))
            if os.path.exists(label_path):
                print(f'Visualisiere {image_file}')
                draw_bounding_boxes(image_path, label_path)
            else:
                print(f'Keine Label-Datei für {image_file} gefunden.')

# Beispiel-Aufruf
image_directory = r'D:\Bienen_KI2\PYthon\data\images'
label_directory = r'D:\Bienen_KI2\PYthon\data\labels'
visualize_yolo_annotations(image_directory, label_directory)

