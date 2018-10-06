# -*- coding: utf-8 -*-

from __future__ import division
import logging
from openfisca_france.model.base import *

log = logging.getLogger(__name__)

# Variables utilisées à la fois pour le PFL et pour la partie IR du PFU


class produit_epargne_solidaire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produit d'épargne solidaire"
    definition_period = YEAR


class produit_etats_non_cooperatif(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits de placement à revenus fixe ou de contrats de capitalisation et d'assurance-vie versés à un bénéficiaire résidant dans un état non-coopératif"
    definition_period = YEAR
