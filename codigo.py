import pydf
import smtplib
import ssl
import email.message
from datetime import date, datetime
import os
import xml.etree.ElementTree as ET
import psycopg2

diacadastro = date.today().day
mescadastro = date.today().month
anocadastro = date.today().year
horacadastro = datetime.now().hour
minutocadastro = datetime.now().minute
segundoscadastro = datetime.now().second

#arquivos pdf
def pdfpadrao():
    pdf = pydf.generate_pdf(f'<h1>{nomecompleto}</h1><h2>Contato:</h2><br>Email: {emailpaciente}</br><br>Tel: {telefone} '
    f'<h2>Dados:</h2><br>RG: {rg}</br><br>Data nascimento: {dianascimento}/{mesnasimento}/{anonascimento} ({calculoidade} anos)</br>'
    f'<h2>Sintomas: </h2><br>{sintomas}</br>'
    f'<p><b>Cadastro realizado em: {diacadastro}/{mescadastro}/{anocadastro}')
    with open(f'{nomedopdf}.pdf', 'wb') as f:
        f.write(pdf)


def pdfgrupoderisco():
    pdf = pydf.generate_pdf(f'<h1>{nomecompleto}(Em grupo de risco)</h1><h2>Contato:</h2><br>Email: {emailpaciente}</br><br>Tel: {telefone} '
    f'<h2>Dados:</h2><br>RG: {rg}</br><br>Data nascimento: {dianascimento}/{mesnasimento}/{anonascimento} ({calculoidade} anos)</br>'
    f'<h2>Sintomas: </h2><br>{sintomas}</br>'
    f'<p><b>Cadastro realizado em: {diacadastro}/{mescadastro}/{anocadastro}')
    with open(f'{nomedopdf}.pdf', 'wb') as f:
        f.write(pdf)


#email 
def enviaremail():
    msg = email.message.Message()
    msg['Subject'] = ("Clinica Saúde")


    body = f"""
    <p>Olá {nomecompleto}</p>
    
    <p>Sua consulta foi agendada, seus dados foram salvos, por favor confirme seus dados e informacoes</p>
    <p><br><b>Dados:</b></br> Telefone: {telefone}, <b>RG:</b> {rg}, <b>Data de nascimento:</b> {dianascimento}/{mesnasimento}/{anonascimento}, {calculoidade} anos
    
    <p><br><b>Sintomas:</b> {sintomas}</br></p>
    <p>Caso aja alguma divergencia contatar a clinica</p>
    
    <p>Atenciosamente, Recepção</p>
    """

    #por seugranca e privacidade retirei o email e a senha que usei do codigo. 
    msg['From'] = '' #digitar o email entre aspas
    password = '' #digitar senha do email entre aspas
    msg['To'] = emailpaciente
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(body)

    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587) as conexao:
        conexao.ehlo()
        conexao.starttls(context=context)
        conexao.login(msg['From'], password)
        conexao.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))
    

def salvardados():

    dadosparaarquivo = f""" \n"{nomecompleto}","{emailpaciente}",{telefone},"{dianascimento}/{mesnasimento}/{anonascimento}","{risco}",{rg}"""
    with open('./dados.csv', 'a') as arquivo:
        arquivo.write(dadosparaarquivo)

def banco_de_dados():
    tree = ET.parse('informacoespaciente.xml')
    root = tree.getroot()
    
    pacientes = []
    for paciente in root.iter('paciente'):
        nome2 = paciente.find('nome').text
        email2 = paciente.find('email').text
        telefone2 = paciente.find('telefone').text
        rg2 = paciente.find('rg').text
        datanascimento2 = paciente.find('aniverssario').text
        pacientes.append((nome2, email2, telefone2, rg2, datanascimento2))
    
    conexao = psycopg2.connect(
        host = 'localhost',
        database = '',#digitar nome da database entre aspas
        user = '',#digitar usuario do pgadmin entre aspas
        password = ''#digitar senha do pgadmin entre aspas
    )

    cursor = conexao.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pacientes(
    nome VARCHAR(60),
    email VARCHAR(60),
    telefone VARCHAR(60),
    rg VARCHAR(60),
    aniverssario VARCHAR(60)
    )
    ''')

    for paciente in pacientes:
        cursor.execute(
            'INSERT INTO pacientes (nome, email, telefone, rg, aniverssario) VALUES (%s, %s, %s, %s, %s)',
            paciente
        )

    conexao.commit()
    cursor.close()
    conexao.close()


#dados
while True:
    print('-'*60)
    sintomas = input("digite os sintomas: ")
    nomecompleto = input("Digite o nome completo: ")
    emailpaciente = input("Digite o email: ")
    telefone = input("Digite o telefone: ")
    rg = input("Digite o RG: ")

    print('Data de nascimento: ')
    dianascimento = input('Dia: ')
    if not dianascimento.isnumeric():
        print('Data invalida, digite novamente')
        continue
    dianascimento = int(dianascimento)
    if dianascimento < 1 or dianascimento >= 32:
        print('Data invalida, digite novamente')
        continue
    
    mesnasimento = input('Mes: ')
    if not mesnasimento.isnumeric():
        print('Mes invalido digite apenas numeros')
        continue
    mesnasimento = int(mesnasimento)
    if mesnasimento < 1 or mesnasimento > 12:
        print('Mes invalido, digite novamente')
        continue
    
    anonascimento = input("Ano: ")
    if not anonascimento.isnumeric():
        print('Ano invalido, digite apenas numeros')
        continue
    anonascimento = int(anonascimento)
    if anonascimento > date.today().year:
        print('Ano invalido, digite novamente')
        continue
    
    calculoidade = date.today().year - int(anonascimento)
    nomedopdf = input("Digite um nome para o arquivo pdf: ")

    risco = ''
    if calculoidade < 65:
        risco ='nao'
    elif calculoidade > 65:
        risco = 'sim'

    if calculoidade < 65:
        pdfpadrao()
    elif calculoidade > 65:
        pdfgrupoderisco()
    else:
        print()
    
    dataformatada = (f'{dianascimento}/{mesnasimento}/{anonascimento}')
    informacoes = {}
    informacoes['nome'] = nomecompleto
    informacoes['emailpaciente'] = emailpaciente
    informacoes['telefone'] = telefone
    informacoes['rg'] = rg
    informacoes['aniverssario'] = dataformatada

    arquivo_xml = 'informacoespaciente.xml'
    if os.path.exists(arquivo_xml):
        os.remove(arquivo_xml)
    if os.path.isfile(arquivo_xml):
        tree = ET.parse(arquivo_xml)
        raiz = tree.getroot()
    else:
        raiz = ET.Element('informacoes')
        tree = ET.ElementTree(raiz)
    
    novo_elemento = ET.Element('paciente')
    raiz.insert(0, novo_elemento)
    novo_elemento.tail = '\n'
    nome1 = ET.Element('nome')
    nome1.text = informacoes['nome']
    nome1.tail = '\n'
    novo_elemento.append(nome1)
    email1 = ET.Element('email')
    email1.text = informacoes['emailpaciente']
    email1.tail = '\n'
    novo_elemento.append(email1)
    telefone1 = ET.Element('telefone')
    telefone1.text = informacoes['telefone']
    telefone1.tail = '\n'
    novo_elemento.append(telefone1)
    rg1 = ET.Element('rg')
    rg1.text = informacoes['rg']
    rg1.tail = '\n'
    novo_elemento.append(rg1)
    aniverssario1 = ET.Element('aniverssario')
    aniverssario1.text = informacoes['aniverssario']
    aniverssario1.tail = '\n'
    novo_elemento.append(aniverssario1)
    raiz.tail = '\n'
    novo_elemento.tail = '\n'
    tree.write(arquivo_xml)


    banco_de_dados()
    
    print('cadastrando, aguarde')

    enviaremail()

    salvardados()

    print("Cadastrado com sucesso.")
    continuar = input("Deseja cadastrar outro paciente? sim/nao: ")
    if continuar in ["nao"]:
        break
    if continuar in ["sim"]:
        pass
    else:
        print("Opcao invalida, tente novamente")
        break
