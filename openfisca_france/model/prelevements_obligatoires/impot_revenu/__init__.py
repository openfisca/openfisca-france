import numpy as np


def arrondi_fiscal(x):
    '''
    Arrondit les montants conformément aux règles prévues à l'article 1657 du CGI :
    - Les valeurs positives sont arrondies à l'entier le plus proche, avec un arrondi vers le haut en cas de .5 (ex: 1.5 devient 2).
    - Les valeurs négatives sont arrondies à l'entier le plus proche, avec un arrondi vers le bas en cas de .5 (ex: -1.5 devient -2).
    - Les autres valeurs sont arrondies à l'entier le plus proche de manière classique (ex: 1.2 devient 1, -1.2 devient -1).

    C'est pour cela que l'on ne peut pas utiliser np.round, qui arrondit les .5 vers l'entier pair le plus proche (ex: 1.5 devient 2, mais 2.5 devient 2).
    '''
    return np.where(x >= 0, np.floor(x + 0.5), -np.floor(np.abs(x) + 0.5))
