from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.graphics import Color, RoundedRectangle

from carte_widget import CarteWidget
from database import Database
from navigation_bar import NavigationBar

class CarteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.projets_originaux = []
        self.boutons_projets = {}
        self.markers_projets = {}
        self.projet_selectionne_id = None

        # Layout principal
        self.main_layout = BoxLayout(orientation='vertical', spacing=0)
        self.add_widget(self.main_layout)

        # Navigation bar en haut
        self.navbar = NavigationBar(self.manager, current_screen_name="carte")
        self.main_layout.add_widget(self.navbar)

        # Contenu principal : sidebar + carte
        content = BoxLayout(orientation='horizontal', spacing=10, padding=20)

        # Sidebar gauche
        left_side = GridLayout(cols=1, spacing=30, padding=20, size_hint=(0.3, 1))
        with left_side.canvas.before:
            Color(0.0, 0.22, 0.33, 1)
            self.sidebar_bg = RoundedRectangle(pos=left_side.pos, size=left_side.size, radius=[20])
        left_side.bind(pos=self.update_sidebar_bg, size=self.update_sidebar_bg)

        # Filtres
        filter_box = BoxLayout(orientation='vertical', spacing=15, padding=[10, 10])
        filter_box.add_widget(Label(text="Filtres", font_size=26, bold=True, color=(1, 1, 1, 1), size_hint=(1, None), height=50))

        self.lieu_input = TextInput(hint_text="Filtrer par lieu...", font_size=20, size_hint=(1, None), height=60)
        self.lieu_input.bind(text=self.apply_filters)
        self.date_input = TextInput(hint_text="Filtrer par date (AAAA-MM-JJ)...", font_size=20, size_hint=(1, None), height=60)
        self.date_input.bind(text=self.apply_filters)

        statut_buttons = BoxLayout(size_hint=(1, None), height=60, spacing=10)
        self.btn_en_cours = Button(text="En cours", font_size=18, background_color=(0.4, 0.8, 1, 1), bold=True)
        self.btn_prevu = Button(text="Prévu", font_size=18, background_color=(0.4, 0.8, 1, 1), bold=True)
        self.btn_en_cours.bind(on_press=lambda instance: self.toggle_statut('en cours'))
        self.btn_prevu.bind(on_press=lambda instance: self.toggle_statut('prévu'))
        statut_buttons.add_widget(self.btn_en_cours)
        statut_buttons.add_widget(self.btn_prevu)

        filter_box.add_widget(self.lieu_input)
        filter_box.add_widget(self.date_input)
        filter_box.add_widget(statut_buttons)
        left_side.add_widget(filter_box)

        # Liste projets
        scroll_box = BoxLayout(orientation='vertical', padding=[10, 10])
        scroll_box.add_widget(Label(text="Projets", font_size=26, bold=True, color=(1, 1, 1, 1), size_hint=(1, None), height=50))
        scroll = ScrollView(size_hint=(1, 1))
        self.projet_list = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.projet_list.bind(minimum_height=self.projet_list.setter('height'))
        scroll.add_widget(self.projet_list)
        scroll_box.add_widget(scroll)
        left_side.add_widget(scroll_box)

        # Détails projet
        detail_box = BoxLayout(orientation='vertical', padding=[10, 10])
        detail_box.add_widget(Label(text="Détails du projet", font_size=26, bold=True, color=(1, 1, 1, 1), size_hint=(1, None), height=50))
        self.projet_details = Label(
            text="Sélectionnez un projet",
            size_hint=(1, 1),
            halign='left',
            valign='top',
            markup=True,
            font_size=18,
            color=(1, 1, 1, 1)
        )
        self.projet_details.bind(size=self.update_details_text_size)
        self.projet_details.bind(texture_size=self.projet_details.setter('size'))
        detail_box.add_widget(self.projet_details)
        left_side.add_widget(detail_box)

        # Carte
        self.mapview = CarteWidget(size_hint=(0.7, 1))
        self.mapview.zoom = 2
        self.mapview.lat = 20
        self.mapview.lon = 0

        content.add_widget(left_side)
        content.add_widget(self.mapview)

        # Ajouter le contenu à la layout principale
        self.main_layout.add_widget(content)

        self.selected_statut = None
        self.load_projets()

    def update_sidebar_bg(self, *args):
        self.sidebar_bg.pos = self.children[0].children[0].children[-1].pos
        self.sidebar_bg.size = self.children[0].children[0].children[-1].size

    def update_details_text_size(self, instance, value):
        self.projet_details.text_size = (self.projet_details.width - 20, None)

    def load_projets(self):
        self.projets_originaux = self.db.get_projets()
        self.refresh_affichage()

    def refresh_affichage(self):
        self.projet_list.clear_widgets()
        self.boutons_projets.clear()
        self.markers_projets.clear()

        for child in self.mapview.children[:]:
            if isinstance(child, MapMarkerPopup):
                self.mapview.remove_widget(child)

        for projet in self.projets_originaux:
            if not self.passe_filtres(projet):
                continue

            projet_btn = Button(
                text=f"{projet['nom_projet']} - {projet['date_projet']}",
                font_size=18,
                size_hint_y=None,
                height=50,
                background_color=(0.5, 0.5, 0.5, 1)
            )
            projet_btn.bind(on_press=lambda instance, p=projet: self.selectionner_projet(p))
            self.projet_list.add_widget(projet_btn)
            self.boutons_projets[projet['id']] = projet_btn

            marker = MapMarkerPopup(lat=projet['latitude'], lon=projet['longitude'])
            marker.bind(on_release=lambda instance, p=projet: self.selectionner_projet(p))
            self.mapview.add_widget(marker)
            self.markers_projets[projet['id']] = marker

    def passe_filtres(self, projet):
        if self.lieu_input.text.strip() and self.lieu_input.text.strip().lower() not in projet['lieu'].lower():
            return False
        if self.date_input.text.strip() and self.date_input.text.strip() not in str(projet['date_projet']):
            return False
        if self.selected_statut and projet['statut'] != self.selected_statut:
            return False
        return True

    def afficher_details(self, projet):
        details = f"""[b]Nom :[/b] {projet['nom_projet']}
[b]Lieu :[/b] {projet['lieu']}
[b]Date :[/b] {projet['date_projet']}
[b]Statut :[/b] {projet['statut']}
[b]Membres :[/b] {projet.get('membres', 'Non précisé')}
[b]Équipements :[/b] {projet.get('equipements', 'Non précisé')}
"""
        self.projet_details.text = details

    def selectionner_projet(self, projet):
        self.afficher_details(projet)
        self.mapview.center_on(projet['latitude'], projet['longitude'])
        self.mapview.zoom = 10

        if self.projet_selectionne_id is not None:
            ancien_btn = self.boutons_projets.get(self.projet_selectionne_id)
            if ancien_btn:
                ancien_btn.background_color = (0.5, 0.5, 0.5, 1)

        self.projet_selectionne_id = projet['id']
        nouveau_btn = self.boutons_projets.get(projet['id'])
        if nouveau_btn:
            nouveau_btn.background_color = (0.1, 0.6, 0.8, 1)

    def apply_filters(self, instance, value):
        self.refresh_affichage()

    def toggle_statut(self, statut):
        if self.selected_statut == statut:
            self.selected_statut = None
        else:
            self.selected_statut = statut
        self.refresh_affichage()