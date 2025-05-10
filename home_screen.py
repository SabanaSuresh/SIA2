from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.clock import Clock

from carte_widget import CarteWidget
from equipement_widget import EquipementWidget
from database import Database
from navigation_bar import NavigationBar


class AccueilScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        self.root_layout = BoxLayout(orientation='vertical', spacing=5, padding=10)
        with self.root_layout.canvas.before:
            Color(0.90, 0.95, 0.97, 1)
            self.bg_rect = RoundedRectangle(pos=self.root_layout.pos, size=self.root_layout.size)
        self.root_layout.bind(pos=self.update_bg, size=self.update_bg)
        self.add_widget(self.root_layout)

        Clock.schedule_once(self.init_ui, 0)

    def init_ui(self, *args):
        self.navbar = NavigationBar(screen_manager=self.manager, current_screen_name="accueil")
        self.bind(on_pre_enter=self.update_navbar_manager)
        self.root_layout.add_widget(self.navbar)

        alert_box = BoxLayout(size_hint=(1, None), height=40, padding=10)
        with alert_box.canvas.before:
            Color(1.0, 0.60, 0.0, 1)
            alert_box.bg = RoundedRectangle(pos=alert_box.pos, size=alert_box.size, radius=[10])
        alert_box.bind(pos=self.update_alert_bg, size=self.update_alert_bg)

        alert_btn = Button(
            text="Alerte ! Demande d'intervention suite à une tempête N°Client : 52041",
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            font_size=16,
            halign='center',
            valign='middle'
        )
        alert_btn.bind(on_press=self.ouvrir_demande_client_52041)
        alert_box.add_widget(alert_btn)
        self.root_layout.add_widget(alert_box)

        content = GridLayout(cols=2, spacing=10, padding=10, size_hint=(1, 0.8))
        content.add_widget(self.make_projets_section())
        content.add_widget(self.make_equipement_section())
        content.add_widget(self.make_interventions_section())
        content.add_widget(self.make_carte_section())
        self.root_layout.add_widget(content)

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def update_alert_bg(self, instance, value):
        if hasattr(instance, 'bg'):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size

    def update_section_bg(self, instance, value):
        if hasattr(instance, 'bg'):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size

    def make_section_box(self):
        box = BoxLayout(orientation='vertical', spacing=0, padding=0)
        with box.canvas.before:
            Color(0.75, 0.88, 0.96, 1)
            box.bg = RoundedRectangle(pos=box.pos, size=box.size, radius=[15])
        box.bind(pos=self.update_section_bg, size=self.update_section_bg)
        box.size_hint = (1, 1)
        return box

    def make_projets_section(self):
        box = self.make_section_box()
        
        # Widget espace en haut plus petit pour monter le titre
        box.add_widget(Widget(size_hint_y=0.3))
        
        # Layout principal centré
        content_layout = BoxLayout(orientation='vertical', spacing=0, padding=(5, 5, 5, 5), size_hint_y=None)
        
        # Espacement entre les lignes
        row_spacing = 15
        
        # Calculer la hauteur du contenu avec les espacements ajoutés
        title_height = 30
        header_height = 25
        row_height = 45
        num_projets = len(self.db.get_projets())
        content_height = title_height + header_height + (row_height * num_projets) + (row_spacing * (num_projets - 1))
        content_layout.height = content_height
        
        # Titre - maintenant avec un padding top négatif pour le monter un peu
        title_label = Label(
            text="",
            font_size=20,
            bold=True,
            color=(0.00, 0.23, 0.36, 1),
            halign='center',
            size_hint_y=None,
            height=title_height,
            padding=(0, -5)  # Padding négatif en haut pour monter le texte
        )
        title_label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        content_layout.add_widget(title_label)
        
        # En-tête du tableau
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=header_height)
        header.add_widget(Label(text="Nom du projet", color=(0.00, 0.23, 0.36, 1), bold=True, size_hint_x=0.5, halign='left'))
        header.add_widget(Label(text="Membres", color=(0.00, 0.23, 0.36, 1), bold=True, size_hint_x=0.25, halign='left'))
        header.add_widget(Label(text="Statut", color=(0.00, 0.23, 0.36, 1), bold=True, size_hint_x=0.25, halign='center'))
        content_layout.add_widget(header)
        
        # Lignes du tableau avec espacement
        projets = self.db.get_projets()
        for i, p in enumerate(projets):
            ligne = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height, spacing=5)
            with ligne.canvas.before:
                Color(1, 1, 1, 1)
                ligne.bg = RoundedRectangle(pos=ligne.pos, size=ligne.size, radius=[8])
            ligne.bind(pos=self.update_section_bg, size=self.update_section_bg)

            ligne.add_widget(Label(text=p.get("nom_projet", "") or "", color=(0.00, 0.23, 0.36, 1), size_hint_x=0.5, halign='left', padding=(10, 0)))
            ligne.add_widget(Label(text=p.get("membres", "") or "Aucun membre", color=(0.00, 0.23, 0.36, 1), size_hint_x=0.25, halign='left'))

            statut_box = BoxLayout(size_hint_x=0.25, padding=(5, 2))
            with statut_box.canvas.before:
                statut = p.get("statut")
                if statut == "en cours":
                    Color(1, 1, 1, 1)
                elif statut == "prévu":
                    Color(1, 1, 1, 1)
                else:
                    Color(1, 1, 1, 1)
                statut_box.bg = RoundedRectangle(pos=statut_box.pos, size=statut_box.size, radius=[5])
            statut_box.bind(pos=self.update_section_bg, size=self.update_section_bg)
            statut_box.add_widget(Label(text=statut or "", color=(0.00, 0.23, 0.36, 1), halign='center', valign='middle'))
            ligne.add_widget(statut_box)

            content_layout.add_widget(ligne)
            
            # Ajouter un espace après chaque ligne sauf la dernière
            if i < len(projets) - 1:
                content_layout.add_widget(Widget(size_hint_y=None, height=row_spacing))
        
        box.add_widget(content_layout)
        
        # Espace en bas ajusté pour équilibrer l'ensemble
        box.add_widget(Widget(size_hint_y=0.7))
        
        return box

    def make_equipement_section(self):
        from equipement_widget import DonutGraph

        box = self.make_section_box()

        # Titre
        title_label = Label(
            text="",
            font_size=20,
            bold=True,
            color=(0.00, 0.23, 0.36, 1),
            size_hint_y=None,
            height=30,
            halign='center',
            valign='middle'
        )
        title_label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))

        # Conteneur principal horizontal
        container = BoxLayout(orientation='horizontal', spacing=20, padding=10)

        # === LÉGENDE ===
        legend = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.2, 1), pos_hint={'center_y': 0.5})
        
        # Ajouter un widget vide en haut pour pousser la légende vers le centre
        legend.add_widget(Widget(size_hint_y=0.5))
        
        def legend_item(text, color, bg_color=None):
            if bg_color is None:
                r, g, b, a = color
                bg_color = (r, g, b, 0.7)
                
            item = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=35)
            
            # Cercle indicateur
            dot_container = BoxLayout(size_hint=(None, None), width=20, height=35)
            dot = Widget(size_hint=(None, None), size=(14, 14), pos_hint={'center_x': 0.5, 'center_y': 0.5})
            with dot.canvas:
                Color(*color)
                Ellipse(pos=(0, 0), size=(14, 14))
            dot_container.add_widget(dot)
            
            # Label avec fond coloré
            label_box = BoxLayout(size_hint=(1, 1))
            with label_box.canvas.before:
                Color(*bg_color)
                label_box.bg = RoundedRectangle(pos=label_box.pos, size=label_box.size, radius=[5])
            label_box.bind(pos=self.update_section_bg, size=self.update_section_bg)
            
            label = Label(
                text=text, 
                font_size=14, 
                color=(0, 0, 0, 1), 
                padding=(10, 0),
                halign='left',
                valign='middle'
            )
            label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
            label_box.add_widget(label)
            
            item.add_widget(dot_container)
            item.add_widget(label_box)
            return item

        # Couleurs constantes pour assurer la cohérence
        COULEUR_EN_STOCK = (0, 0.4, 0.6, 1)  # Bleu foncé
        COULEUR_UTILISE = (0.5, 0.8, 1, 1)        # Bleu clair
        COULEUR_RUPTURE = (1.0, 0.45, 0.09, 1)          # Orange

        legend.add_widget(legend_item("En stock", COULEUR_EN_STOCK))
        legend.add_widget(legend_item("Utilisé", COULEUR_UTILISE))
        legend.add_widget(legend_item("Rupture", COULEUR_RUPTURE, bg_color=(1.0, 0.45, 0.09, 1)))
        
        # Ajouter un widget vide en bas pour maintenir la légende centrée
        legend.add_widget(Widget(size_hint_y=0.5))

        # === DONUTS ===
        donut_grid = GridLayout(
            cols=3,
            spacing=20,
            size_hint=(0.8, 1),
            row_default_height=160,
            row_force_default=True
        )

        equipements = [
            {'nom': 'Caisson Hyperbare', 'pourcentage': 60, 'rupture': False},
            {'nom': 'Sonar de Plongée', 'pourcentage': 50, 'rupture': False},
            {'nom': 'Combinaison de Plongée Étanche', 'pourcentage': 75, 'rupture': False},
            {'nom': 'Propulseur Sous-Marin', 'pourcentage': 70, 'rupture': True},
            {'nom': 'Robot Sous-Marin (ROV)', 'pourcentage': 60, 'rupture': True},
            {'nom': 'Équipement de Soudure', 'pourcentage': 55, 'rupture': True}
        ]

        for e in equipements:
            pourcentage = e['pourcentage']
            en_rupture = e.get('rupture', False)
            
            # IMPORTANT: Correction des couleurs selon la rupture de stock
            if en_rupture:
                couleur_dispo = COULEUR_EN_STOCK  # Bleu foncé pour "En stock"
                couleur_manquant = COULEUR_RUPTURE  # Orange pour "Rupture"
            else:
                couleur_dispo = COULEUR_EN_STOCK  # Bleu foncé pour "En stock"
                couleur_manquant = COULEUR_UTILISE  # Bleu clair pour "Utilisé"

            donut_box = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 1))
            
            # Centrer le donut horizontalement
            donut_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=120)
            donut_container.add_widget(Widget(size_hint_x=0.5))  # Espace à gauche
            
            # Donut agrandi (120x120 au lieu de 100x100)
            donut = DonutGraph(
                pourcentage=pourcentage,
                couleur_dispo=couleur_dispo,
                couleur_manquant=couleur_manquant,
                size_hint=(None, None),
                size=(120, 120),
                show_text=False  # Ne pas afficher le pourcentage au centre
            )
            
            donut_container.add_widget(donut)
            donut_container.add_widget(Widget(size_hint_x=0.5))  # Espace à droite
            
            donut_box.add_widget(Widget(size_hint_y=None, height=5))  # Espacement en haut
            donut_box.add_widget(donut_container)
            
            # Label centré avec le nom
            label = Label(
                text=e['nom'],
                font_size=14,
                size_hint=(1, None),
                height=25,
                color=(0, 0, 0, 1),
                halign='center',
                valign='middle'
            )
            label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
            donut_box.add_widget(label)

            donut_grid.add_widget(donut_box)

        # Assembler
        container.add_widget(legend)
        container.add_widget(donut_grid)

        box.add_widget(title_label)
        box.add_widget(container)

        return box



    
    def aller_a_equipement(self, instance):
        if self.manager:
            self.manager.current = 'equipement'

    def make_interventions_section(self):
        box = self.make_section_box()
        
        # Widget espace en haut plus petit pour monter le titre
        box.add_widget(Widget(size_hint_y=0.3))
        
        # Layout principal centré
        content_layout = BoxLayout(orientation='vertical', spacing=0, padding=(5, 5, 5, 5), size_hint_y=None)
        
        # Espacement entre les lignes
        row_spacing = 15
        
        # Calculer la hauteur du contenu avec les espacements ajoutés
        title_height = 30
        header_height = 25
        row_height = 45
        num_interventions = len(self.db.get_interventions())
        content_height = title_height + header_height + (row_height * num_interventions) + (row_spacing * (num_interventions - 1))
        content_layout.height = content_height
        
        # Titre - maintenant avec un padding top négatif pour le monter un peu
        title_label = Label(
            text="",
            font_size=20,
            bold=True,
            color=(0.00, 0.23, 0.36, 1),
            halign='center',
            size_hint_y=None,
            height=title_height,
            padding=(0, -5)  # Padding négatif en haut pour monter le texte
        )
        title_label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        content_layout.add_widget(title_label)
        
        # En-tête du tableau
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=header_height)
        header.add_widget(Label(text="Référence", color=(0.00, 0.23, 0.36, 1), bold=True, size_hint_x=0.25, halign='left'))
        header.add_widget(Label(text="Intitulé", color=(0.00, 0.23, 0.36, 1), bold=True, size_hint_x=0.5, halign='left'))
        header.add_widget(Label(text="Date", color=(0.00, 0.23, 0.36, 1), bold=True, size_hint_x=0.2, halign='center'))
        header.add_widget(Label(text="", size_hint_x=0.05))
        content_layout.add_widget(header)
        
        # Lignes du tableau avec espacement
        interventions = self.db.get_interventions()
        for i, intervention in enumerate(interventions):
            ligne = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height, spacing=5)
            with ligne.canvas.before:
                Color(1, 1, 1, 1)
                ligne.bg = RoundedRectangle(pos=ligne.pos, size=ligne.size, radius=[8])
            ligne.bind(pos=self.update_section_bg, size=self.update_section_bg)

            ligne.add_widget(Label(text=str(intervention.get("reference_demande") or ""), color=(0.00, 0.23, 0.36, 1), size_hint_x=0.25, halign='left', padding=(10, 0)))
            ligne.add_widget(Label(text=str(intervention.get("intitule") or ""), color=(0.00, 0.23, 0.36, 1), size_hint_x=0.5, halign='left', shorten=True, shorten_from='right'))

            date_str = intervention.get("date_intervention", "")
            if date_str:
                date_str = date_str.strftime('%d/%m')
            ligne.add_widget(Label(text=str(date_str or ""), color=(0.00, 0.23, 0.36, 1), size_hint_x=0.2, halign='center'))

            importance_box = BoxLayout(size_hint_x=0.05, padding=5)
            dot = Widget(size_hint=(None, None), size=(12, 12))
            importance_color = {
                'haute': (1, 0, 0, 1),
                'moyenne': (1, 0.6, 0, 1),
                'basse': (0.3, 0.7, 0.2, 1)
            }.get(intervention.get("importance", "").lower(), (0.6, 0.6, 0.6, 1))
            with dot.canvas:
                Color(*importance_color)
                Ellipse(pos=(0, 0), size=(12, 12))
            importance_box.add_widget(dot)
            ligne.add_widget(importance_box)

            content_layout.add_widget(ligne)
            
            # Ajouter un espace après chaque ligne sauf la dernière
            if i < len(interventions) - 1:
                content_layout.add_widget(Widget(size_hint_y=None, height=row_spacing))
        
        box.add_widget(content_layout)
        
        # Espace en bas ajusté pour équilibrer l'ensemble
        box.add_widget(Widget(size_hint_y=0.7))
        
        return box

    def make_carte_section(self):
        box = self.make_section_box()
        
        # La carte est déjà centrée naturellement
        content_layout = BoxLayout(orientation='vertical', spacing=0, padding=(5, 5, 5, 5))
        
        # Titre
        title_label = Label(
            text="",
            font_size=20,
            bold=True,
            color=(0.00, 0.23, 0.36, 1),
            halign='center',
            size_hint_y=None,
            height=30
        )
        title_label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        content_layout.add_widget(title_label)
        
        # Carte
        content_layout.add_widget(CarteWidget(size_hint=(1, 1)))
        
        box.add_widget(content_layout)
        return box

    def ouvrir_demande_client_52041(self, instance):
        try:
            demande_screen = self.manager.get_screen('demande')
            demande_screen.search_bar.text = "52041"
            Clock.schedule_once(lambda dt: self._ouvrir_details_52041(demande_screen), 0.3)
            self.manager.current = 'demande'
        except Exception as e:
            print(f"Erreur navigation vers demande : {e}")

    def _ouvrir_details_52041(self, screen):
        demandes = screen.db.get_demandes()
        for d in demandes:
            if str(d.get("numero_client")) == "52041":
                screen.afficher_details(d)
                break

    def on_pre_enter(self, *args):
        self.root_layout.clear_widgets()
        self.init_ui()

    def update_navbar_manager(self, *args):
        self.navbar.screen_manager = self.manager