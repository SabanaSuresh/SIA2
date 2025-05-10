from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle, Rectangle
from database import Database
from geopy.geocoders import Nominatim
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock



class InterventionDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.current_intervention = None
        self.mapview = None  # Référence à stocker
        
        # Initialiser les listes comme vides
        self.membres = []
        self.equipements = []

        # Fond de l'écran en bleu très clair
        self.root_layout = BoxLayout(orientation='vertical', spacing=0, padding=0)
        with self.root_layout.canvas.before:
            Color(0.85, 0.95, 1, 1)  # Bleu très clair comme dans la maquette
            self.bg_rect = Rectangle(pos=self.root_layout.pos, size=self.root_layout.size)
        self.root_layout.bind(pos=lambda *a: setattr(self.bg_rect, 'pos', self.root_layout.pos))
        self.root_layout.bind(size=lambda *a: setattr(self.bg_rect, 'size', self.root_layout.size))
        self.add_widget(self.root_layout)

        # Zone du haut avec Airblio, carte et infos
        top_area = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))
        
        # Colonne gauche: Logo et bouton retour
        left_top = BoxLayout(orientation='vertical', size_hint=(0.25, 1), spacing=15, padding=[0, 0, 10, 10])

        # Logo Airblio flottant en position absolue (tout en haut à gauche)
        logo_float = FloatLayout(size_hint=(1, None), height=40)
        logo = Label(
            text=" ",
            font_size=32,
            bold=True,
            color=(0.13, 0.62, 0.74, 1),
            size_hint=(None, None),
            size=(120, 40),
            pos=(5, 5)  # Position très proche du coin supérieur gauche
        )
        # Ajouter le logo au float layout
        logo_float.add_widget(logo)

        # Ajouter le float layout avant tout
        self.root_layout.add_widget(logo_float)
        
        # Bouton de retour en orange comme dans la maquette
        btn_retour = Button(
            text="Retour à la liste des interventions", 
            size_hint=(1, None), 
            height=50,
            background_normal='',
            background_color=(0, 0, 0, 0),  # Transparent car nous utilisons notre propre fond
            color=(1, 1, 1, 1),
            font_size=18
        )
        with btn_retour.canvas.before:
            Color(0.96, 0.55, 0.09, 1)  # Orange
            self.btn_retour_rect = RoundedRectangle(pos=btn_retour.pos, size=btn_retour.size, radius=[5])
        btn_retour.bind(pos=lambda *args, b=btn_retour: setattr(self.btn_retour_rect, 'pos', b.pos))
        btn_retour.bind(size=lambda *args, b=btn_retour: setattr(self.btn_retour_rect, 'size', b.size))
        btn_retour.bind(on_press=lambda instance: setattr(self.manager, 'current', 'intervention'))
        left_top.add_widget(btn_retour)

        spacer = Widget(size_hint=(1, None), height=40)
        left_top.add_widget(spacer)
        
        top_area.add_widget(left_top)
        
        # Colonne centrale: Carte
        map_container = BoxLayout(orientation='vertical', size_hint=(0.5, 1), padding=[10, 10, 10, 10])
        self.mapview = MapView(zoom=10, size_hint=(1, 1))
        
        # Ajouter une bordure à la carte
        with map_container.canvas.before:
            Color(0.13, 0.59, 0.75, 1)  # Bleu comme dans la maquette
            map_border = RoundedRectangle(pos=map_container.pos, size=map_container.size, radius=[5])
        # Utiliser des références explicites pour éviter les problèmes de portée des variables
        map_container.bind(pos=lambda *a, container=map_container, border=map_border: setattr(border, 'pos', container.pos))
        map_container.bind(size=lambda *a, container=map_container, border=map_border: setattr(border, 'size', container.size))
            
        map_container.add_widget(self.mapview)
        top_area.add_widget(map_container)
        
        # Colonne droite: Avancement et Coûts
        right_top = BoxLayout(orientation='vertical', size_hint=(0.25, 1), spacing=10, padding=[10, 10, 20, 10])
        
        # Boîtes d'informations
        self.avancement_box = self.create_info_box("Avancement", "0%")
        right_top.add_widget(self.avancement_box)
        
        self.cout_box = self.create_info_box("Coûts", "0€")
        right_top.add_widget(self.cout_box)
        
        top_area.add_widget(right_top)
        
        self.root_layout.add_widget(top_area)
        
        # Zone principale (panneau des membres, contenu principal)
        main_area = BoxLayout(orientation='horizontal', size_hint=(1, 0.6))
        
        # Colonne gauche: Membres et Équipements
        left_panel = BoxLayout(orientation='vertical', size_hint=(0.35, 1), spacing=15, padding=[20, 15, 5, 15])
        
        # Panneau des membres - initialisé vide
        self.membres_card = self.create_dropdown_card("Membres", [])
        left_panel.add_widget(self.membres_card)
        
        # Panneau des équipements - initialisé vide
        self.equipements_card = self.create_dropdown_card("Équipements", [])
        left_panel.add_widget(self.equipements_card)
        
        main_area.add_widget(left_panel)
        
        # Colonne centrale/droite: Fiche d'intervention
        self.central_card = BoxLayout(orientation='vertical', size_hint=(0.65, 1), padding=[20, 20, 20, 10], spacing=5)
        with self.central_card.canvas.before:
            Color(1, 1, 1, 1)  # Fond blanc
            central_bg = RoundedRectangle(pos=self.central_card.pos, size=self.central_card.size, radius=[5])
        # Utiliser des références explicites
        self.central_card.bind(pos=lambda *a, card=self.central_card, bg=central_bg: setattr(bg, 'pos', card.pos))
        self.central_card.bind(size=lambda *a, card=self.central_card, bg=central_bg: setattr(bg, 'size', card.size))
        
        # En-tête de la fiche
        header_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=100, spacing=5)
        
        # N° d'intervention et référence
        ref_box = BoxLayout(size_hint=(1, None), height=30)
        self.ref_label = Label(
            text="N° -    Demande N° -",
            color=(0, 0, 0, 0.7), 
            font_size=16, 
            halign='left',
            valign='middle',
            size_hint=(1, 1),
            text_size=(800, 30)
        )
        ref_box.add_widget(self.ref_label)
        header_box.add_widget(ref_box)
        
        # Titre de l'intervention
        title_box = BoxLayout(size_hint=(1, None), height=70)
        self.title_label = Label(
            text="Intervention - Titre non défini",
            color=(0, 0, 0, 1),
            font_size=26,
            bold=True,
            halign='center',
            valign='middle',
            size_hint=(1, 1),
            text_size=(800, 70)
        )
        title_box.add_widget(self.title_label)
        header_box.add_widget(title_box)
        
        self.central_card.add_widget(header_box)
        
        # Informations client/site/contact
        info_grid = GridLayout(cols=2, size_hint=(1, None), height=160, spacing=[10, 5])
        
        # Colonne gauche
        self.info_left = BoxLayout(orientation='vertical', spacing=5)
        
        self.entreprise_label = Label(
            text="Entreprise : -",
            color=(0, 0, 0, 1),
            font_size=16,
            halign='left',
            size_hint=(1, 1),
            text_size=(400, None)
        )
        self.info_left.add_widget(self.entreprise_label)
        
        self.site_label = Label(
            text="Site concerné : -",
            color=(0, 0, 0, 1),
            font_size=16,
            halign='left',
            size_hint=(1, 1),
            text_size=(400, None)
        )
        self.info_left.add_widget(self.site_label)
        
        self.contact_label = Label(
            text="Contact sur site : -\nDate de réalisation : -",
            color=(0, 0, 0, 1),
            font_size=16,
            halign='left',
            size_hint=(1, 1),
            text_size=(400, None)
        )
        self.info_left.add_widget(self.contact_label)
        
        # Colonne droite - alignée à droite
        self.info_right = BoxLayout(orientation='vertical', spacing=5)
        
        self.date_label = Label(
            text="-\n-",
            color=(0, 0, 0, 1),
            font_size=16,
            halign='right',
            size_hint=(1, 1),
            text_size=(380, None)
        )
        self.info_right.add_widget(self.date_label)
        
        self.info_right.add_widget(Widget())  # Spacer
        
        # Ajouter colonnes au grid
        info_grid.add_widget(self.info_left)
        info_grid.add_widget(self.info_right)
        
        self.central_card.add_widget(info_grid)
        
        # Description
        desc_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=200, padding=[10, 10, 10, 10])
        self.desc_label = Label(
            text="Aucune description disponible.",
            color=(0, 0, 0, 1),
            font_size=16,
            halign='left',
            valign='top',
            size_hint=(1, 1),
            text_size=(800, 200)
        )
        desc_box.add_widget(self.desc_label)
        self.central_card.add_widget(desc_box)
        
        # Statut et importance
        status_box = BoxLayout(size_hint=(1, None), height=30, spacing=20)
        
        self.status_label = Label(
            text="Statut : -",
            color=(0, 0, 0, 1),
            font_size=16,
            halign='left',
            size_hint=(0.5, 1),
            text_size=(380, 30)
        )
        
        self.importance_label = Label(
            text="Importance : -",
            color=(0, 0, 0, 1),
            font_size=16,
            halign='right',
            size_hint=(0.5, 1),
            text_size=(380, 30)
        )
        
        status_box.add_widget(self.status_label)
        status_box.add_widget(self.importance_label)
        
        self.central_card.add_widget(status_box)
        
        # Bouton "Ajouter un commentaire" à l'intérieur de la carte blanche
        comment_btn_container = BoxLayout(size_hint=(1, None), height=40, padding=[0, 5, 0, 5])
        comment_container_center = AnchorLayout(anchor_x='center', anchor_y='center')

        self.btn_commentaire = Button(
            text="Ajouter un Commentaire",
            size_hint=(None, None),  # Taille fixe au lieu de prendre toute la largeur
            size=(250, 30),         # Plus petit en hauteur et en largeur
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            font_size=16            # Police légèrement plus petite
        )
        with self.btn_commentaire.canvas.before:
            Color(0.40, 0.72, 0.85, 1)  # Bleu plus clair comme sur la capture d'écran
            self.btn_commentaire_rect = RoundedRectangle(pos=self.btn_commentaire.pos, size=self.btn_commentaire.size, radius=[5])
        self.btn_commentaire.bind(pos=lambda *args, b=self.btn_commentaire: setattr(self.btn_commentaire_rect, 'pos', b.pos))
        self.btn_commentaire.bind(size=lambda *args, b=self.btn_commentaire: setattr(self.btn_commentaire_rect, 'size', b.size))
        self.btn_commentaire.bind(on_press=self.show_comment_popup)

        comment_container_center.add_widget(self.btn_commentaire)
        comment_btn_container.add_widget(comment_container_center)
        self.central_card.add_widget(comment_btn_container)

        
        main_area.add_widget(self.central_card)
        
        self.root_layout.add_widget(main_area)
        
        # Barre de boutons en bas (sans le bouton commentaire)
        self.bottom_bar = BoxLayout(size_hint=(1, None), height=70, spacing=15, padding=[20, 10, 20, 10])
        self.root_layout.add_widget(self.bottom_bar)

        # Boutons du bas avec style bleu clair de la maquette
        self.create_bottom_buttons()
        
        # Initialisation de la carte avec une position par défaut
        self.mapview.center_on(43.3, 5.37)  # Coordonnées par défaut (Marseille)
        marker = MapMarker(lat=43.3, lon=5.37)
        self.mapview.add_widget(marker)

    def create_bottom_buttons(self):
        # Modifié pour avoir des boutons plus courts et alignés à droite
        button_style = {
            'font_size': 18,
            'size_hint': (None, 1),  # Largeur fixe au lieu de prendre toute la largeur
            'width': 200,           # Largeur fixe pour chaque bouton (ajustez selon vos besoins)
            'background_normal': '',
            'background_color': (0.13, 0.59, 0.75, 1),  # Bleu comme dans la maquette
            'color': (1, 1, 1, 1)
        }
        
        self.btn_creer = Button(text="Créer une Intervention", **button_style)
        self.btn_modifier = Button(text="Modifier l'Intervention", **button_style)
        self.btn_clore = Button(text="Clore l'Intervention", **button_style)
        
        # Créer des références pour les rectangles de fond des boutons
        self.btn_rects = {}
        for btn in [self.btn_creer, self.btn_modifier, self.btn_clore]:
            btn.background_color = (0, 0, 0, 0)  # Transparent
            with btn.canvas.before:
                Color(0.13, 0.59, 0.75, 1)  # Bleu maquette
                self.btn_rects[btn] = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[5])
            btn.bind(pos=lambda *args, b=btn: setattr(self.btn_rects[b], 'pos', b.pos))
            btn.bind(size=lambda *args, b=btn: setattr(self.btn_rects[b], 'size', b.size))
                
        self.btn_creer.bind(on_press=self.go_to_form)
        self.btn_modifier.bind(on_press=self.go_to_modif)
        self.btn_clore.bind(on_press=self.confirm_clore_intervention)
        
        # Modifier la barre du bas pour aligner les boutons à droite
        # Ajout d'un widget espaceur qui prendra l'espace restant à gauche
        spacer = Widget(size_hint=(1, 1))
        self.bottom_bar.add_widget(spacer)
        
        # Ajouter les boutons
        self.bottom_bar.add_widget(self.btn_creer)
        self.bottom_bar.add_widget(self.btn_modifier)
        self.bottom_bar.add_widget(self.btn_clore)

    def go_to_form(self, instance):
        form_screen = self.manager.get_screen('form_intervention')
        form_screen.reset_form()
        self.manager.current = 'form_intervention'

    def go_to_modif(self, instance):
        if self.current_intervention:
            modif_screen = self.manager.get_screen('intervention_modif_screen')
            modif_screen.load_intervention(self.current_intervention)
            self.manager.current = 'intervention_modif_screen'

    def create_dropdown_card(self, title, items=[]):
        print(f"[DEBUG] Création d'une carte {title} avec {len(items)} items")
        
        # Création de la carte avec dropdown comme dans la maquette - Augmenter la hauteur
        card = BoxLayout(orientation='vertical', size_hint=(1, None), height=200, spacing=0)  # Hauteur augmentée de 80 à 150
        
        # En-tête avec flèche dropdown
        header = BoxLayout(size_hint=(1, None), height=40)
        with header.canvas.before:
            Color(0.13, 0.59, 0.75, 1)  # Bleu foncé pour l'en-tête
            header_rect = RoundedRectangle(pos=header.pos, size=header.size, radius=[5, 5, 0, 0])
        header.bind(pos=lambda *a, widget=header, rect=header_rect: setattr(rect, 'pos', widget.pos))
        header.bind(size=lambda *a, widget=header, rect=header_rect: setattr(rect, 'size', widget.size))
        
        title_label = Label(text=title, color=(1, 1, 1, 1), bold=True, font_size=18)
        arrow = Label(text="▼", size_hint=(None, 1), width=30, color=(1, 1, 1, 1))
        header.add_widget(title_label)
        header.add_widget(arrow)
        
        # Contenu - Faire défiler si nécessaire avec un ScrollView
        scroll_container = ScrollView(size_hint=(1, None), height=160)  # Hauteur pour le contenu
        content = BoxLayout(orientation='vertical', size_hint=(1, None))
        content.bind(minimum_height=content.setter('height'))  # Important pour le défilement
        
        with content.canvas.before:
            Color(1, 1, 1, 1)  # Fond blanc pour le contenu
            content_rect = RoundedRectangle(pos=content.pos, size=content.size, radius=[0, 0, 5, 5])
        content.bind(pos=lambda *a, widget=content, rect=content_rect: setattr(rect, 'pos', widget.pos))
        content.bind(size=lambda *a, widget=content, rect=content_rect: setattr(rect, 'size', widget.size))
        
        # Ajouter les éléments
        content_height = 0
        if items:
            print(f"[DEBUG] Ajout de {len(items)} items à la carte {title}")
            for item in items:
                if item:  # Vérifier que l'item n'est pas vide
                    print(f"[DEBUG] Ajout de l'item: '{item}'")
                    item_label = Label(
                        text=item.strip(),
                        color=(0, 0, 0, 1),
                        font_size=16,
                        size_hint=(1, None),
                        height=30,
                        halign='left',
                        valign='middle',
                        text_size=(250, 30)  # Largeur augmentée pour le texte
                    )
                    content.add_widget(item_label)
                    content_height += 30
        else:
            print(f"[DEBUG] Aucun item à ajouter à la carte {title}")
            item_label = Label(
                text="Aucun élément",
                color=(0.5, 0.5, 0.5, 1),  # Gris
                font_size=16,
                size_hint=(1, None),
                height=30,
                halign='left',
                valign='middle',
                text_size=(250, 30)
            )
            content.add_widget(item_label)
            content_height += 30
        
        # Ajuster la hauteur du contenu
        content.height = max(content_height, 160)
        scroll_container.add_widget(content)
        
        # Ajuster la hauteur de la carte
        card.height = header.height + scroll_container.height
        
        card.add_widget(header)
        card.add_widget(scroll_container)
        return card

    def create_info_box(self, title, value, color=(0.13, 0.59, 0.75, 1)):
        # Boîte d'info avec bordure et fond bleu clair comme dans la maquette
        box = BoxLayout(orientation='vertical', size_hint=(1, None), height=100, padding=[0, 5, 0, 5])
        
        # Créer des références pour les rectangles
        border_rect = None
        inner_rect = None
        
        with box.canvas.before:
            Color(*color)  # Couleur de bordure
            border_rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[5])
            
            # Fond intérieur légèrement plus clair
            Color(0.85, 0.95, 1, 1)  # Bleu très clair
            inner_rect = RoundedRectangle(
                pos=(box.pos[0] + 2, box.pos[1] + 2),
                size=(box.size[0] - 4, box.size[1] - 4),
                radius=[3]
            )
        
        # Utiliser des références locales pour les liaisons
        border = border_rect
        inner = inner_rect
        
        box.bind(pos=lambda *a, box=box, border=border: setattr(border, 'pos', box.pos))
        box.bind(size=lambda *a, box=box, border=border: setattr(border, 'size', box.size))
        box.bind(pos=lambda *a, box=box, inner=inner: setattr(inner, 'pos', (box.pos[0] + 2, box.pos[1] + 2)))
        box.bind(size=lambda *a, box=box, inner=inner: setattr(inner, 'size', (box.size[0] - 4, box.size[1] - 4)))
        
        # Titre et valeur dans la boîte d'info
        box.add_widget(Label(text=title, font_size=18, color=(0, 0, 0, 1), size_hint=(1, 0.4)))
        box.add_widget(Label(text=str(value), font_size=24, bold=True, color=(0, 0, 0, 1), size_hint=(1, 0.6)))
        
        return box
    
    def show_comment_popup(self, instance):
        if not self.current_intervention:
            return

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Label(text="Ajouter un commentaire :", font_size=20))

        comment_input = TextInput(hint_text="Votre commentaire ici...", multiline=True, size_hint=(1, 0.6))
        layout.add_widget(comment_input)

        btn_layout = BoxLayout(size_hint=(1, 0.3), spacing=10)
        btn_cancel = Button(text="Annuler")
        btn_validate = Button(text="Valider", background_color=(0.13, 0.59, 0.75, 1), color=(1, 1, 1, 1))

        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_validate)

        layout.add_widget(btn_layout)

        popup = Popup(title="Nouveau commentaire",
                  content=layout,
                  size_hint=(None, None),
                  size=(500, 400),
                  auto_dismiss=False)

        btn_cancel.bind(on_press=popup.dismiss)

        def save_comment(instance):
            new_comment = comment_input.text.strip()
            query = "UPDATE interventions SET commentaire = %s WHERE id = %s"
            self.db.cursor.execute(query, (new_comment or '', self.current_intervention['id']))
            self.db.conn.commit()
            popup.dismiss()
            self.load_intervention(self.current_intervention['id'])  # Recharge les données

        btn_validate.bind(on_press=save_comment)

        popup.open()

    def confirm_clore_intervention(self, instance):
        if not self.current_intervention:
            return

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text="Êtes-vous sûr de vouloir clore cette intervention ?", font_size=20))

        btn_row = BoxLayout(spacing=10, size_hint=(1, 0.3))
        btn_annuler = Button(text="Annuler")
        btn_confirmer = Button(text="Oui", background_color=(0.96, 0.55, 0.09, 1), color=(1, 1, 1, 1))  # Orange maquette

        btn_row.add_widget(btn_annuler)
        btn_row.add_widget(btn_confirmer)
        layout.add_widget(btn_row)

        popup = Popup(title="Confirmation de clôture",
                    content=layout,
                    size_hint=(None, None), size=(500, 300),
                    auto_dismiss=False)

        btn_annuler.bind(on_press=popup.dismiss)

        # La fonction est définie ici avec une référence correcte à self et popup
        def mark_as_completed(instance):
            try:
                # Mettre à jour le statut au lieu de supprimer
                query = "UPDATE interventions SET statut = 'Terminée' WHERE id = %s"
                self.db.cursor.execute(query, (self.current_intervention['id'],))
                self.db.conn.commit()
                popup.dismiss()
                
                # Recharger l'intervention pour voir le statut mis à jour
                self.load_intervention(self.current_intervention['id'])
                
                # Afficher une confirmation
                success_popup = Popup(title="Intervention clôturée",
                                    content=Label(text="L'intervention a été marquée comme terminée.", font_size=16),
                                    size_hint=(None, None), size=(500, 200))
                success_popup.open()
                
                # Après 2 secondes, fermer la popup
                Clock.schedule_once(lambda dt: success_popup.dismiss(), 2)
                
                # Optionnel: si vous voulez aussi retourner à la liste des interventions
                # self.manager.get_screen('intervention').load_interventions()
                # self.manager.current = 'intervention'
            except Exception as e:
                popup.dismiss()
                error_popup = Popup(title="Erreur",
                                content=Label(text=str(e), font_size=16),
                                size_hint=(None, None), size=(500, 200))
                error_popup.open()

        # Lier correctement la fonction au bouton
        btn_confirmer.bind(on_press=mark_as_completed)
        popup.open()

    def mark_as_completed(instance):
        try:
            # Mettre à jour le statut au lieu de supprimer
            query = "UPDATE interventions SET statut = 'Terminée' WHERE id = %s"
            self.db.cursor.execute(query, (self.current_intervention['id'],))
            self.db.conn.commit()
            popup.dismiss()
            
            # Recharger l'intervention pour voir le statut mis à jour
            self.load_intervention(self.current_intervention['id'])
            
            # Afficher une confirmation
            success_popup = Popup(title="Intervention clôturée",
                                content=Label(text="L'intervention a été marquée comme terminée.", font_size=16),
                                size_hint=(None, None), size=(500, 200))
            success_popup.open()
            
            # Après 2 secondes, fermer la popup
            Clock.schedule_once(lambda dt: success_popup.dismiss(), 2)
            
            # Optionnel: si vous voulez aussi retourner à la liste des interventions
            # self.manager.get_screen('intervention').load_interventions()
            # self.manager.current = 'intervention'
        except Exception as e:
            popup.dismiss()
            error_popup = Popup(title="Erreur",
                            content=Label(text=str(e), font_size=16),
                            size_hint=(None, None), size=(500, 200))
            error_popup.open()

        btn_confirmer.bind(on_press=mark_as_completed)
        popup.open()

    def update_avancement(self, statut):
        # Mise à jour de l'avancement en fonction du statut
        if statut == "Terminée":
            avancement = "100%"
        elif statut == "En cours":
            avancement = "50%"
        elif statut == "A venir":
            avancement = "0%"
        else:
            avancement = "0%"
            
        # Mettre à jour la boîte d'avancement
        self.avancement_box.clear_widgets()
        self.avancement_box.add_widget(Label(text="Avancement", font_size=18, color=(0, 0, 0, 1), size_hint=(1, 0.4)))
        self.avancement_box.add_widget(Label(text=avancement, font_size=24, bold=True, color=(0, 0, 0, 1), size_hint=(1, 0.6)))
        
        return avancement

    def load_intervention(self, intervention_id):
        try:
            # Récupérer les données d'intervention
            print(f"[DEBUG] Chargement de l'intervention ID: {intervention_id}")
            print(f"[DEBUG] Type de ID: {type(intervention_id)}")
            
            query = "SELECT * FROM interventions WHERE id = %s"
            print(f"[DEBUG] Exécution de la requête: {query} avec ID: {intervention_id}")
            self.db.cursor.execute(query, (intervention_id,))
            intervention = self.db.cursor.fetchone()
            
            print(f"[DEBUG] Résultat de la requête: {intervention}")
            
            if not intervention:
                print(f"Aucune intervention trouvée avec l'ID {intervention_id}")
                return

            # Convertir les valeurs None en chaînes vides pour éviter les erreurs
            for key in intervention.keys():
                if intervention[key] is None:
                    intervention[key] = ''

            self.current_intervention = intervention
            
            # Récupérer les données de la demande associée
            reference_demande = intervention.get('reference_demande')
            if reference_demande:  # Vérifier que reference_demande n'est pas None ou vide
                query_demande = "SELECT * FROM demandes WHERE numero_demande = %s"
                print(f"[DEBUG] Exécution de la requête demande: {query_demande} avec ref: {reference_demande}")
                self.db.cursor.execute(query_demande, (reference_demande,))
                demande = self.db.cursor.fetchone()
                print(f"[DEBUG] Résultat de la requête demande: {demande}")
            else:
                print("[DEBUG] Pas de référence de demande, création d'un dictionnaire vide")
                demande = {}  # Créer un dictionnaire vide si aucune référence de demande n'est trouvée
            
            if demande is None:
                demande = {}  # Créer un dictionnaire vide si aucune demande n'est trouvée

            # Mettre à jour l'avancement en fonction du statut
            statut = intervention.get('statut', 'A venir')
            avancement = self.update_avancement(statut)
            
            # Mettre à jour les coûts
            self.cout_box.clear_widgets()
            self.cout_box.add_widget(Label(text="Coûts", font_size=18, color=(0, 0, 0, 1), size_hint=(1, 0.4)))
            self.cout_box.add_widget(Label(text=f"{intervention.get('cout', 0)}€", font_size=24, bold=True, color=(0, 0, 0, 1), size_hint=(1, 0.6)))

            # Mettre à jour la carte avec la position correcte
            try:
                geolocator = Nominatim(user_agent="airblio_app")
                raw_address = intervention.get('lieu', '') or demande.get('site', '')
                if raw_address:
                    location = geolocator.geocode(raw_address)
                    
                    if location:
                        lat, lon = location.latitude, location.longitude
                        self.mapview.center_on(lat, lon)
                        
                        # Supprimer les marqueurs existants
                        for marker in [w for w in self.mapview.children if isinstance(w, MapMarker)]:
                            self.mapview.remove_widget(marker)
                        
                        # Ajouter le nouveau marqueur
                        new_marker = MapMarker(lat=lat, lon=lon)
                        self.mapview.add_widget(new_marker)
                    else:
                        # Position par défaut si l'adresse n'est pas trouvée
                        self.mapview.center_on(43.3, 5.37)  # Coordonnées par défaut (Marseille)
                else:
                    self.mapview.center_on(43.3, 5.37)  # Coordonnées par défaut (Marseille)
            
            except Exception as e:
                print(f"Erreur lors de la mise à jour de la carte: {e}")
                # Fallback to default location
                self.mapview.center_on(43.3, 5.37)
                
            # Mettre à jour les informations de l'intervention dans l'interface
            self.title_label.text = f"Intervention - {intervention.get('intitule', '') or demande.get('intitule', 'Sans titre')}"
            
            # Mettre à jour les références
            self.ref_label.text = f"N° {intervention.get('id', '')}    Demande N° {intervention.get('reference_demande', '')}"
            
            # Mettre à jour les informations client/site/contact
            self.entreprise_label.text = f"Entreprise : {demande.get('entreprise', 'Non spécifié')}"
            
            site_info = f"Site concerné : {intervention.get('lieu', 'Non spécifié')}"
            self.site_label.text = site_info
            
            contact_info = f"Contact sur site : {demande.get('contact', 'Non spécifié')}\nDate de réalisation : {intervention.get('date_intervention', 'Non planifiée')}"
            self.contact_label.text = contact_info
            
            # Colonne droite
            date_info = f"{demande.get('date_demande', '')}\n{demande.get('heure_demande', '')}"
            self.date_label.text = date_info
            
            # Mettre à jour la description
            self.desc_label.text = intervention.get('description', 'Aucune description disponible.')
            
            # Mettre à jour les commentaires s'ils existent
            comment_text = intervention.get('commentaire', '')
            # Supprimer l'ancien widget de commentaires s'il existe
            for i, child in enumerate(self.central_card.children):
                if isinstance(child, BoxLayout) and len(child.children) == 1 and isinstance(child.children[0], Label) and "Commentaires :" in child.children[0].text:
                    self.central_card.remove_widget(child)
                    break
                
            if comment_text:
                comment_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=80, padding=[10, 5, 10, 5])
                comment_label = Label(
                    text=f"Commentaires : {comment_text}",
                    italic=True,
                    color=(0, 0, 0, 0.8),
                    font_size=16,
                    halign='left',
                    valign='top',
                    size_hint=(1, 1),
                    text_size=(780, 80)
                )
                comment_box.add_widget(comment_label)
                
                # Trouver l'index de la description pour insérer le commentaire juste après
                desc_index = None
                for i, child in enumerate(self.central_card.children):
                    if isinstance(child, BoxLayout) and len(child.children) == 1 and isinstance(child.children[0], Label) and child.children[0] == self.desc_label:
                        desc_index = i
                        break
                
                # Insérer après la description si trouvée, sinon en haut
                if desc_index is not None:
                    self.central_card.add_widget(comment_box, index=desc_index)
                else:
                    # Fallback - ajouter en haut
                    self.central_card.add_widget(comment_box)
            
            # Mettre à jour le statut et l'importance
            self.status_label.text = f"Statut : {intervention.get('statut', 'En attente')}"
            
            # Interpréter l'importance
            importance = intervention.get('importance', '')
            importance_text = "Faible"
            if importance == "moyenne" or importance == "orange":
                importance_text = "Moyenne"
            elif importance == "haute" or importance == "red":
                importance_text = "Haute"
                
            self.importance_label.text = f"Importance : {importance_text}"
            
            # Mettre à jour les panneaux des membres et équipements
            # Récupérer les membres depuis la BDD
            membres_str = intervention.get('membre', '')
            print(f"[DEBUG] Membres string: '{membres_str}'")
            if membres_str and isinstance(membres_str, str):
                membres = [m.strip() for m in membres_str.split(',')]
            else:
                membres = []
            print(f"[DEBUG] Liste membres après traitement: {membres}")
                
            # Récupérer les équipements depuis la BDD
            equipements_str = intervention.get('equipement', '')
            print(f"[DEBUG] Équipements string: '{equipements_str}'")
            if equipements_str and isinstance(equipements_str, str):
                equipements = [e.strip() for e in equipements_str.split(',')]
            else:
                equipements = []
            print(f"[DEBUG] Liste équipements après traitement: {equipements}")
                
            # Mettre à jour les panneaux des membres et équipements
            print(f"[DEBUG] Membres: {membres}")
            print(f"[DEBUG] Équipements: {equipements}")

            # Ne pas utiliser l'accès direct aux widgets par leurs indices, c'est fragile
            # Utiliser des références directes à ces widgets

            # Supprimer les widgets existants des membres et équipements
            # Solution directe : recréer les cartes et les ajouter à des conteneurs existants
            try:
                print(f"[DEBUG] Création de nouvelles cartes membres et équipements")
                
                # Récupérer une référence au BoxLayout vertical dans le panneau gauche
                # Ce BoxLayout doit exister dans votre interface (créé dans __init__)
                main_area = [child for child in self.root_layout.children if isinstance(child, BoxLayout) and child.size_hint[1] == 0.6][0]
                left_panel = [child for child in main_area.children if isinstance(child, BoxLayout) and child.size_hint[0] == 0.35][0]
                
                # Effacer tous les widgets du panneau gauche
                left_panel.clear_widgets()
                
                # Créer de nouvelles cartes
                print(f"[DEBUG] Création de la carte des membres avec {len(membres)} membres")
                membres_card = self.create_dropdown_card("Membres", membres)
                left_panel.add_widget(membres_card)
                
                print(f"[DEBUG] Création de la carte des équipements avec {len(equipements)} équipements")
                equipements_card = self.create_dropdown_card("Équipements", equipements)
                left_panel.add_widget(equipements_card)
                
                print("[DEBUG] Cartes membres et équipements ajoutées avec succès")
            except Exception as e:
                print(f"[ERROR] Erreur lors de la mise à jour des cartes membres/équipements: {e}")
                import traceback
                traceback.print_exc()

                
            except Exception as e:
                print(f"[ERROR] Erreur lors de la mise à jour des panneaux membres/équipements: {e}")
                import traceback
                traceback.print_exc()
            
            print(f"Intervention {intervention_id} chargée avec succès")
            
        except Exception as e:
            print(f"Erreur lors du chargement de l'intervention: {e}")
            import traceback
            traceback.print_exc()

    def set_intervention_id(self, intervention_id):
        print(f"[DEBUG] set_intervention_id appelée avec ID: {intervention_id}")
        # Vérifier la connexion à la BDD
        if not self.db.conn.is_connected():
            print("[ERROR] La connexion à la BDD est fermée, tentative de reconnexion...")
            self.db = Database()  # Reconnexion
        self.load_intervention(intervention_id)