from kivy.uix.screenmanager import Screen
from ..services.api import api_client


class LoginScreen(Screen):
    def do_login(self):
        email = self.ids.email.text
        password = self.ids.senha.text
        try:
            api_client.login(email, password)
            self.manager.current = "home"
        except Exception as e:
            print("Erro login", e)
