from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.core.window import Window
from navigation_bar import NavigationBar



from database import Database

class DemandeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        with self.layout.canvas.before:
            Color(222 / 255, 240 / 255, 248 / 255, 1)  # RGB from hex DEF0F8
            self.bg_rect = RoundedRectangle(pos=self.layout.pos, size=self.layout.size)
        self.layout.bind(pos=self.update_bg, size=self.update_bg)
        self.navbar = NavigationBar(screen_manager=self.manager, current_screen_name="demande")
        self.bind(on_pre_enter=self.update_navbar_manager)
        self.layout.add_widget(self.navbar, index=len(self.layout.children))

        self.add_widget(self.layout)

        self.layout.add_widget(Widget(size_hint_y=None, height=20))  # Décale la barre de recherche vers le bas
        self.create_search_bar()
        self.layout.add_widget(Widget(size_hint_y=None, height=120))  # Décale vers le bas
        self.create_headers()
        self.create_scrollview()
        self.load_demandes()


    def create_search_bar(self):
        search_box = BoxLayout(size_hint=(1, None), height=60, padding=(10, 10), spacing=10)

        with search_box.canvas.before:
            Color(1, 1, 1, 1)
            self.search_bg = RoundedRectangle(pos=search_box.pos, size=search_box.size, radius=[10])
        search_box.bind(pos=self.update_search_bg, size=self.update_search_bg)

        self.search_bar = TextInput(
            hint_text="Rechercher une demande...",
            background_color=(0, 0, 0, 0),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 0, 1),
            size_hint=(1, 1),
            multiline=False,
            font_size=22,
            padding=(10, 10)
        )
        self.search_bar.bind(text=self.on_search_text)
        search_box.add_widget(self.search_bar)
        self.layout.add_widget(search_box)

    def update_search_bg(self, instance, value):
        self.search_bg.pos = instance.pos
        self.search_bg.size = instance.size

    def on_search_text(self, instance, value):
        self.load_demandes()

    def create_headers(self):
        headers = GridLayout(cols=6, size_hint_y=None, height=50, spacing=20, padding=(10, 0))
        titles = ["N° Demande", "N° Client", "Intitulé", "Date", "Importance", ""]
        
        # Utiliser les mêmes proportions de largeur pour les en-têtes et les contenus
        widths = [0.15, 0.15, 0.35, 0.15, 0.1, 0.05]
        aligns = ['center', 'center', 'center', 'center', 'center', 'center']

        for title, width, align in zip(titles, widths, aligns):
            label = Label(
                text=title,
                size_hint_x=width,
                font_size=28,
                color=(0, 0, 0, 1),
                halign=align,
                valign="middle",
                bold=True
            )
            label.bind(size=label.setter("text_size"))
            headers.add_widget(label)

        self.layout.add_widget(headers)

    def create_scrollview(self):
        self.scroll = ScrollView(size_hint=(1, 1))
        self.demandes_list = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=(0, 10))
        self.demandes_list.bind(minimum_height=self.demandes_list.setter('height'))
        self.scroll.add_widget(self.demandes_list)
        self.layout.add_widget(self.scroll)

    def load_demandes(self):
        self.demandes_list.clear_widgets()
        all_demandes = self.db.get_demandes()
        search_text = self.search_bar.text.lower().strip()

        demandes = [d for d in all_demandes if search_text in d.get("intitule", "").lower()]

        for index, demande in enumerate(demandes):
            row = BoxLayout(size_hint_y=None, height=60, padding=10, spacing=20)

            def on_mouse_pos(_, pos, row=row):
                if not row.get_root_window():
                    return  # évite erreur si widget non monté
                inside = row.collide_point(*row.to_widget(*pos))
                with row.canvas.before:
                    row.canvas.before.clear()
                    if inside:
                        Color(0.56, 0.79, 0.9, 1)  # couleur 8ECAE6
                    else:
                        Color(1, 1, 1, 1)
                    row.bg_rect = RoundedRectangle(pos=row.pos, size=row.size, radius=[8])

                row.bind(pos=self.update_row_rect, size=self.update_row_rect)

            Window.bind(mouse_pos=on_mouse_pos)



            numero_demande = str(demande.get("numero_demande", ""))
            client = str(demande.get("numero_client", ""))
            intitule = demande.get("intitule", "")
            if len(intitule) > 50:
                intitule = intitule[:50] + "..."
            date = str(demande.get("date_demande", ""))
            importance = demande.get("importance", "")
            id_demande = numero_demande

            # Définir les mêmes proportions que les en-têtes
            widths = [0.15, 0.15, 0.35, 0.15]
            aligns = ['center', 'center', 'left', 'center']
            
            # Créer les labels avec les mêmes proportions que les en-têtes
            for text, width, align in zip([numero_demande, client, intitule, date], widths, aligns):
                label = Label(
                    text=text,
                    size_hint_x=width,
                    font_size=25,
                    halign=align,
                    valign="middle",
                    color=(0, 0.2, 0.3, 1),
                )
                label.bind(size=label.setter('text_size'))
                row.add_widget(label)

            # Conteneur pour l'indicateur d'importance (pastille)
            importance_box = BoxLayout(size_hint_x=0.1, padding=(80, 5, 5, 5))  # left, top, right, bottom
            
            importance_color = {
                "red": (1, 0, 0, 1),
                "orange": (1, 0.6, 0, 1),
                "green": (0, 0.6, 0, 1)
            }.get(importance, (0.5, 0.5, 0.5, 1))

            pastille_container = BoxLayout(size_hint=(None, 1), width=40, padding=(5, 10))
            pastille = Widget(size_hint=(None, None), size=(20, 20))
            with pastille.canvas:
                Color(*importance_color)
                circle = RoundedRectangle(pos=pastille.pos, size=pastille.size, radius=[10])
            pastille.bind(pos=lambda inst, val, rect=circle: setattr(rect, 'pos', inst.pos))
            pastille.bind(size=lambda inst, val, rect=circle: setattr(rect, 'size', inst.size))
            pastille_container.add_widget(pastille)
            importance_box.add_widget(pastille_container)
            row.add_widget(importance_box)

            # Bouton de suppression avec la bonne proportion
            delete_box = BoxLayout(size_hint_x=0.05)
            btn_delete = Button(
                size_hint=(None, 1),
                width=40,
                background_normal='trash.png',  # chemin vers ton image
                #background_down='icons/trash.png',    # facultatif
                background_color=(1, 1, 1, 1)
            )
            btn_delete.bind(on_press=self.make_delete_handler(id_demande))
            delete_box.add_widget(btn_delete)
            row.add_widget(delete_box)
            
            row.bind(on_touch_down=self.make_row_touch_handler(demande, btn_delete))

            self.demandes_list.add_widget(row)
            
    def make_row_touch_handler(self, demande, delete_btn):
        def handler(instance, touch):
            # Ignorer si on clique sur le bouton supprimer
            if delete_btn.collide_point(*touch.pos):
                return False
            if instance.collide_point(*touch.pos):
                self.afficher_details(demande)
                return True
            return False
        return handler

    def update_row_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            instance.bg_rect = RoundedRectangle(pos=instance.pos, size=instance.size, radius=[10])

    def _update_border_rect(self, instance, value):
        if hasattr(self, 'border_rect'):
            self.border_rect.pos = instance.pos
            self.border_rect.size = instance.size

    def delete_demande(self, demande_id):
        try:
            self.db.delete_demande(demande_id)
            self.load_demandes()
        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")

    def make_delete_handler(self, demande_id):
        return lambda instance: self.delete_demande(demande_id)

    def afficher_details(self, demande):
        popup = ModalView(size_hint=(0.65, 0.7), auto_dismiss=True)

        # Récupérer l'importance pour définir la couleur de la bordure
        importance = demande.get("importance", "").lower()
        
        # Déterminer la couleur de la bordure en fonction de l'importance
        border_color = {
            "red": (1, 0, 0, 1),   # Rouge pour importance haute
            "orange": (1, 0.6, 0, 1),  # Orange pour importance moyenne
            "green": (0, 0.6, 0, 1)   # Vert pour importance basse
        }.get(importance, (0.5, 0.5, 0.5, 1))  # Gris par défaut

        # Container principal avec bordure colorée selon l'importance
        main_container = BoxLayout(orientation='vertical', padding=8)  # Ajouter un padding pour voir la bordure
        
        # Container interne blanc 
        container = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Appliquer les canvas APRÈS avoir ajouté les widgets aux containers
        # mais AVANT d'ajouter le container à la popup
        
        # Récupération des données
        numero_demande = demande.get("numero_demande", "D001")
        client = demande.get("numero_client", "Inconnu")
        intitule = demande.get("intitule", "Sans titre")
        date_complete = str(demande.get("date_demande", ""))
        description = demande.get("description", "Pas de description disponible.")
        entreprise = demande.get("entreprise", "Entreprise X")
        site_concerne = demande.get("site", "St Malo, 35400")
        contact_site = demande.get("contact", "Client Z")
        
        # Formatage de la date (si disponible)
        date_parts = date_complete.split() if date_complete else ["", ""]
        date = date_parts[0] if len(date_parts) > 0 else ""
        heure = date_parts[1] if len(date_parts) > 1 else ""
        
        # En-tête avec numéro, intitulé et date
        header_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
        
        # Première ligne - numéro à gauche, intitulé au milieu (gras), date à droite
        top_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        
        # Numéro de demande (gauche)
        num_label = Label(
            text=f"N° {numero_demande}",
            font_size=24,
            color=(0, 0, 0, 1),
            size_hint_x=0.25,
            halign="left",
            valign="middle",
            bold=True
        )
        num_label.bind(size=num_label.setter("text_size"))
        
        # Intitulé (centre, en gras)
        intitule_label = Label(
            text=intitule,
            font_size=24,
            color=(0, 0, 0, 1),
            size_hint_x=0.5,
            halign="center",
            valign="middle",
            bold=True
        )
        intitule_label.bind(size=intitule_label.setter("text_size"))
        
        # Date (droite)
        date_label = Label(
            text=date,
            font_size=24,
            color=(0, 0, 0, 1),
            size_hint_x=0.25,
            halign="right",
            valign="middle"
        )
        date_label.bind(size=date_label.setter("text_size"))
        
        top_row.add_widget(num_label)
        top_row.add_widget(intitule_label)
        top_row.add_widget(date_label)
        
        # Deuxième ligne - heure sous l'intitulé au milieu
        middle_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        
        # Espaceur gauche
        middle_row.add_widget(Widget(size_hint_x=0.25))
        
        # Heure (centre)
        heure_label = Label(
            text=heure,
            font_size=18,
            color=(0, 0, 0, 1),
            size_hint_x=0.5,
            halign="center",
            valign="top"
        )
        heure_label.bind(size=heure_label.setter("text_size"))
        middle_row.add_widget(heure_label)
        
        # Espaceur droite
        middle_row.add_widget(Widget(size_hint_x=0.25))
        
        header_layout.add_widget(top_row)
        header_layout.add_widget(middle_row)
        
        # Informations client (entreprise, site, contact)
        info_client = BoxLayout(orientation='vertical', size_hint_y=None, height=90, padding=(0, 5))
        
        entreprise_label = Label(
            text=f"Entreprise : {entreprise}",
            font_size=18,
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=30,
            text_size=(800, None)
        )
        
        site_label = Label(
            text=f"Site : {site_concerne}",
            font_size=18,
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=30,
            text_size=(800, None)
        )
        
        contact_label = Label(
            text=f"Contact : {contact_site}",
            font_size=18,
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=30,
            text_size=(800, None)
        )
        
        info_client.add_widget(entreprise_label)
        info_client.add_widget(site_label)
        info_client.add_widget(contact_label)
        
        # Description avec espace supplémentaire au-dessus
        description_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # Ajouter un espace avant la description
        spacing_widget = Widget(size_hint_y=None, height=180)
        description_layout.add_widget(spacing_widget)
        
        description_label = Label(
            text=description,
            font_size=18,
            color=(0, 0, 0, 1),
            halign="left",
            valign="top",
            text_size=(800, None)
        )
        description_label.bind(texture_size=description_label.setter("size"))
        
        description_layout.add_widget(description_label)
        
        # Bouton en bas centré
        btn_box = BoxLayout(size_hint_y=None, height=70, orientation='vertical')
        btn = Button(
            text="Créer une Intervention",
            size_hint=(None, None),
            size=(280, 50),
            pos_hint={"center_x": 0.5},
            background_color=(0.2, 0.4, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=18
        )
        def aller_vers_creation(instance):
            popup.dismiss()
            form_screen = self.manager.get_screen('form_intervention')
            form_screen.charger_depuis_demande(demande)
            self.manager.current = 'form_intervention'

        btn.bind(on_press=aller_vers_creation)
        btn_box.add_widget(btn)
        
        # Assemblage de tous les éléments
        container.add_widget(header_layout)
        container.add_widget(info_client)
        container.add_widget(description_layout)
        container.add_widget(Widget(size_hint_y=1))  # Espace flexible
        container.add_widget(btn_box)
        
        # Ajouter le container blanc au container principal
        main_container.add_widget(container)
        
        # Couche de bordure colorée
        with main_container.canvas.before:
            self.border_color_instruction = Color(*border_color)
            self.border_rect = RoundedRectangle(pos=main_container.pos, size=main_container.size, radius=[10])
        main_container.bind(pos=self._update_border_rect, size=self._update_border_rect)

        # Maintenant ajouter le canvas au container interne (fond blanc)
        with container.canvas.before:
            Color(1, 1, 1, 1)  # Fond blanc
            container.bg_rect = RoundedRectangle(pos=container.pos, size=container.size, radius=[8])
        
        def _update_border_rect(self, instance, value):
            if hasattr(self, 'border_rect'):
                self.border_rect.pos = instance.pos
                self.border_rect.size = instance.size

        def update_bg_rect(instance, value):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        
        main_container.bind(pos=self._update_border_rect, size=self._update_border_rect)
        container.bind(pos=update_bg_rect, size=update_bg_rect)
        
        # Enfin, ajouter le container principal à la popup
        popup.add_widget(main_container)
        popup.open()
        
    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    

    def on_pre_enter(self, *args):
        self.load_demandes()

    def update_navbar_manager(self, *args):
        self.navbar.screen_manager = self.manager
