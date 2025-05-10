from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.clock import Clock

from database import Database
from navigation_bar import NavigationBar


class InterventionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        with self.layout.canvas.before:
            Color(222 / 255, 240 / 255, 248 / 255, 1)
            self.bg_rect = RoundedRectangle(pos=self.layout.pos, size=self.layout.size)
        self.layout.bind(pos=self.update_bg, size=self.update_bg)

        self.navbar = NavigationBar(screen_manager=self.manager, current_screen_name="intervention")
        self.bind(on_pre_enter=self.update_navbar_manager)
        self.layout.add_widget(self.navbar, index=len(self.layout.children))

        self.add_widget(self.layout)

        self.layout.add_widget(Widget(size_hint_y=None, height=20))
        self.create_top_row()
        self.layout.add_widget(Widget(size_hint_y=None, height=20))
        self.create_headers()
        self.create_scrollview()
        self.load_interventions()

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def create_top_row(self):
        row = BoxLayout(size_hint=(1, None), height=100, spacing=10)

        left_box = BoxLayout(orientation='horizontal', spacing=10, size_hint=(0.3, 1))
        create_button = Button(
            text="Créer une Intervention",
            size_hint=(None, None),
            width=230,
            height=60,
            background_normal='',
            background_color=(33 / 255, 158 / 255, 188 / 255, 1),
            color=(1, 1, 1, 1),
            font_size=18
        )
        create_button.bind(on_press=self.go_to_form)

        search_container = BoxLayout(size_hint=(None, None), width=630, height=60)
        with search_container.canvas.before:
            Color(1, 1, 1, 1)
            self.search_bg = RoundedRectangle(pos=search_container.pos, size=search_container.size, radius=[10])
        search_container.bind(pos=self.update_search_bg, size=self.update_search_bg)

        self.search_input = TextInput(
            hint_text="Rechercher une intervention",
            background_color=(0, 0, 0, 0),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 0, 1),
            size_hint=(1, 1),
            font_size=20,
            multiline=False,
            padding=(10, 10)
        )
        self.search_input.bind(text=self.on_search_text)
        search_container.add_widget(self.search_input)

        left_box.add_widget(create_button)
        left_box.add_widget(search_container)

        spacer = Widget(size_hint=(0.05, 1))
        cards_layout = BoxLayout(orientation='horizontal', spacing=50, size_hint=(0.4, 1))
        cards = [
            ("Interventions terminées", "150", (0, 0.6, 0, 1)),
            ("Interventions en cours", "25", (1, 0.6, 0, 1)),
            ("Interventions à venir", "15", (1, 0.75, 0.1, 1)),
            ("Interventions en retard", "5", (1, 0, 0, 1))
        ]
        for title, count, color in cards:
            card = BoxLayout(orientation='vertical', padding=10, size_hint=(1, 1))
            card.add_widget(Label(text=title, color=(0, 0, 0, 1), font_size=18))
            card.add_widget(Label(text=count, color=color, font_size=34))
            with card.canvas.before:
                Color(180 / 255, 225 / 255, 240 / 255, 1)
                card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[10])
            card.bind(pos=self.update_card_bg, size=self.update_card_bg)
            cards_layout.add_widget(card)

        row.add_widget(left_box)
        row.add_widget(spacer)
        row.add_widget(cards_layout)
        self.layout.add_widget(row)

    def update_search_bg(self, instance, value):
        self.search_bg.pos = instance.pos
        self.search_bg.size = instance.size

    def update_card_bg(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def create_headers(self):
        row = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=(10, 0))

        headers_grid = GridLayout(cols=6, size_hint_x=0.9, spacing=10)
        titles = ["N° Intervention", "Réf Demande", "Intitulé", "Date", "Lieu", "Statut"]
        for title in titles:
            label = Label(
                text='[b]' + title + '[/b]',
                markup=True,
                font_size=24,
                color=(0, 0, 0, 1),
                halign='center',
                valign='middle'
            )
            label.bind(size=label.setter("text_size"))
            headers_grid.add_widget(label)

        row.add_widget(headers_grid)

        # Colonne "Importance"
        importance_box = BoxLayout(size_hint_x=0.1)
        importance_label = Label(
            text='[b]Importance[/b]',
            markup=True,
            font_size=24,
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle'
        )
        importance_label.bind(size=importance_label.setter("text_size"))
        importance_box.add_widget(importance_label)

        row.add_widget(importance_box)
        self.layout.add_widget(row)


    def create_scrollview(self):
        self.scroll = ScrollView(size_hint=(1, 1))
        self.intervention_list = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=(0, 10))
        self.intervention_list.bind(minimum_height=self.intervention_list.setter('height'))
        self.scroll.add_widget(self.intervention_list)
        self.layout.add_widget(self.scroll)

    def load_interventions(self):
        self.intervention_list.clear_widgets()
        all_interventions = self.db.get_interventions()
        search_text = self.search_input.text.lower().strip()

        filtered = [i for i in all_interventions if search_text in str(i.get("intitule", "")).lower() or
                    search_text in str(i.get("id", "")).lower() or
                    search_text in str(i.get("lieu", "")).lower() or
                    search_text in str(i.get("reference_demande", "")).lower()]

        for intervention in reversed(filtered):
            row = BoxLayout(size_hint_y=None, height=60, spacing=10)

            def on_mouse_pos(_, pos, row=row):
                if not row.get_root_window():
                    return
                inside = row.collide_point(*row.to_widget(*pos))
                with row.canvas.before:
                    row.canvas.before.clear()
                    Color(0.56, 0.79, 0.9, 1) if inside else Color(1, 1, 1, 1)
                    row.bg_rect = RoundedRectangle(pos=row.pos, size=row.size, radius=[8])
                row.bind(pos=self.update_row_rect, size=self.update_row_rect)

            Window.bind(mouse_pos=on_mouse_pos)

            # Bloc gauche : données
            data_layout = GridLayout(cols=6, size_hint_x=0.9)
            for key in ["id", "reference_demande", "intitule", "date_intervention", "lieu", "statut"]:
                val = str(intervention.get(key, ""))
                if key == "intitule" and len(val) > 44:
                    val = val[:37] + "..."
                if key == "lieu" and ',' in val:
                    val = val.split(',', 1)[1].strip()
                data_layout.add_widget(Label(text=val, color=(0, 0.2, 0.3, 1), font_size=22))
            row.add_widget(data_layout)

            # Bloc droite : pastille
            color_map = {"Faible": (0, 0.6, 0, 1), "Moyenne": (1, 0.6, 0, 1), "Élevée": (1, 0, 0, 1)}
            importance = intervention.get("importance", "Faible")
            dot_color = color_map.get(importance, (0.5, 0.5, 0.5, 1))

            dot_box = BoxLayout(size_hint_x=0.1, padding=(20, 5, 5, 5))
            dot = Widget(size_hint=(None, None), size=(20, 20))
            with dot.canvas:
                Color(*dot_color)
                dot_shape = RoundedRectangle(pos=dot.pos, size=dot.size, radius=[10])
            dot.bind(pos=lambda inst, val, shape=dot_shape: setattr(shape, 'pos', inst.pos))
            dot.bind(size=lambda inst, val, shape=dot_shape: setattr(shape, 'size', inst.size))
            dot_box.add_widget(dot)
            row.add_widget(dot_box)

            row.bind(on_touch_down=self.make_row_touch_handler(intervention))
            self.intervention_list.add_widget(row)


    def update_row_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            instance.bg_rect = RoundedRectangle(pos=instance.pos, size=instance.size, radius=[10])

    def make_row_touch_handler(self, intervention):
        def handler(instance, touch):
            if instance.collide_point(*touch.pos):
                print(f"[DEBUG] Clic sur l'intervention avec ID: {intervention['id']}")
                print(f"[DEBUG] Type de l'ID: {type(intervention['id'])}")
                self.show_details(intervention["id"])
                return True
            return False
        return handler

    def go_to_form(self, instance):
        form_screen = self.manager.get_screen('form_intervention')
        form_screen.reset_form()
        self.manager.current = 'form_intervention'

    def show_details(self, intervention_id):
        detail_screen = self.manager.get_screen('intervention_detail')
        detail_screen.set_intervention_id(intervention_id)  # <- appelle la bonne méthode !
        self.manager.current = 'intervention_detail'

    def on_pre_enter(self, *args):
        self.load_interventions()

    def update_navbar_manager(self, *args):
        self.navbar.screen_manager = self.manager

    def on_search_text(self, instance, value):
        self.load_interventions()