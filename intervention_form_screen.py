from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.widget import Widget

from database import Database
from navigation_bar import NavigationBar


class BorderedSpinner(BoxLayout):
    def __init__(self, text="Sélectionner", values=(), **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = 30
        self.orientation = 'vertical'

        self.spinner = Spinner(
            text=text,
            values=values,
            background_normal='',
            background_color=(1, 1, 1, 1),
            color=(0.07, 0.40, 0.51, 1),
            size_hint=(1, 1)
        )
        self.add_widget(self.spinner)

        with self.canvas.after:
            Color(0.07, 0.40, 0.51, 1)
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=1)

        self.bind(pos=self._update_border, size=self._update_border)

    def _update_border(self, *args):
        self.border.rectangle = (self.x, self.y, self.width, self.height)

    @property
    def text(self):
        return self.spinner.text

class InterventionFormScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.87, 0.94, 0.97, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.db = Database()
        self.date_selected = ""

        main_layout = FloatLayout()

        self.navbar = NavigationBar(screen_manager=self.manager, current_screen_name="form_intervention")
        self.bind(on_pre_enter=self.update_navbar_manager)
        self.navbar.size_hint = (1, None)
        self.navbar.height = 100
        self.navbar.pos_hint = {'top': 1}
        main_layout.add_widget(self.navbar)

        title = Label(text="[b]Créer une Intervention[/b]", markup=True, font_size=28, color=(0, 0, 0, 1), size_hint=(1, None), height=40, pos_hint={'center_x': 0.5, 'top': 0.86})
        main_layout.add_widget(title)

        form_container = RelativeLayout(size_hint=(0.9, 0.55), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        with form_container.canvas.before:
            Color(1, 1, 1, 1)
            self.white_rect = Rectangle(pos=(0, 0), size=form_container.size)
        form_container.bind(size=self._update_white_rect_absolute)

        form_layout = GridLayout(cols=2, row_default_height=40, spacing=10, padding=[15, 15, 15, 15], size_hint=(1, 1))

        def label_field(text):
            lbl = Label(text=text, color=(0, 0, 0, 1), size_hint=(0.4, None), height=30, halign='left', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            return lbl

        self.intitule_input = TextInput(multiline=False, size_hint=(1, None), height=40, background_color=(1, 1, 1, 1), foreground_color=(0.07, 0.40, 0.51, 1))
        with self.intitule_input.canvas.after:
            Color(0.07, 0.40, 0.51, 1)
            self.intitule_border = Line(rectangle=(self.intitule_input.x, self.intitule_input.y, self.intitule_input.width, self.intitule_input.height), width=1)
        self.intitule_input.bind(pos=self._update_intitule_border, size=self._update_intitule_border)

        self.reference_input = BorderedSpinner(text="Sélectionner", values=("D682714", "D682713","D682712","D682711","D682710","D682709","D682708","D682707","D682706"))
        self.date_button = Button(
            text="Sélectionner une date",
            size_hint=(1, None),
            height=30,
            background_normal='',
            background_color=(1, 1, 1, 1),
            color=(0.07, 0.40, 0.51, 1)
        )
        with self.date_button.canvas.after:
            Color(0.07, 0.40, 0.51, 1)
            self.date_border = Line(rectangle=(self.date_button.x, self.date_button.y, self.date_button.width, self.date_button.height), width=1)
        self.date_button.bind(pos=self._update_date_border, size=self._update_date_border)

        self.date_button.bind(on_press=self.open_date_picker)
        self.lieu_input = TextInput(multiline=False, size_hint=(1, None), height=40, background_color=(1, 1, 1, 1), foreground_color=(0.07, 0.40, 0.51, 1))
        with self.lieu_input.canvas.after:
            Color(0.07, 0.40, 0.51, 1)
            self.lieu_border = Line(rectangle=(self.lieu_input.x, self.lieu_input.y, self.lieu_input.width, self.lieu_input.height), width=1)
        self.lieu_input.bind(pos=self._update_lieu_border, size=self._update_lieu_border)
        self.statut_input = BorderedSpinner(text="En cours", values=("Terminée", "À venir", "En cours", "En retard"))
        self.importance_input = BorderedSpinner(text="Faible", values=("Faible", "Moyenne", "Élevée"))
        self.equipement_input = BorderedSpinner(text="Sélectionner", values=("Caisson Hyperbare", "Sonar de Plongée", "Combinaison de Plongée Etanche", "Propulseur Sous-Marin", "Robot Sous-Marin (ROV)", "Equipement de Soudure Sous-Marine"))
        self.membre_input = BorderedSpinner(text="Sélectionner", values=("M. Lefèvre (Chef de mission)", "C. Marin (Technicien Plongée)", "J. Dubois (Assistant technique)", "S. Moreau (Ingénieur sécurité)", "L. Fontaine (Responsable logistique)", "A. Roche (Technicien surface)", "B. Garnier (Pilote drone sous-marin)", "E. Durand (Analyste données sous-marines)"))

        self.description_input = TextInput(multiline=True, size_hint=(1, None), height=80, background_color=(1, 1, 1, 1), foreground_color=(0.07, 0.40, 0.51, 1))
        with self.description_input.canvas.after:
            Color(0.07, 0.40, 0.51, 1)
            self.description_border = Line(rectangle=(self.description_input.x, self.description_input.y, self.description_input.width, self.description_input.height), width=1)
        self.description_input.bind(pos=self._update_description_border, size=self._update_description_border)

        self.cout_input = TextInput(hint_text="en €", multiline=False, size_hint=(1, None), height=40, background_color=(1, 1, 1, 1), foreground_color=(0.07, 0.40, 0.51, 1))
        with self.cout_input.canvas.after:
            Color(0.07, 0.40, 0.51, 1)
            self.cout_border = Line(rectangle=(self.cout_input.x, self.cout_input.y, self.cout_input.width, self.cout_input.height), width=1)
        self.cout_input.bind(pos=self._update_cout_border, size=self._update_cout_border)


        form_layout.add_widget(label_field("Intitulé de l'intervention :"))
        form_layout.add_widget(self.intitule_input)
        form_layout.add_widget(label_field("Référence de la demande :"))
        form_layout.add_widget(self.reference_input)
        form_layout.add_widget(label_field("Date de l'intervention :"))
        form_layout.add_widget(self.date_button)
        form_layout.add_widget(label_field("Lieu de l'intervention :"))
        form_layout.add_widget(self.lieu_input)
        form_layout.add_widget(label_field("Statut :"))
        form_layout.add_widget(self.statut_input)
        form_layout.add_widget(label_field("Importance :"))
        form_layout.add_widget(self.importance_input)
        form_layout.add_widget(label_field("Équipements mobilisés :"))
        form_layout.add_widget(self.equipement_input)
        form_layout.add_widget(label_field("Membre de l'équipe :"))
        form_layout.add_widget(self.membre_input)

        description_label = Label(text="Description de l'intervention :", color=(0, 0, 0, 1), size_hint=(0.4, None), height=80, halign='left', valign='top')
        description_label.bind(size=description_label.setter('text_size'))
        form_layout.add_widget(description_label)
        form_layout.add_widget(self.description_input)
        form_layout.add_widget(label_field("Coût estimé :"))
        form_layout.add_widget(self.cout_input)

        form_container.add_widget(form_layout)
        main_layout.add_widget(form_container)

        buttons_box = BoxLayout(size_hint=(None, None), width=400, height=50, spacing=20, pos_hint={'center_x': 0.5, 'y': 0.05})

        annuler_btn = Button(
            text="Annuler",
            size_hint=(None, 1),
            width=180,
            background_normal='',
            background_color=(0.07, 0.40, 0.51, 1),
            color=(1, 1, 1, 1)
        )

        enregistrer_btn = Button(
            text="Créer l'Intervention",
            size_hint=(None, 1),
            width=220,
            background_normal='',
            background_color=(0.07, 0.40, 0.51, 1),
            color=(1, 1, 1, 1)
        )

        annuler_btn.bind(on_press=self.go_back)
        enregistrer_btn.bind(on_press=self.create_intervention)
        buttons_box.add_widget(annuler_btn)
        buttons_box.add_widget(enregistrer_btn)
        main_layout.add_widget(buttons_box)

        self.add_widget(main_layout)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _update_white_rect_absolute(self, instance, value):
        self.white_rect.pos = (0, 0)
        self.white_rect.size = instance.size

    def open_date_picker(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        year_spinner = Spinner(text="2025", values=[str(i) for i in range(1970, 2026)], size_hint_y=None, height=40)
        month_spinner = Spinner(text="Mai", values=["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"], size_hint_y=None, height=40)
        day_spinner = Spinner(text="1", values=[str(i) for i in range(1, 32)], size_hint_y=None, height=40)
        validate_btn = Button(text="OK", size_hint_y=None, height=40)

        content.add_widget(year_spinner)
        content.add_widget(month_spinner)
        content.add_widget(day_spinner)
        content.add_widget(validate_btn)

        popup = Popup(title="Choisir une date", content=content, size_hint=(None, None), size=(300, 300))

        def on_validate(_):
            month_map = {
                "Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04", "Mai": "05", "Juin": "06",
                "Juillet": "07", "Août": "08", "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"
            }
            day = day_spinner.text.zfill(2)
            month = month_map[month_spinner.text]
            year = year_spinner.text

            self.date_selected = f"{year}-{month}-{day}"  # format SQL correct
            self.date_button.text = f"{int(day)} {month_spinner.text} {year}"  # texte affiché lisible
            popup.dismiss()


        validate_btn.bind(on_press=on_validate)
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'intervention'

    def create_intervention(self, instance):
        # Récupère le dernier ID existant
        last_interventions = self.db.get_interventions()
        if last_interventions:
            max_id = max(inter["id"] for inter in last_interventions)
        else:
            max_id = 0
        new_id = max_id + 1

        self.db.add_intervention(
            new_id,
            self.reference_input.text,
            self.intitule_input.text,
            self.date_selected,
            self.lieu_input.text,
            self.statut_input.text,
            self.importance_input.text,
            self.equipement_input.text,
            self.membre_input.text,
            self.description_input.text,
            self.cout_input.text
        )

        if self.manager:
            intervention_screen = self.manager.get_screen('intervention')
            if hasattr(intervention_screen, 'charger_interventions'):
                intervention_screen.charger_interventions()

        self.manager.current = 'intervention'


    def charger_depuis_demande(self, demande):
        self.reference_input.spinner.text = str(demande.get("numero_demande", ""))
        self.intitule_input.text = demande.get("intitule", "")
        self.lieu_input.text = demande.get("site", "")
        importance_couleur = demande.get("importance", "green")
        if importance_couleur == "red":
            importance_texte = "Élevée"
        elif importance_couleur == "orange":
            importance_texte = "Moyenne"
        else:
            importance_texte = "Faible"
        self.importance_input.spinner.text = importance_texte

    def _update_date_border(self, *args):
        self.date_border.rectangle = (self.date_button.x, self.date_button.y, self.date_button.width, self.date_button.height)
 
    def _update_intitule_border(self, *args):
        self.intitule_border.rectangle = (self.intitule_input.x, self.intitule_input.y, self.intitule_input.width, self.intitule_input.height)

    def _update_description_border(self, *args):
        self.description_border.rectangle = (self.description_input.x, self.description_input.y, self.description_input.width, self.description_input.height)

    def _update_cout_border(self, *args):
        self.cout_border.rectangle = (self.cout_input.x, self.cout_input.y, self.cout_input.width, self.cout_input.height)

    def _update_lieu_border(self, *args):
        self.lieu_border.rectangle = (self.lieu_input.x, self.lieu_input.y, self.lieu_input.width, self.lieu_input.height)

    def update_navbar_manager(self, *args):
        self.navbar.screen_manager = self.manager

    def reset_form(self):
        self.reference_input.spinner.text = "Sélectionner"
        self.intitule_input.text = ""
        self.date_selected = ""
        self.date_button.text = "Sélectionner une date"
        self.lieu_input.text = ""
        self.statut_input.spinner.text = "En cours"
        self.importance_input.spinner.text = "Faible"
        self.equipement_input.spinner.text = "Sélectionner"
        self.membre_input.spinner.text = "Sélectionner"
        self.description_input.text = ""
        self.cout_input.text = ""
