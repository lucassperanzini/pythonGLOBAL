import json 
import re
import requests
import fusoHorario
import CadastroLogin






caminhoRegistro = 'registroUsuario.json'

def validar_numero(mensagem):
    while True:
        entrada = input(mensagem)
        if re.match(r"^\d+$", entrada):
            return int(entrada)
        else:
            print("Por favor, digite apenas números.")
def DadosPessoais():
    try:
        with open("usuarioLogado.txt",'r') as f:
            usuarioLogou = f.read().strip().replace('"', '')

        with open(caminhoRegistro, "r") as f:
            usuarios = json.load(f)

        for usuario in usuarios:
                if usuarioLogou in usuario:
                    if "infoPessoais" in usuario[usuarioLogou]:
                        print("Informações pessoais já registradas.")
                        return
        1
        
        try:
            
            idade = validar_numero("\n\nQuantos anos você tem? ")
            if not (0 <= idade <= 120):
                print("Idade inválida. A idade deve estar entre 0 e 120 anos.")
            else:
                altura = validar_numero("Qual é sua altura em cm? ")
                peso = validar_numero("Qual é seu peso? ")

            

        except ValueError:
            print("O valor inserido não é válido.")

        condicao_medica = print("""
    Por favor, selecione sua condição médica (com exemplos):
    [1] Diabetes (ex: Tipo 1, Tipo 2)
    [2] Hipertensão (ex: Primária, Secundária)
    [3] Doenças Infecciosas (ex: COVID-19, Tuberculose)
    [4] Doenças Renais (ex: Doença Renal Crônica, Nefrite)
    [5] Doenças do Coração (ex: Insuficiência Cardíaca, Arritmia)
    [6] Nenhuma das opções anteriores
    """)
    
        opcao = int(input("Digite o número correspondente à sua condição médica: "))

        if opcao == 1:
            condicao_medica = "Diabetes"
        elif opcao == 2:
            condicao_medica = "Hipertensao"
        elif opcao == 3:
            condicao_medica = "Doenças Infecciosas"
        elif opcao == 4:
            condicao_medica = "Doenças Renais"
        elif opcao == 5:
            condicao_medica = "Doenças do coração"
        elif opcao == 6:
            condicao_medica = ""
        else:
            print("Opção inválida. Por favor, selecione um número entre 1 e 6.")
        


        informaçõesPessoais = {
                "idade":idade,
                "altura":altura,
                "peso":peso,
                "condicao": condicao_medica
            }
        


        

    
        for usuario in usuarios:
            if usuarioLogou in usuario:
                usuario[usuarioLogou]["infoPessoais"] = informaçõesPessoais
                break


        with open(caminhoRegistro, "w") as f:
            json.dump(usuarios, f)
        print("Informações pessoais atualizadas com sucesso.")


    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")




def DadosSensor():
        
    url = "http://46.17.108.113:8666/STH/v1/contextEntities/type/iot/id/urn:ngsi-ld:Flooence/attributes/distancia?lastN=15"

    payload = {}
    headers = {
    'fiware-service': 'smart',
    'fiware-servicepath': '/'
    }

    response = requests.get(url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()  # Obter os dados JSON da resposta

    else: 
        print(f'Erro ao receber os dados. Código de status: {response.status_code}')

    

    return data
       

                
        

def PorcentagemAguaIngerida():
    #o sensor muitas vezes registra mais de uma vez o mesmo valor, então so vai aparecer valores diferentes
    SetMLingeridos = set()

    with open("usuarioLogado.txt",'r') as f:
        usuarioLogou = f.read().strip().replace('"', '')

    with open(caminhoRegistro, "r") as f:
        usuarios = json.load(f)


    for usuario in usuarios:
        if usuarioLogou in usuario:
            info = usuario[usuarioLogou]['infoPessoais']
            break


    QuantidadeAguaNecessaria =  info['peso'] * 35
   



    data = DadosSensor()
    
    with open("dadosHistoricos.json","r") as arquivo_json:
        for contextResponse in data["contextResponses"]:
            contextElement = contextResponse["contextElement"]
            for attribute in contextElement["attributes"]:
                for value in attribute['values']:
                    if value['attrValue'] == 0:
                        continue
                    SetMLingeridos.add(value['attrValue'])
                    quantidadeIngerida = sum(SetMLingeridos)
    
    


    porcentagemIngerida = (quantidadeIngerida / QuantidadeAguaNecessaria) * 100
    
    print(f"""\n\n 
        {'-'*40}

        condicao: {info['condicao']}

        Quantidade de água necessária : {QuantidadeAguaNecessaria}ml

        {'-'*40}


        quantidade ingerida : {quantidadeIngerida}ml
        

        {'-'*40}

        Voce completou {round(porcentagemIngerida,2)}% da sua meta!

        {'-'*40}



""")
    
def historicoDados():

    print('\n\nHISTÓRICO DE CONSUMO DE ÁGUA\n')
    print("{:<10} {:<15} {:<10}".format("Dia", "Horário", "Quantidade (ml)\n"))
    data = DadosSensor()

    for contextResponse in data["contextResponses"]:
        contextElement = contextResponse["contextElement"]
        for attribute in contextElement["attributes"]:
            for value in attribute['values']:
                if value['attrValue'] == 0:
                    continue

                DataHorarioEuropa = value['recvTime'][:19]
                fuso_horario_original = 'Europe/Madrid'
                fuso_horario_destino = 'America/Sao_Paulo'
                

                data_hora_brasil = fusoHorario.converter_fuso_horario(DataHorarioEuropa,fuso_horario_original, fuso_horario_destino)

                dataBrasil = data_hora_brasil[:10]

                horarioBrasil = data_hora_brasil[11:16]

                 
             
                print("-" * 40)
                print(f"{value['attrValue']}ml          {horarioBrasil}           {dataBrasil}")



    

        

    







def aplicacao():
    print ("\n" * 80) 
  

    print("""


Bem vindo ao Fluence!
      
___________.__                                     
\_   _____/|  |  __ __   ____   ____   ____  ____  
 |    __)  |  | |  |  \_/ __ \ /    \_/ ___\/ __ \ 
 |     \   |  |_|  |  /\  ___/|   |  \  \__\  ___/ 
 \___  /   |____/____/  \___  >___|  /\___  >___  >
     \/                     \/     \/     \/    \/ 
                                                                                                            
                                                                                                                               



""")
    while True:
        print("\n\n1: Registrar")
        print("2: Login")
        print("3: Sair")
        escolha = int(input("Escolha uma opção: "))
        
        if escolha == 1:
            CadastroLogin.register()
            
        elif escolha == 2:
            userLogou = CadastroLogin.login()
            if userLogou:
                DadosPessoais()

                while True:

                    print("\n\n1: Histórico de hidratação")
                    print("2: Porcentagem de água ingerida da meta diária")
                    print("3: Logout")
                    print("4: Sair")
                    
                    task_choice = int(input("Escolha uma opção: "))
                
                    if task_choice == 1:
                        historicoDados()

                    elif task_choice == 2:
                        PorcentagemAguaIngerida()
                    elif task_choice ==3:
                        print('Fazendo logout....') 
                        aplicacao() 
                       
                    elif task_choice == 4:
                        exit()
                    else:
                        print('Não existe essa opção')


        elif escolha == "3":
            print("Saindo do sistema. Até mais!")
            exit()
        else:
            print("Opção inválida")
            

aplicacao()