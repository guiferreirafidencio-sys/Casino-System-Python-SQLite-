import sqlite3


def apresentação():
    print('Seja bem vindo Club cass')
    print('Possui Cadastro?? \n1- Posssuo login \n2- Desejo fazer Cadastro')
    resposta = int(input('-'))
    return resposta



def colocar_no_Banco(user, senha, idade):
    conexão = sqlite3.connect('banco.db')
    cursor = conexão.cursor()

    try:
       
        cursor.execute("SELECT * FROM Contas WHERE user = ?", (user,))
        existe = cursor.fetchone()

        if existe:
            print("Usuário já existe!")
            return

        
        cursor.execute("""
            INSERT INTO Contas (user, senha, idade, saldo)
            VALUES (?, ?, ?, ?)
        """, (user, senha, idade, 1000))

        conexão.commit()
        return True

    except Exception as e:
        print("Erro:", e)

    finally:
        conexão.close()

def opcção_2():
    try:
        idade = int(input('digite usa idade - '))
    except ValueError:
        print('DIGITES APENAS NUMERO')

    if idade >= 18:
        usuario = input('digite seu nome de user -')
        senha  = input('digite sua senha -')
        colocar_no_Banco(usuario,senha,idade)



    else:
        print('Saia desse site imediatamente')
        

def verificação(senha, senha_sql):
    if  senha == senha_sql:
        print('Entrando sistema ')
        return True
    else:
       
        return False
    
def consultar_dados(user):
    conexão = sqlite3.connect('banco.db')
    cursor = conexão.cursor()
    try:
        cursor.execute('SELECT user,senha    FROM Contas WHERE user = ?', (user,))
        resultado = cursor.fetchone()
    except None:
        print('Usuario inesistente')

    print('Usuario existestante')
    conexão.close()
    return resultado

def opção_1():
    user = input('digite seu usuario - ')
    dados = consultar_dados(user)
    if dados and dados[0] == user:
        contador = 0 
        for x in range(3): 
            if contador > 0:
                print('senha errada digite novamnte')
            senha = input('digite sua senha -')
            info = verificação(senha,dados[1])
            contador += 1 
            if info :
                return user
                break

            



def fluxo_crud():
    reposta = apresentação()

    if reposta == 1:
        user = opção_1()
        if user: 
            return True, user
        return False, None

    elif reposta == 2:
        opcção_2()
        return False, None

    return False, None

