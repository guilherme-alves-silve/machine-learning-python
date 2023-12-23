import spacy
import numpy as np


nlp = spacy.load("pt_core_news_sm", disable=["parser", "ner", "tagger", "textcat"])


def tokenizador(texto):
    doc = nlp(texto)
    tokens_validos = []

    for token in doc:
       
        eh_valido = not token.is_stop and token.is_alpha

        if eh_valido:
            tokens_validos.append(token.text.lower())

    return tokens_validos


def combinacao_de_vetores_por_soma(palavras, modelo):

    vetor = np.zeros((1, 300))
    for pn in palavras:
        try:
            vetor += modelo.get_vector(pn)
        except KeyError:
            pass

    return vetor
