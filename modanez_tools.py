import re, os, glob

import pandas as pd

from datetime import datetime


# Variáveis criadas para buscar a regex correspondente o nome de cada uma
acordao = r'(?:[Aa]c[óo]rd[ãa]os?)'
alinea = r'(?:[Aa]l[ií]neas?)'
ano = r'((19\d\d|20[012]\d)|(?<=\/)(\d{2})(?!\/)(?!\d))'
artigo = r'(?:artigos?|\barts?\.?)'
barra = r'(?:\/)'
camara = r'(?:[cC][aâ]mara)'
caput = r'(?:[cC]aput)'
cef = r'(?:Caixa Econ[oô]mica Federal)'
combinado_com = r'(?:c\/c)'
constituicao = r'(?:\b[cC]\.?[fF]\.?\b|[cC]onstitui[cç][aã]o [fF]ederal|[cC]arta [mM]agna|[cC]arta [mM]agna (do)? ([bB]rasil|[bB]rasileira)\b)'
contrato = r'(?:\b[cC]ontrato\b)'
da = r'(?:da)?'
divisor = r'(?:[\/|-])'
data_full = r'(?:[0-9]{1,2}[\°|\º]?)'+divisor+'(?:[0-9]{2})'+divisor+'([0-9]{2,4})'# r'([0-9]{2})'+divisor+'([0-9]{2})'+divisor+'([0-9]{2,4})'
de = r'(?:de)?'
decreto = r'(?:[dD]ecreto)'
decisao = r'(?:[dD]ecis[aã]o)'
do = r'(?:do)?'
e = r'(?:e)?'
hifen = r'(?:-)*'
lei = r'(?:[Ll][Ee][Ii])'
decreto_lei = decreto + hifen + lei
espaco = r'(?:\s)*'
inciso = r'(?:incisos?|\bincs?.?\b)'
instrucao_normativa = r'(?:\bInstru[cç][aã]o Normativa\b)'
ldo = r'(?:[lL][dD][oO]|'+ lei + r'(?:[dD]iretrizes [oO]r[cç]ament[aá]rias))'
lei_complementar = lei + r'(?:[cC]omplementar)'
lei_licitacacao = lei + espaco + de + espaco + r'(?:[lL]icita[cç]([aã]o|[oõ]es))'
numero = r'(?:\bn[\°|\º])?'
numerais = r'([\d.]{1,})'
ordinais = r'(?:[\°|\º|\ª]?)'
paragrafo = r'(?:§ §|§§?|[pP]aragr[aá]fos?)'
plenario = r'(?:[pP]len[aá]rio)'
precedente = r'(?:[pP]recedente)'
paradigma = r'(?:[pP]aradigma)'
ponto = r'(?:\.)?'
portaria = r'(?:\b[pP]ortaria\b)'
regimento_interno = r'(?:[Rr]egimento [Ii]nterno)'
relacao = r'(?:[Rr]ela[cç][aã]o)'
romano = r'([MDCLXVI]+\b)'
r'\b([MDCLXVI]+)\b ?,? ?e? ?'
# Remove o ponto de leis, decretos etc
sem_ponto = r'(\d+)(?:\.)(\d+)(?=\/)'
sumula = r'(?:\b[sS][uú]mula\b)'
tcu = r'(?:\b[tT][cC][uU]|[tT]ribunal de [cC]ontas da [uU]nião\b)'
tcu_opt = r'(?:tcu)*'
todos = r'(?:todos)'
virgula = r'(?:,)?'
underscore = r'(?:_)'
unico = '(?:[úÚuU]nico)?'


# Definição dos padrões a serem buscados no texto e de como eles serão substituídos
pa_lei = re.compile(lei+espaco+numero+espaco+numerais+ordinais+divisor+ano, re.I)
re_lei = r'LEI_\1_\2'

pa_lei_datafull = re.compile(lei+espaco+numero+espaco+numerais+ordinais+virgula+espaco+de+espaco+data_full, re.I)
re_lei_datafull = r'LEI_\1_\2'

pa_decreto = re.compile(decreto+espaco+numerais+ordinais+divisor+ano, re.I)
re_decreto = r'DECRETO_\1_\2'

# pa_portaria
# re_portaria

pa_artigo = re.compile(artigo+espaco+numerais+ordinais)
re_artigo = r'ARTIGO_\1'

pa_paragrafo = re.compile(paragrafo+espaco+numerais+ordinais)
re_paragrafo = r'PARAGRAFO_\1'

pa_inciso = re.compile(inciso+espaco+romano, re.I)
re_inciso = r'INCISO_\1'

# pa_alinea
# re_alinea

pa_cef = re.compile(cef, re.I)
re_cef = r'CEF'

pa_constituicao = re.compile(constituicao, re.I)
re_constituicao = r'CONSTITUICAO_FEDERAL'

# pa_instrucao_normativa
# re_instrucao_normativa

pa_tcu = re.compile(tcu, re.I)
re_tcu = r'TCU'

pa_ritcu = re.compile(regimento_interno+espaco+do+espaco+tcu, re.I)
re_ritcu = r'RI_TCU'

decisao_camara = espaco+numerais+ordinais+divisor+ano+espaco+hifen+espaco+tcu_opt+espaco+hifen+espaco
decisao_pl = decisao_camara+plenario
decisao_1c = decisao_camara+'1'+ordinais+espaco+camara
decisao_2c = decisao_camara+'2'+ordinais+espaco+camara
acordao_relacao = acordao+espaco+de+espaco+relacao

pa_acpl = re.compile(acordao+decisao_pl, re.I)
re_acpl = r'AC-\1-\2-PL'

pa_ac1c = re.compile(acordao+decisao_1c, re.I)
re_ac1c = r'AC-\1-\2-1C'

pa_ac2c = re.compile(acordao+decisao_2c, re.I)
re_ac2c = r'AC-\1-\2-2C'

pa_arpl = re.compile(acordao_relacao+decisao_pl, re.I)
re_arpl = r'AR-\1-\2-PL'

pa_ar1c = re.compile(acordao_relacao+decisao_1c, re.I)
re_ar1c = r'AR-\1-\2-1C'

pa_ar2c = re.compile(acordao_relacao+decisao_2c, re.I)
re_ar2c = r'AR-\1-\2-2C'

pa_depl = re.compile(decisao+decisao_pl, re.I)
re_depl = r'DE-\1-\2-PL'

pa_de1c = re.compile(decisao+decisao_1c, re.I)
re_de1c = r'DE-\1-\2-1C'

pa_de2c = re.compile(decisao+decisao_2c, re.I)
re_de2c = r'DE-\1-\2-2C'

pa_ldo = re.compile(ldo, re.I)
re_ldo = r'LDO'

pa_sem_ponto = re.compile(r'(\d+)(?:\.)(\d+)(?=\/)')
re_sem_ponto = r'\1\2'

pa_transform_emails = re.compile(r'[^\s]+@[^\s]+', re.UNICODE)
re_transform_emails = 'EMAIL'

pa_transform_url = re.compile(r'(http|https)://[^\s]+', re.UNICODE)
re_transform_url = 'URL'

pa_html = re.compile(r'<(\/|\\)?.+?>', re.UNICODE)

# pa_remove_numr = re.compile(r'((?<!\_)([\d]+)[?=(\.|\/|\°|\º|\ª|])|(?<=\/)([\d]+)(?=\.|\/|\s|;|,|-)')
pa_remove_numr = re.compile(r'(?<=\s|\/|\.|,|:|;)([\d]+)(?<!\s|\))')
re_vazio = ''

pa_hifens_numr = re.compile(r'(?<=\s)(-[\d]+|-)(?<!\s)')

pa_punctuation = re.compile(r'[.,;:?!–\\¿\/\°\º\ª\(\)\$\%\&\#]')

pa_2caracter = re.compile(r'(?<=\s)[a-zA-Z]{1,2}(?=\s|,|;)')

pa_generico = re.compile(r'(fls|folha[s]?|peça[s]?|grifo[s]? nosso[s]?|-?[X]-?|CPF|CNPJ|LTDA)', re.I)

pa_espacos = re.compile(r'([\s]{2,})')
re_espacos = ' '


def padronizacao(texto):
    texto = pa_html.sub(re_espacos, texto.DECISAO)
    
    texto = pa_sem_ponto.sub(re_sem_ponto, texto)

    texto = pa_lei.sub(re_lei, pa_decreto.sub(re_decreto, texto))
    texto = pa_inciso.sub(re_inciso, pa_paragrafo.sub(re_paragrafo, pa_artigo.sub(re_artigo, texto)))
    texto = pa_tcu.sub(re_tcu, pa_ritcu.sub(re_ritcu, texto))
    texto = pa_acpl.sub(re_acpl, pa_ac1c.sub(re_ac1c, pa_ac2c.sub(re_ac2c, pa_constituicao.sub(re_constituicao, texto))))
    texto = pa_depl.sub(re_depl, pa_de1c.sub(re_de1c, pa_de2c.sub(re_de2c, texto)))
    texto = pa_arpl.sub(re_arpl, pa_ar1c.sub(re_ar1c, pa_ar2c.sub(re_ar2c, texto)))
    texto = pa_transform_emails.sub(re_transform_emails, pa_transform_url.sub(re_transform_url, texto))
    texto = pa_remove_numr.sub(re_vazio, pa_punctuation.sub(re_vazio, pa_generico.sub(re_vazio, texto)))
    texto = pa_2caracter.sub(re_vazio, pa_hifens_numr.sub(re_vazio, texto))
    texto = pa_espacos.sub(re_espacos, texto)

    return texto.lower()
    

def find_case_insensitive(dirname, extensions):
    list_files = []
    for filename in glob.glob(dirname):
        base, ext = os.path.splitext(filename)
        if ext.lower() in extensions:
            filename = filename.replace('\\', '/')            
            list_files.append(filename)

    return sorted(list_files)
    
    
def extrairTipoSessao(texto):
    if len(re.findall('PRIMEIRA', texto)) != 0:
        return '1C'
    elif len(re.findall('SEGUNDA', texto)) > 0:
        return '2C'
    else:
        return 'PL'
    
    
def criaChaveAcordao(row):

    return row.TIPO_DECISAO + '-' + row.NUMERO_ACORDAO.zfill(6) + '-' + str(row.ANO_ACORDAO) + '-' + extrairTipoSessao(row.COLEGIADO.upper())


def read_file(file, separator='|', encoding='utf-8'):
    start_time = datetime.now()
    df = pd.read_csv(file, sep=separator, encoding=encoding)
    print('Duration: {}'.format(datetime.now() - start_time))
    return df


def save_file(df, file, separator='|', encoding='utf-8'):
    start_time = datetime.now()
    df.to_csv(file, sep=separator, index=False, encoding=encoding)
    print('Duration: {}'.format(datetime.now() - start_time))