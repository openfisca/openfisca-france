# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from ..base import *  # noqa


### VARIABLES MANQUANTES dans OpenFisca : ###
## 8TC 2011-    8WE -2006   7UP, 7UQ -2009  7LS 2010    7JY 2009-2011   7XN 2007-2010
## 7XJ, 7XK -2007   7XD -2006   7WQ 2006-2008   7UL -2009   7IY 2009-2011   7GS 2009-2011
## 6CH -2006    3VT ?


# Socio-economic data
# Données d'entrée de la simulation à fournir à partir d'une enquête ou générées par le générateur de cas type
build_column('idmen', IntCol(is_permanent = True, label = u"Identifiant du ménage"))
build_column('idfoy', IntCol(is_permanent = True, label = u"Identifiant du foyer"))
build_column('idfam', IntCol(is_permanent = True, label = u"Identifiant de la famille"))

build_column('quimen', EnumCol(QUIMEN, is_permanent = True))
build_column('quifoy', EnumCol(QUIFOY, is_permanent = True))
build_column('quifam', EnumCol(QUIFAM, is_permanent = True))

build_column('birth', DateCol(is_permanent = True, label = u"Date de naissance"))

build_column(Familles.name_key, StrCol(entity = 'fam', is_permanent = True, label = u"Nom"))
build_column(FoyersFiscaux.name_key, StrCol(entity = 'foy', is_permanent = True, label = u"Nom"))
build_column(Individus.name_key, StrCol(is_permanent = True, label = u"Prénom"))
build_column(Menages.name_key, StrCol(entity = 'men', is_permanent = True, label = u"Nom"))


build_column('enceinte', BoolCol(entity = 'ind', label = u"Est enceinte"))

# Prestations familiales
build_column('inactif', BoolCol(entity = 'fam',
                    label = u"Parent inactif (PAJE-CLCA)"))

build_column('partiel1', BoolCol(entity = 'fam',
                     label = u"Parent actif à moins de 50% (PAJE-CLCA)"))

build_column('partiel2', BoolCol(entity = 'fam',
                     label = u"Parent actif entre 50% et 80% (PAJE-CLCA)"))

build_column('categ_inv', PeriodSizeIndependentIntCol(label = u"Catégorie de handicap (AEEH)"))

build_column('opt_colca', BoolCol(entity = 'fam',
                      label = u"Opte pour le COLCA"))

build_column('empl_dir', BoolCol(entity = 'fam',
                     label = u"Emploi direct (CLCMG)"))

build_column('ass_mat', BoolCol(entity = 'fam',
                    label = u"Assistante maternelle (CLCMG)"))

build_column('gar_dom', BoolCol(entity = 'fam',
                    label = u"Garde à domicile (CLCMG)"))

# Autres
build_column('coloc', BoolCol(label = u"Vie en colocation"))
build_column(
    'csg_rempl',
    EnumCol(
        label = u"Taux retenu sur la CSG des revenus de remplacment",
        entity = 'ind',
        enum = Enum([
            u"Non renseigné/non pertinent",
            u"Exonéré",
            u"Taux réduit",
            u"Taux plein",
            ]),
        default = 3,
        ),
    )
build_column('aer', IntCol(label = u"Allocation équivalent retraite (AER)"))  # L'AER est remplacée depuis le 1er juillet 2011 par l'allocation transitoire de solidarité (ATS).
build_column('f5sq', IntCol())

build_column('zthabm', IntCol(entity = 'men'))  # TODO: Devrait être renommée tax_hab

build_column(
    'proprietaire_proche_famille',
    BoolCol(
        entity = "fam",
        label = u"Le propriétaire du logement a un lien de parenté avec la personne de référence ou son conjoint",
        ),
    )

build_column('adoption', BoolCol(entity = "ind", label = u"Enfant adopté"))

build_column('ass_precondition_remplie', BoolCol(entity = "ind", label = u"Éligible à l'ASS"))

build_column('elig_creimp_jeunes', BoolCol(entity = "ind", label = u"Éligible au crédit d'impôt jeunes",
                    start = date(2005, 1, 1),
                    end = date(2008, 1, 1))) #Sert à savoir si son secteur d'activité permet au jeune de bénéficier du crédit impôts jeunes

# ('tax_hab', IntCol())
