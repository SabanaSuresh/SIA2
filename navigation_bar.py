from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.app import App

class NavigationBar(BoxLayout):
    def __init__(self, screen_manager, current_screen_name, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager  # L'initialisation correcte de screen_manager
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 100  # Plus haut qu'avant
        self.spacing = 10
        self.padding = [10, 10]

        # Couleur de fond
        with self.canvas.before:
            Color(222 / 255, 240 / 255, 248 / 255, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Logo Airblio
        logo = Label(
            text="Airblio",
            font_size=32,
            bold=True,
            color=(0.13, 0.62, 0.74, 1),
            size_hint=(None, 1),
            width=120
        )
        self.add_widget(logo)

        # Boutons de navigation
        pages = [
            ("Accueil", "accueil"),
            ("Intervention", "intervention"),
            ("Carte", "carte"),
            ("Equipement", "equipement"),
            ("Demande", "demande")
        ]

        for name, screen in pages:
            is_current = (screen == current_screen_name)
            btn = Button(
                text=f"[b]{name}[/b]" if is_current else name,
                markup=True,
                font_size=26,
                background_normal='',
                background_color=(0, 0.4, 0.6, 1),
                color=(1, 0.6, 0, 1) if is_current else (1, 1, 1, 1),
                size_hint=(1, 1)
            )
            # Correction de la lambda, assurez-vous qu'elle est correctement liée à `change_screen`
            btn.bind(on_press=self.change_screen(screen))  # Modification ici
            self.add_widget(btn)

        # Déconnexion
        logout = Button(
            size_hint=(None, 1),
            width=50,
            background_normal='logout.png',
            background_down='logout.png',
            background_color=(1, 1, 1, 1),
            border=(0, 0, 0, 0)
        )
        logout.bind(on_press=lambda instance: setattr(self.screen_manager, 'current', 'connexion'))
        self.add_widget(logout)

    def change_screen(self, screen):
        """ Fonction pour changer l'écran actuel """
        def _change(instance):
            if self.screen_manager:
                self.screen_manager.current = screen
            else:
                print("Screen manager is None!")  # Pour le debug
        return _change

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
