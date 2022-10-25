import pydf
import smtplib
import ssl
import email.message
from datetime import date, datetime

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
    if calculoidade < 65:
        dadosparaarquivo = f"""

        
        Nome: {nomecompleto}
        Email: {emailpaciente}
        Telefone: {telefone}
        RG: {rg}
        Data de Nascimento: {dianascimento}/{mesnasimento}/{anonascimento} ({calculoidade} anos)
        Cadastro realizado em: {diacadastro}/{mescadastro}/{anocadastro} sessao iniciada as: {horacadastro}:{minutocadastro}:{segundoscadastro}
        """
        with open('./dados.txt', 'a') as arquivo:
            arquivo.write(dadosparaarquivo)
    elif calculoidade > 65:
        dadosparaarquivo = f"""

        
        Nome: {nomecompleto} (Em grupo de risco)
        Email: {emailpaciente}
        Telefone: {telefone}
        RG: {rg}
        Data de Nascimento: {dianascimento}/{mesnasimento}/{anonascimento} ({calculoidade} anos)
        Cadastro realizado em: {diacadastro}/{mescadastro}/{anocadastro} sessao iniciada as: {horacadastro}:{minutocadastro}:{segundoscadastro}
        """
        with open('./dados.txt', 'a') as arquivo:
            arquivo.write(dadosparaarquivo)


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
    mesnasimento = input('Mes: ')
    anonascimento = input("Ano: ")
    calculoidade = date.today().year - int(anonascimento)
    nomedopdf = input("Digite um nome para o arquivo pdf: ")

    if calculoidade < 65:
        pdfpadrao()
    elif calculoidade > 65:
        pdfgrupoderisco()
    else:
        print()
    
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
