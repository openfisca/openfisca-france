import numpy as np


def arrondi_fiscal(n):
    """
    Arrondit les montants conformément aux règles prévues à l'article 1657 du CGI :
    - les montants sont arrondis à l'euro le plus proche ;
    - lorsque la fraction d'euro est égale à 0.5, le montant est arrondi à l'euro supérieur.
    """
    return np.where(n >= 0, np.floor(n + 0.5), -np.floor(abs(n) + 0.5))
