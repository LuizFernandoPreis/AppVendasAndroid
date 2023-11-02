from botoes import ImageButton, LabelButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
import requests
from kivy.app import App
from functools import partial
class BannerVendedor(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__()
        try:
            with self.canvas:
                Color(rgb=(0, 0, 0, 1))
                self.rec = Rectangle(size=self.size, pos=self.pos)
            self.bind(pos=self.atualizar_Rec, size=self.atualizar_Rec)
            id_vendedor = kwargs["id_vendedor"]

            link = f'https://aplicativovendashash-2dc43-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor}"'
            requisicao = requests.get(link)
            requisicao_dic = requisicao.json()
            valor = list(requisicao_dic.values())[0]
            avatar = valor['avatar']
            total_vendas = valor['total_vendas']

            meuApp = App.get_running_app()

            imagem = ImageButton(source=f"icones/fotos_perfil/{avatar}",
                                 pos_hint={"right":0.4, "top": 0.9},
                                 size_hint = (0.3, 0.8),
                                 on_release = partial(meuApp.carregar_vendas_vendedores, valor))
            label_id = LabelButton(text= f"ID Vendedor: {id_vendedor}",
                                   pos_hint={"right":0.9, "top": 0.9},
                                   size_hint = (0.5, 0.5),
                                 on_release = partial(meuApp.carregar_vendas_vendedores, valor))
            t_vendas = LabelButton(text=f'Total de vendas: {total_vendas}',
                                   pos_hint={"right":0.9, "top": 0.5},
                                   size_hint = (0.5, 0.5),
                                 on_release = partial(meuApp.carregar_vendas_vendedores, valor))
            self.add_widget(t_vendas)
            self.add_widget(imagem)
            self.add_widget(label_id)
        except:
            pass

    def atualizar_Rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size

