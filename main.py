import sys
import os
#sys.path.append(os.path.join(os.path.expanduser("~"), ".kivy", "garden", "garden.mapview"))
sys.path.append(r'C:\Users\srssa\.kivy\garden\garden.mapview')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

from home_screen import AccueilScreen
from demande_screen import DemandeScreen
from carte_screen import CarteScreen
from equipement_screen import EquipementScreen
from intervention_screen import InterventionScreen
from intervention_form_screen import InterventionFormScreen
from intervention_modif_screen import InterventionModifScreen
from intervention_detail_screen import InterventionDetailScreen
from database import Database

Window.clearcolor = (0.07, 0.41, 0.50, 1)  # bleu de fond

class ConnexionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        root_layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        title = Label(text="Airblio", font_size=50, color=(1, 1, 1, 1), size_hint=(1, 0.2))
        root_layout.add_widget(title)

        form_container = AnchorLayout(anchor_x='center', anchor_y='center')
        form_box = BoxLayout(orientation='vertical', spacing=15, padding=30,
                             size_hint=(None, None), size=(400, 350),
                             pos_hint={'center_x': 0.5, 'center_y': 0.5})

        with form_box.canvas.before:
            Color(1, 1, 1, 1)
            self.border = RoundedRectangle(size=(form_box.width + 4, form_box.height + 4),
                                           pos=(form_box.x - 2, form_box.y - 2), radius=[12])
            Color(0.25, 0.73, 0.83, 1)
            self.bg = RoundedRectangle(size=form_box.size, pos=form_box.pos, radius=[10])
        form_box.bind(size=self._update_rect, pos=self._update_rect)

        form_box.add_widget(Label(text="Connexion", font_size=24, bold=True, color=(1, 1, 1, 1)))

        email_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=70)
        email_label = Label(text="Email", font_size=16, color=(1, 1, 1, 1))
        self.email_input = TextInput(multiline=False, size_hint=(1, None), height=45, font_size=18)
        email_layout.add_widget(email_label)
        email_layout.add_widget(self.email_input)
        form_box.add_widget(email_layout)

        password_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=70)
        password_label = Label(text="Mot de passe", font_size=16, color=(1, 1, 1, 1))
        self.password_input = TextInput(password=True, multiline=False, size_hint=(1, None), height=45, font_size=18)
        password_layout.add_widget(password_label)
        password_layout.add_widget(self.password_input)
        form_box.add_widget(password_layout)

        checkbox_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=30, padding=(5, 5))
        checkbox = CheckBox(size_hint=(None, None), size=(20, 20))
        checkbox_label = Label(text="Se souvenir de moi", font_size=14, color=(1, 1, 1, 1), valign='middle')
        checkbox_label.bind(size=checkbox_label.setter('text_size'))
        checkbox_layout.add_widget(checkbox)
        checkbox_layout.add_widget(checkbox_label)
        form_box.add_widget(checkbox_layout)

        btn = Button(text="Se connecter", size_hint=(1, None), height=50,
                     background_color=(0, 0.15, 0.25, 1), color=(1, 1, 1, 1),
                     font_size=18, bold=True)
        btn.bind(on_press=self.connect)
        form_box.add_widget(btn)

        form_container.add_widget(form_box)
        root_layout.add_widget(form_container)
        self.add_widget(root_layout)

    def _update_rect(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size
        self.border.pos = (instance.pos[0] - 2, instance.pos[1] - 2)
        self.border.size = (instance.size[0] + 4, instance.size[1] + 4)

    def connect(self, instance):
        email = self.email_input.text.strip()
        mot_de_passe = self.password_input.text.strip()

        if self.db.verifier_utilisateur(email, mot_de_passe):
            self.manager.current = 'accueil'
        else:
            self.email_input.text = ""
            self.password_input.text = ""
            self.email_input.hint_text = "Email incorrect"
            self.password_input.hint_text = "Mot de passe incorrect"

class AirblioApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ConnexionScreen(name='connexion'))
        sm.add_widget(AccueilScreen(name='accueil'))
        sm.add_widget(DemandeScreen(name='demande'))
        sm.add_widget(CarteScreen(name='carte'))
        sm.add_widget(EquipementScreen(name='equipement'))
        sm.add_widget(InterventionScreen(name='intervention'))
        sm.add_widget(InterventionFormScreen(name="form_intervention"))
        sm.add_widget(InterventionDetailScreen(name='intervention_detail'))
        sm.add_widget(InterventionModifScreen(name='intervention_modif_screen'))
        return sm

if __name__ == '__main__':
    AirblioApp().run()
