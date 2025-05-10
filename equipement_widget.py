from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty
from kivy.clock import Clock


class DonutGraph(FloatLayout):
    pourcentage = NumericProperty(0)

    def __init__(self, pourcentage=0, couleur_dispo=(0.2, 0.6, 0.86, 1), couleur_manquant=(0.8, 0.8, 0.8, 1), show_text=True, **kwargs):
        super().__init__(**kwargs)
        self.pourcentage = pourcentage
        self.couleur_dispo = couleur_dispo
        self.couleur_manquant = couleur_manquant
        self.show_text = show_text

        with self.canvas:
            Color(*self.couleur_manquant)
            self.bg_circle = Ellipse()

            Color(*self.couleur_dispo)
            self.progress_circle = Ellipse(angle_start=0)

            Color(1, 1, 1, 1)
            self.hole_circle = Ellipse()

        if self.show_text:
            self.percent_label = Label(
                text=f"{self.pourcentage}%",
                font_size='20sp',
                bold=True,
                color=(0, 0, 0, 1),
                size_hint=(None, None),
                size=(100, 40),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                halign='center',
                valign='middle'
            )
            self.add_widget(self.percent_label)


        self.bind(pos=self.update_graph, size=self.update_graph)
        self.bind(pourcentage=self.update_text)
        Clock.schedule_once(lambda dt: self.update_graph())

    def update_text(self, *args):
        if self.show_text:
            self.percent_label.text = f"{self.pourcentage}%"

    def update_graph(self, *args):
        size = min(self.width, self.height)
        donut_size = size * 0.9

        self.bg_circle.size = (donut_size, donut_size)
        self.bg_circle.pos = (self.center_x - donut_size / 2, self.center_y - donut_size / 2)

        self.progress_circle.size = (donut_size, donut_size)
        self.progress_circle.pos = self.bg_circle.pos
        self.progress_circle.angle_end = 360 * self.pourcentage / 100

        hole_size = donut_size * 0.5
        self.hole_circle.size = (hole_size, hole_size)
        self.hole_circle.pos = (
            self.center_x - hole_size / 2,
            self.center_y - hole_size / 2
        )


class EquipementWidget(BoxLayout):
    couleur_nom = ListProperty([0.01, 0.19, 0.28, 1])  # 023047

    def __init__(self, nom_equipement, statut, pourcentage, couleur_dispo, couleur_manquant, couleur_statut=(0.2, 0.2, 0.2, 1), couleur_nom=None, **kwargs):
        if couleur_nom:
            kwargs['couleur_nom'] = couleur_nom

        super().__init__(
            orientation='vertical',
            padding=10,
            spacing=10,
            size_hint=(1, None),
            height=350,
            **kwargs
        )

        self.graph = DonutGraph(
            pourcentage=pourcentage,
            couleur_dispo=couleur_dispo,
            couleur_manquant=couleur_manquant,
            size_hint=(1, 0.7)
        )
        self.add_widget(self.graph)

        self.add_widget(Label(
            text=nom_equipement,
            font_size='18sp',
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=40,
            color=self.couleur_nom
        ))

        self.add_widget(Label(
            text=statut,
            font_size='14sp',
            color=couleur_statut,
            size_hint=(1, None),
            height=30
        ))
