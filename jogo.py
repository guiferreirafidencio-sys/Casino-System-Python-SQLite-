import random
import sqlite3

objetos = ['🍓', '🍌', '🍋']

def girar():
    return [random.choice(objetos) for _ in range(3)]

def ganho(resultado, dinheiro):
    formatado = set(resultado)
    if len(formatado) == 1:
        return dinheiro * 0.75
    if len(formatado) == 2:
        return dinheiro * 0.25
    return -dinheiro

def mexer_banco(soma, user):
    with sqlite3.connect('banco.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
        UPDATE Contas
        SET saldo = saldo + ?
        WHERE user = ?
        ''', (soma, user))

def ver_saldo(nome):
    with sqlite3.connect('banco.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT saldo FROM Contas WHERE user = ?", (nome,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0