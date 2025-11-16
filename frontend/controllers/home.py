from kivy.uix.screenmanager import Screen
from ..services.api import api_client
from kivymd.uix.list import OneLineListItem


class HomeScreen(Screen):
    def on_enter(self):
        try:
            ests = api_client.get_estabelecimentos()
            lista = self.ids.lista_estabelecimentos
            lista.clear_widgets()
            for e in ests:
                lista.add_widget(OneLineListItem(text=e.get("nome", "---")))
        except Exception as exc:
            print("Erro ao buscar estabelecimentos", exc)
