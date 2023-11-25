import json
import re
import os
caminhoRegistro = 'registroUsuario.json'


def register():
    try:
   
        with open(caminhoRegistro, 'r') as f:
            user_info_array = json.load(f)

    # Se um dos seguintes erros ocorrer, execute o bloco dentro de 'except'
    except (FileNotFoundError, json.JSONDecodeError) as e:
    # Se o arquivo não for encontrado (FileNotFoundError) 
    # ou se o arquivo JSON for inválido (JSONDecodeError),
    # inicialize user_info como um dicionário vazio.
        print(f"criando...")
        user_info_array = []
  

    usuario = input('Qual é o seu nome de usuário?')

        


    senha = input('Qual é a sua senha?')
    email = input('Qual é o seu email?')
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if re.search(padrao,email):

        user_info = {}

        user_info[f'{usuario}'] = {
                'nome':usuario,
                'senha':senha,
                'email':email
            }


        user_info_array.append(user_info)
                        


        with open(caminhoRegistro,'w') as f:
            json.dump(user_info_array,f)
                            
            print('Registrado com sucesso!')
                        
    else:
        print('Email inválido')

    


def login():
    try:
        if not os.path.exists(caminhoRegistro):
            print('Arquivo de registro não encontrado.')
    
            

        
        nomeLogin = input('Qual é o seu nome login?')
        senhaLogin = input('qual é a sua senha?')
        

        Acesso = False

        with open(caminhoRegistro,'r') as f:
            userJson = json.load(f)

        try:
            with open(caminhoRegistro, 'r') as f:
                userJson = json.load(f)

            usuarioEncontrado = False

            for usuario in userJson:
                if nomeLogin in usuario:
                    usuarioEncontrado = True
                    if usuario[nomeLogin]['senha'] == senhaLogin:
                        with open("usuarioLogado.txt", 'w') as f:
                            json.dump(nomeLogin, f)
                        print("-"*20)
                        print(f'\nAcesso liberado, Bem-vindo {nomeLogin}!')
                        print("-"*20)
                        return True
                    else:
                        print('\nUsuário ou senha incorretos')
                        return False

            if not usuarioEncontrado:
                print('\nUsuário inexistente')

        except FileNotFoundError:
            print('Arquivo de registro não encontrado')

        return False
    
    except ( json.JSONDecodeError):
        print('Não há registro de usuários na aplicação ou houve um erro!')