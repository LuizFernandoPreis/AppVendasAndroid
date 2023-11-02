from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests
from bannervenda import BannerVenda
import os
from functools import partial
from myfirebase import MyFireBase
from bannervendedor import BannerVendedor
from datetime import date
GUI = Builder.load_file('main.kv')
class MainApp(App):
    cliente = None
    produto = None
    unidade = None
    foto_perfil = None

    def build(self):
        self.firebase = MyFireBase()
        return GUI

    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids['screen_manager']
        gerenciador_telas.current = id_tela

    def on_start(self):
        # carregar as fotos de perfil
        arquivos = os.listdir("icones/fotos_perfil")
        pagina_foto = self.root.ids['mudarfoto']
        lista_fotos = pagina_foto.ids['fotos_perfil']
        for foto in arquivos:
            imagem = ImageButton(source=f'icones/fotos_perfil/{foto}', on_release= partial(self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(imagem)

        # carregar foto cliente
        arquivos = os.listdir("icones/fotos_clientes")
        adicionarvendas = self.root.ids["adicionarvendaspage"]
        lista_clientes = adicionarvendas.ids["lista_clientes"]
        for foto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_clientes/{foto}", on_release = partial(self.selecionar_clientes, foto))
            Label = LabelButton(text=foto.replace(".png","").capitalize(),  on_release = partial(self.selecionar_clientes, foto))
            lista_clientes.add_widget(imagem)
            lista_clientes.add_widget(Label)

        # carregar foto_produto
        arquivos = os.listdir("icones/fotos_produtos")
        lista_produto = adicionarvendas.ids["lista_produtos"]
        for foto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_produtos/{foto}", on_release = partial(self.selecionar_produtos, foto))
            Label = LabelButton(text=foto.replace(".png", "").capitalize(), on_release = partial(self.selecionar_produtos, foto))
            lista_produto.add_widget(imagem)
            lista_produto.add_widget(Label)

        # carregar data
        label_data = adicionarvendas.ids["label_data"]
        label_data.text = f"Data: {date.today().strftime('%d/%m/%Y')}"



        # pegar informações do usuário
        self.carregar_infos()

    def carregar_infos(self):
        try:
            with open("refreshToken.txt", "r") as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token
            self.mudar_tela("homepage")

        # pegar informações do usuário
            requisicao = requests.get(
                f"https://aplicativovendashash-2dc43-default-rtdb.firebaseio.com/{self.local_id}.json")
            requisicao_dic = requisicao.json()
            self.foto_perfil = requisicao_dic['avatar']
            # pegar foto de perfil
            avatar = requisicao_dic['avatar']
            foto_perfil = self.root.ids["foto_perfil"]
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        # prencher id unico
            id_vendedor = requisicao_dic['id_vendedor']
            pagina_ajustes = self.root.ids['ajustespage']
            pagina_ajustes.ids['id_vendedor'].text = f"Seu ID Único: {id_vendedor}"
            print(local_id)
        except:
            pass

        try:
        # prencher valor de venda
            total_vendas = requisicao_dic['total_vendas']
            homepage = self.root.ids['homepage']
            homepage.ids['label_total_vendas'].text = f"[color=#000000]Total de vendas:[/color] [b]R${total_vendas}[/b]"
        # preencher lista de vendas

            vendas = requisicao_dic['vendas']


            for id_venda in vendas:
                venda = vendas[id_venda]
                banner = BannerVenda(cliente=venda['cliente'], data=venda['data'], foto_cliente=venda['foto_cliente'],
                                     foto_produto=venda['foto_produto'],
                                     preco=venda['preco'], produto=venda['produto'], quantidade=venda['quantidade'],
                                     unidade=venda['unidade'])
                pagina_homepage = self.root.ids['homepage']

                lista_vendas = pagina_homepage.ids["lista_vendas"]
                lista_vendas.add_widget(banner)
        except Exception as erro:
            print(erro)
            pass
        try:
            equipe = requisicao_dic['equipe:']
            lista_equipe = equipe.split(',')
            pagina_listavendedores = self.root.ids["listarvendedorespage"]
            lista_vendedores = pagina_listavendedores.ids["lista"]

            for id_vendedor_equipe in lista_equipe:
                if id_vendedor_equipe != "":
                    try:
                        banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_equipe)
                        lista_vendedores.add_widget(banner_vendedor)
                    except:
                        pass
        except:
            pass



    def mudar_foto_perfil(self, foto, *args):
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{foto}"
        info =f'{{"avatar": "{foto}"}}'
        requisicao = requests.patch(f"https://aplicativovendashash-2dc43-default-rtdb.firebaseio.com/{self.local_id}.json",
                                  data=info)

        self.mudar_tela('ajustespage')

    def selecionar_clientes(self, foto, *args):
        self.cliente = foto.replace(".png","")
        adicionarvendas = self.root.ids["adicionarvendaspage"]
        lista_clientes = adicionarvendas.ids["lista_clientes"]
        for item in list(lista_clientes.children):
            item.color = (1,1,1,1)
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0,207/255,219/255,1)
            except:
                pass
    def selecionar_produtos(self, foto, *args):
        self.produto = foto.replace(".png", "")
        adicionarvendas = self.root.ids["adicionarvendaspage"]
        lista_clientes = adicionarvendas.ids["lista_produtos"]
        for item in list(lista_clientes.children):
            item.color = (1,1,1,1)
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0,207/255,219/255,1)
            except:
                pass
    def selecionar_unidade(self, id , *args):
        self.unidade = id.replace("unidades_","")
        adicionarvendas = self.root.ids["adicionarvendaspage"]
        adicionarvendas.ids["unidades_kg"].color = (1, 1, 1, 1)
        adicionarvendas.ids["unidades_unidades"].color = (1, 1, 1, 1)
        adicionarvendas.ids["unidades_litros"].color = (1, 1, 1, 1)
        adicionarvendas.ids[id].color = (0,207/255,219/255,1)

    def adicionar_venda(self):
        cliente = self.cliente
        produto = self.produto
        unidade = self.unidade
        adicionarvendas = self.root.ids["adicionarvendaspage"]
        data = adicionarvendas.ids['label_data'].text.replace("Data: ", "")
        preco = adicionarvendas.ids["preco_total"].text
        quantidade = adicionarvendas.ids["quantidade_total"].text

        if not cliente:
            adicionarvendas.ids["selecione_cliente"].color = (1,0,0,1)
        if not produto:
            adicionarvendas.ids["selecione_produto"].color = (1,0,0,1)
        if not unidade:
            adicionarvendas.ids["unidades_kg"].color = (1,0,0,1)
            adicionarvendas.ids["unidades_unidades"].color = (1,0,0,1)
            adicionarvendas.ids["unidades_litros"].color = (1,0,0,1)
        if not preco:
            adicionarvendas.ids["label_preco"].color = (1,0,0,1)
        else:
            try:
                preco = float(preco)
            except:
                adicionarvendas.ids["label_preco"].color = (1,0,0,1)
        if not quantidade:
            adicionarvendas.ids["label_quantidade"].color = (1,0,0,1)
        else:
            try:
                quantidade = float(quantidade)
            except:
                adicionarvendas.ids["label_quantidade"].color = (1,0,0,1)
        try:
            if cliente and produto and unidade and preco and quantidade and (type(preco) == float) and (type(quantidade) == float):
                foto_produto = produto + ".png"
                foto_cliente = cliente + ".png"

                info = f'{{"cliente": "{cliente}", "produto": "{produto}", "foto_cliente": "{foto_cliente}", "foto_produto":"{foto_produto}",' \
                       f'"data": "{data}", "unidade": "{unidade}", "preco": "{preco}", "quantidade": "{quantidade}"}}'
                requests.post(f"https://aplicativovendashash-2dc43-default-rtdb.firebaseio.com/{self.local_id}/vendas.json", data=info)
        except:
            pass
        self.cliente = None
        self.produto = None
        self.unidade = None

        banner = BannerVenda(cliente=cliente, data=data, foto_cliente= foto_cliente, foto_produto = foto_produto, preco=preco, produto=produto, quantidade=quantidade, unidade=unidade)
        pagina_homepage = self.root.ids['homepage']
        lista_vendas = pagina_homepage.ids["lista_vendas"]
        lista_vendas.add_widget(banner)
        requisicao = requests.get(f'https://aplicativovendashash-2dc43-default-rtdb.firebaseio.com/{self.local_id}/total_vendas.json')
        total_vendas = float(requisicao.json())
        total_vendas += preco
        print(total_vendas)
        info = f'{{"total_vendas":"{total_vendas}"}}'
        requests.patch(f"https://aplicativovendashash-2dc43-default-rtdb.firebaseio.com/{self.local_id}.json", data = info)
        pagina_homepage.ids['label_total_vendas'].text = f"[color=#000000]Total de vendas:[/color] [b]R${total_vendas}[/b]"
        self.mudar_tela('homepage')

    def carregar_todas_as_vendas(self):
        pagina_homepage = self.root.ids['todasvendaspage']
        lista_vendas = pagina_homepage.ids["lista_vendas"]

        for item in list(lista_vendas.children):
            lista_vendas.remove_widget(item)
        # pegar informações da empresa
        requisicao = requests.get(
            f'https://aplicativovendashash-2dc43-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"')
        requisicao_dic = requisicao.json()
        print(requisicao_dic)

        # pegar foto de perfil
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/hash.png"

        total_vendas = 0
        for local_id_usuario in requisicao_dic:
            try:
                vendas = requisicao_dic[local_id_usuario]['vendas']

                for id_venda in vendas:
                    venda = vendas[id_venda]
                    total_vendas += float(venda['preco'])
                    banner = BannerVenda(cliente=venda['cliente'], data=venda['data'],
                                         foto_cliente=venda['foto_cliente'],
                                         foto_produto=venda['foto_produto'],
                                         preco=venda['preco'], produto=venda['produto'], quantidade=venda['quantidade'],
                                         unidade=venda['unidade'])
                    lista_vendas.add_widget(banner)


                pagina_homepage.ids[
                    'label_total_vendas'].text = f"[color=#000000]Total de vendas:[/color] [b]R${total_vendas}[/b]"

            except Exception as err:
                print(err)
                pass

        self.mudar_tela("todasvendaspage")

    def sair_todas_as_vendas(self):
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{self.foto_perfil}"
        self.mudar_tela("homepage")

    def carregar_vendas_vendedores(self, id_vendedor, *args):
        pagina_vendas = self.root.ids['outrosvendedorespage']
        lista_vendas = pagina_vendas.ids['lista_vendas']
        vendas = id_vendedor['vendas']
        for item in list(lista_vendas.children):
            lista_vendas.remove_widget(item)
        print(id_vendedor)
        total_vendas = id_vendedor['total_vendas']
        for id_venda in vendas:
            venda = vendas[id_venda]
            banner = BannerVenda(cliente=venda['cliente'], data=venda['data'],
                                 foto_cliente=venda['foto_cliente'],
                                 foto_produto=venda['foto_produto'],
                                 preco=venda['preco'], produto=venda['produto'], quantidade=venda['quantidade'],
                                 unidade=venda['unidade'])
            lista_vendas.add_widget(banner)

        pagina_vendas.ids[
            'label_total_vendas'].text = f"[color=#000000]Total de vendas:[/color] [b]R${total_vendas}[/b]"

        # pegar foto de perfil
        foto_perfil = self.root.ids["foto_perfil"]
        perfil = id_vendedor['avatar']
        foto_perfil.source = f"icones/fotos_perfil/{perfil}"

        self.mudar_tela("outrosvendedorespage")

MainApp().run()