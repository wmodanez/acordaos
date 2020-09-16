
# coding: utf-8

# In[ ]:


class PortugueseStopWords:
    
    __artigos = ['o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'ao', 'à', 'aos', 'às', 'do', 'da', 'dos', 'das', 
               'dum', 'duma', 'duns', 'dumas', 'no', 'na', 'nos', 'nas', 'num', 'numa', 'nuns', 'numas', 'pelo', 
               'pela', 'pelos', 'pelas', 'polo', 'pola', 'polos', 'polas']
    __conjuncoes = ['e', 'ou', 'mas', 'ora', 'porém', 'contudo', 'não obstante', 'logo', 'portanto', 
                    'por conseguinte']
    __juridicas = []
    __preposicoes = ['a', 'ante', 'após', 'até', 'com', 'contra', 'de', 'desde', 'em', 'entre', 'para', 'per', 
                   'perante', 'por', 'sem', 'sob', 'sobre', 'trás', 'conforme', 'consoante', 'durante', 'exceto', 
                   'fora', 'afora', 'mediante', 'menos', 'salvante', 'salvo', 'segundo', 'tirante']
    __pronomes = ['eu', 'tu', 'ele', 'nós', 'vós', 'eles', 'me', 'te', 'a', 'o', 'lhe', 'se', 'nos', 'vos', 'os', 
                'as lhes', 'se', 'mim', 'comigo', 'ti', 'contigo', 'si', 'consigo', 'ela', 'nosco', 'conosco', 
                'convosco', 'elas', 'alguém', 'ninguém', 'tudo', 'nada', 'algo', 'cada', 'outrem', 'mais', 
                'menos', 'demais', 'algum', 'alguns', 'alguma', 'algumas', 'nenhum', 'nenhuns', 'nenhuma', 
                'nenhumas', 'todo', 'toda', 'todos', 'todas', 'muito', 'muitos', 'muita', 'muitas', 'pouco', 
                'pouca', 'poucos', 'poucas', 'certo', 'certa', 'certos', 'certas', 'vário', 'vários', 'vária', 
                'várias', 'tanto', 'tantos', 'tanta', 'tantas', 'quanto', 'quantos', 'quanta', 'quantas', 'um', 
                'uns', 'uma', 'umas', 'bastante', 'bastantes', 'qualquer', 'quaisquer', 'meu', 'minha', 'meus', 
                'minhas', 'teu', 'tua', 'teus', 'tuas', 'seu', 'sua', 'seus', 'suas', 'nosso', 'nossa', 'nossos', 
                'nossas', 'vosso', 'vossa', 'vossos', 'vossas', 'seu', 'sua', 'seus', 'suas', 'que', 'quem', 
                'onde', 'qual', 'quais', 'os quais', 'as quais', 'cujo', 'cuja', 'cujos', 'cujas', 'quanto', 
                'quanta', 'quantos', 'quantas', 'como', 'quando', 'você', 'vocês', 'senhor', 'senhores', 
                'senhorita', 'senhoritas', 'senhora', 'senhoras', 'senhoria', 'senhorias']
    
    
    def LegalStopWords(self):
        return sorted(list(set(self.__artigos  + self.__conjuncoes + self.__preposicoes + 
                        self.__pronomes)))
    
    
    def FullStopWords(self):
        return sorted(list(set(self.LegalStopWords() + self.__juridicas)))
        
