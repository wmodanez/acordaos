import re

import pandas as pd

from datetime import datetime


'''
    Transforma o texto em string; letras maiúsculas; remove espaços nas laterais da string
'''


def padronizaTexto(texto):
    return str(texto.upper().strip())


'''
    Função que gera a chave para os acordãos, utilizando a coluna 'TITULO' do dataset positivo ou a coluna 'ACORDAO' do 
    dataset negativo
'''


def criaChaveAcordao(texto):
    # Aplica função de padronizar o dado de entrada
    texto = padronizaTexto(texto)

    # Extraindo os valores para variável tipoDecisao:
    tipoDecisao = extrairTipoDecisao(texto)

    # Extraindo os valores para as variáveis nrAcordao e ano:
    ## Procura no texto todos os números e retorna uma lista
    anoAcordao = extrairAnoAcordao(texto)

    # Extraindo os valores para variável tipoSessao:
    tipoSessao = extrairTipoSessao(texto)

    return tipoDecisao + '-' + anoAcordao[0].zfill(6) + '-' + anoAcordao[1] + '-' + tipoSessao


'''
    Função que gera a chave para os acordãos, utilizando uma linha do dataset principal
'''


def criaChaveAcordaoPrincipal(row):
    # Extraindo os valores para variável tipoDecisao:
    tipoDecisao = extrairTipoDecisao(padronizaTexto(row.URN))

    # Extraindo os valores para variável tipoSessao:
    tipoSessao = extrairTipoSessao(padronizaTexto(row.NUMERO_ATA))

    return tipoDecisao + '-' + row.NUMERO_ACORDAO.zfill(6) + '-' + row.ANO_ACORDAO + '-' + tipoSessao


'''
    Função que extrai o número do acordao e o ano, retornando uma lista
'''


def extrairAnoAcordao(texto):
    anoAcordao = re.findall("[0-9]+", texto)
    if len(anoAcordao[1]) < 4:
        if int(anoAcordao[1]) <= 30:
            anoAcordao[1] = '20' + anoAcordao[1]
        else:
            anoAcordao[1] = '19' + anoAcordao[1]
    return anoAcordao


'''
    Atribui valores à variável de acordo com o tipo de sessão:
    'PL' para PLENÁRIO; -> Valor padrão
    '1C' para PRIMEIRA CÂMARA;
    '2C' para SEGUNDA CÂMARA.
'''


def extrairTipoSessao(texto):
    if len(re.findall('PRIMEIRA', texto)) != 0:
        return '1C'
    elif len(re.findall('SEGUNDA', texto)) > 0:
        return '2C'
    else:
        return 'PL'

'''
    Atribui valores à variável de acordo com o tipo de decisão: 
    'AC' para ACÓRDÃO; -> Valor padrão 
    'AR' para ACÓRDÃO;
    'DE' para DECISÃO
'''


def extrairTipoDecisao(texto):
    if len(re.findall('RELA[Ç|C][Ã|A]O', texto)) > 0:
        return 'AR'
    elif len(re.findall('DECIS[Ã|A]O', texto)) > 0:
        return 'DE'
    else:
        return 'AC'

    
def read_file(file, separator, encoding):
    start_time = datetime.now()
    df = pd.read_csv(file, sep=separator, encoding=encoding)
    print('Duration: {}'.format(datetime.now() - start_time))
    return df