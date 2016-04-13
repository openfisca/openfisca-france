# -*- coding: utf-8 -*-

"""Tools to use income taxes calculator from finances.gouv.fr web site."""


import urllib
import urllib2


__all__ = [
    'call_tax_calculator',
    'openfisca_variable_name_by_tax_calculator_code',
    'transform_scenario_to_tax_calculator_inputs',
    ]

openfisca_variable_name_by_tax_calculator_code = dict(
    AVFISCOPTER = None,
    BCSG = None,
    BPRS = None,
    BRDS = None,
    CIADCRE = None,
    CICA = None,
    CICORSE = None,
    CIDEPENV = None,
    CIDEVDUR = None,
    CIGARD = None,
    CIGE = None,
    CIHABPRIN = None,
    CIMOBIL = None,
    CIPERT = None,
    CIPRETUD = None,
    CIRCM = None,
    CIRELANCE = None,
    CITEC = None,
    I2DH = None,
    IAVF2 = None,
    IAVIM = u'iai',
    IDEC = u'decote',
    IDRS2 = u'ir_plaf_qf',
    IINET = None,
    IINETIR = u'irpp',
    IPROP = None,
    IREST = None,
    IRESTIR = u'irpp',
    IRETS = None,
    ITRED = u'reductions',
    NAPCR = None,
    NAPCRP = None,
    NAPCS = None,
    NAPPS = None,
    NAPRD = None,
    NBP = u'nbptr',
    NBPT = u'nbptr',
    PERPPLAFTC = None,
    PERPPLAFTP = None,
    PERPPLAFTV = None,
    PPETOT = u'ppe',
    RAA = None,
    RAH = None,
    RAIDE = None,
    RCEL = None,
    RCEL2012 = None,
    RCELCOM = None,
    RCELFABC = None,
    RCELFD = None,
    RCELHJK = None,
    RCELHL = None,
    RCELHM = None,
    RCELHNO = None,
    RCELHR = None,
    RCELJBGL = None,
    RCELJOQR = None,
    RCELJP = None,
    RCELLIER = None,
    RCELNBGL = None,
    RCELNQ = None,
    RCELREPGJ = None,
    RCELREPGK = None,
    RCELREPGL = None,
    RCELREPGP = None,
    RCELREPGS = None,
    RCELREPGT = None,
    RCELREPGU = None,
    RCELREPGV = None,
    RCELREPGW = None,
    RCELREPGX = None,
    RCELREPHA = None,
    RCELREPHB = None,
    RCELREPHD = None,
    RCELREPHE = None,
    RCELREPHF = None,
    RCELREPHG = None,
    RCELREPHH = None,
    RCELREPHR = None,
    RCELREPHS = None,
    RCELREPHT = None,
    RCELREPHU = None,
    RCELREPHV = None,
    RCELREPHW = None,
    RCELREPHX = None,
    RCELREPHZ = None,
    RCELRRED09 = None,
    RCELRREDLA = None,
    RCELRREDLB = None,
    RCELRREDLC = None,
    RCELRREDLD = None,
    RCELRREDLE = None,
    RCELRREDLF = None,
    RCELRREDLM = None,
    RCELRREDLS = None,
    RCELRREDLZ = None,
    RCELRREDMG = None,
    RCINE = None,
    RCODELOP = None,
    RCODJT = None,
    RCODJU = None,
    RCODJV = None,
    RCODJW = None,
    RCODJX = None,
    RCOLENT = None,
    RCONS = None,
    RCOTFOR = None,
    RDIFAGRI = None,
    RDONS = None,
    RDUFLOGIH = None,
    REI = None,
    REVKIRE = u'rfr',
    RFCPI = None,
    RFIPC = None,
    RFOR = None,
    RFORET = None,
    RHEBE = None,
    RIDOMENT = None,
    RIDOMPROE1 = None,
    RIDOMPROE2 = None,
    RIDOMPROE3 = None,
    RIDOMPROE4 = None,
    RIDOMPROE5 = None,
    RILMIA = None,
    RILMIB = None,
    RILMIC = None,
    RILMIH = None,
    RILMIX = None,
    RILMIZ = None,
    RILMJI = None,
    RILMJS = None,
    RILMJV = None,
    RILMJW = None,
    RILMJX = None,
    RINNO = None,
    RINVDOMTOMLG = None,
    RINVRED = None,
    RLOCIDEFG = None,
    RLOGDOM = None,
    RMEUBLE = None,
    RNI = None,
    RNICOL = u'rni',
    RNOUV = None,
    RPATNAT = None,
    RPATNATOT = None,
    RPECHE = None,
    RPRESCOMPREP = None,
    RPROREP = None,
    RRBG = u'rbg',
    RRDOM = None,
    RREDMEUB = None,
    RREDREP = None,
    RREPA = None,
    RREPMEU = None,
    RREPNPRO = None,
    RRESIMEUB = None,
    RRESINEUV = None,
    RRESIVIEU = None,
    RRESTIMO = None,
    RRIRENOV = None,
    RRPRESCOMP = None,
    RSOCREPR = None,
    RSOUFIP = None,
    RSURV = None,
    RTELEIR = None,
    RTITPRISE = None,
    RTOUHOTR = None,
    RTOUR = None,
    RTOUREPA = None,
    RTOURES = None,
    RTOURHOT = None,
    RTOURNEUF = None,
    RTOURREP = None,
    RTOURTRA = None,
    TEFF = None,
    TOTPAC = None,  # Nombre de personnes à charge dans le foyer fiscal
    TXMARJ = None,
    TXMOYIMP = None,
    )


def call_tax_calculator(year, inputs):
    url = 'http://www3.finances.gouv.fr/cgi-bin/calc-{}.cgi'.format(year)
    request = urllib2.Request(url, headers = {
        'User-Agent': 'OpenFisca-Script',
        })
    response = urllib2.urlopen(request, urllib.urlencode([
        (name, str(value))
        for name, value in inputs.iteritems()
        ]))
    response_html = response.read()
    if 'Erreur' in response_html:
        raise Exception(u"Erreur : {}".format(response_html.decode('iso-8859-1')).encode('utf-8'))
    return response_html


def transform_scenario_to_tax_calculator_inputs(scenario):
    tax_benefit_system = scenario.tax_benefit_system
    test_case = scenario.test_case
    impots_arguments = {
        'pre_situation_residence': 'M',  # Métropole
        }
    individu_by_id = {
        individu['id']: individu
        for individu in test_case['individus']
        }
    for foyer_fiscal in test_case['foyers_fiscaux']:
        foyer_fiscal = foyer_fiscal.copy()

        for declarant_index, declarant_id in enumerate(foyer_fiscal.pop('declarants')):
            declarant = individu_by_id[declarant_id].copy()

            date_naissance = declarant.pop('date_naissance')
            impots_arguments['0D{}'.format(chr(ord('A') + declarant_index))] = date_naissance.year

            statmarit = declarant.pop('statmarit', None)
            column = tax_benefit_system.column_by_name['statmarit']
            if statmarit is None:
                statmarit = column.enum._vars[column.default]
            pre_situation_famille = {
                u"Marié": 'M',
                u"Célibataire": 'C',
                u"Divorcé": 'D',
                u"Veuf": 'V',
                u"Pacsé": 'O',
                # u"Jeune veuf": TODO
                }[statmarit if isinstance(statmarit, basestring) else column.enum._vars[statmarit]]
            assert 'pre_situation_famille' not in impots_arguments \
                or impots_arguments['pre_situation_famille'] == pre_situation_famille, str((impots_arguments,
                    pre_situation_famille))
            impots_arguments['pre_situation_famille'] = pre_situation_famille

            for column_code, value in declarant.iteritems():
                if column_code in (
                        'activite',
                        'cadre',
                        'id',
                        ):
                    continue
                column = tax_benefit_system.column_by_name[column_code]
                cerfa_field = column.cerfa_field
                assert cerfa_field is not None and isinstance(cerfa_field, dict), column_code
                impots_arguments[cerfa_field[declarant_index]] = value

        impots_arguments['0CF'] = len(foyer_fiscal['personnes_a_charge'])
        for personne_a_charge_index, personne_a_charge_id in enumerate(foyer_fiscal.pop('personnes_a_charge')):
            personne_a_charge = individu_by_id[personne_a_charge_id].copy()

            date_naissance = personne_a_charge.pop('date_naissance')
            impots_arguments['0F{}'.format(personne_a_charge_index)] = date_naissance.year

            personne_a_charge.pop('statmarit', None)

            for column_code, value in personne_a_charge.iteritems():
                if column_code in (
                        'activite',
                        'cadre',
                        'id',
                        ):
                    continue
                column = tax_benefit_system.column_by_name[column_code]
                cerfa_field = column.cerfa_field
                assert cerfa_field is not None and isinstance(cerfa_field, dict), column_code
                impots_arguments[cerfa_field[personne_a_charge_index]] = value

        if foyer_fiscal.pop('caseT', False):
            impots_arguments['0BT'] = '1'

        for column_code, value in foyer_fiscal.iteritems():
            if column_code == 'id':
                continue
            if column_code == 'f7uf':
                impots_arguments['7UG'] = str(value)  # bug dans le site des impots
            if column_code == 'f7ud':
                impots_arguments['7UE'] = str(value)  # bug dans le site des impots
            if column_code == 'f7vc':
                impots_arguments['7VD'] = str(value)  # bug dans le site des impots
            column = tax_benefit_system.column_by_name[column_code]
            cerfa_field = column.cerfa_field
            assert cerfa_field is not None and isinstance(cerfa_field, basestring), column_code
            impots_arguments[cerfa_field] = int(value) if isinstance(value, bool) else value

    return impots_arguments
