# === Nouveau fichier propre pour carte_widget.py ===

from mapview import MapView, MapMarkerPopup
from database import Database

class CarteWidget(MapView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zoom = 2
        self.lat = 20.0
        self.lon = 0.0

        self.db = Database()
        self.charger_marqueurs()

    def charger_marqueurs(self):
        projets = self.db.get_projets()
        for projet in projets:
            if projet.get('latitude') is not None and projet.get('longitude') is not None:
                marker = MapMarkerPopup(lat=projet['latitude'], lon=projet['longitude'])
                self.add_widget(marker)

