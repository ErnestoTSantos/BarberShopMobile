from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager

from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem

from services.api import api_client


class LoginScreen(Screen):
    def login_user(self):
        email = self.ids.email.text
        password = self.ids.password.text

        if api_client.login(email, password):
            self.manager.current = "home"
        else:
            print("Invalid credentials")


class RegisterScreen(Screen):
    def register_user(self):
        name = self.ids.name.text
        email = self.ids.email.text
        password = self.ids.password.text

        if api_client.register(name, email, password):
            self.manager.current = "login"
        else:
            print("Registration failed")


class HomeScreen(Screen):
    def on_enter(self):
        self.load_establishments()

    def load_establishments(self):
        lista = self.ids.establishment_list
        lista.clear_widgets()

        try:
            establishments = api_client.get_establishments()
        except:
            establishments = [
                "John's Barbershop",
                "Elite Barber Studio",
                "Premium Barber House",
            ]

        for name in establishments:
            item = OneLineListItem(text=name)
            lista.add_widget(item)


class WindowManager(ScreenManager):
    pass


class BarberApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("screens/screens.kv")


Window.size = (360, 640)
BarberApp().run()
