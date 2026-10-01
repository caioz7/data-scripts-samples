import argparse
import csv
import unicodedata

from faker import Faker

fake = Faker('pt_BR')

''' Gera um arquivo csv contendo os campos
"id_vendedor, matricula, sobrenome, nome, email, data_de_ingresso"
'''

CAMPOS = ['id_vendedor', 'matricula', 'sobrenome', 'nome', 'email', 'data_de_ingresso']


def sem_acento(texto):
    '''remove acentos e caracteres nao ASCII'''
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()


def gen_email(nome, sobrenome, dominio='incolume.com.br'):
    '''recebe nome, sobrenome e dominio, retorna email'''
    local = sem_acento(f'{nome}.{sobrenome}'.lower()).replace(' ', '')
    return f'{local}@{dominio}'


def gen_matricula(data_ingresso, usadas):
    '''ano de ingresso + 5 digitos, sem repetir valores ja usados'''
    while True:
        matricula = f'{data_ingresso.year}{fake.numerify("#####")}'
        if matricula not in usadas:
            usadas.add(matricula)
            return matricula


def gen_linha(id_vendedor, usadas, dominio='incolume.com.br'):
    nome = fake.first_name()
    sobrenome = fake.last_name()
    ingresso = fake.date_between(start_date='-15y', end_date='today')
    return {
        'id_vendedor': id_vendedor,
        'matricula': gen_matricula(ingresso, usadas),
        'sobrenome': sobrenome,
        'nome': nome,
        'email': gen_email(nome, sobrenome, dominio),
        'data_de_ingresso': ingresso.isoformat(),
    }


def gen_massa(qlinhas, csvname):
    '''cria csvname com a quantidade de linhas informadas em qlinhas'''
    usadas = set()
    with open(csvname, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=CAMPOS)
        writer.writeheader()
        for id_vendedor in range(1, qlinhas + 1):
            writer.writerow(gen_linha(id_vendedor, usadas))
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gera CSV de teste')
    parser.add_argument('-n', '--quantidade', type=int, default=100)
    parser.add_argument('-o', '--saida', default='dados_gerados.csv')
    parser.add_argument('--seed', type=int, help='torna a massa reproduzivel')
    args = parser.parse_args()

    if args.seed is not None:
        Faker.seed(args.seed)

    print(gen_massa(args.quantidade, args.saida))
