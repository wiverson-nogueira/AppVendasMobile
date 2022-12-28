import requests
from kivy.app import App


class MyFirebase():
    API_KEY = 'AIzaSyAgppd7zgmQE33HTsw9omAahy_8wU0m5JU'

    def criar_conta(self, email, senha):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}'
        info = {'email': email,
                'password': senha,
                'returnSecureToken': True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        if requisicao.ok:
            # Token que mantém o usuário logado
            refresh_token = requisicao_dic['refreshToken']
            # ID Usuário
            local_id = requisicao_dic['localId']
            # Autenticação
            id_token = requisicao_dic['idToken']

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open('refreshtoken.txt', 'w') as arquivo:
                arquivo.write(refresh_token)

            req_id = requests.get(f'https://aplicativovendashash-e68d3-default-rtdb.firebaseio.com/proximo_id_vendedor.json?auth={id_token}')
            id_vendedor = req_id.json()

            link = f'https://aplicativovendashash-e68d3-default-rtdb.firebaseio.com/{local_id}.json?auth={id_token}'
            info_usuario = f'{{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": "", "id_vendedor": "{id_vendedor}"}}'
            requisicao_usuario = requests.patch(link, data=info_usuario)

            # Atualizar o valor do proximo_id_vendedor
            proximo_id_vendedor = int(id_vendedor) + 1
            inf_id_vendedor = f'{{"proximo_id_vendedor": "{proximo_id_vendedor}"}}'
            requests.patch(f'https://aplicativovendashash-e68d3-default-rtdb.firebaseio.com/.json?auth={id_token}', data=inf_id_vendedor)

            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.mudar_tela('homepage')

        else:
            mensagem_erro = requisicao_dic['error']['message']
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids['loginpage']
            pagina_login.ids['mensagem_login'].text = mensagem_erro
            pagina_login.ids['mensagem_login'].color = (1, 0, 0, 1)


    def fazer_login(self, email, senha):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}'
        info = {'email': email,
                'password': senha,
                'returnSecureToken': True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        if requisicao.ok:
            # Token que mantém o usuário logado
            refresh_token = requisicao_dic['refreshToken']
            # ID Usuário
            local_id = requisicao_dic['localId']
            # Autenticação
            id_token = requisicao_dic['idToken']

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open('refreshtoken.txt', 'w') as arquivo:
                arquivo.write(refresh_token)

            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.mudar_tela('homepage')

        else:
            mensagem_erro = requisicao_dic['error']['message']
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids['loginpage']
            pagina_login.ids['mensagem_login'].text = mensagem_erro
            pagina_login.ids['mensagem_login'].color = (1, 0, 0, 1)
        pass

    def trocar_token(self, refresh_token):
        link = f'https://securetoken.googleapis.com/v1/token?key={self.API_KEY}'
        info = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        local_id = requisicao_dic['user_id']
        id_token = requisicao_dic['id_token']
        return local_id, id_token