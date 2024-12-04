'''
EKSPORT WIDOKOW Z QGIS.
Pozwoli na zautomatyzowane generowanie danych do projektu

'''
import os
from qgis.core import QgsMapSettings, QgsRectangle, QgsMapRendererCustomPainterJob
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QSize

# 1. Ustawienia
grid_layer_name = "Siatka"  # Nazwa warstwy siatki
image_width, image_height = 500, 500  # Rozmiar obrazów

output_folder_vectors = "D:/qgis_tests/new_mapy"  # Folder na obrazy wektorów
output_folder_rasters = "D:/qgis_tests/new_zdjecia"  # Folder na obrazy rastrowe
os.makedirs(output_folder_vectors, exist_ok=True)
os.makedirs(output_folder_rasters, exist_ok=True)

# Pobierz warstwę siatki
grid_layer = QgsProject.instance().mapLayersByName(grid_layer_name)[0]

# Pobierz wszystkie warstwy w projekcie
layers = QgsProject.instance().mapLayers().values()

# Iteracja przez oczka siatki
for feature in grid_layer.getFeatures():
    extent = feature.geometry().boundingBox()
    print(f"Renderowanie oczka ID {feature.id()} (Extent: {extent.toString()})")

    # Podziel warstwy na wektorowe i rastrowe
    vector_layers = [layer for layer in layers if layer.type() == QgsMapLayer.VectorLayer and extent.intersects(layer.extent())]
    raster_layers = [layer for layer in layers if layer.type() == QgsMapLayer.RasterLayer and extent.intersects(layer.extent())]

    # Renderowanie warstw wektorowych
    if vector_layers:
        map_settings = QgsMapSettings()
        map_settings.setLayers(vector_layers)
        map_settings.setExtent(extent)
        map_settings.setOutputSize(QSize(image_width, image_height))
        map_settings.setBackgroundColor(Qt.transparent)  # Przezroczyste tło

        # Tworzenie obrazu
        image_vectors = QImage(QSize(image_width, image_height), QImage.Format_ARGB32_Premultiplied)
        image_vectors.fill(Qt.transparent)  # Wypełnij przezroczystością
        painter = QPainter(image_vectors)
        render_job = QgsMapRendererCustomPainterJob(map_settings, painter)
        render_job.start()
        render_job.waitForFinished()
        painter.end()

        # Zapis obrazu
        vector_path = os.path.join(output_folder_vectors, f"cell_{feature.id()}_vectors.png")
        image_vectors.save(vector_path)
        print(f"Zapisano obraz wektorów dla oczka ID: {feature.id()}")

    # Renderowanie warstw rastrowych
    if raster_layers:
        map_settings = QgsMapSettings()
        map_settings.setLayers(raster_layers)
        map_settings.setExtent(extent)
        map_settings.setOutputSize(QSize(image_width, image_height))
        map_settings.setBackgroundColor(Qt.white)  # Białe tło dla rasterów

        # Tworzenie obrazu
        image_rasters = QImage(QSize(image_width, image_height), QImage.Format_ARGB32_Premultiplied)
        image_rasters.fill(Qt.white)  # Wypełnij białym tłem
        painter = QPainter(image_rasters)
        render_job = QgsMapRendererCustomPainterJob(map_settings, painter)
        render_job.start()
        render_job.waitForFinished()
        painter.end()

        # Zapis obrazu
        raster_path = os.path.join(output_folder_rasters, f"cell_{feature.id()}_rasters.png")
        image_rasters.save(raster_path)
        print(f"Zapisano obraz rastrowy dla oczka ID: {feature.id()}")

print("Renderowanie zakończone.")