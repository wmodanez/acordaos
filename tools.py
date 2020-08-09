import re


# Transforma o texto em string; letras maiúsculas; remove espaços nas laterais da strig
def padronizaTexto(texto):
    return str(texto.upper().strip())


# Função que gera a chave para os acordãos, criada para ser aplicada na coluna "Título" do dataset positivo
def criaChaveAcordao(texto):
    # Atribui valor inicil para a variável indicadors do tipo da sessão
    tipoSessao = 'PL'

    # Aplica função de padronizar o dado de entrada
    texto = padronizaTexto(texto)

    # Extraindo os valores para variável tipoDecisao:
    if len(re.findall('AC[O|Ó]RD[Ã|A]O\s[A-Z]', texto)) > 0:
        tipoDecisao = 'AR'
    elif len(re.findall('DECIS[Ã|A]O', texto)) > 0:
        tipoDecisao = 'DE'
    else:
        tipoDecisao = 'AC'

    # Extraindo os valores para as variáveis nrAcordao e ano:
    ## Procura no texto todos os números e gera uma lista
    anoAcordao = re.findall("[0-9]+", texto)

    if len(anoAcordao[1]) < 4:
        if int(anoAcordao[1]) <= 30:
            anoAcordao[1] = '20' + anoAcordao[1]
        else:
            anoAcordao[1] = '19' + anoAcordao[1]

    # Extraindo os valores para variável tipoSessao:

    ### Atribui valores à variável de acordo com o tipo de sessão. Caso seja PLENÁRIO, a variável tiposessão recebe valor "PL";
    ### caso seja PRIMEIRA CÂMARA, a variável tiposessão recebe valor "1C";
    ### caso seja SEGUNDA CÂMARA, a variável tiposessão recebe valor "2C"
    if (len(re.findall('PLEN[Á|A]RIO', texto)) == 0):
        if (len(re.findall('PRIMEIRA', texto)) != 0):
            tipoSessao = '1C'
        elif (len(re.findall('SEGUNDA', texto)) > 0):
            tipoSessao = '2C'

    return tipoDecisao + '-' + anoAcordao[0].zfill(6) + '-' + anoAcordao[1] + '-' + tipoSessao
