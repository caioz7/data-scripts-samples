import csv
import names
from rstr import rstr
from string import digits
import datetime
import re
from random import randint
from faker import Faker
fake = Faker()
 
''' Gera um arquivo csv contendo os campos 
"cpf, matricula, sobrenome, nome, email, data de ingresso" 
'''
 
def get_matricula(data_ingresso):
    try:
        return '{}{}'.format(datetime.datetime.strptime(
            data_ingresso, "%Y-%m-%d").strftime("%Y"), rstr(digits, 5))
    except:
        return '{}{}'.format(datetime.datetime.now().strftime("%Y"), rstr(digits, 5))
 
def get_cpf():
    ''' retorna string de CPF não verificado'''
    while True:
        return '{}.{}.{}-{}'.format(
            rstr(digits, 3),
            rstr(digits, 3),
            rstr(digits, 3),
            rstr(digits, 2),
        )
 
def gen_nome_completo():
    '''retorna string com nome, sobrenome'''
    while True:
        yield (names.get_full_name())
 
def gen_email(nomecompleto, dominio='incolume.com.br'):
    '''recebe nome completo e dominio, retorna email'''
    try:
        return '{}.{}@{}'.format(*(nomecompleto.lower().split()), dominio)
    except:
        return None
 
def gen_data_ingresso():
    data_random=fake.date_between(start_date='-15y', end_date='now').strftime('%Y-%m-%d')
    return data_random

    # ''':return data'''
    # seconds = int('{}{}'.format(
    #     randint(12, 14),
    #     rstr(digits, 8)
    # ))
    # return ctime(seconds)
 
 
def gen_massa(qlinhas, cvsname):
    '''cria cvsname com a quantidade de linhas informadas em qlinhas '''
    try:
        header = "cpf, matricula, sobrenome, nome, email, data de ingresso"
        with open(cvsname, 'w') as file:
            csvhandler = csv.writer(file)
            csvhandler.writerow(header.split(', '))
            for i in range(qlinhas):
                nome = gen_nome_completo()
                person = next(nome)
                date = gen_data_ingresso()
                linha = '{}, {}, {c[1]}, {c[0]}, {}, {}'.format(
                    get_cpf(),
                    get_matricula(date),
                    gen_email(nomecompleto=person),
                    date,
                    c = person.split(),
                    )
                csvhandler.writerow(linha.split(','))
        return True
    except:
        raise
 
 
if __name__ == '__main__':
    QUANT_REGISTROS=100

    print(gen_massa(QUANT_REGISTROS, '/home/<USUARIO>/datasets/dados_gerados.csv'))
