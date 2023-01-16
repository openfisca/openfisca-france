import logging
from numpy import around
from openfisca_france.model.base import *


log = logging.getLogger(__name__)

# Le cas particulier des investissements d'outremer (domsoc, domlog, doment): la mise à jour des formules et la prise en compte d'un plafond approximatif
#   n'est réalisée qu'à partir de 2016. Au vu de la complexité de ces dispositifs (rétrocession, investissements avec des plafonds particuliers..),
#   les plafonds sont approximés (par année et par dispositif) et ils ne prennent pas en compte les interactions entre les trois dispositifs d'outremer ni
#   l'interaction avec le plafonnement global des avantages fiscaux. De ce point de vue, l'approximation surestime les plafonds pour les investissements d'outremer.
#   D'un autre côté lors de la déclaration d'impôt il possible de choisir pour ces dispositifs entre un plafond absolu et un plafond relatif en pourcentage de RNI,
#   seul le plafond absolu est codé pour le moment, cela peut entrainer une sous estimation des réductions d'impôt pour les personnes qui ont un RNI
#   supérieur à environ 300 000.


class reductions_iom(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réductions d'impôt sur les investissements d'outremer"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Approximations de plafonds déjà appliquées dans les formules
        '''
        reductions_om = [
            # plafonds séparés, déjà appliqués dans les formules :
            'doment',
            'domlog',
            'domsoc',
            ]

        red_iom = sum([around(foyer_fiscal(reduction, period)) for reduction in reductions_om])

        return red_iom


class doment(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'doment'
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        f7ur = foyer_fiscal('f7ur', period)
        f7oz = foyer_fiscal('f7oz_2011', period)
        f7pz = foyer_fiscal('f7pz_2013', period)
        f7qz = foyer_fiscal('f7qz_2012', period)
        f7rz = foyer_fiscal('f7rz_2010', period)

        return f7ur + f7oz + f7pz + f7qz + f7rz

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        f7ur = foyer_fiscal('f7ur', period)
        f7oz = foyer_fiscal('f7oz_2011', period)
        f7pz = foyer_fiscal('f7pz_2013', period)
        f7qz = foyer_fiscal('f7qz_2012', period)
        f7rz = foyer_fiscal('f7rz_2010', period)
        f7sz = foyer_fiscal('f7sz_2009', period)

        return f7ur + f7oz + f7pz + f7qz + f7rz + f7sz

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        f7oz = foyer_fiscal('f7oz_2011', period)
        f7pz = foyer_fiscal('f7pz_2013', period)
        f7qz = foyer_fiscal('f7qz_2012', period)
        f7rz = foyer_fiscal('f7rz_2010', period)
        f7sz = foyer_fiscal('f7sz_2009', period)
        f7qe = foyer_fiscal('f7qe_2012', period)
        f7qf = foyer_fiscal('f7qf_2012', period)
        f7qg = foyer_fiscal('f7qg_2012', period)
        f7qh = foyer_fiscal('f7qh_2012', period)
        f7qi = foyer_fiscal('f7qi_2012', period)
        f7qj = foyer_fiscal('f7qj_2010', period)

        return f7oz + f7pz + f7qz + f7rz + f7sz + f7qe + f7qf + f7qg + f7qh + f7qi + f7qj

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        f7oz = foyer_fiscal('f7oz_2011', period)
        f7pz = foyer_fiscal('f7pz_2013', period)
        f7qz = foyer_fiscal('f7qz_2012', period)
        f7rz = foyer_fiscal('f7rz_2010', period)
        f7qe = foyer_fiscal('f7qe_2012', period)
        f7qf = foyer_fiscal('f7qf_2012', period)
        f7qg = foyer_fiscal('f7qg_2012', period)
        f7qh = foyer_fiscal('f7qh_2012', period)
        f7qi = foyer_fiscal('f7qi_2012', period)
        f7qj = foyer_fiscal('f7qj_2010', period)
        f7qo = foyer_fiscal('f7qo_2012', period)
        f7qp = foyer_fiscal('f7qp_2012', period)
        f7qq = foyer_fiscal('f7qq_2012', period)
        f7qr = foyer_fiscal('f7qr_2012', period)
        f7qs = foyer_fiscal('f7qs_2012', period)
        f7mm = foyer_fiscal('f7mm_2012', period)
        f7ma = foyer_fiscal('f7ma_2012', period)
        f7lg = foyer_fiscal('f7lg_2012', period)
        f7ks = foyer_fiscal('f7ks', period)
        f7ls = foyer_fiscal('f7ls_2010', period)

        return (
            f7ks
            + f7lg + f7ls
            + f7ma + f7mm
            + f7oz
            + f7pz
            + f7qe + f7qf + f7qg + f7qh + f7qi + f7qj + f7qo + f7qp + f7qq + f7qr + f7qs + f7qz
            + f7rz
            )

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        f7ks = foyer_fiscal('f7ks', period)
        f7kt = foyer_fiscal('f7kt', period)
        f7ku = foyer_fiscal('f7ku', period)
        f7lg = foyer_fiscal('f7lg_2012', period)
        f7lh = foyer_fiscal('f7lh_2012', period)
        f7li = foyer_fiscal('f7li_2012', period)
        f7mm = foyer_fiscal('f7mm_2012', period)
        f7ma = foyer_fiscal('f7ma_2012', period)
        f7mb = foyer_fiscal('f7mb_2012', period)
        f7mc = foyer_fiscal('f7mc_2012', period)
        f7mn = foyer_fiscal('f7mn', period)
        f7oz = foyer_fiscal('f7oz_2011', period)
        f7pa = foyer_fiscal('f7pa_2012', period)
        f7pb = foyer_fiscal('f7pb_2012', period)
        f7pd = foyer_fiscal('f7pd_2012', period)
        f7pe = foyer_fiscal('f7pe_2012', period)
        f7pf = foyer_fiscal('f7pf_2012', period)
        f7ph = foyer_fiscal('f7ph_2012', period)
        f7pi = foyer_fiscal('f7pi_2012', period)
        f7pj = foyer_fiscal('f7pj_2012', period)
        f7pl = foyer_fiscal('f7pl_2012', period)
        f7pz = foyer_fiscal('f7pz_2013', period)
        f7qz = foyer_fiscal('f7qz_2012', period)
        f7qe = foyer_fiscal('f7qe_2012', period)
        f7qf = foyer_fiscal('f7qf_2012', period)
        f7qg = foyer_fiscal('f7qg_2012', period)
        f7qi = foyer_fiscal('f7qi_2012', period)
        f7qo = foyer_fiscal('f7qo_2012', period)
        f7qp = foyer_fiscal('f7qp_2012', period)
        f7qr = foyer_fiscal('f7qr_2012', period)
        f7qv = foyer_fiscal('f7qv', period)

        return (
            f7ks + f7kt + f7ku
            + f7lg + f7lh + f7li
            + f7mb + f7mn + f7mc + f7mm + f7ma
            + f7oz
            + f7pa + f7pb + f7pd + f7pe + f7pf + f7ph + f7pi + f7pj + f7pl + f7pz
            + f7qz + f7qf + f7qg + f7qi + f7qo + f7qp + f7qr + f7qe + f7qv
            )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        f7ks = foyer_fiscal('f7ks', period)
        f7kt = foyer_fiscal('f7kt', period)
        f7ku = foyer_fiscal('f7ku', period)
        f7lg = foyer_fiscal('f7lg_2012', period)
        f7lh = foyer_fiscal('f7lh_2012', period)
        f7li = foyer_fiscal('f7li_2012', period)
        f7ma = foyer_fiscal('f7ma_2012', period)
        f7mb = foyer_fiscal('f7mb_2012', period)
        f7mc = foyer_fiscal('f7mc_2012', period)
        f7mm = foyer_fiscal('f7mm_2012', period)
        f7mn = foyer_fiscal('f7mn', period)
        f7nu = foyer_fiscal('f7nu_2012', period)
        f7nv = foyer_fiscal('f7nv_2012', period)
        f7nw = foyer_fiscal('f7nw_2012', period)
        f7ny = foyer_fiscal('f7ny_2012', period)
        f7pa = foyer_fiscal('f7pa_2012', period)
        f7pb = foyer_fiscal('f7pb_2012', period)
        f7pd = foyer_fiscal('f7pd_2012', period)
        f7pe = foyer_fiscal('f7pe_2012', period)
        f7pf = foyer_fiscal('f7pf_2012', period)
        f7ph = foyer_fiscal('f7ph_2012', period)
        f7pi = foyer_fiscal('f7pi_2012', period)
        f7pj = foyer_fiscal('f7pj_2012', period)
        f7pl = foyer_fiscal('f7pl_2012', period)
        f7pm = foyer_fiscal('f7pm_2012', period)
        f7pn = foyer_fiscal('f7pn_2012', period)
        f7po = foyer_fiscal('f7po_2012', period)
        f7pp = foyer_fiscal('f7pp_2012', period)
        f7pr = foyer_fiscal('f7pr_2012', period)
        f7ps = foyer_fiscal('f7ps_2012', period)
        f7pt = foyer_fiscal('f7pt_2012', period)
        f7pu = foyer_fiscal('f7pu_2013', period)
        f7pw = foyer_fiscal('f7pw_2013', period)
        f7px = foyer_fiscal('f7px_2013', period)
        f7py = foyer_fiscal('f7py_2013', period)
        f7pz = foyer_fiscal('f7pz_2013', period)
        f7qe = foyer_fiscal('f7qe_2012', period)
        f7qf = foyer_fiscal('f7qf_2012', period)
        f7qg = foyer_fiscal('f7qg_2012', period)
        f7qi = foyer_fiscal('f7qi_2012', period)
        f7qo = foyer_fiscal('f7qo_2012', period)
        f7qp = foyer_fiscal('f7qp_2012', period)
        f7qr = foyer_fiscal('f7qr_2012', period)
        f7qv = foyer_fiscal('f7qv', period)
        f7qz = foyer_fiscal('f7qz_2012', period)
        f7rg = foyer_fiscal('f7rg_2012', period)
        f7ri = foyer_fiscal('f7ri_2012', period)
        f7rj = foyer_fiscal('f7rj_2012', period)
        f7rk = foyer_fiscal('f7rk_2012', period)
        f7rl = foyer_fiscal('f7rl_2012', period)
        f7rm = foyer_fiscal('f7rm_2012', period)
        f7ro = foyer_fiscal('f7ro_2012', period)
        f7rp = foyer_fiscal('f7rp_2012', period)
        f7rq = foyer_fiscal('f7rq_2012', period)
        f7rr = foyer_fiscal('f7rr_2012', period)
        f7rt = foyer_fiscal('f7rt_2012', period)
        f7ru = foyer_fiscal('f7ru_2012', period)
        f7rv = foyer_fiscal('f7rv_2012', period)
        f7rw = foyer_fiscal('f7rw_2012', period)
        f7ry = foyer_fiscal('f7ry_2012', period)

        return (
            f7ks + f7kt + f7ku
            + f7lg + f7lh + f7li
            + f7ma + f7mb + f7mc + f7mm + f7mn
            + f7pz
            + f7nu + f7nv + f7nw + f7ny
            + f7pa + f7pb + f7pd + f7pe + f7pf + f7ph + f7pi + f7pj + f7pl + f7pm + f7pn + f7po + f7pp + f7pr + f7ps
            + f7pt + f7pu + f7pw + f7px + f7py
            + f7qe + f7qf + f7qg + f7qi + f7qo + f7qp + f7qr + f7qv + f7qz
            + f7rg + f7ri + f7rj + f7rk + f7rl + f7rm + f7ro + f7rp + f7rq + f7rr + f7rt + f7ru + f7rv + f7rw + f7ry
            )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        fhsa = foyer_fiscal('fhsa', period)
        fhsb = foyer_fiscal('fhsb', period)
        fhsf = foyer_fiscal('fhsf', period)
        fhsg = foyer_fiscal('fhsg', period)
        fhsc = foyer_fiscal('fhsc', period)
        fhsh = foyer_fiscal('fhsh', period)
        fhse = foyer_fiscal('fhse', period)
        fhsj = foyer_fiscal('fhsj', period)
        fhsk = foyer_fiscal('fhsk', period)
        fhsl = foyer_fiscal('fhsl', period)
        fhsp = foyer_fiscal('fhsp', period)
        fhsq = foyer_fiscal('fhsq', period)
        fhsm = foyer_fiscal('fhsm', period)
        fhsr = foyer_fiscal('fhsr', period)
        fhso = foyer_fiscal('fhso', period)
        fhst = foyer_fiscal('fhst', period)
        fhsu = foyer_fiscal('fhsu', period)
        fhsv = foyer_fiscal('fhsv', period)
        fhsw = foyer_fiscal('fhsw', period)
        fhsz = foyer_fiscal('fhsz', period)
        fhta = foyer_fiscal('fhta', period)
        fhtb = foyer_fiscal('fhtb', period)
        fhtd = foyer_fiscal('fhtd', period)
        fhks = foyer_fiscal('fhks', period)
        fhkt = foyer_fiscal('fhkt', period)
        fhku = foyer_fiscal('fhku', period)
        fhlg = foyer_fiscal('fhlg', period)
        fhlh = foyer_fiscal('fhlh', period)
        fhli = foyer_fiscal('fhli', period)
        fhma = foyer_fiscal('fhma', period)
        fhmb = foyer_fiscal('fhmb', period)
        fhmc = foyer_fiscal('fhmc', period)
        fhmm = foyer_fiscal('fhmm', period)
        fhmn = foyer_fiscal('fhmn', period)
        fhnu = foyer_fiscal('fhnu', period)
        fhnv = foyer_fiscal('fhnv', period)
        fhnw = foyer_fiscal('fhnw', period)
        fhny = foyer_fiscal('fhny', period)
        fhpa = foyer_fiscal('fhpa', period)
        fhpb = foyer_fiscal('fhpb', period)
        fhpd = foyer_fiscal('fhpd', period)
        fhpe = foyer_fiscal('fhpe', period)
        fhpf = foyer_fiscal('fhpf', period)
        fhph = foyer_fiscal('fhph', period)
        fhpi = foyer_fiscal('fhpi', period)
        fhpj = foyer_fiscal('fhpj', period)
        fhpl = foyer_fiscal('fhpl', period)
        fhpm = foyer_fiscal('fhpm', period)
        fhpn = foyer_fiscal('fhpn', period)
        fhpo = foyer_fiscal('fhpo', period)
        fhpp = foyer_fiscal('fhpp', period)
        fhpr = foyer_fiscal('fhpr', period)
        fhps = foyer_fiscal('fhps', period)
        fhpt = foyer_fiscal('fhpt', period)
        fhpu = foyer_fiscal('fhpu', period)
        fhpw = foyer_fiscal('fhpw', period)
        fhpx = foyer_fiscal('fhpx', period)
        fhpy = foyer_fiscal('fhpy', period)
        fhqe = foyer_fiscal('fhqe', period)
        fhqf = foyer_fiscal('fhqf', period)
        fhqg = foyer_fiscal('fhqg', period)
        fhqi = foyer_fiscal('fhqi', period)
        fhqo = foyer_fiscal('fhqo', period)
        fhqp = foyer_fiscal('fhqp', period)
        fhqr = foyer_fiscal('fhqr', period)
        fhqv = foyer_fiscal('fhqv', period)
        fhqz = foyer_fiscal('fhqz', period)
        fhrg = foyer_fiscal('fhrg', period)
        fhri = foyer_fiscal('fhri', period)
        fhrj = foyer_fiscal('fhrj', period)
        fhrk = foyer_fiscal('fhrk', period)
        fhrl = foyer_fiscal('fhrl', period)
        fhrm = foyer_fiscal('fhrm', period)
        fhro = foyer_fiscal('fhro', period)
        fhrp = foyer_fiscal('fhrp', period)
        fhrq = foyer_fiscal('fhrq', period)
        fhrr = foyer_fiscal('fhrr', period)
        fhrt = foyer_fiscal('fhrt', period)
        fhru = foyer_fiscal('fhru', period)
        fhrv = foyer_fiscal('fhrv', period)
        fhrw = foyer_fiscal('fhrw', period)
        fhry = foyer_fiscal('fhry', period)

        return (
            fhsa + fhsb + fhsf + fhsg + fhsc + fhsh + fhse + fhsj + fhsk + fhsl + fhsp + fhsq + fhsm + fhsr + fhso
            + fhst + fhsu + fhsv + fhsw + fhsz + fhta + fhtb + fhtd + fhks + fhkt + fhku + fhlg + fhlh + fhli + fhma
            + fhmb + fhmc + fhmm + fhmn + fhnu + fhnv + fhnw + fhny + fhpa + fhpb + fhpd + fhpe + fhpf + fhph + fhpi
            + fhpj + fhpl + fhpm + fhpn + fhpo + fhpp + fhpr + fhps + fhpt + fhpu + fhpw + fhpx + fhpy + fhqe + fhqf
            + fhqg + fhqi + fhqo + fhqp + fhqr + fhqv + fhqz + fhrg + fhri + fhrj + fhrk + fhrl + fhrm + fhro + fhrp
            + fhrq + fhrr + fhrt + fhru + fhrv + fhrw + fhry
            )

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        fhaa = foyer_fiscal('fhaa', period)
        fhab = foyer_fiscal('fhab', period)
        fhac = foyer_fiscal('fhac', period)
        fhae = foyer_fiscal('fhae', period)
        fhaf = foyer_fiscal('fhaf', period)
        fhag = foyer_fiscal('fhag', period)
        fhah = foyer_fiscal('fhah', period)
        fhaj = foyer_fiscal('fhaj', period)
        fhak = foyer_fiscal('fhak', period)
        fhal = foyer_fiscal('fhal', period)
        fham = foyer_fiscal('fham', period)
        fhao = foyer_fiscal('fhao', period)
        fhap = foyer_fiscal('fhap', period)
        fhaq = foyer_fiscal('fhaq', period)
        fhar = foyer_fiscal('fhar', period)
        fhat = foyer_fiscal('fhat', period)
        fhau = foyer_fiscal('fhau', period)
        fhav = foyer_fiscal('fhav', period)
        fhaw = foyer_fiscal('fhaw', period)
        fhay = foyer_fiscal('fhay', period)
        fhba = foyer_fiscal('fhba', period)
        fhbb = foyer_fiscal('fhbb', period)
        fhbe = foyer_fiscal('fhbe', period)
        fhbg = foyer_fiscal('fhbg', period)
        fhks = foyer_fiscal('fhks', period)
        fhkt = foyer_fiscal('fhkt', period)
        fhku = foyer_fiscal('fhku', period)
        fhlg = foyer_fiscal('fhlg', period)
        fhlh = foyer_fiscal('fhlh', period)
        fhli = foyer_fiscal('fhli', period)
        fhma = foyer_fiscal('fhma', period)
        fhmb = foyer_fiscal('fhmb', period)
        fhmc = foyer_fiscal('fhmc', period)
        fhmm = foyer_fiscal('fhmm', period)
        fhmn = foyer_fiscal('fhmn', period)
        fhnu = foyer_fiscal('fhnu', period)
        fhnv = foyer_fiscal('fhnv', period)
        fhnw = foyer_fiscal('fhnw', period)
        fhny = foyer_fiscal('fhny', period)
        fhpa = foyer_fiscal('fhpa', period)
        fhpb = foyer_fiscal('fhpb', period)
        fhpd = foyer_fiscal('fhpd', period)
        fhpe = foyer_fiscal('fhpe', period)
        fhpf = foyer_fiscal('fhpf', period)
        fhph = foyer_fiscal('fhph', period)
        fhpi = foyer_fiscal('fhpi', period)
        fhpj = foyer_fiscal('fhpj', period)
        fhpl = foyer_fiscal('fhpl', period)
        fhpm = foyer_fiscal('fhpm', period)
        fhpn = foyer_fiscal('fhpn', period)
        fhpo = foyer_fiscal('fhpo', period)
        fhpp = foyer_fiscal('fhpp', period)
        fhpr = foyer_fiscal('fhpr', period)
        fhps = foyer_fiscal('fhps', period)
        fhpt = foyer_fiscal('fhpt', period)
        fhpu = foyer_fiscal('fhpu', period)
        fhpw = foyer_fiscal('fhpw', period)
        fhpx = foyer_fiscal('fhpx', period)
        fhpy = foyer_fiscal('fhpy', period)
        fhqe = foyer_fiscal('fhqe', period)
        fhqf = foyer_fiscal('fhqf', period)
        fhqg = foyer_fiscal('fhqg', period)
        fhqi = foyer_fiscal('fhqi', period)
        fhqo = foyer_fiscal('fhqo', period)
        fhqp = foyer_fiscal('fhqp', period)
        fhqr = foyer_fiscal('fhqr', period)
        fhqv = foyer_fiscal('fhqv', period)
        fhrg = foyer_fiscal('fhrg', period)
        fhri = foyer_fiscal('fhri', period)
        fhrj = foyer_fiscal('fhrj', period)
        fhrk = foyer_fiscal('fhrk', period)
        fhrl = foyer_fiscal('fhrl', period)
        fhrm = foyer_fiscal('fhrm', period)
        fhro = foyer_fiscal('fhro', period)
        fhrp = foyer_fiscal('fhrp', period)
        fhrq = foyer_fiscal('fhrq', period)
        fhrr = foyer_fiscal('fhrr', period)
        fhrt = foyer_fiscal('fhrt', period)
        fhru = foyer_fiscal('fhru', period)
        fhrv = foyer_fiscal('fhrv', period)
        fhrw = foyer_fiscal('fhrw', period)
        fhry = foyer_fiscal('fhry', period)
        fhsa = foyer_fiscal('fhsa', period)
        fhsb = foyer_fiscal('fhsb', period)
        fhsc = foyer_fiscal('fhsc', period)
        fhse = foyer_fiscal('fhse', period)
        fhsf = foyer_fiscal('fhsf', period)
        fhsg = foyer_fiscal('fhsg', period)
        fhsh = foyer_fiscal('fhsh', period)
        fhsj = foyer_fiscal('fhsj', period)
        fhsk = foyer_fiscal('fhsk', period)
        fhsl = foyer_fiscal('fhsl', period)
        fhsm = foyer_fiscal('fhsm', period)
        fhso = foyer_fiscal('fhso', period)
        fhsp = foyer_fiscal('fhsp', period)
        fhsq = foyer_fiscal('fhsq', period)
        fhsr = foyer_fiscal('fhsr', period)
        fhst = foyer_fiscal('fhst', period)
        fhsu = foyer_fiscal('fhsu', period)
        fhsv = foyer_fiscal('fhsv', period)
        fhsw = foyer_fiscal('fhsw', period)
        fhsz = foyer_fiscal('fhsz', period)
        fhta = foyer_fiscal('fhta', period)
        fhtb = foyer_fiscal('fhtb', period)
        fhtd = foyer_fiscal('fhtd', period)

        return (
            fhaa + fhab + fhac + fhae + fhaf + fhag + fhah + fhaj + fhak + fhal + fham + fhao + fhap + fhaq + fhar
            + fhat + fhau + fhav + fhaw + fhay + fhba + fhbb + fhbe + fhbg
            + fhsa + fhsb + fhsf + fhsg + fhsc + fhsh + fhse + fhsj + fhsk + fhsl + fhsp + fhsq + fhsm + fhsr + fhso
            + fhst + fhsu + fhsv + fhsw + fhsz + fhta + fhtb + fhtd + fhks + fhkt + fhku + fhlg + fhlh + fhli + fhma
            + fhmb + fhmc + fhmm + fhmn + fhnu + fhnv + fhnw + fhny + fhpa + fhpb + fhpd + fhpe + fhpf + fhph + fhpi
            + fhpj + fhpl + fhpm + fhpn + fhpo + fhpp + fhpr + fhps + fhpt + fhpu + fhpw + fhpx + fhpy + fhqe + fhqf
            + fhqg + fhqi + fhqo + fhqp + fhqr + fhqv + fhrg + fhri + fhrj + fhrk + fhrl + fhrm + fhro + fhrp
            + fhrq + fhrr + fhrt + fhru + fhrv + fhrw + fhry
            )

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        fhaa = foyer_fiscal('fhaa', period)
        fhab = foyer_fiscal('fhab', period)
        fhac = foyer_fiscal('fhac', period)
        fhae = foyer_fiscal('fhae', period)
        fhaf = foyer_fiscal('fhaf', period)
        fhag = foyer_fiscal('fhag', period)
        fhah = foyer_fiscal('fhah', period)
        fhaj = foyer_fiscal('fhaj', period)
        fhak = foyer_fiscal('fhak', period)
        fhal = foyer_fiscal('fhal', period)
        fham = foyer_fiscal('fham', period)
        fhao = foyer_fiscal('fhao', period)
        fhap = foyer_fiscal('fhap', period)
        fhaq = foyer_fiscal('fhaq', period)
        fhar = foyer_fiscal('fhar', period)
        fhat = foyer_fiscal('fhat', period)
        fhau = foyer_fiscal('fhau', period)
        fhav = foyer_fiscal('fhav', period)
        fhaw = foyer_fiscal('fhaw', period)
        fhay = foyer_fiscal('fhay', period)
        fhba = foyer_fiscal('fhba', period)
        fhbb = foyer_fiscal('fhbb', period)
        fhbe = foyer_fiscal('fhbe', period)
        fhbg = foyer_fiscal('fhbg', period)
        fhbi = foyer_fiscal('fhbi', period)
        fhbj = foyer_fiscal('fhbj', period)
        fhbk = foyer_fiscal('fhbk', period)
        fhbm = foyer_fiscal('fhbm', period)
        fhbn = foyer_fiscal('fhbn', period)
        fhbo = foyer_fiscal('fhbo', period)
        fhbp = foyer_fiscal('fhbp', period)
        fhbr = foyer_fiscal('fhbr', period)
        fhbs = foyer_fiscal('fhbs', period)
        fhbt = foyer_fiscal('fhbt', period)
        fhbu = foyer_fiscal('fhbu', period)
        fhbw = foyer_fiscal('fhbw', period)
        fhbx = foyer_fiscal('fhbx', period)
        fhby = foyer_fiscal('fhby', period)
        fhbz = foyer_fiscal('fhbz', period)
        fhcb = foyer_fiscal('fhcb', period)
        fhcc = foyer_fiscal('fhcc', period)
        fhcd = foyer_fiscal('fhcd', period)
        fhce = foyer_fiscal('fhce', period)
        fhcg = foyer_fiscal('fhcg', period)
        fhkt = foyer_fiscal('fhkt', period)
        fhku = foyer_fiscal('fhku', period)
        fhlh = foyer_fiscal('fhlh', period)
        fhli = foyer_fiscal('fhli', period)
        fhmb = foyer_fiscal('fhmb', period)
        fhmc = foyer_fiscal('fhmc', period)
        fhmn = foyer_fiscal('fhmn', period)
        fhnu = foyer_fiscal('fhnu', period)
        fhnv = foyer_fiscal('fhnv', period)
        fhnw = foyer_fiscal('fhnw', period)
        fhny = foyer_fiscal('fhny', period)
        fhpa = foyer_fiscal('fhpa', period)
        fhpb = foyer_fiscal('fhpb', period)
        fhpd = foyer_fiscal('fhpd', period)
        fhpe = foyer_fiscal('fhpe', period)
        fhpf = foyer_fiscal('fhpf', period)
        fhph = foyer_fiscal('fhph', period)
        fhpi = foyer_fiscal('fhpi', period)
        fhpj = foyer_fiscal('fhpj', period)
        fhpl = foyer_fiscal('fhpl', period)
        fhpm = foyer_fiscal('fhpm', period)
        fhpn = foyer_fiscal('fhpn', period)
        fhpo = foyer_fiscal('fhpo', period)
        fhpp = foyer_fiscal('fhpp', period)
        fhpr = foyer_fiscal('fhpr', period)
        fhps = foyer_fiscal('fhps', period)
        fhpt = foyer_fiscal('fhpt', period)
        fhpu = foyer_fiscal('fhpu', period)
        fhpw = foyer_fiscal('fhpw', period)
        fhpx = foyer_fiscal('fhpx', period)
        fhpy = foyer_fiscal('fhpy', period)
        fhqe = foyer_fiscal('fhqe', period)
        fhqf = foyer_fiscal('fhqf', period)
        fhqg = foyer_fiscal('fhqg', period)
        fhqi = foyer_fiscal('fhqi', period)
        fhqo = foyer_fiscal('fhqo', period)
        fhqp = foyer_fiscal('fhqp', period)
        fhqr = foyer_fiscal('fhqr', period)
        fhqv = foyer_fiscal('fhqv', period)
        fhrg = foyer_fiscal('fhrg', period)
        fhri = foyer_fiscal('fhri', period)
        fhrj = foyer_fiscal('fhrj', period)
        fhrk = foyer_fiscal('fhrk', period)
        fhrl = foyer_fiscal('fhrl', period)
        fhrm = foyer_fiscal('fhrm', period)
        fhro = foyer_fiscal('fhro', period)
        fhrp = foyer_fiscal('fhrp', period)
        fhrq = foyer_fiscal('fhrq', period)
        fhrr = foyer_fiscal('fhrr', period)
        fhrt = foyer_fiscal('fhrt', period)
        fhru = foyer_fiscal('fhru', period)
        fhrv = foyer_fiscal('fhrv', period)
        fhrw = foyer_fiscal('fhrw', period)
        fhry = foyer_fiscal('fhry', period)
        fhsa = foyer_fiscal('fhsa', period)
        fhsb = foyer_fiscal('fhsb', period)
        fhsc = foyer_fiscal('fhsc', period)
        fhse = foyer_fiscal('fhse', period)
        fhsf = foyer_fiscal('fhsf', period)
        fhsg = foyer_fiscal('fhsg', period)
        fhsh = foyer_fiscal('fhsh', period)
        fhsj = foyer_fiscal('fhsj', period)
        fhsk = foyer_fiscal('fhsk', period)
        fhsl = foyer_fiscal('fhsl', period)
        fhsm = foyer_fiscal('fhsm', period)
        fhso = foyer_fiscal('fhso', period)
        fhsp = foyer_fiscal('fhsp', period)
        fhsq = foyer_fiscal('fhsq', period)
        fhsr = foyer_fiscal('fhsr', period)
        fhst = foyer_fiscal('fhst', period)
        fhsu = foyer_fiscal('fhsu', period)
        fhsv = foyer_fiscal('fhsv', period)
        fhsw = foyer_fiscal('fhsw', period)
        fhsz = foyer_fiscal('fhsz', period)
        fhta = foyer_fiscal('fhta', period)
        fhtb = foyer_fiscal('fhtb', period)
        fhtd = foyer_fiscal('fhtd', period)

        return (
            fhbi + fhbj + fhbk + fhbm + fhbn + fhbo + fhbp + fhbr + fhbs + fhbt + fhbu + fhbw + fhbx + fhby + fhbz
            + fhcb + fhcc + fhcd + fhce + fhcg
            + fhaa + fhab + fhac + fhae + fhaf + fhag + fhah + fhaj + fhak + fhal + fham + fhao + fhap + fhaq + fhar
            + fhat + fhau + fhav + fhaw + fhay + fhba + fhbb + fhbe + fhbg
            + fhsa + fhsb + fhsf + fhsg + fhsc + fhsh + fhse + fhsj + fhsk + fhsl + fhsp + fhsq + fhsm + fhsr + fhso
            + fhst + fhsu + fhsv + fhsw + fhsz + fhta + fhtb + fhtd + fhkt + fhku + fhlh + fhli
            + fhmb + fhmc + fhmn + fhnu + fhnv + fhnw + fhny + fhpa + fhpb + fhpd + fhpe + fhpf + fhph + fhpi
            + fhpj + fhpl + fhpm + fhpn + fhpo + fhpp + fhpr + fhps + fhpt + fhpu + fhpw + fhpx + fhpy + fhqe + fhqf
            + fhqg + fhqi + fhqo + fhqp + fhqr + fhqv + fhrg + fhri + fhrj + fhrk + fhrl + fhrm + fhro + fhrp
            + fhrq + fhrr + fhrt + fhru + fhrv + fhrw + fhry
            )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.

        ATTENTION : Rupture important à partir de cette date, prise en compte du plafond.
        '''
        P10 = parameters('2010').impot_revenu.calcul_reductions_impots.outremer_investissement.doment.retrocession
        P11 = parameters('2011').impot_revenu.calcul_reductions_impots.outremer_investissement.doment.retrocession
        P15 = parameters('2015').impot_revenu.calcul_reductions_impots.outremer_investissement.doment.retrocession
        PP10 = parameters('2010').impot_revenu.calcul_reductions_impots.outremer_investissement
        PP11 = parameters('2011').impot_revenu.calcul_reductions_impots.outremer_investissement
        PP15 = parameters('2015').impot_revenu.calcul_reductions_impots.outremer_investissement

        fhqv = foyer_fiscal('fhqv', period)
        fhpm = foyer_fiscal('fhpm', period)
        fhrj = foyer_fiscal('fhrj', period)
        fhqe = foyer_fiscal('fhqe', period)

        fhnu = foyer_fiscal('fhnu', period)
        fhrk = foyer_fiscal('fhrk', period)
        fhrp = foyer_fiscal('fhrp', period)
        fhru = foyer_fiscal('fhru', period)
        fhpa = foyer_fiscal('fhpa', period)
        fhpe = foyer_fiscal('fhpe', period)
        fhpi = foyer_fiscal('fhpi', period)
        fhsz = foyer_fiscal('fhsz', period)
        fhsk = foyer_fiscal('fhsk', period)
        fhsp = foyer_fiscal('fhsp', period)
        fhsu = foyer_fiscal('fhsu', period)
        fhak = foyer_fiscal('fhak', period)
        fhap = foyer_fiscal('fhap', period)
        fhau = foyer_fiscal('fhau', period)
        fhba = foyer_fiscal('fhba', period)
        fhbi = foyer_fiscal('fhbi', period)
        fhbn = foyer_fiscal('fhbn', period)
        fhbs = foyer_fiscal('fhbs', period)
        fhbx = foyer_fiscal('fhbx', period)
        fhci = foyer_fiscal('fhci', period)
        fhcn = foyer_fiscal('fhcn', period)

        fhrl = foyer_fiscal('fhrl', period)
        fhrq = foyer_fiscal('fhrq', period)
        fhrv = foyer_fiscal('fhrv', period)
        fhpb = foyer_fiscal('fhpb', period)
        fhpf = foyer_fiscal('fhpf', period)
        fhpj = foyer_fiscal('fhpj', period)
        fhnv = foyer_fiscal('fhnv', period)
        fhsl = foyer_fiscal('fhsl', period)
        fhsq = foyer_fiscal('fhsq', period)
        fhsv = foyer_fiscal('fhsv', period)
        fhta = foyer_fiscal('fhta', period)
        fhal = foyer_fiscal('fhal', period)
        fhaq = foyer_fiscal('fhaq', period)
        fhav = foyer_fiscal('fhav', period)
        fhbb = foyer_fiscal('fhbb', period)
        fhbj = foyer_fiscal('fhbj', period)
        fhbo = foyer_fiscal('fhbo', period)
        fhbt = foyer_fiscal('fhbt', period)
        fhby = foyer_fiscal('fhby', period)
        fhcj = foyer_fiscal('fhcj', period)
        fhco = foyer_fiscal('fhco', period)

        fhcc = foyer_fiscal('fhcc', period)
        fhcs = foyer_fiscal('fhcs', period)

        fhcd = foyer_fiscal('fhcd', period)
        fhct = foyer_fiscal('fhct', period)

        fhpx = foyer_fiscal('fhpx', period)
        fhaa = foyer_fiscal('fhaa', period)
        fhaf = foyer_fiscal('fhaf', period)
        fhsa = foyer_fiscal('fhsa', period)
        fhsf = foyer_fiscal('fhsf', period)

        fhpy = foyer_fiscal('fhpy', period)
        fhab = foyer_fiscal('fhab', period)
        fhag = foyer_fiscal('fhag', period)
        fhsb = foyer_fiscal('fhsb', period)
        fhsg = foyer_fiscal('fhsg', period)

        fhpn = foyer_fiscal('fhpn', period)
        fhps = foyer_fiscal('fhps', period)
        fhqo = foyer_fiscal('fhqo', period)
        fhqf = foyer_fiscal('fhqf', period)

        fhpo = foyer_fiscal('fhpo', period)
        fhpt = foyer_fiscal('fhpt', period)
        fhqp = foyer_fiscal('fhqp', period)
        fhqg = foyer_fiscal('fhqg', period)

        inv_no_plaf = fhqv + fhpm + fhrj + fhqe

        inv_5263_306_34 = (fhnu + fhrk
            + fhrp + fhru + fhsz + fhsk
            + fhsp + fhsu + fhak + fhap
            + fhau + fhba + fhbi + fhbn
            + fhbs + fhbx + fhci + fhcn + fhpa
            + fhpe + fhpi)

        inv_625_306_51 = (fhrl + fhrq
            + fhrv + fhnv + fhsl + fhsq
            + fhsv + fhta + fhal + fhaq
            + fhav + fhbb + fhbj + fhbo
            + fhbt + fhby + fhcj + fhco + fhpb
            + fhpf + fhpj)

        inv_56_306_38945 = (fhcc
            + fhcs)

        inv_66_306_594 = (fhcd
            + fhct)

        inv_5263_36_40 = (fhpx
            + fhaa
            + fhaf
            + fhsa
            + fhsf)

        inv_625_36_60 = (fhpy
            + fhab
            + fhag
            + fhsb
            + fhsg)

        inv_50_40_40 = (fhpn
            + fhps
            + fhqo
            + fhqf)

        inv_60_40_60 = (fhpo
            + fhpt
            + fhqp
            + fhqg)

        nr_66_306_594 = min_(inv_66_306_594 * (1 - P15.taux_retro_1), max_(0, PP15.plafond))
        nr_625_36_60 = min_(inv_625_36_60 * (1 - P11.taux_retro_1), max_(0, PP11.plafond - nr_66_306_594))
        nr_625_306_51 = min_(inv_625_306_51 * (1 - P15.taux_retro_1), max_(0, PP15.plafond - nr_66_306_594 - nr_625_36_60))
        nr_60_40_60 = min_(inv_60_40_60 * (1 - P10.taux_retro_1), max_(0, PP10.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51))
        nr_56_306_38945 = min_(inv_56_306_38945 * (1 - P15.taux_retro_2), max_(0, PP15.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51 - nr_60_40_60))
        nr_5263_36_40 = min_(inv_5263_36_40 * (1 - P11.taux_retro_2), max_(0, PP11.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51 - nr_60_40_60 - nr_56_306_38945))
        nr_5263_306_34 = min_(inv_5263_306_34 * (1 - P15.taux_retro_2), max_(0, PP15.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51 - nr_60_40_60 - nr_56_306_38945 - nr_5263_36_40))
        nr_50_40_40 = min_(inv_50_40_40 * (1 - P10.taux_retro_2), max_(0, PP10.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51 - nr_60_40_60 - nr_56_306_38945 - nr_5263_36_40 - nr_5263_306_34))

        r_66_306_594 = nr_66_306_594 / (1 - P15.taux_retro_1) * P15.taux_retro_1
        r_625_36_60 = nr_625_36_60 / (1 - P11.taux_retro_1) * P11.taux_retro_1
        r_625_306_51 = nr_625_306_51 / (1 - P15.taux_retro_1) * P15.taux_retro_1
        r_60_40_60 = nr_60_40_60 / (1 - P10.taux_retro_1) * P10.taux_retro_1
        r_56_306_38945 = nr_56_306_38945 / (1 - P15.taux_retro_2) * P15.taux_retro_2
        r_5263_36_40 = nr_5263_36_40 / (1 - P11.taux_retro_2) * P11.taux_retro_2
        r_5263_306_34 = nr_5263_306_34 / (1 - P15.taux_retro_2) * P15.taux_retro_2
        r_50_40_40 = nr_50_40_40 / (1 - P10.taux_retro_2) * P10.taux_retro_2

        inv = (nr_66_306_594
            + nr_625_36_60
            + nr_625_306_51
            + nr_60_40_60
            + nr_56_306_38945
            + nr_5263_36_40
            + nr_5263_306_34
            + nr_50_40_40
            + r_66_306_594
            + r_625_36_60
            + r_625_306_51
            + r_60_40_60
            + r_56_306_38945
            + r_5263_36_40
            + r_5263_306_34
            + r_50_40_40)

        # propre entreprise

        # 30.6
        fhrm = foyer_fiscal('fhrm', period)
        fhrr = foyer_fiscal('fhrr', period)
        fhrw = foyer_fiscal('fhrw', period)
        fhnw = foyer_fiscal('fhnw', period)
        fhsm = foyer_fiscal('fhsm', period)
        fhsr = foyer_fiscal('fhsr', period)
        fhsw = foyer_fiscal('fhsw', period)
        fhtb = foyer_fiscal('fhtb', period)
        fham = foyer_fiscal('fham', period)
        fhar = foyer_fiscal('fhar', period)
        fhaw = foyer_fiscal('fhaw', period)
        fhbe = foyer_fiscal('fhbe', period)
        fhbk = foyer_fiscal('fhbk', period)
        fhbp = foyer_fiscal('fhbp', period)
        fhbu = foyer_fiscal('fhbu', period)
        fhbz = foyer_fiscal('fhbz', period)
        fhce = foyer_fiscal('fhce', period)
        fhck = foyer_fiscal('fhck', period)
        fhcp = foyer_fiscal('fhcp', period)
        fhcu = foyer_fiscal('fhcu', period)

        # 36
        fhrg = foyer_fiscal('fhrg', period)
        fhsc = foyer_fiscal('fhsc', period)
        fhsh = foyer_fiscal('fhsh', period)
        fhac = foyer_fiscal('fhac', period)
        fhah = foyer_fiscal('fhah', period)

        # 40
        fhpp = foyer_fiscal('fhpp', period)
        fhpu = foyer_fiscal('fhpu', period)
        fhqr = foyer_fiscal('fhqr', period)
        fhqi = foyer_fiscal('fhqi', period)

        # 76.5
        fhro = foyer_fiscal('fhro', period)
        fhrt = foyer_fiscal('fhrt', period)
        fhry = foyer_fiscal('fhry', period)
        fhpd = foyer_fiscal('fhpd', period)
        fhph = foyer_fiscal('fhph', period)
        fhpl = foyer_fiscal('fhpl', period)
        fhny = foyer_fiscal('fhny', period)
        fhso = foyer_fiscal('fhso', period)
        fhst = foyer_fiscal('fhst', period)
        fhsy = foyer_fiscal('fhsy', period)
        fhtd = foyer_fiscal('fhtd', period)
        fhao = foyer_fiscal('fhao', period)
        fhat = foyer_fiscal('fhat', period)
        fhay = foyer_fiscal('fhay', period)
        fhbg = foyer_fiscal('fhbg', period)
        fhbm = foyer_fiscal('fhbm', period)
        fhbr = foyer_fiscal('fhbr', period)
        fhbw = foyer_fiscal('fhbw', period)
        fhcb = foyer_fiscal('fhcb', period)
        fhcg = foyer_fiscal('fhcg', period)
        fhcm = foyer_fiscal('fhcm', period)
        fhcr = foyer_fiscal('fhcr', period)
        fhcw = foyer_fiscal('fhcw', period)

        # 90
        fhri = foyer_fiscal('fhri', period)
        fhse = foyer_fiscal('fhse', period)
        fhsj = foyer_fiscal('fhsj', period)
        fhae = foyer_fiscal('fhae', period)
        fhaj = foyer_fiscal('fhaj', period)

        # 100
        fhpr = foyer_fiscal('fhpr', period)
        fhpw = foyer_fiscal('fhpw', period)

        propre_306 = (fhrm + fhrr + fhrw + fham
            + fhnw + fhsm + fhsr + fhsw
            + fhtb + fhar + fhaw + fhbe
            + fhbk + fhbp + fhbu + fhbz
            + fhce + fhck + fhcp + fhcu)

        propre_36 = (fhrg
            + fhsc + fhsh
            + fhac + fhah)

        propre_40 = fhpp + fhpu + fhqr + fhqi

        propre_765 = (fhro + fhrt + fhry
            + fhpd + fhph + fhpl + fhao
            + fhny + fhso + fhst + fhsy
            + fhtd + fhat + fhay + fhbg
            + fhbm + fhbr + fhbw + fhcb
            + fhcg + fhcm + fhcr + fhcw)

        propre_90 = (fhri
            + fhse
            + fhsj
            + fhae
            + fhaj)

        propre_100 = fhpr + fhpw

        ri_propre = (min_(PP10.plafond, propre_40)
            + min_(PP11.plafond, propre_36)
            + min_(PP15.plafond, propre_306)
            + min_(PP10.plafond * PP10.doment.propre_entreprise.majoration, propre_100)
            + min_(PP11.plafond * PP11.doment.propre_entreprise.majoration, propre_90)
            + min_(PP15.plafond * PP15.doment.propre_entreprise.majoration, propre_765))

        return ri_propre + inv_no_plaf + inv

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        P10 = parameters('2010').impot_revenu.calcul_reductions_impots.outremer_investissement.doment.retrocession
        P11 = parameters('2011').impot_revenu.calcul_reductions_impots.outremer_investissement.doment.retrocession
        P15 = parameters('2015').impot_revenu.calcul_reductions_impots.outremer_investissement.doment.retrocession
        PP10 = parameters('2010').impot_revenu.calcul_reductions_impots.outremer_investissement
        PP11 = parameters('2011').impot_revenu.calcul_reductions_impots.outremer_investissement
        PP15 = parameters('2015').impot_revenu.calcul_reductions_impots.outremer_investissement

        fhpm = foyer_fiscal('fhpm', period)
        fhrj = foyer_fiscal('fhrj', period)

        fhdi = foyer_fiscal('fhdi', period)
        fhdn = foyer_fiscal('fhdn', period)
        fhnu = foyer_fiscal('fhnu', period)
        fhrk = foyer_fiscal('fhrk', period)
        fhrp = foyer_fiscal('fhrp', period)
        fhru = foyer_fiscal('fhru', period)
        fhsz = foyer_fiscal('fhsz', period)
        fhsk = foyer_fiscal('fhsk', period)
        fhsp = foyer_fiscal('fhsp', period)
        fhsu = foyer_fiscal('fhsu', period)
        fhak = foyer_fiscal('fhak', period)
        fhap = foyer_fiscal('fhap', period)
        fhau = foyer_fiscal('fhau', period)
        fhba = foyer_fiscal('fhba', period)
        fhbi = foyer_fiscal('fhbi', period)
        fhbn = foyer_fiscal('fhbn', period)
        fhbs = foyer_fiscal('fhbs', period)
        fhbx = foyer_fiscal('fhbx', period)
        fhci = foyer_fiscal('fhci', period)
        fhcn = foyer_fiscal('fhcn', period)

        fhdj = foyer_fiscal('fhdj', period)
        fhdo = foyer_fiscal('fhdo', period)
        fhrl = foyer_fiscal('fhrl', period)
        fhrq = foyer_fiscal('fhrq', period)
        fhrv = foyer_fiscal('fhrv', period)
        fhnv = foyer_fiscal('fhnv', period)
        fhsl = foyer_fiscal('fhsl', period)
        fhsq = foyer_fiscal('fhsq', period)
        fhsv = foyer_fiscal('fhsv', period)
        fhta = foyer_fiscal('fhta', period)
        fhal = foyer_fiscal('fhal', period)
        fhaq = foyer_fiscal('fhaq', period)
        fhav = foyer_fiscal('fhav', period)
        fhbb = foyer_fiscal('fhbb', period)
        fhbj = foyer_fiscal('fhbj', period)
        fhbo = foyer_fiscal('fhbo', period)
        fhbt = foyer_fiscal('fhbt', period)
        fhby = foyer_fiscal('fhby', period)
        fhcj = foyer_fiscal('fhcj', period)
        fhco = foyer_fiscal('fhco', period)

        fhds = foyer_fiscal('fhds', period)
        fhcc = foyer_fiscal('fhcc', period)
        fhcs = foyer_fiscal('fhcs', period)

        fhdt = foyer_fiscal('fhdt', period)
        fhcd = foyer_fiscal('fhcd', period)
        fhct = foyer_fiscal('fhct', period)

        fhpx = foyer_fiscal('fhpx', period)
        fhaa = foyer_fiscal('fhaa', period)
        fhaf = foyer_fiscal('fhaf', period)
        fhsa = foyer_fiscal('fhsa', period)
        fhsf = foyer_fiscal('fhsf', period)

        fhpy = foyer_fiscal('fhpy', period)
        fhab = foyer_fiscal('fhab', period)
        fhag = foyer_fiscal('fhag', period)
        fhsb = foyer_fiscal('fhsb', period)
        fhsg = foyer_fiscal('fhsg', period)

        fhpn = foyer_fiscal('fhpn', period)
        fhps = foyer_fiscal('fhps', period)

        fhpo = foyer_fiscal('fhpo', period)
        fhpt = foyer_fiscal('fhpt', period)

        inv_no_plaf = fhpm + fhrj

        inv_5263_306_34 = (fhdi + fhdn + fhnu + fhrk
            + fhrp + fhru + fhsz + fhsk
            + fhsp + fhsu + fhak + fhap
            + fhau + fhba + fhbi + fhbn
            + fhbs + fhbx + fhci + fhcn)

        inv_625_306_51 = (fhdj + fhdo + fhrl + fhrq
            + fhrv + fhnv + fhsl + fhsq
            + fhsv + fhta + fhal + fhaq
            + fhav + fhbb + fhbj + fhbo
            + fhbt + fhby + fhcj + fhco)

        inv_56_306_38945 = (fhds
            + fhcc
            + fhcs)

        inv_66_306_594 = (fhdt
            + fhcd
            + fhct)

        inv_5263_36_40 = (fhpx
            + fhaa
            + fhaf
            + fhsa
            + fhsf)

        inv_625_36_60 = (fhpy
            + fhab
            + fhag
            + fhsb
            + fhsg)

        inv_50_40_40 = (fhpn
            + fhps)

        inv_60_40_60 = (fhpo
            + fhpt)

        nr_66_306_594 = min_(inv_66_306_594 * (1 - P15.taux_retro_1), max_(0, PP15.plafond))
        nr_625_36_60 = min_(inv_625_36_60 * (1 - P11.taux_retro_1), max_(0, PP11.plafond - nr_66_306_594))
        nr_625_306_51 = min_(inv_625_306_51 * (1 - P15.taux_retro_1), max_(0, PP15.plafond - nr_66_306_594 - nr_625_36_60))
        nr_60_40_60 = min_(inv_60_40_60 * (1 - P10.taux_retro_1), max_(0, PP10.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51))
        nr_56_306_38945 = min_(inv_56_306_38945 * (1 - P15.taux_retro_2), max_(0, PP15.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51 - nr_60_40_60))
        nr_5263_36_40 = min_(inv_5263_36_40 * (1 - P11.taux_retro_2), max_(0, PP11.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51 - nr_60_40_60 - nr_56_306_38945))
        nr_5263_306_34 = min_(inv_5263_306_34 * (1 - P15.taux_retro_2), max_(0, PP15.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51 - nr_60_40_60 - nr_56_306_38945 - nr_5263_36_40))
        nr_50_40_40 = min_(inv_50_40_40 * (1 - P10.taux_retro_2), max_(0, PP10.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51 - nr_60_40_60 - nr_56_306_38945 - nr_5263_36_40 - nr_5263_306_34))

        r_66_306_594 = nr_66_306_594 / (1 - P15.taux_retro_1) * P15.taux_retro_1
        r_625_36_60 = nr_625_36_60 / (1 - P11.taux_retro_1) * P11.taux_retro_1
        r_625_306_51 = nr_625_306_51 / (1 - P15.taux_retro_1) * P15.taux_retro_1
        r_60_40_60 = nr_60_40_60 / (1 - P10.taux_retro_1) * P10.taux_retro_1
        r_56_306_38945 = nr_56_306_38945 / (1 - P15.taux_retro_2) * P15.taux_retro_2
        r_5263_36_40 = nr_5263_36_40 / (1 - P11.taux_retro_2) * P11.taux_retro_2
        r_5263_306_34 = nr_5263_306_34 / (1 - P15.taux_retro_2) * P15.taux_retro_2
        r_50_40_40 = nr_50_40_40 / (1 - P10.taux_retro_2) * P10.taux_retro_2

        inv = (nr_66_306_594
            + nr_625_36_60
            + nr_625_306_51
            + nr_60_40_60
            + nr_56_306_38945
            + nr_5263_36_40
            + nr_5263_306_34
            + nr_50_40_40
            + r_66_306_594
            + r_625_36_60
            + r_625_306_51
            + r_60_40_60
            + r_56_306_38945
            + r_5263_36_40
            + r_5263_306_34
            + r_50_40_40)

        # propre entreprise

        # 30.6
        fhdk = foyer_fiscal('fhdk', period)
        fhdp = foyer_fiscal('fhdp', period)
        fhdu = foyer_fiscal('fhdu', period)
        fhrm = foyer_fiscal('fhrm', period)
        fhrr = foyer_fiscal('fhrr', period)
        fhrw = foyer_fiscal('fhrw', period)
        fhnw = foyer_fiscal('fhnw', period)
        fhsm = foyer_fiscal('fhsm', period)
        fhsr = foyer_fiscal('fhsr', period)
        fhsw = foyer_fiscal('fhsw', period)
        fhtb = foyer_fiscal('fhtb', period)
        fham = foyer_fiscal('fham', period)
        fhar = foyer_fiscal('fhar', period)
        fhaw = foyer_fiscal('fhaw', period)
        fhbe = foyer_fiscal('fhbe', period)
        fhbk = foyer_fiscal('fhbk', period)
        fhbp = foyer_fiscal('fhbp', period)
        fhbu = foyer_fiscal('fhbu', period)
        fhbz = foyer_fiscal('fhbz', period)
        fhce = foyer_fiscal('fhce', period)
        fhck = foyer_fiscal('fhck', period)
        fhcp = foyer_fiscal('fhcp', period)
        fhcu = foyer_fiscal('fhcu', period)

        # 36
        fhrg = foyer_fiscal('fhrg', period)
        fhsc = foyer_fiscal('fhsc', period)
        fhsh = foyer_fiscal('fhsh', period)
        fhac = foyer_fiscal('fhac', period)
        fhah = foyer_fiscal('fhah', period)

        # 40
        fhpp = foyer_fiscal('fhpp', period)
        fhpu = foyer_fiscal('fhpu', period)

        # 76.5
        fhdm = foyer_fiscal('fhdm', period)
        fhdr = foyer_fiscal('fhdr', period)
        fhdw = foyer_fiscal('fhdw', period)
        fhro = foyer_fiscal('fhro', period)
        fhrt = foyer_fiscal('fhrt', period)
        fhry = foyer_fiscal('fhry', period)
        fhny = foyer_fiscal('fhny', period)
        fhso = foyer_fiscal('fhso', period)
        fhst = foyer_fiscal('fhst', period)
        fhsy = foyer_fiscal('fhsy', period)
        fhtd = foyer_fiscal('fhtd', period)
        fhao = foyer_fiscal('fhao', period)
        fhat = foyer_fiscal('fhat', period)
        fhay = foyer_fiscal('fhay', period)
        fhbg = foyer_fiscal('fhbg', period)
        fhbm = foyer_fiscal('fhbm', period)
        fhbr = foyer_fiscal('fhbr', period)
        fhbw = foyer_fiscal('fhbw', period)
        fhcb = foyer_fiscal('fhcb', period)
        fhcg = foyer_fiscal('fhcg', period)
        fhcm = foyer_fiscal('fhcm', period)
        fhcr = foyer_fiscal('fhcr', period)
        fhcw = foyer_fiscal('fhcw', period)

        # 90
        fhri = foyer_fiscal('fhri', period)
        fhse = foyer_fiscal('fhse', period)
        fhsj = foyer_fiscal('fhsj', period)
        fhae = foyer_fiscal('fhae', period)
        fhaj = foyer_fiscal('fhaj', period)

        # 100
        fhpr = foyer_fiscal('fhpr', period)
        fhpw = foyer_fiscal('fhpw', period)

        propre_306 = (fhdk + fhdp + fham
            + fhdu + fhrm + fhrr + fhrw
            + fhnw + fhsm + fhsr + fhsw
            + fhtb + fhar + fhaw + fhbe
            + fhbk + fhbp + fhbu + fhbz
            + fhce + fhck + fhcp + fhcu)

        propre_36 = (fhrg
            + fhsc + fhsh
            + fhac + fhah)

        propre_40 = fhpp + fhpu

        propre_765 = (fhdm + fhdr + fhao
            + fhdw + fhro + fhrt + fhry
            + fhny + fhso + fhst + fhsy
            + fhtd + fhat + fhay + fhbg
            + fhbm + fhbr + fhbw + fhcb
            + fhcg + fhcm + fhcr + fhcw)

        propre_90 = (fhri
            + fhse
            + fhsj
            + fhae
            + fhaj)

        propre_100 = fhpr + fhpw

        ri_propre = (min_(PP10.plafond, propre_40)
            + min_(PP11.plafond, propre_36)
            + min_(PP15.plafond, propre_306)
            + min_(PP10.plafond * PP10.doment.propre_entreprise.majoration, propre_100)
            + min_(PP11.plafond * PP11.doment.propre_entreprise.majoration, propre_90)
            + min_(PP15.plafond * PP15.doment.propre_entreprise.majoration, propre_765))

        return ri_propre + inv_no_plaf + inv

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        P11 = parameters('2011').impot_revenu.calcul_reductions_impots.outremer_investissement.doment.retrocession
        P15 = parameters('2015').impot_revenu.calcul_reductions_impots.outremer_investissement.doment.retrocession
        PP11 = parameters('2011').impot_revenu.calcul_reductions_impots.outremer_investissement
        PP15 = parameters('2015').impot_revenu.calcul_reductions_impots.outremer_investissement

        fhdi = foyer_fiscal('fhdi', period)
        fhdn = foyer_fiscal('fhdn', period)
        fhen = foyer_fiscal('fhen', period)
        fhsz = foyer_fiscal('fhsz', period)
        fhsk = foyer_fiscal('fhsk', period)
        fhsp = foyer_fiscal('fhsp', period)
        fhsu = foyer_fiscal('fhsu', period)
        fhak = foyer_fiscal('fhak', period)
        fhap = foyer_fiscal('fhap', period)
        fhau = foyer_fiscal('fhau', period)
        fhba = foyer_fiscal('fhba', period)
        fhbi = foyer_fiscal('fhbi', period)
        fhbn = foyer_fiscal('fhbn', period)
        fhbs = foyer_fiscal('fhbs', period)
        fhbx = foyer_fiscal('fhbx', period)
        fhci = foyer_fiscal('fhci', period)
        fhcn = foyer_fiscal('fhcn', period)

        fhdj = foyer_fiscal('fhdj', period)
        fhdo = foyer_fiscal('fhdo', period)
        fheo = foyer_fiscal('fheo', period)
        fhsl = foyer_fiscal('fhsl', period)
        fhsq = foyer_fiscal('fhsq', period)
        fhsv = foyer_fiscal('fhsv', period)
        fhta = foyer_fiscal('fhta', period)
        fhal = foyer_fiscal('fhal', period)
        fhaq = foyer_fiscal('fhaq', period)
        fhav = foyer_fiscal('fhav', period)
        fhbb = foyer_fiscal('fhbb', period)
        fhbj = foyer_fiscal('fhbj', period)
        fhbo = foyer_fiscal('fhbo', period)
        fhbt = foyer_fiscal('fhbt', period)
        fhby = foyer_fiscal('fhby', period)
        fhcj = foyer_fiscal('fhcj', period)
        fhco = foyer_fiscal('fhco', period)

        fhds = foyer_fiscal('fhds', period)
        fhes = foyer_fiscal('fhes', period)
        fhcc = foyer_fiscal('fhcc', period)
        fhcs = foyer_fiscal('fhcs', period)

        fhdt = foyer_fiscal('fhdt', period)
        fhet = foyer_fiscal('fhet', period)
        fhcd = foyer_fiscal('fhcd', period)
        fhct = foyer_fiscal('fhct', period)

        fhaa = foyer_fiscal('fhaa', period)
        fhaf = foyer_fiscal('fhaf', period)
        fhsa = foyer_fiscal('fhsa', period)
        fhsf = foyer_fiscal('fhsf', period)

        fhab = foyer_fiscal('fhab', period)
        fhag = foyer_fiscal('fhag', period)
        fhsb = foyer_fiscal('fhsb', period)
        fhsg = foyer_fiscal('fhsg', period)

        inv_5263_306_34 = (fhdi + fhdn + fhen + fhsz + fhsk
            + fhsp + fhsu + fhak + fhap
            + fhau + fhba + fhbi + fhbn
            + fhbs + fhbx + fhci + fhcn)

        inv_625_306_51 = (fhdj + fhdo + fheo + fhsl + fhsq
            + fhsv + fhta + fhal + fhaq
            + fhav + fhbb + fhbj + fhbo
            + fhbt + fhby + fhcj + fhco)

        inv_56_306_38945 = (fhds
            + fhes
            + fhcc
            + fhcs)

        inv_66_306_594 = (fhdt
            + fhet
            + fhcd
            + fhct)

        inv_5263_36_40 = (fhaa
            + fhaf
            + fhsa
            + fhsf)

        inv_625_36_60 = (fhab
            + fhag
            + fhsb
            + fhsg)

        nr_66_306_594 = min_(inv_66_306_594 * (1 - P15.taux_retro_1), max_(0, PP15.plafond))
        nr_625_36_60 = min_(inv_625_36_60 * (1 - P11.taux_retro_1), max_(0, PP11.plafond - nr_66_306_594))
        nr_625_306_51 = min_(inv_625_306_51 * (1 - P15.taux_retro_1), max_(0, PP15.plafond - nr_66_306_594 - nr_625_36_60))
        nr_56_306_38945 = min_(inv_56_306_38945 * (1 - P15.taux_retro_2), max_(0, PP15.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51))
        nr_5263_36_40 = min_(inv_5263_36_40 * (1 - P11.taux_retro_2), max_(0, PP11.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51 - nr_56_306_38945))
        nr_5263_306_34 = min_(inv_5263_306_34 * (1 - P15.taux_retro_2), max_(0, PP15.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51 - nr_56_306_38945 - nr_5263_36_40))

        r_66_306_594 = nr_66_306_594 / (1 - P15.taux_retro_1) * P15.taux_retro_1
        r_625_36_60 = nr_625_36_60 / (1 - P11.taux_retro_1) * P11.taux_retro_1
        r_625_306_51 = nr_625_306_51 / (1 - P15.taux_retro_1) * P15.taux_retro_1
        r_56_306_38945 = nr_56_306_38945 / (1 - P15.taux_retro_2) * P15.taux_retro_2
        r_5263_36_40 = nr_5263_36_40 / (1 - P11.taux_retro_2) * P11.taux_retro_2
        r_5263_306_34 = nr_5263_306_34 / (1 - P15.taux_retro_2) * P15.taux_retro_2

        inv = (nr_66_306_594
            + nr_625_36_60
            + nr_625_306_51
            + nr_56_306_38945
            + nr_5263_36_40
            + nr_5263_306_34
            + r_66_306_594
            + r_625_36_60
            + r_625_306_51
            + r_56_306_38945
            + r_5263_36_40
            + r_5263_306_34)

        # propre entreprise

        # 30.6
        fhdk = foyer_fiscal('fhdk', period)
        fhdp = foyer_fiscal('fhdp', period)
        fhep = foyer_fiscal('fhep', period)
        fhdu = foyer_fiscal('fhdu', period)
        fheu = foyer_fiscal('fheu', period)
        fhsm = foyer_fiscal('fhsm', period)
        fhsr = foyer_fiscal('fhsr', period)
        fhsw = foyer_fiscal('fhsw', period)
        fhtb = foyer_fiscal('fhtb', period)
        fham = foyer_fiscal('fham', period)
        fhar = foyer_fiscal('fhar', period)
        fhaw = foyer_fiscal('fhaw', period)
        fhbe = foyer_fiscal('fhbe', period)
        fhbk = foyer_fiscal('fhbk', period)
        fhbp = foyer_fiscal('fhbp', period)
        fhbu = foyer_fiscal('fhbu', period)
        fhbz = foyer_fiscal('fhbz', period)
        fhce = foyer_fiscal('fhce', period)
        fhck = foyer_fiscal('fhck', period)
        fhcp = foyer_fiscal('fhcp', period)
        fhcu = foyer_fiscal('fhcu', period)

        # 36
        fhsc = foyer_fiscal('fhsc', period)
        fhsh = foyer_fiscal('fhsh', period)
        fhac = foyer_fiscal('fhac', period)
        fhah = foyer_fiscal('fhah', period)

        # 76.5
        fhdm = foyer_fiscal('fhdm', period)
        fhdr = foyer_fiscal('fhdr', period)
        fher = foyer_fiscal('fher', period)
        fhdw = foyer_fiscal('fhdw', period)
        fhew = foyer_fiscal('fhew', period)
        fhso = foyer_fiscal('fhso', period)
        fhst = foyer_fiscal('fhst', period)
        fhsy = foyer_fiscal('fhsy', period)
        fhtd = foyer_fiscal('fhtd', period)
        fhao = foyer_fiscal('fhao', period)
        fhat = foyer_fiscal('fhat', period)
        fhay = foyer_fiscal('fhay', period)
        fhbg = foyer_fiscal('fhbg', period)
        fhbm = foyer_fiscal('fhbm', period)
        fhbr = foyer_fiscal('fhbr', period)
        fhbw = foyer_fiscal('fhbw', period)
        fhcb = foyer_fiscal('fhcb', period)
        fhcg = foyer_fiscal('fhcg', period)
        fhcm = foyer_fiscal('fhcm', period)
        fhcr = foyer_fiscal('fhcr', period)
        fhcw = foyer_fiscal('fhcw', period)

        # 90
        fhse = foyer_fiscal('fhse', period)
        fhsj = foyer_fiscal('fhsj', period)
        fhae = foyer_fiscal('fhae', period)
        fhaj = foyer_fiscal('fhaj', period)

        propre_306 = (fhdk + fhdp
            + fhdu + fhep + fham
            + fheu + fhsm + fhsr + fhsw
            + fhtb + fhar + fhaw + fhbe
            + fhbk + fhbp + fhbu + fhbz
            + fhce + fhck + fhcp + fhcu)

        propre_36 = (fhsc + fhsh
            + fhac + fhah)

        propre_765 = (fhdm + fhdr
            + fhdw + fher + fhew
            + fhso + fhst + fhsy + fhao
            + fhtd + fhat + fhay + fhbg
            + fhbm + fhbr + fhbw + fhcb
            + fhcg + fhcm + fhcr + fhcw)

        propre_90 = (fhse
            + fhsj
            + fhae
            + fhaj)

        ri_propre = (min_(PP11.plafond, propre_36)
            + min_(PP15.plafond, propre_306)
            + min_(PP11.plafond * PP11.doment.propre_entreprise.majoration, propre_90)
            + min_(PP15.plafond * PP15.doment.propre_entreprise.majoration, propre_765))

        return ri_propre + inv

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        P11 = parameters('2011').impot_revenu.calcul_reductions_impots.outremer_investissement.doment.retrocession
        P15 = parameters('2015').impot_revenu.calcul_reductions_impots.outremer_investissement.doment.retrocession
        PP11 = parameters('2011').impot_revenu.calcul_reductions_impots.outremer_investissement
        PP15 = parameters('2015').impot_revenu.calcul_reductions_impots.outremer_investissement

        fhdi = foyer_fiscal('fhdi', period)
        fhdn = foyer_fiscal('fhdn', period)
        fhen = foyer_fiscal('fhen', period)
        fhfn = foyer_fiscal('fhfn', period)
        fhak = foyer_fiscal('fhak', period)
        fhap = foyer_fiscal('fhap', period)
        fhau = foyer_fiscal('fhau', period)
        fhba = foyer_fiscal('fhba', period)
        fhbi = foyer_fiscal('fhbi', period)
        fhbn = foyer_fiscal('fhbn', period)
        fhbs = foyer_fiscal('fhbs', period)
        fhbx = foyer_fiscal('fhbx', period)
        fhci = foyer_fiscal('fhci', period)
        fhcn = foyer_fiscal('fhcn', period)

        fhdj = foyer_fiscal('fhdj', period)
        fhdo = foyer_fiscal('fhdo', period)
        fheo = foyer_fiscal('fheo', period)
        fhfo = foyer_fiscal('fhfo', period)
        fhal = foyer_fiscal('fhal', period)
        fhaq = foyer_fiscal('fhaq', period)
        fhav = foyer_fiscal('fhav', period)
        fhbb = foyer_fiscal('fhbb', period)
        fhbj = foyer_fiscal('fhbj', period)
        fhbo = foyer_fiscal('fhbo', period)
        fhbt = foyer_fiscal('fhbt', period)
        fhby = foyer_fiscal('fhby', period)
        fhcj = foyer_fiscal('fhcj', period)
        fhco = foyer_fiscal('fhco', period)

        fhds = foyer_fiscal('fhds', period)
        fhes = foyer_fiscal('fhes', period)
        fhfs = foyer_fiscal('fhfs', period)
        fhcc = foyer_fiscal('fhcc', period)
        fhcs = foyer_fiscal('fhcs', period)

        fhdt = foyer_fiscal('fhdt', period)
        fhet = foyer_fiscal('fhet', period)
        fhft = foyer_fiscal('fhft', period)
        fhcd = foyer_fiscal('fhcd', period)
        fhct = foyer_fiscal('fhct', period)

        fhaa = foyer_fiscal('fhaa', period)
        fhaf = foyer_fiscal('fhaf', period)

        fhab = foyer_fiscal('fhab', period)
        fhag = foyer_fiscal('fhag', period)

        inv_5263_306_34 = (fhdi + fhdn + fhen + fhfn
            + fhak + fhap
            + fhau + fhba + fhbi + fhbn
            + fhbs + fhbx + fhci + fhcn)

        inv_625_306_51 = (fhdj + fhdo + fheo + fhfo
            + fhal + fhaq
            + fhav + fhbb + fhbj + fhbo
            + fhbt + fhby + fhcj + fhco)

        inv_56_306_38945 = (fhds
            + fhes
            + fhfs
            + fhcc
            + fhcs)

        inv_66_306_594 = (fhdt
            + fhet
            + fhft
            + fhcd
            + fhct)

        inv_5263_36_40 = (fhaa
            + fhaf)

        inv_625_36_60 = (fhab
            + fhag)

        nr_66_306_594 = min_(inv_66_306_594 * (1 - P15.taux_retro_1), max_(0, PP15.plafond))
        nr_625_36_60 = min_(inv_625_36_60 * (1 - P11.taux_retro_1), max_(0, PP11.plafond - nr_66_306_594))
        nr_625_306_51 = min_(inv_625_306_51 * (1 - P15.taux_retro_1), max_(0, PP15.plafond - nr_66_306_594 - nr_625_36_60))
        nr_56_306_38945 = min_(inv_56_306_38945 * (1 - P15.taux_retro_2), max_(0, PP15.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51))
        nr_5263_36_40 = min_(inv_5263_36_40 * (1 - P11.taux_retro_2), max_(0, PP11.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51 - nr_56_306_38945))
        nr_5263_306_34 = min_(inv_5263_306_34 * (1 - P15.taux_retro_2), max_(0, PP15.plafond - nr_66_306_594 - nr_625_36_60 - nr_625_306_51 - nr_56_306_38945 - nr_5263_36_40))

        r_66_306_594 = nr_66_306_594 / (1 - P15.taux_retro_1) * P15.taux_retro_1
        r_625_36_60 = nr_625_36_60 / (1 - P11.taux_retro_1) * P11.taux_retro_1
        r_625_306_51 = nr_625_306_51 / (1 - P15.taux_retro_1) * P15.taux_retro_1
        r_56_306_38945 = nr_56_306_38945 / (1 - P15.taux_retro_2) * P15.taux_retro_2
        r_5263_36_40 = nr_5263_36_40 / (1 - P11.taux_retro_2) * P11.taux_retro_2
        r_5263_306_34 = nr_5263_306_34 / (1 - P15.taux_retro_2) * P15.taux_retro_2

        inv = (nr_66_306_594
            + nr_625_36_60
            + nr_625_306_51
            + nr_56_306_38945
            + nr_5263_36_40
            + nr_5263_306_34
            + r_66_306_594
            + r_625_36_60
            + r_625_306_51
            + r_56_306_38945
            + r_5263_36_40
            + r_5263_306_34)

        # propre entreprise

        # 30.6
        fhdk = foyer_fiscal('fhdk', period)
        fhdp = foyer_fiscal('fhdp', period)
        fhep = foyer_fiscal('fhep', period)
        fhfp = foyer_fiscal('fhfp', period)
        fhdu = foyer_fiscal('fhdu', period)
        fheu = foyer_fiscal('fheu', period)
        fhfu = foyer_fiscal('fhfu', period)
        fham = foyer_fiscal('fham', period)
        fhar = foyer_fiscal('fhar', period)
        fhaw = foyer_fiscal('fhaw', period)
        fhbe = foyer_fiscal('fhbe', period)
        fhbk = foyer_fiscal('fhbk', period)
        fhbp = foyer_fiscal('fhbp', period)
        fhbu = foyer_fiscal('fhbu', period)
        fhbz = foyer_fiscal('fhbz', period)
        fhce = foyer_fiscal('fhce', period)
        fhck = foyer_fiscal('fhck', period)
        fhcp = foyer_fiscal('fhcp', period)
        fhcu = foyer_fiscal('fhcu', period)

        # 36
        fhac = foyer_fiscal('fhac', period)
        fhah = foyer_fiscal('fhah', period)

        # 76.5
        fhdm = foyer_fiscal('fhdm', period)
        fhdr = foyer_fiscal('fhdr', period)
        fher = foyer_fiscal('fher', period)
        fhfr = foyer_fiscal('fhfr', period)
        fhdw = foyer_fiscal('fhdw', period)
        fhew = foyer_fiscal('fhew', period)
        fhfw = foyer_fiscal('fhfw', period)
        fhao = foyer_fiscal('fhao', period)
        fhat = foyer_fiscal('fhat', period)
        fhay = foyer_fiscal('fhay', period)
        fhbg = foyer_fiscal('fhbg', period)
        fhbm = foyer_fiscal('fhbm', period)
        fhbr = foyer_fiscal('fhbr', period)
        fhbw = foyer_fiscal('fhbw', period)
        fhcb = foyer_fiscal('fhcb', period)
        fhcg = foyer_fiscal('fhcg', period)
        fhcm = foyer_fiscal('fhcm', period)
        fhcr = foyer_fiscal('fhcr', period)
        fhcw = foyer_fiscal('fhcw', period)

        # 90
        fhae = foyer_fiscal('fhae', period)
        fhaj = foyer_fiscal('fhaj', period)

        propre_306 = (fhdk + fhdp
            + fhdu + fhep
            + fheu + fhfp + fham
            + fhfu + fhar + fhaw + fhbe
            + fhbk + fhbp + fhbu + fhbz
            + fhce + fhck + fhcp + fhcu)

        propre_36 = (fhac + fhah)

        propre_765 = (fhdm + fhdr
            + fhdw + fher + fhew
            + fhfr + fhao
            + fhfw + fhat + fhay + fhbg
            + fhbm + fhbr + fhbw + fhcb
            + fhcg + fhcm + fhcr + fhcw)

        propre_90 = (fhae
            + fhaj)

        ri_propre = (min_(PP11.plafond, propre_36)
            + min_(PP15.plafond, propre_306)
            + min_(PP11.plafond * PP11.doment.propre_entreprise.majoration, propre_90)
            + min_(PP15.plafond * PP15.doment.propre_entreprise.majoration, propre_765))

        return ri_propre + inv

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        P15 = parameters('2015').impot_revenu.calcul_reductions_impots.outremer_investissement.doment.retrocession
        PP15 = parameters('2015').impot_revenu.calcul_reductions_impots.outremer_investissement

        fhdi = foyer_fiscal('fhdi', period)
        fhdn = foyer_fiscal('fhdn', period)
        fhen = foyer_fiscal('fhen', period)
        fhfn = foyer_fiscal('fhfn', period)
        fhbi = foyer_fiscal('fhbi', period)
        fhbn = foyer_fiscal('fhbn', period)
        fhbs = foyer_fiscal('fhbs', period)
        fhbx = foyer_fiscal('fhbx', period)
        fhci = foyer_fiscal('fhci', period)
        fhcn = foyer_fiscal('fhcn', period)

        fhdj = foyer_fiscal('fhdj', period)
        fhdo = foyer_fiscal('fhdo', period)
        fheo = foyer_fiscal('fheo', period)
        fhfo = foyer_fiscal('fhfo', period)
        fhbj = foyer_fiscal('fhbj', period)
        fhbo = foyer_fiscal('fhbo', period)
        fhbt = foyer_fiscal('fhbt', period)
        fhby = foyer_fiscal('fhby', period)
        fhcj = foyer_fiscal('fhcj', period)
        fhco = foyer_fiscal('fhco', period)

        fhds = foyer_fiscal('fhds', period)
        fhes = foyer_fiscal('fhes', period)
        fhfs = foyer_fiscal('fhfs', period)
        fhgs = foyer_fiscal('fhgs', period)
        fhcc = foyer_fiscal('fhcc', period)
        fhcs = foyer_fiscal('fhcs', period)

        fhdt = foyer_fiscal('fhdt', period)
        fhet = foyer_fiscal('fhet', period)
        fhft = foyer_fiscal('fhft', period)
        fhgt = foyer_fiscal('fhgt', period)
        fhcd = foyer_fiscal('fhcd', period)
        fhct = foyer_fiscal('fhct', period)

        inv_5263_306_34 = (fhdi + fhdn + fhen + fhfn
            + fhbi + fhbn
            + fhbs + fhbx + fhci + fhcn)

        inv_625_306_51 = (fhdj + fhdo + fheo + fhfo
            + fhbj + fhbo
            + fhbt + fhby + fhcj + fhco)

        inv_56_306_38945 = (fhds
            + fhes
            + fhfs
            + fhgs
            + fhcc
            + fhcs)

        inv_66_306_594 = (fhdt
            + fhet
            + fhft
            + fhgt
            + fhcd
            + fhct)

        nr_66_306_594 = min_(inv_66_306_594 * (1 - P15.taux_retro_1), max_(0, PP15.plafond))
        nr_625_306_51 = min_(inv_625_306_51 * (1 - P15.taux_retro_1), max_(0, PP15.plafond - nr_66_306_594))
        nr_56_306_38945 = min_(inv_56_306_38945 * (1 - P15.taux_retro_2), max_(0, PP15.plafond - nr_66_306_594 - nr_625_306_51))
        nr_5263_306_34 = min_(inv_5263_306_34 * (1 - P15.taux_retro_2), max_(0, PP15.plafond - nr_66_306_594 - nr_625_306_51 - nr_56_306_38945))

        r_66_306_594 = nr_66_306_594 / (1 - P15.taux_retro_1) * P15.taux_retro_1
        r_625_306_51 = nr_625_306_51 / (1 - P15.taux_retro_1) * P15.taux_retro_1
        r_56_306_38945 = nr_56_306_38945 / (1 - P15.taux_retro_2) * P15.taux_retro_2
        r_5263_306_34 = nr_5263_306_34 / (1 - P15.taux_retro_2) * P15.taux_retro_2

        inv = (nr_66_306_594
            + nr_625_306_51
            + nr_56_306_38945
            + nr_5263_306_34
            + r_66_306_594
            + r_625_306_51
            + r_56_306_38945
            + r_5263_306_34)

        # propre entreprise

        # 30.6
        fhdk = foyer_fiscal('fhdk', period)
        fhdp = foyer_fiscal('fhdp', period)
        fhep = foyer_fiscal('fhep', period)
        fhfp = foyer_fiscal('fhfp', period)
        fhdu = foyer_fiscal('fhdu', period)
        fheu = foyer_fiscal('fheu', period)
        fhfu = foyer_fiscal('fhfu', period)
        fhgu = foyer_fiscal('fhgu', period)
        fhbk = foyer_fiscal('fhbk', period)
        fhbp = foyer_fiscal('fhbp', period)
        fhbu = foyer_fiscal('fhbu', period)
        fhbz = foyer_fiscal('fhbz', period)
        fhce = foyer_fiscal('fhce', period)
        fhck = foyer_fiscal('fhck', period)
        fhcp = foyer_fiscal('fhcp', period)
        fhcu = foyer_fiscal('fhcu', period)

        # 76.5
        fhdm = foyer_fiscal('fhdm', period)
        fhdr = foyer_fiscal('fhdr', period)
        fher = foyer_fiscal('fher', period)
        fhfr = foyer_fiscal('fhfr', period)
        fhdw = foyer_fiscal('fhdw', period)
        fhew = foyer_fiscal('fhew', period)
        fhfw = foyer_fiscal('fhfw', period)
        fhgw = foyer_fiscal('fhgw', period)
        fhbm = foyer_fiscal('fhbm', period)
        fhbr = foyer_fiscal('fhbr', period)
        fhbw = foyer_fiscal('fhbw', period)
        fhcb = foyer_fiscal('fhcb', period)
        fhcg = foyer_fiscal('fhcg', period)
        fhcm = foyer_fiscal('fhcm', period)
        fhcr = foyer_fiscal('fhcr', period)
        fhcw = foyer_fiscal('fhcw', period)

        propre_306 = (fhdk + fhdp
            + fhdu + fhep
            + fheu + fhfp
            + fhfu + fhgu
            + fhbk + fhbp + fhbu + fhbz
            + fhce + fhck + fhcp + fhcu)

        propre_765 = (fhdm + fhdr
            + fhdw + fher + fhew
            + fhfr
            + fhfw + fhgw
            + fhbm + fhbr + fhbw + fhcb
            + fhcg + fhcm + fhcr + fhcw)

        ri_propre = (min_(PP15.plafond, propre_306)
            + min_(PP15.plafond * PP15.doment.propre_entreprise.majoration, propre_765))

        return ri_propre + inv

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entreprise.
        '''
        P15 = parameters('2015').impot_revenu.calcul_reductions_impots.outremer_investissement.doment.retrocession
        PP15 = parameters('2015').impot_revenu.calcul_reductions_impots.outremer_investissement

        fhdi = foyer_fiscal('fhdi', period)
        fhdn = foyer_fiscal('fhdn', period)
        fhen = foyer_fiscal('fhen', period)
        fhfn = foyer_fiscal('fhfn', period)
        fhci = foyer_fiscal('fhci', period)
        fhcn = foyer_fiscal('fhcn', period)

        fhdj = foyer_fiscal('fhdj', period)
        fhdo = foyer_fiscal('fhdo', period)
        fheo = foyer_fiscal('fheo', period)
        fhfo = foyer_fiscal('fhfo', period)
        fhcj = foyer_fiscal('fhcj', period)
        fhco = foyer_fiscal('fhco', period)

        fhds = foyer_fiscal('fhds', period)
        fhes = foyer_fiscal('fhes', period)
        fhfs = foyer_fiscal('fhfs', period)
        fhgs = foyer_fiscal('fhgs', period)
        fhcs = foyer_fiscal('fhcs', period)

        fhdt = foyer_fiscal('fhdt', period)
        fhet = foyer_fiscal('fhet', period)
        fhft = foyer_fiscal('fhft', period)
        fhgt = foyer_fiscal('fhgt', period)
        fhct = foyer_fiscal('fhct', period)

        inv_5263_306_34 = (fhdi + fhdn + fhen + fhfn
            + fhci + fhcn)

        inv_625_306_51 = (fhdj + fhdo + fheo + fhfo
            + fhcj + fhco)

        inv_56_306_38945 = (fhds
            + fhes
            + fhfs
            + fhgs
            + fhcs)

        inv_66_306_594 = (fhdt
            + fhet
            + fhft
            + fhgt
            + fhct)

        nr_66_306_594 = min_(inv_66_306_594 * (1 - P15.taux_retro_1), max_(0, PP15.plafond))
        nr_625_306_51 = min_(inv_625_306_51 * (1 - P15.taux_retro_1), max_(0, PP15.plafond - nr_66_306_594))
        nr_56_306_38945 = min_(inv_56_306_38945 * (1 - P15.taux_retro_2), max_(0, PP15.plafond - nr_66_306_594 - nr_625_306_51))
        nr_5263_306_34 = min_(inv_5263_306_34 * (1 - P15.taux_retro_2), max_(0, PP15.plafond - nr_66_306_594 - nr_625_306_51 - nr_56_306_38945))

        r_66_306_594 = nr_66_306_594 / (1 - P15.taux_retro_1) * P15.taux_retro_1
        r_625_306_51 = nr_625_306_51 / (1 - P15.taux_retro_1) * P15.taux_retro_1
        r_56_306_38945 = nr_56_306_38945 / (1 - P15.taux_retro_2) * P15.taux_retro_2
        r_5263_306_34 = nr_5263_306_34 / (1 - P15.taux_retro_2) * P15.taux_retro_2

        inv = (nr_66_306_594
            + nr_625_306_51
            + nr_56_306_38945
            + nr_5263_306_34
            + r_66_306_594
            + r_625_306_51
            + r_56_306_38945
            + r_5263_306_34)

        # propre entreprise

        # 30.6
        fhdk = foyer_fiscal('fhdk', period)
        fhdp = foyer_fiscal('fhdp', period)
        fhep = foyer_fiscal('fhep', period)
        fhfp = foyer_fiscal('fhfp', period)
        fhdu = foyer_fiscal('fhdu', period)
        fheu = foyer_fiscal('fheu', period)
        fhfu = foyer_fiscal('fhfu', period)
        fhgu = foyer_fiscal('fhgu', period)
        fhck = foyer_fiscal('fhck', period)
        fhcp = foyer_fiscal('fhcp', period)
        fhcu = foyer_fiscal('fhcu', period)

        # 76.5
        fhdm = foyer_fiscal('fhdm', period)
        fhdr = foyer_fiscal('fhdr', period)
        fher = foyer_fiscal('fher', period)
        fhfr = foyer_fiscal('fhfr', period)
        fhdw = foyer_fiscal('fhdw', period)
        fhew = foyer_fiscal('fhew', period)
        fhfw = foyer_fiscal('fhfw', period)
        fhgw = foyer_fiscal('fhgw', period)
        fhcm = foyer_fiscal('fhcm', period)
        fhcr = foyer_fiscal('fhcr', period)
        fhcw = foyer_fiscal('fhcw', period)

        propre_306 = (fhdk + fhdp
            + fhdu + fhep
            + fheu + fhfp
            + fhfu + fhgu
            + fhck + fhcp + fhcu)

        propre_765 = (fhdm + fhdr
            + fhdw + fher + fhew
            + fhfr
            + fhfw + fhgw
            + fhcm + fhcr + fhcw)

        ri_propre = (min_(PP15.plafond, propre_306)
            + min_(PP15.plafond * PP15.doment.propre_entreprise.majoration, propre_765))

        return ri_propre + inv


class domlog(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt au titre des investissements outre-mer réalisés par des personnes physiques"
    reference = 'http://bofip.impots.gouv.fr/bofip/6716-PGP'
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2002
        '''
        f7ua = foyer_fiscal('f7ua_2007', period)
        f7ub = foyer_fiscal('f7ub_2007', period)
        f7uc = foyer_fiscal('f7uc_2002', period)
        f7uj = foyer_fiscal('f7uj_2002', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc

        return P.taux1 * f7uj + P.taux2 * (f7ua + f7ub + f7uc)

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2003-2004
        '''
        f7ua = foyer_fiscal('f7ua_2007', period)
        f7ub = foyer_fiscal('f7ub_2007', period)
        f7uc = foyer_fiscal('f7uc_2002', period)
        f7ui = foyer_fiscal('f7ui_2008', period)
        f7uj = foyer_fiscal('f7uj_2002', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc

        return P.taux1 * f7uj + P.taux2 * (f7ua + f7ub + f7uc) + f7ui

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2005-2007
        '''
        f7ua = foyer_fiscal('f7ua_2007', period)
        f7ub = foyer_fiscal('f7ub_2007', period)
        f7ui = foyer_fiscal('f7ui_2008', period)
        f7uj = foyer_fiscal('f7uj_2002', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc

        return P.taux1 * f7uj + P.taux2 * (f7ua + f7ub) + f7ui

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2008
        '''
        f7ui = foyer_fiscal('f7ui_2008', period)

        return f7ui

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2009
        '''
        f7qb = foyer_fiscal('f7qb_2012', period)
        f7qc = foyer_fiscal('f7qc_2012', period)
        f7qd = foyer_fiscal('f7qd_2012', period)
        f7qk = foyer_fiscal('f7qk_2009', period)

        return f7qb + f7qc + f7qd + f7qk / 2

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2010
        TODO: Plafonnement sur la notice
        '''
        f7qb = foyer_fiscal('f7qb_2012', period)
        f7qc = foyer_fiscal('f7qc_2012', period)
        f7qd = foyer_fiscal('f7qd_2012', period)
        f7ql = foyer_fiscal('f7ql_2012', period)
        f7qt = foyer_fiscal('f7qt_2012', period)
        f7qm = foyer_fiscal('f7qm_2012', period)

        return f7qb + f7qc + f7qd + f7ql + f7qt + f7qm

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2011
        TODO: Plafonnement sur la notice
        '''
        f7qb = foyer_fiscal('f7qb_2012', period)
        f7qc = foyer_fiscal('f7qc_2012', period)
        f7qd = foyer_fiscal('f7qd_2012', period)
        f7ql = foyer_fiscal('f7ql_2012', period)
        f7qm = foyer_fiscal('f7qm_2012', period)
        f7qt = foyer_fiscal('f7qt_2012', period)
        f7oa = foyer_fiscal('f7oa_2012', period)
        f7ob = foyer_fiscal('f7ob_2012', period)
        f7oc = foyer_fiscal('f7oc_2012', period)
        f7oh = foyer_fiscal('f7oh_2012', period)
        f7oi = foyer_fiscal('f7oi_2012', period)
        f7oj = foyer_fiscal('f7oj_2012', period)
        f7ok = foyer_fiscal('f7ok_2012', period)

        return f7qb + f7qc + f7qd + f7ql + f7qm + f7qt + f7oa + f7ob + f7oc + f7oh + f7oi + f7oj + f7ok

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2012
        TODO: Plafonnement sur la notice
        '''
        f7qb = foyer_fiscal('f7qb_2012', period)
        f7qc = foyer_fiscal('f7qc_2012', period)
        f7qd = foyer_fiscal('f7qd_2012', period)
        f7ql = foyer_fiscal('f7ql_2012', period)
        f7qm = foyer_fiscal('f7qm_2012', period)
        f7qt = foyer_fiscal('f7qt_2012', period)
        f7oa = foyer_fiscal('f7oa_2012', period)
        f7ob = foyer_fiscal('f7ob_2012', period)
        f7oc = foyer_fiscal('f7oc_2012', period)
        f7oh = foyer_fiscal('f7oh_2012', period)
        f7oi = foyer_fiscal('f7oi_2012', period)
        f7oj = foyer_fiscal('f7oj_2012', period)
        f7ok = foyer_fiscal('f7ok_2012', period)
        f7ol = foyer_fiscal('f7ol_2012', period)
        f7om = foyer_fiscal('f7om_2012', period)
        f7on = foyer_fiscal('f7on_2012', period)
        f7oo = foyer_fiscal('f7oo_2012', period)
        f7op = foyer_fiscal('f7op_2012', period)
        f7oq = foyer_fiscal('f7oq_2012', period)
        f7or = foyer_fiscal('f7or_2012', period)
        f7os = foyer_fiscal('f7os_2012', period)
        f7ot = foyer_fiscal('f7ot_2012', period)
        f7ou = foyer_fiscal('f7ou_2012', period)
        f7ov = foyer_fiscal('f7ov_2012', period)
        f7ow = foyer_fiscal('f7ow_2012', period)

        return (
            f7qb + f7qc + f7qd + f7ql + f7qm + f7qt
            + f7oa + f7ob + f7oc + f7oh + f7oi + f7oj + f7ok + f7ol + f7om + f7on
            + f7oo + f7op + f7oq + f7or + f7os + f7ot + f7ou + f7ov + f7ow
            )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2013
        TODO: Plafonnement sur la notice
        '''
        fhod = foyer_fiscal('fhod', period)
        fhoe = foyer_fiscal('fhoe', period)
        fhof = foyer_fiscal('fhof', period)
        fhog = foyer_fiscal('fhog', period)
        fhox = foyer_fiscal('fhox', period)
        fhoy = foyer_fiscal('fhoy', period)
        fhoz = foyer_fiscal('fhoz', period)
        fhqb = foyer_fiscal('fhqb', period)
        fhqc = foyer_fiscal('fhqc', period)
        fhqd = foyer_fiscal('fhqd', period)
        fhql = foyer_fiscal('fhql', period)
        fhqm = foyer_fiscal('fhqm', period)
        fhqt = foyer_fiscal('fhqt', period)
        fhoa = foyer_fiscal('fhoa', period)
        fhob = foyer_fiscal('fhob', period)
        fhoc = foyer_fiscal('fhoc', period)
        fhoh = foyer_fiscal('fhoh', period)
        fhoi = foyer_fiscal('fhoi', period)
        fhoj = foyer_fiscal('fhoj', period)
        fhok = foyer_fiscal('fhok', period)
        fhol = foyer_fiscal('fhol', period)
        fhom = foyer_fiscal('fhom', period)
        fhon = foyer_fiscal('fhon', period)
        fhoo = foyer_fiscal('fhoo', period)
        fhop = foyer_fiscal('fhop', period)
        fhoq = foyer_fiscal('fhoq', period)
        fhor = foyer_fiscal('fhor', period)
        fhos = foyer_fiscal('fhos', period)
        fhot = foyer_fiscal('fhot', period)
        fhou = foyer_fiscal('fhou', period)
        fhov = foyer_fiscal('fhov', period)
        fhow = foyer_fiscal('fhow', period)

        return (
            fhqb + fhqc + fhqd + fhql + fhqm + fhqt
            + fhoa + fhob + fhoc + fhoh + fhoi + fhoj + fhok + fhol + fhom + fhon + fhoo + fhop
            + fhoq + fhor + fhos + fhot + fhou + fhov + fhow + fhod + fhoe + fhof + fhog + fhox
            + fhoy + fhoz
            )

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2014
        '''
        fhod = foyer_fiscal('fhod', period)
        fhoe = foyer_fiscal('fhoe', period)
        fhof = foyer_fiscal('fhof', period)
        fhog = foyer_fiscal('fhog', period)
        fhox = foyer_fiscal('fhox', period)
        fhoy = foyer_fiscal('fhoy', period)
        fhoz = foyer_fiscal('fhoz', period)
        fhqb = foyer_fiscal('fhqb', period)
        fhqc = foyer_fiscal('fhqc', period)
        fhqd = foyer_fiscal('fhqd', period)
        fhql = foyer_fiscal('fhql', period)
        fhqm = foyer_fiscal('fhqm', period)
        fhqt = foyer_fiscal('fhqt', period)
        fhoa = foyer_fiscal('fhoa', period)
        fhob = foyer_fiscal('fhob', period)
        fhoc = foyer_fiscal('fhoc', period)
        fhoh = foyer_fiscal('fhoh', period)
        fhoi = foyer_fiscal('fhoi', period)
        fhoj = foyer_fiscal('fhoj', period)
        fhok = foyer_fiscal('fhok', period)
        fhol = foyer_fiscal('fhol', period)
        fhom = foyer_fiscal('fhom', period)
        fhon = foyer_fiscal('fhon', period)
        fhoo = foyer_fiscal('fhoo', period)
        fhop = foyer_fiscal('fhop', period)
        fhoq = foyer_fiscal('fhoq', period)
        fhor = foyer_fiscal('fhor', period)
        fhos = foyer_fiscal('fhos', period)
        fhot = foyer_fiscal('fhot', period)
        fhou = foyer_fiscal('fhou', period)
        fhov = foyer_fiscal('fhov', period)
        fhow = foyer_fiscal('fhow', period)
        fhua = foyer_fiscal('fhua', period)
        fhub = foyer_fiscal('fhub', period)
        fhuc = foyer_fiscal('fhuc', period)
        fhud = foyer_fiscal('fhud', period)
        fhue = foyer_fiscal('fhue', period)
        fhuf = foyer_fiscal('fhuf', period)
        fhug = foyer_fiscal('fhug', period)

        return (
            fhqb + fhqc + fhqd + fhql + fhqm + fhqt
            + fhoa + fhob + fhoc + fhoh + fhoi + fhoj + fhok + fhol + fhom
            + fhon + fhoo + fhop + fhoq + fhor + fhos + fhot + fhou + fhov + fhow + fhod + fhoe
            + fhof + fhog + fhox + fhoy + fhoz + fhua + fhub + fhuc + fhud + fhue + fhuf + fhug
            )

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2015
        '''
        fhod = foyer_fiscal('fhod', period)
        fhoe = foyer_fiscal('fhoe', period)
        fhof = foyer_fiscal('fhof', period)
        fhog = foyer_fiscal('fhog', period)
        fhox = foyer_fiscal('fhox', period)
        fhoy = foyer_fiscal('fhoy', period)
        fhoz = foyer_fiscal('fhoz', period)
        fhqb = foyer_fiscal('fhqb', period)
        fhqc = foyer_fiscal('fhqc', period)
        fhqd = foyer_fiscal('fhqd', period)
        fhql = foyer_fiscal('fhql', period)
        fhqm = foyer_fiscal('fhqm', period)
        fhqt = foyer_fiscal('fhqt', period)
        fhoa = foyer_fiscal('fhoa', period)
        fhob = foyer_fiscal('fhob', period)
        fhoc = foyer_fiscal('fhoc', period)
        fhoh = foyer_fiscal('fhoh', period)
        fhoi = foyer_fiscal('fhoi', period)
        fhoj = foyer_fiscal('fhoj', period)
        fhok = foyer_fiscal('fhok', period)
        fhol = foyer_fiscal('fhol', period)
        fhom = foyer_fiscal('fhom', period)
        fhon = foyer_fiscal('fhon', period)
        fhoo = foyer_fiscal('fhoo', period)
        fhop = foyer_fiscal('fhop', period)
        fhoq = foyer_fiscal('fhoq', period)
        fhor = foyer_fiscal('fhor', period)
        fhos = foyer_fiscal('fhos', period)
        fhot = foyer_fiscal('fhot', period)
        fhou = foyer_fiscal('fhou', period)
        fhov = foyer_fiscal('fhov', period)
        fhow = foyer_fiscal('fhow', period)
        fhua = foyer_fiscal('fhua', period)
        fhub = foyer_fiscal('fhub', period)
        fhuc = foyer_fiscal('fhuc', period)
        fhud = foyer_fiscal('fhud', period)
        fhue = foyer_fiscal('fhue', period)
        fhuf = foyer_fiscal('fhuf', period)
        fhug = foyer_fiscal('fhug', period)
        fhuh = foyer_fiscal('fhuh', period)
        fhui = foyer_fiscal('fhui', period)
        fhuj = foyer_fiscal('fhuj', period)
        fhuk = foyer_fiscal('fhuk', period)
        fhul = foyer_fiscal('fhul', period)
        fhum = foyer_fiscal('fhum', period)
        fhun = foyer_fiscal('fhun', period)

        return (
            fhqb + fhqc + fhqd + fhql + fhqm + fhqt
            + fhoa + fhob + fhoc + fhoh + fhoi + fhoj + fhok + fhol + fhom + fhon + fhoo + fhop
            + fhoq + fhor + fhos + fhot + fhou + fhov + fhow + fhod + fhoe + fhof + fhog + fhox
            + fhoy + fhoz
            + fhua + fhub + fhuc + fhud + fhue + fhuf + fhug + fhuh + fhui + fhuj + fhuk + fhul
            + fhum + fhun
            )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2016

        ATTENTION : Rupture importante dans cette variable à partir de 2016 (prise en compte partielle du plafond).
        '''
        fhod = foyer_fiscal('fhod', period)
        fhoe = foyer_fiscal('fhoe', period)
        fhof = foyer_fiscal('fhof', period)
        fhog = foyer_fiscal('fhog', period)
        fhox = foyer_fiscal('fhox', period)
        fhoy = foyer_fiscal('fhoy', period)
        fhoz = foyer_fiscal('fhoz', period)
        fhqb = foyer_fiscal('fhqb', period)
        fhqc = foyer_fiscal('fhqc', period)
        fhqd = foyer_fiscal('fhqd', period)
        fhql = foyer_fiscal('fhql', period)
        fhqm = foyer_fiscal('fhqm', period)
        fhqt = foyer_fiscal('fhqt', period)
        fhoa = foyer_fiscal('fhoa', period)
        fhob = foyer_fiscal('fhob', period)
        fhoc = foyer_fiscal('fhoc', period)
        fhoh = foyer_fiscal('fhoh', period)
        fhoi = foyer_fiscal('fhoi', period)
        fhoj = foyer_fiscal('fhoj', period)
        fhok = foyer_fiscal('fhok', period)
        fhol = foyer_fiscal('fhol', period)
        fhom = foyer_fiscal('fhom', period)
        fhon = foyer_fiscal('fhon', period)
        fhoo = foyer_fiscal('fhoo', period)
        fhop = foyer_fiscal('fhop', period)
        fhoq = foyer_fiscal('fhoq', period)
        fhor = foyer_fiscal('fhor', period)
        fhos = foyer_fiscal('fhos', period)
        fhot = foyer_fiscal('fhot', period)
        fhou = foyer_fiscal('fhou', period)
        fhov = foyer_fiscal('fhov', period)
        fhow = foyer_fiscal('fhow', period)
        fhua = foyer_fiscal('fhua', period)
        fhub = foyer_fiscal('fhub', period)
        fhuc = foyer_fiscal('fhuc', period)
        fhud = foyer_fiscal('fhud', period)
        fhue = foyer_fiscal('fhue', period)
        fhuf = foyer_fiscal('fhuf', period)
        fhug = foyer_fiscal('fhug', period)
        fhuh = foyer_fiscal('fhuh', period)
        fhui = foyer_fiscal('fhui', period)
        fhuj = foyer_fiscal('fhuj', period)
        fhuk = foyer_fiscal('fhuk', period)
        fhul = foyer_fiscal('fhul', period)
        fhum = foyer_fiscal('fhum', period)
        fhun = foyer_fiscal('fhun', period)
        fhuo = foyer_fiscal('fhuo', period)
        fhup = foyer_fiscal('fhup', period)
        fhuq = foyer_fiscal('fhuq', period)
        fhur = foyer_fiscal('fhur', period)
        fhus = foyer_fiscal('fhus', period)
        fhut = foyer_fiscal('fhut', period)
        fhuu = foyer_fiscal('fhuu', period)

        ri_avant_2011 = (fhqb + fhqc + fhql + fhqd + fhqm
            + fhqt + fhoa + fhob + fhoc
            + fhod + fhua + fhuh + fhuo)

        ri_2011 = (fhoh + fhoi + fhoj + fhok + fhol + fhom
            + fhon + fhoo + fhop + fhoq + fhor + fhoe + fhof
            + fhub + fhuc + fhui + fhuj + fhup + fhuq)

        ri_apres_2011 = (fhos + fhot + fhou + fhov + fhow
            + fhog + fhox + fhoy + fhoz + fhud + fhue + fhuf + fhug +
            + fhuk + fhul + fhum + fhun +
            + fhur + fhus + fhut + fhuu)

        # application du plafonnement
        P2010 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement
        P2011 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement
        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement

        # rni = foyer_fiscal('rni', period)

        # # si plafond rélatif à 11, 13, 15 % (case HQA)
        # ri_plaf_rel_2010 = min_(ri_avant_2011, rni * P2010.plaf_relatif)
        # ri_plaf_rel_2011 = min_(max_(0, rni * P2011.plaf_relatif - ri_plaf_rel_2010), ri_2011)
        # ri_plaf_rel_2012 = min_(max_(0, rni * P2012.plaf_relatif - ri_plaf_rel_2011 - ri_plaf_rel_2010), ri_apres_2011)

        # ri_rel = ri_plaf_rel_2010 + ri_plaf_rel_2011 + ri_plaf_rel_2012

        # si plafond absolu
        ri_plaf_2010 = min_(ri_avant_2011, P2010.plafond)
        ri_plaf_2011 = min_(max_(0, P2011.plafond - ri_plaf_2010), ri_2011)
        ri_plaf_2012 = min_(max_(0, P.plafond - ri_plaf_2011 - ri_plaf_2010), ri_apres_2011)

        ri_abs = ri_plaf_2010 + ri_plaf_2011 + ri_plaf_2012

        # choix optimal
        # ri_opt = max_(ri_rel, ri_abs)

        # choix observé
        # ri_choix = (foyer_fiscal('fhqa', period) * ri_rel
        #     + (1 - foyer_fiscal('fhqa', period)) * ri_abs)

        # Pourquoi tout ce trouble de calculer ri_opt si on n'utilise que ri_abs à la fin ?
        # C'est une approximation parce qu'il y a bel et bien l'option avec plafond relatif.
        # En même temps on a dû faire des économies de temps, on ne pouvait pas coder le plafond relatif
        # pour tous les trois dispositifs, juste ici pour domlog. Afin d'être cohérent, on utilise
        # quand-même toujours le plafond absolu, mais on garde l'option de le changer facilement ici.

        return ri_abs

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2017
        '''
        fhod = foyer_fiscal('fhod', period)
        fhoe = foyer_fiscal('fhoe', period)
        fhof = foyer_fiscal('fhof', period)
        fhog = foyer_fiscal('fhog', period)
        fhox = foyer_fiscal('fhox', period)
        fhoy = foyer_fiscal('fhoy', period)
        fhoz = foyer_fiscal('fhoz', period)
        fhqb = foyer_fiscal('fhqb', period)
        fhqc = foyer_fiscal('fhqc', period)
        fhqd = foyer_fiscal('fhqd', period)
        fhql = foyer_fiscal('fhql', period)
        fhqm = foyer_fiscal('fhqm', period)
        fhqt = foyer_fiscal('fhqt', period)
        fhoa = foyer_fiscal('fhoa', period)
        fhob = foyer_fiscal('fhob', period)
        fhoc = foyer_fiscal('fhoc', period)
        fhoh = foyer_fiscal('fhoh', period)
        fhoi = foyer_fiscal('fhoi', period)
        fhoj = foyer_fiscal('fhoj', period)
        fhok = foyer_fiscal('fhok', period)
        fhol = foyer_fiscal('fhol', period)
        fhom = foyer_fiscal('fhom', period)
        fhon = foyer_fiscal('fhon', period)
        fhoo = foyer_fiscal('fhoo', period)
        fhop = foyer_fiscal('fhop', period)
        fhoq = foyer_fiscal('fhoq', period)
        fhor = foyer_fiscal('fhor', period)
        fhos = foyer_fiscal('fhos', period)
        fhot = foyer_fiscal('fhot', period)
        fhou = foyer_fiscal('fhou', period)
        fhov = foyer_fiscal('fhov', period)
        fhow = foyer_fiscal('fhow', period)
        fhua = foyer_fiscal('fhua', period)
        fhub = foyer_fiscal('fhub', period)
        fhuc = foyer_fiscal('fhuc', period)
        fhud = foyer_fiscal('fhud', period)
        fhue = foyer_fiscal('fhue', period)
        fhuf = foyer_fiscal('fhuf', period)
        fhug = foyer_fiscal('fhug', period)
        fhuh = foyer_fiscal('fhuh', period)
        fhui = foyer_fiscal('fhui', period)
        fhuj = foyer_fiscal('fhuj', period)
        fhuk = foyer_fiscal('fhuk', period)
        fhul = foyer_fiscal('fhul', period)
        fhum = foyer_fiscal('fhum', period)
        fhun = foyer_fiscal('fhun', period)
        fhuo = foyer_fiscal('fhuo', period)
        fhup = foyer_fiscal('fhup', period)
        fhuq = foyer_fiscal('fhuq', period)
        fhur = foyer_fiscal('fhur', period)
        fhus = foyer_fiscal('fhus', period)
        fhut = foyer_fiscal('fhut', period)
        fhuu = foyer_fiscal('fhuu', period)
        fhva = foyer_fiscal('fhva', period)
        fhvb = foyer_fiscal('fhvb', period)
        fhvc = foyer_fiscal('fhvc', period)
        fhvd = foyer_fiscal('fhvd', period)
        fhve = foyer_fiscal('fhve', period)
        fhvf = foyer_fiscal('fhvf', period)
        fhvg = foyer_fiscal('fhvg', period)

        ri_avant_2011 = (fhqb + fhqc + fhql + fhqd + fhqm
            + fhqt + fhoa + fhob + fhoc
            + fhod + fhua + fhuh + fhuo + fhva)

        ri_2011 = (fhoh + fhoi + fhoj + fhok + fhol + fhom
            + fhon + fhoo + fhop + fhoq + fhor + fhoe + fhof
            + fhub + fhuc + fhui + fhuj + fhup + fhuq + fhvb + fhvc)

        ri_apres_2011 = (fhos + fhot + fhou + fhov + fhow
            + fhog + fhox + fhoy + fhoz + fhud + fhue + fhuf + fhug +
            + fhuk + fhul + fhum + fhun +
            + fhur + fhus + fhut + fhuu +
            + fhvd + fhve + fhvf + fhvg)

        # application du plafonnement
        P2010 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement
        P2011 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement
        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement

        # rni = foyer_fiscal('rni', period)

        # # si plafond rélatif à 11, 13, 15 % (case HQA)
        # ri_plaf_rel_2010 = min_(ri_avant_2011, rni * P2010.plaf_relatif)
        # ri_plaf_rel_2011 = min_(max_(0, rni * P2011.plaf_relatif - ri_plaf_rel_2010), ri_2011)
        # ri_plaf_rel_2012 = min_(max_(0, rni * P2012.plaf_relatif - ri_plaf_rel_2011 - ri_plaf_rel_2010), ri_apres_2011)

        # ri_rel = ri_plaf_rel_2010 + ri_plaf_rel_2011 + ri_plaf_rel_2012

        # si plafond absolu
        ri_plaf_2010 = min_(ri_avant_2011, P2010.plafond)
        ri_plaf_2011 = min_(max_(0, P2011.plafond - ri_plaf_2010), ri_2011)
        ri_plaf_2012 = min_(max_(0, P.plafond - ri_plaf_2011 - ri_plaf_2010), ri_apres_2011)

        ri_abs = ri_plaf_2010 + ri_plaf_2011 + ri_plaf_2012

        # choix optimal
        # ri_opt = max_(ri_rel, ri_abs)

        # choix observé
        # ri_choix = (foyer_fiscal('fhqa', period) * ri_rel
        #     + (1 - foyer_fiscal('fhqa', period)) * ri_abs)

        return ri_abs

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2018
        '''

        fhqb = foyer_fiscal('fhqb', period)
        fhqc = foyer_fiscal('fhqc', period)
        fhql = foyer_fiscal('fhql', period)
        fhqt = foyer_fiscal('fhqt', period)
        fhqm = foyer_fiscal('fhqm', period)
        fhqd = foyer_fiscal('fhqd', period)
        fhoa = foyer_fiscal('fhoa', period)
        fhob = foyer_fiscal('fhob', period)
        fhoc = foyer_fiscal('fhoc', period)
        fhol = foyer_fiscal('fhol', period)
        fhom = foyer_fiscal('fhom', period)
        fhon = foyer_fiscal('fhon', period)
        fhod = foyer_fiscal('fhod', period)
        fhua = foyer_fiscal('fhua', period)
        fhuh = foyer_fiscal('fhuh', period)
        fhuo = foyer_fiscal('fhuo', period)
        fhva = foyer_fiscal('fhva', period)

        fhoh = foyer_fiscal('fhoh', period)
        fhoi = foyer_fiscal('fhoi', period)
        fhoj = foyer_fiscal('fhoj', period)
        fhok = foyer_fiscal('fhok', period)
        fhoo = foyer_fiscal('fhoo', period)
        fhop = foyer_fiscal('fhop', period)
        fhoq = foyer_fiscal('fhoq', period)
        fhor = foyer_fiscal('fhor', period)
        fhoe = foyer_fiscal('fhoe', period)
        fhof = foyer_fiscal('fhof', period)
        fhub = foyer_fiscal('fhub', period)
        fhuc = foyer_fiscal('fhuc', period)
        fhui = foyer_fiscal('fhui', period)
        fhuj = foyer_fiscal('fhuj', period)
        fhup = foyer_fiscal('fhup', period)
        fhuq = foyer_fiscal('fhuq', period)
        fhvb = foyer_fiscal('fhvb', period)
        fhvc = foyer_fiscal('fhvc', period)

        fhos = foyer_fiscal('fhos', period)
        fhot = foyer_fiscal('fhot', period)
        fhou = foyer_fiscal('fhou', period)
        fhov = foyer_fiscal('fhov', period)
        fhow = foyer_fiscal('fhow', period)
        fhog = foyer_fiscal('fhog', period)
        fhox = foyer_fiscal('fhox', period)
        fhoy = foyer_fiscal('fhoy', period)
        fhoz = foyer_fiscal('fhoz', period)
        fhud = foyer_fiscal('fhud', period)
        fhue = foyer_fiscal('fhue', period)
        fhuf = foyer_fiscal('fhuf', period)
        fhug = foyer_fiscal('fhug', period)
        fhuk = foyer_fiscal('fhuk', period)
        fhul = foyer_fiscal('fhul', period)
        fhum = foyer_fiscal('fhum', period)
        fhun = foyer_fiscal('fhun', period)
        fhur = foyer_fiscal('fhur', period)
        fhus = foyer_fiscal('fhus', period)
        fhut = foyer_fiscal('fhut', period)
        fhuu = foyer_fiscal('fhuu', period)
        fhvd = foyer_fiscal('fhvd', period)
        fhve = foyer_fiscal('fhve', period)
        fhvf = foyer_fiscal('fhvf', period)
        fhvg = foyer_fiscal('fhvg', period)

        ri_avant_2011 = (fhqb
            + fhqc
            + fhql
            + fhqt
            + fhqm
            + fhqd
            + fhoa
            + fhob
            + fhoc
            + fhol
            + fhom
            + fhon
            + fhod
            + fhua
            + fhuh
            + fhuo
            + fhva)

        ri_2011 = (fhoh
            + fhoi
            + fhoj
            + fhok
            + fhoo
            + fhop
            + fhoq
            + fhor
            + fhoe
            + fhof
            + fhub
            + fhuc
            + fhui
            + fhuj
            + fhup
            + fhuq
            + fhvb
            + fhvc)

        ri_apres_2011 = (fhos
            + fhot
            + fhou
            + fhov
            + fhow
            + fhog
            + fhox
            + fhoy
            + fhoz
            + fhud
            + fhue
            + fhuf
            + fhug
            + fhuk
            + fhul
            + fhum
            + fhun
            + fhur
            + fhus
            + fhut
            + fhuu
            + fhvd
            + fhve
            + fhvf
            + fhvg)

        # application du plafonnement
        P2010 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement
        P2011 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement
        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement

        # rni = foyer_fiscal('rni', period)

        # # si plafond rélatif à 11, 13, 15 % (case HQA)
        # ri_plaf_rel_2010 = min_(ri_avant_2011, rni * P2010.plaf_relatif)
        # ri_plaf_rel_2011 = min_(max_(0, rni * P2011.plaf_relatif - ri_plaf_rel_2010), ri_2011)
        # ri_plaf_rel_2012 = min_(max_(0, rni * P2012.plaf_relatif - ri_plaf_rel_2011 - ri_plaf_rel_2010), ri_apres_2011)

        # ri_rel = ri_plaf_rel_2010 + ri_plaf_rel_2011 + ri_plaf_rel_2012

        # si plafond absolu
        ri_plaf_2010 = min_(ri_avant_2011, P2010.plafond)
        ri_plaf_2011 = min_(max_(0, P2011.plafond - ri_plaf_2010), ri_2011)
        ri_plaf_2012 = min_(max_(0, P.plafond - ri_plaf_2011 - ri_plaf_2010), ri_apres_2011)

        ri_abs = ri_plaf_2010 + ri_plaf_2011 + ri_plaf_2012

        # choix optimal
        # ri_opt = max_(ri_rel, ri_abs)

        # choix observé
        # ri_choix = (foyer_fiscal('fhqa', period) * ri_rel
        #     + (1 - foyer_fiscal('fhqa', period)) * ri_abs)

        return ri_abs

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2019
        '''

        fhqb = foyer_fiscal('fhqb', period)
        fhqc = foyer_fiscal('fhqc', period)
        fhql = foyer_fiscal('fhql', period)
        fhqt = foyer_fiscal('fhqt', period)
        fhqm = foyer_fiscal('fhqm', period)
        fhqd = foyer_fiscal('fhqd', period)
        fhoa = foyer_fiscal('fhoa', period)
        fhob = foyer_fiscal('fhob', period)
        fhoc = foyer_fiscal('fhoc', period)
        fhol = foyer_fiscal('fhol', period)
        fhom = foyer_fiscal('fhom', period)
        fhon = foyer_fiscal('fhon', period)
        fhod = foyer_fiscal('fhod', period)
        fhua = foyer_fiscal('fhua', period)
        fhuh = foyer_fiscal('fhuh', period)
        fhuo = foyer_fiscal('fhuo', period)
        fhva = foyer_fiscal('fhva', period)

        fhoh = foyer_fiscal('fhoh', period)
        fhoi = foyer_fiscal('fhoi', period)
        fhoj = foyer_fiscal('fhoj', period)
        fhok = foyer_fiscal('fhok', period)
        fhoo = foyer_fiscal('fhoo', period)
        fhop = foyer_fiscal('fhop', period)
        fhoq = foyer_fiscal('fhoq', period)
        fhor = foyer_fiscal('fhor', period)
        fhoe = foyer_fiscal('fhoe', period)
        fhof = foyer_fiscal('fhof', period)
        fhub = foyer_fiscal('fhub', period)
        fhuc = foyer_fiscal('fhuc', period)
        fhui = foyer_fiscal('fhui', period)
        fhuj = foyer_fiscal('fhuj', period)
        fhup = foyer_fiscal('fhup', period)
        fhuq = foyer_fiscal('fhuq', period)
        fhvb = foyer_fiscal('fhvb', period)
        fhvc = foyer_fiscal('fhvc', period)

        fhos = foyer_fiscal('fhos', period)
        fhot = foyer_fiscal('fhot', period)
        fhou = foyer_fiscal('fhou', period)
        fhov = foyer_fiscal('fhov', period)
        fhow = foyer_fiscal('fhow', period)
        fhog = foyer_fiscal('fhog', period)
        fhox = foyer_fiscal('fhox', period)
        fhoy = foyer_fiscal('fhoy', period)
        fhoz = foyer_fiscal('fhoz', period)
        fhud = foyer_fiscal('fhud', period)
        fhue = foyer_fiscal('fhue', period)
        fhuf = foyer_fiscal('fhuf', period)
        fhug = foyer_fiscal('fhug', period)
        fhuk = foyer_fiscal('fhuk', period)
        fhul = foyer_fiscal('fhul', period)
        fhum = foyer_fiscal('fhum', period)
        fhun = foyer_fiscal('fhun', period)
        fhur = foyer_fiscal('fhur', period)
        fhus = foyer_fiscal('fhus', period)
        fhut = foyer_fiscal('fhut', period)
        fhuu = foyer_fiscal('fhuu', period)
        fhvd = foyer_fiscal('fhvd', period)
        fhve = foyer_fiscal('fhve', period)
        fhvf = foyer_fiscal('fhvf', period)
        fhvg = foyer_fiscal('fhvg', period)
        fhvh = foyer_fiscal('fhvh', period)
        fhvi = foyer_fiscal('fhvi', period)

        ri_avant_2011 = (fhqb
            + fhqc
            + fhql
            + fhqt
            + fhqm
            + fhqd
            + fhoa
            + fhob
            + fhoc
            + fhol
            + fhom
            + fhon
            + fhod
            + fhua
            + fhuh
            + fhuo
            + fhva)

        ri_2011 = (fhoh
            + fhoi
            + fhoj
            + fhok
            + fhoo
            + fhop
            + fhoq
            + fhor
            + fhoe
            + fhof
            + fhub
            + fhuc
            + fhui
            + fhuj
            + fhup
            + fhuq
            + fhvb
            + fhvc)

        ri_apres_2011 = (fhos
            + fhot
            + fhou
            + fhov
            + fhow
            + fhog
            + fhox
            + fhoy
            + fhoz
            + fhud
            + fhue
            + fhuf
            + fhug
            + fhuk
            + fhul
            + fhum
            + fhun
            + fhur
            + fhus
            + fhut
            + fhuu
            + fhvd
            + fhve
            + fhvf
            + fhvg
            + fhvh
            + fhvi)

        # application du plafonnement
        P2010 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement
        P2011 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement
        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement

        # rni = foyer_fiscal('rni', period)

        # # si plafond rélatif à 11, 13, 15 % (case HQA)
        # ri_plaf_rel_2010 = min_(ri_avant_2011, rni * P2010.plaf_relatif)
        # ri_plaf_rel_2011 = min_(max_(0, rni * P2011.plaf_relatif - ri_plaf_rel_2010), ri_2011)
        # ri_plaf_rel_2012 = min_(max_(0, rni * P2012.plaf_relatif - ri_plaf_rel_2011 - ri_plaf_rel_2010), ri_apres_2011)

        # ri_rel = ri_plaf_rel_2010 + ri_plaf_rel_2011 + ri_plaf_rel_2012

        # si plafond absolu
        ri_plaf_2010 = min_(ri_avant_2011, P2010.plafond)
        ri_plaf_2011 = min_(max_(0, P2011.plafond - ri_plaf_2010), ri_2011)
        ri_plaf_2012 = min_(max_(0, P.plafond - ri_plaf_2011 - ri_plaf_2010), ri_apres_2011)

        ri_abs = ri_plaf_2010 + ri_plaf_2011 + ri_plaf_2012

        # choix optimal
        # ri_opt = max_(ri_rel, ri_abs)

        # choix observé
        # ri_choix = (foyer_fiscal('fhqa', period) * ri_rel
        #     + (1 - foyer_fiscal('fhqa', period)) * ri_abs)

        return ri_abs

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2020
        '''

        fhqb = foyer_fiscal('fhqb', period)
        fhqc = foyer_fiscal('fhqc', period)
        fhql = foyer_fiscal('fhql', period)
        fhqt = foyer_fiscal('fhqt', period)
        fhqm = foyer_fiscal('fhqm', period)
        fhqd = foyer_fiscal('fhqd', period)
        fhoa = foyer_fiscal('fhoa', period)
        fhob = foyer_fiscal('fhob', period)
        fhoc = foyer_fiscal('fhoc', period)
        fhol = foyer_fiscal('fhol', period)
        fhom = foyer_fiscal('fhom', period)
        fhon = foyer_fiscal('fhon', period)
        fhod = foyer_fiscal('fhod', period)
        fhua = foyer_fiscal('fhua', period)
        fhuh = foyer_fiscal('fhuh', period)
        fhuo = foyer_fiscal('fhuo', period)
        fhva = foyer_fiscal('fhva', period)

        fhoh = foyer_fiscal('fhoh', period)
        fhoi = foyer_fiscal('fhoi', period)
        fhoj = foyer_fiscal('fhoj', period)
        fhok = foyer_fiscal('fhok', period)
        fhoo = foyer_fiscal('fhoo', period)
        fhop = foyer_fiscal('fhop', period)
        fhoq = foyer_fiscal('fhoq', period)
        fhor = foyer_fiscal('fhor', period)
        fhoe = foyer_fiscal('fhoe', period)
        fhof = foyer_fiscal('fhof', period)
        fhub = foyer_fiscal('fhub', period)
        fhuc = foyer_fiscal('fhuc', period)
        fhui = foyer_fiscal('fhui', period)
        fhuj = foyer_fiscal('fhuj', period)
        fhup = foyer_fiscal('fhup', period)
        fhuq = foyer_fiscal('fhuq', period)
        fhvb = foyer_fiscal('fhvb', period)
        fhvc = foyer_fiscal('fhvc', period)

        fhos = foyer_fiscal('fhos', period)
        fhot = foyer_fiscal('fhot', period)
        fhou = foyer_fiscal('fhou', period)
        fhov = foyer_fiscal('fhov', period)
        fhow = foyer_fiscal('fhow', period)
        fhog = foyer_fiscal('fhog', period)
        fhox = foyer_fiscal('fhox', period)
        fhoy = foyer_fiscal('fhoy', period)
        fhoz = foyer_fiscal('fhoz', period)
        fhud = foyer_fiscal('fhud', period)
        fhue = foyer_fiscal('fhue', period)
        fhuf = foyer_fiscal('fhuf', period)
        fhug = foyer_fiscal('fhug', period)
        fhuk = foyer_fiscal('fhuk', period)
        fhul = foyer_fiscal('fhul', period)
        fhum = foyer_fiscal('fhum', period)
        fhun = foyer_fiscal('fhun', period)
        fhur = foyer_fiscal('fhur', period)
        fhus = foyer_fiscal('fhus', period)
        fhut = foyer_fiscal('fhut', period)
        fhuu = foyer_fiscal('fhuu', period)
        fhvd = foyer_fiscal('fhvd', period)
        fhve = foyer_fiscal('fhve', period)
        fhvf = foyer_fiscal('fhvf', period)
        fhvg = foyer_fiscal('fhvg', period)
        fhvh = foyer_fiscal('fhvh', period)
        fhvi = foyer_fiscal('fhvi', period)
        fhvj = foyer_fiscal('fhvj', period)

        ri_avant_2011 = (fhqb
            + fhqc
            + fhql
            + fhqt
            + fhqm
            + fhqd
            + fhoa
            + fhob
            + fhoc
            + fhol
            + fhom
            + fhon
            + fhod
            + fhua
            + fhuh
            + fhuo
            + fhva)

        ri_2011 = (fhoh
            + fhoi
            + fhoj
            + fhok
            + fhoo
            + fhop
            + fhoq
            + fhor
            + fhoe
            + fhof
            + fhub
            + fhuc
            + fhui
            + fhuj
            + fhup
            + fhuq
            + fhvb
            + fhvc)

        ri_apres_2011 = (fhos
            + fhot
            + fhou
            + fhov
            + fhow
            + fhog
            + fhox
            + fhoy
            + fhoz
            + fhud
            + fhue
            + fhuf
            + fhug
            + fhuk
            + fhul
            + fhum
            + fhun
            + fhur
            + fhus
            + fhut
            + fhuu
            + fhvd
            + fhve
            + fhvf
            + fhvg
            + fhvh
            + fhvi
            + fhvj)

        # application du plafonnement
        P2010 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement
        P2011 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement
        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement

        # rni = foyer_fiscal('rni', period)

        # # si plafond rélatif à 11, 13, 15 % (case HQA)
        # ri_plaf_rel_2010 = min_(ri_avant_2011, rni * P2010.plaf_relatif)
        # ri_plaf_rel_2011 = min_(max_(0, rni * P2011.plaf_relatif - ri_plaf_rel_2010), ri_2011)
        # ri_plaf_rel_2012 = min_(max_(0, rni * P2012.plaf_relatif - ri_plaf_rel_2011 - ri_plaf_rel_2010), ri_apres_2011)

        # ri_rel = ri_plaf_rel_2010 + ri_plaf_rel_2011 + ri_plaf_rel_2012

        # si plafond absolu
        ri_plaf_2010 = min_(ri_avant_2011, P2010.plafond)
        ri_plaf_2011 = min_(max_(0, P2011.plafond - ri_plaf_2010), ri_2011)
        ri_plaf_2012 = min_(max_(0, P.plafond - ri_plaf_2011 - ri_plaf_2010), ri_apres_2011)

        ri_abs = ri_plaf_2010 + ri_plaf_2011 + ri_plaf_2012

        # choix optimal
        # ri_opt = max_(ri_rel, ri_abs)

        # choix observé
        # ri_choix = (foyer_fiscal('fhqa', period) * ri_rel
        #     + (1 - foyer_fiscal('fhqa', period)) * ri_abs)

        return ri_abs

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2021
        '''

        fhqb = foyer_fiscal('fhqb', period)
        fhqc = foyer_fiscal('fhqc', period)
        fhql = foyer_fiscal('fhql', period)
        fhqt = foyer_fiscal('fhqt', period)
        fhqm = foyer_fiscal('fhqm', period)
        fhqd = foyer_fiscal('fhqd', period)
        fhoa = foyer_fiscal('fhoa', period)
        fhob = foyer_fiscal('fhob', period)
        fhoc = foyer_fiscal('fhoc', period)
        fhol = foyer_fiscal('fhol', period)
        fhom = foyer_fiscal('fhom', period)
        fhon = foyer_fiscal('fhon', period)
        fhod = foyer_fiscal('fhod', period)
        fhua = foyer_fiscal('fhua', period)
        fhuh = foyer_fiscal('fhuh', period)
        fhuo = foyer_fiscal('fhuo', period)
        fhva = foyer_fiscal('fhva', period)

        fhoh = foyer_fiscal('fhoh', period)
        fhoi = foyer_fiscal('fhoi', period)
        fhoj = foyer_fiscal('fhoj', period)
        fhok = foyer_fiscal('fhok', period)
        fhoo = foyer_fiscal('fhoo', period)
        fhop = foyer_fiscal('fhop', period)
        fhoq = foyer_fiscal('fhoq', period)
        fhor = foyer_fiscal('fhor', period)
        fhoe = foyer_fiscal('fhoe', period)
        fhof = foyer_fiscal('fhof', period)
        fhub = foyer_fiscal('fhub', period)
        fhuc = foyer_fiscal('fhuc', period)
        fhui = foyer_fiscal('fhui', period)
        fhuj = foyer_fiscal('fhuj', period)
        fhup = foyer_fiscal('fhup', period)
        fhuq = foyer_fiscal('fhuq', period)
        fhvb = foyer_fiscal('fhvb', period)
        fhvc = foyer_fiscal('fhvc', period)

        fhos = foyer_fiscal('fhos', period)
        fhot = foyer_fiscal('fhot', period)
        fhou = foyer_fiscal('fhou', period)
        fhov = foyer_fiscal('fhov', period)
        fhow = foyer_fiscal('fhow', period)
        fhog = foyer_fiscal('fhog', period)
        fhox = foyer_fiscal('fhox', period)
        fhoy = foyer_fiscal('fhoy', period)
        fhoz = foyer_fiscal('fhoz', period)
        fhud = foyer_fiscal('fhud', period)
        fhue = foyer_fiscal('fhue', period)
        fhuf = foyer_fiscal('fhuf', period)
        fhug = foyer_fiscal('fhug', period)
        fhuk = foyer_fiscal('fhuk', period)
        fhul = foyer_fiscal('fhul', period)
        fhum = foyer_fiscal('fhum', period)
        fhun = foyer_fiscal('fhun', period)
        fhur = foyer_fiscal('fhur', period)
        fhus = foyer_fiscal('fhus', period)
        fhut = foyer_fiscal('fhut', period)
        fhuu = foyer_fiscal('fhuu', period)
        fhvd = foyer_fiscal('fhvd', period)
        fhve = foyer_fiscal('fhve', period)
        fhvf = foyer_fiscal('fhvf', period)
        fhvg = foyer_fiscal('fhvg', period)
        fhvh = foyer_fiscal('fhvh', period)
        fhvi = foyer_fiscal('fhvi', period)
        fhvj = foyer_fiscal('fhvj', period)
        fhvk = foyer_fiscal('fhvk', period)

        ri_avant_2011 = (fhqb
            + fhqc
            + fhql
            + fhqt
            + fhqm
            + fhqd
            + fhoa
            + fhob
            + fhoc
            + fhol
            + fhom
            + fhon
            + fhod
            + fhua
            + fhuh
            + fhuo
            + fhva)

        ri_2011 = (fhoh
            + fhoi
            + fhoj
            + fhok
            + fhoo
            + fhop
            + fhoq
            + fhor
            + fhoe
            + fhof
            + fhub
            + fhuc
            + fhui
            + fhuj
            + fhup
            + fhuq
            + fhvb
            + fhvc)

        ri_apres_2011 = (fhos
            + fhot
            + fhou
            + fhov
            + fhow
            + fhog
            + fhox
            + fhoy
            + fhoz
            + fhud
            + fhue
            + fhuf
            + fhug
            + fhuk
            + fhul
            + fhum
            + fhun
            + fhur
            + fhus
            + fhut
            + fhuu
            + fhvd
            + fhve
            + fhvf
            + fhvg
            + fhvh
            + fhvi
            + fhvj
            + fhvk)

        # application du plafonnement
        P2010 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement
        P2011 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement
        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement

        # rni = foyer_fiscal('rni', period)

        # # si plafond rélatif à 11, 13, 15 % (case HQA)
        # ri_plaf_rel_2010 = min_(ri_avant_2011, rni * P2010.plaf_relatif)
        # ri_plaf_rel_2011 = min_(max_(0, rni * P2011.plaf_relatif - ri_plaf_rel_2010), ri_2011)
        # ri_plaf_rel_2012 = min_(max_(0, rni * P2012.plaf_relatif - ri_plaf_rel_2011 - ri_plaf_rel_2010), ri_apres_2011)

        # ri_rel = ri_plaf_rel_2010 + ri_plaf_rel_2011 + ri_plaf_rel_2012

        # si plafond absolu
        ri_plaf_2010 = min_(ri_avant_2011, P2010.plafond)
        ri_plaf_2011 = min_(max_(0, P2011.plafond - ri_plaf_2010), ri_2011)
        ri_plaf_2012 = min_(max_(0, P.plafond - ri_plaf_2011 - ri_plaf_2010), ri_apres_2011)

        ri_abs = ri_plaf_2010 + ri_plaf_2011 + ri_plaf_2012

        # choix optimal
        # ri_opt = max_(ri_rel, ri_abs)

        # choix observé
        # ri_choix = (foyer_fiscal('fhqa', period) * ri_rel
        #     + (1 - foyer_fiscal('fhqa', period)) * ri_abs)

        return ri_abs


class domsoc(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt au titre de l'acquisition ou de la souscription de logements sociaux outre-mer"
    reference = 'http://bofip.impots.gouv.fr/bofip/9398-PGP'
    definition_period = YEAR

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2010
        '''
        f7qn = foyer_fiscal('f7qn_2012', period)
        f7qk = foyer_fiscal('f7qk_2012', period)
        f7kg = foyer_fiscal('f7kg', period)

        return f7qn + f7qk + f7kg

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2011
        '''
        f7qn = foyer_fiscal('f7qn_2012', period)
        f7qk = foyer_fiscal('f7qk_2012', period)
        f7qu = foyer_fiscal('f7qu_2012', period)
        f7kg = foyer_fiscal('f7kg', period)
        f7kh = foyer_fiscal('f7kh', period)
        f7ki = foyer_fiscal('f7ki', period)

        return f7qn + f7qk + f7qu + f7kg + f7kh + f7ki

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2012
        '''
        f7qn = foyer_fiscal('f7qn_2012', period)
        f7qk = foyer_fiscal('f7qk_2012', period)
        f7qu = foyer_fiscal('f7qu_2012', period)
        f7kg = foyer_fiscal('f7kg', period)
        f7kh = foyer_fiscal('f7kh', period)
        f7ki = foyer_fiscal('f7ki', period)
        f7qj = foyer_fiscal('f7qj_2012', period)
        f7qs = foyer_fiscal('f7qs_2012', period)
        f7qw_2012 = foyer_fiscal('f7qw_2012', period)
        f7qx_2012 = foyer_fiscal('f7qx_2012', period)

        return f7qn + f7qk + f7qu + f7kg + f7kh + f7ki + f7qj + f7qs + f7qw_2012 + f7qx_2012

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2013
        '''
        fhkg = foyer_fiscal('fhkg', period)
        fhkh = foyer_fiscal('fhkh', period)
        fhki = foyer_fiscal('fhki', period)
        fhqj = foyer_fiscal('fhqj', period)
        fhqk = foyer_fiscal('fhqk', period)
        fhqn = foyer_fiscal('fhqn', period)
        fhqs = foyer_fiscal('fhqs', period)
        fhqu = foyer_fiscal('fhqu', period)
        fhqw = foyer_fiscal('fhqw', period)
        fhqx = foyer_fiscal('fhqx', period)
        fhra = foyer_fiscal('fhra', period)
        fhrb = foyer_fiscal('fhrb', period)
        fhrc = foyer_fiscal('fhrc', period)
        fhrd = foyer_fiscal('fhrd', period)

        report_reduc_2009 = fhkg
        report_reduc_2010 = fhkh + fhki
        report_reduc_2011 = fhqn + fhqu + fhqk
        report_reduc_2012 = fhqj + fhqs + fhqw + fhqx
        reduc_invest_2013 = fhra + fhrb + fhrc + fhrd

        return (
            report_reduc_2009
            + report_reduc_2010
            + report_reduc_2011
            + report_reduc_2012
            + reduc_invest_2013
            )

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2014
        '''
        fhkg = foyer_fiscal('fhkg', period)
        fhkh = foyer_fiscal('fhkh', period)
        fhki = foyer_fiscal('fhki', period)
        fhqj = foyer_fiscal('fhqj', period)
        fhqk = foyer_fiscal('fhqk', period)
        fhqn = foyer_fiscal('fhqn', period)
        fhqs = foyer_fiscal('fhqs', period)
        fhqu = foyer_fiscal('fhqu', period)
        fhqw = foyer_fiscal('fhqw', period)
        fhqx = foyer_fiscal('fhqx', period)
        fhra = foyer_fiscal('fhra', period)
        fhrb = foyer_fiscal('fhrb', period)
        fhrc = foyer_fiscal('fhrc', period)
        fhrd = foyer_fiscal('fhrd', period)
        fhxa = foyer_fiscal('fhxa', period)
        fhxb = foyer_fiscal('fhxb', period)
        fhxc = foyer_fiscal('fhxc', period)
        fhxe = foyer_fiscal('fhxe', period)

        report_reduc_2009 = fhkg
        report_reduc_2010 = fhkh + fhki
        report_reduc_2011 = fhqn + fhqu + fhqk
        report_reduc_2012 = fhqj + fhqs + fhqw + fhqx
        report_reduc_2013 = fhra + fhrb + fhrc + fhrd
        reduc_invest_2014 = fhxa + fhxb + fhxc + fhxe

        return (
            report_reduc_2009
            + report_reduc_2010
            + report_reduc_2011
            + report_reduc_2012
            + report_reduc_2013
            + reduc_invest_2014
            )

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2015
        '''
        fhkh = foyer_fiscal('fhkh', period)
        fhki = foyer_fiscal('fhki', period)
        fhqj = foyer_fiscal('fhqj', period)
        fhqk = foyer_fiscal('fhqk', period)
        fhqn = foyer_fiscal('fhqn', period)
        fhqs = foyer_fiscal('fhqs', period)
        fhqu = foyer_fiscal('fhqu', period)
        fhqw = foyer_fiscal('fhqw', period)
        fhqx = foyer_fiscal('fhqx', period)
        fhra = foyer_fiscal('fhra', period)
        fhrb = foyer_fiscal('fhrb', period)
        fhrc = foyer_fiscal('fhrc', period)
        fhrd = foyer_fiscal('fhrd', period)
        fhxa = foyer_fiscal('fhxa', period)
        fhxb = foyer_fiscal('fhxb', period)
        fhxc = foyer_fiscal('fhxc', period)
        fhxe = foyer_fiscal('fhxe', period)
        fhxf = foyer_fiscal('fhxf', period)
        fhxg = foyer_fiscal('fhxg', period)
        fhxh = foyer_fiscal('fhxh', period)
        fhxi = foyer_fiscal('fhxi', period)
        fhxk = foyer_fiscal('fhxk', period)

        report_reduc_2010 = fhkh + fhki
        report_reduc_2011 = fhqn + fhqu + fhqk
        report_reduc_2012 = fhqj + fhqs + fhqw + fhqx
        report_reduc_2013 = fhra + fhrb + fhrc + fhrd
        report_reduc_2014 = fhxa + fhxb + fhxc + fhxe
        reduc_invest_2015 = fhxf + fhxg + fhxh + fhxi + fhxk

        return (
            report_reduc_2010
            + report_reduc_2011
            + report_reduc_2012
            + report_reduc_2013
            + report_reduc_2014
            + reduc_invest_2015
            )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2016

        ATTENTION : Rupture importante à partir de cette année, prise en compte du plafond.
        '''
        fhxf = foyer_fiscal('fhxf', period)
        fhxg = foyer_fiscal('fhxg', period)
        fhxh = foyer_fiscal('fhxh', period)
        fhxi = foyer_fiscal('fhxi', period)
        fhxk = foyer_fiscal('fhxk', period)
        fhxa = foyer_fiscal('fhxa', period)
        fhxb = foyer_fiscal('fhxb', period)
        fhxc = foyer_fiscal('fhxc', period)
        fhxe = foyer_fiscal('fhxe', period)
        fhra = foyer_fiscal('fhra', period)
        fhrb = foyer_fiscal('fhrb', period)
        fhrc = foyer_fiscal('fhrc', period)
        fhrd = foyer_fiscal('fhrd', period)
        fhqj = foyer_fiscal('fhqj', period)
        fhqs = foyer_fiscal('fhqs', period)
        fhqw = foyer_fiscal('fhqw', period)
        fhqx = foyer_fiscal('fhqx', period)
        fhqu = foyer_fiscal('fhqu', period)
        fhqk = foyer_fiscal('fhqk', period)
        fhqn = foyer_fiscal('fhqn', period)
        fhxl = foyer_fiscal('fhxl', period)
        fhxm = foyer_fiscal('fhxm', period)
        fhxn = foyer_fiscal('fhxn', period)
        fhxo = foyer_fiscal('fhxo', period)
        fhxp = foyer_fiscal('fhxp', period)

        ri_soc_65 = (fhqj
            + fhqk
            + fhqn
            + fhqu
            + fhqs
            + fhqw
            + fhqx
            + fhra
            + fhrb
            + fhrc
            + fhrd
            + fhxa
            + fhxb
            + fhxc
            + fhxe
            + fhxf
            + fhxg
            + fhxh
            + fhxi
            + fhxl
            + fhxm
            + fhxn
            + fhxo)

        ri_soc_70 = (fhxk
            + fhxp)

        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc
        P2010 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc

        base_70 = min_(P.partie_non_retro_plaf_abs, ri_soc_70 * (1 - P.retrocession_taux))
        base_65 = min_(P2010.partie_non_retro_plaf_abs - base_70, ri_soc_65 * (1 - P2010.retrocession_taux))

        rc_70 = base_70 * P.retrocession_taux / (1 - P.retrocession_taux)
        rc_65 = base_65 * P2010.retrocession_taux / (1 - P2010.retrocession_taux)

        return base_70 + base_65 + rc_70 + rc_65

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2017
        '''
        # 65 % - avant 2015
        fhxq = foyer_fiscal('fhxq', period)
        fhxr = foyer_fiscal('fhxr', period)
        fhxs = foyer_fiscal('fhxs', period)
        fhxt = foyer_fiscal('fhxt', period)
        fhqj = foyer_fiscal('fhqj', period)
        fhqs = foyer_fiscal('fhqs', period)
        fhqw = foyer_fiscal('fhqw', period)
        fhqx = foyer_fiscal('fhqx', period)
        fhra = foyer_fiscal('fhra', period)
        fhrb = foyer_fiscal('fhrb', period)
        fhrc = foyer_fiscal('fhrc', period)
        fhrd = foyer_fiscal('fhrd', period)
        fhxa = foyer_fiscal('fhxa', period)
        fhxb = foyer_fiscal('fhxb', period)
        fhxc = foyer_fiscal('fhxc', period)
        fhxe = foyer_fiscal('fhxe', period)
        fhxf = foyer_fiscal('fhxf', period)
        fhxg = foyer_fiscal('fhxg', period)
        fhxh = foyer_fiscal('fhxh', period)
        fhxi = foyer_fiscal('fhxi', period)
        fhxl = foyer_fiscal('fhxl', period)
        fhxm = foyer_fiscal('fhxm', period)
        fhxn = foyer_fiscal('fhxn', period)
        fhxo = foyer_fiscal('fhxo', period)

        ri_soc_65 = (fhxq
            + fhxr
            + fhxs
            + fhxt
            + fhqj
            + fhqs
            + fhqw
            + fhqx
            + fhra
            + fhrb
            + fhrc
            + fhrd
            + fhxa
            + fhxb
            + fhxc
            + fhxe
            + fhxf
            + fhxg
            + fhxh
            + fhxi
            + fhxl
            + fhxm
            + fhxn
            + fhxo)

        # 70 % - à partir de 2015
        fhxu = foyer_fiscal('fhxu', period)
        fhxk = foyer_fiscal('fhxk', period)
        fhxp = foyer_fiscal('fhxp', period)

        ri_soc_70 = (fhxu
            + fhxk
            + fhxp)

        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc
        P2010 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc

        base_70 = min_(P.partie_non_retro_plaf_abs, ri_soc_70 * (1 - P.retrocession_taux))
        base_65 = min_(P2010.partie_non_retro_plaf_abs - base_70, ri_soc_65 * (1 - P2010.retrocession_taux))

        rc_70 = base_70 * P.retrocession_taux / (1 - P.retrocession_taux)
        rc_65 = base_65 * P2010.retrocession_taux / (1 - P2010.retrocession_taux)

        return base_70 + base_65 + rc_70 + rc_65

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2018
        '''
        # 65 % - avant 2015
        fhya = foyer_fiscal('fhya', period)
        fhra = foyer_fiscal('fhra', period)
        fhrb = foyer_fiscal('fhrb', period)
        fhrc = foyer_fiscal('fhrc', period)
        fhrd = foyer_fiscal('fhrd', period)
        fhxa = foyer_fiscal('fhxa', period)
        fhxb = foyer_fiscal('fhxb', period)
        fhxc = foyer_fiscal('fhxc', period)
        fhxe = foyer_fiscal('fhxe', period)
        fhxf = foyer_fiscal('fhxf', period)
        fhxg = foyer_fiscal('fhxg', period)
        fhxh = foyer_fiscal('fhxh', period)
        fhxi = foyer_fiscal('fhxi', period)
        fhxl = foyer_fiscal('fhxl', period)
        fhxm = foyer_fiscal('fhxm', period)
        fhxn = foyer_fiscal('fhxn', period)
        fhxo = foyer_fiscal('fhxo', period)
        fhxq = foyer_fiscal('fhxq', period)
        fhxr = foyer_fiscal('fhxr', period)
        fhxs = foyer_fiscal('fhxs', period)
        fhxt = foyer_fiscal('fhxt', period)

        # 70 % - à partir de 2015
        fhyb = foyer_fiscal('fhyb', period)
        fhxk = foyer_fiscal('fhxk', period)
        fhxp = foyer_fiscal('fhxp', period)
        fhxu = foyer_fiscal('fhxu', period)

        ri_soc_65 = (fhxq
            + fhxr
            + fhxs
            + fhxt
            + fhra
            + fhrb
            + fhrc
            + fhrd
            + fhxa
            + fhxb
            + fhxc
            + fhxe
            + fhxf
            + fhxg
            + fhxh
            + fhxi
            + fhxl
            + fhxm
            + fhxn
            + fhxo
            + fhya)

        ri_soc_70 = (fhxu
            + fhxk
            + fhxp
            + fhyb)

        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc
        P2010 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc

        base_70 = min_(P.partie_non_retro_plaf_abs, ri_soc_70 * (1 - P.retrocession_taux))
        base_65 = min_(P2010.partie_non_retro_plaf_abs - base_70, ri_soc_65 * (1 - P2010.retrocession_taux))

        rc_70 = base_70 * P.retrocession_taux / (1 - P.retrocession_taux)
        rc_65 = base_65 * P2010.retrocession_taux / (1 - P2010.retrocession_taux)

        return base_70 + base_65 + rc_70 + rc_65

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2019
        '''
        # 65 % - avant 2015
        fhyc = foyer_fiscal('fhyc', period)
        fhxa = foyer_fiscal('fhxa', period)
        fhxb = foyer_fiscal('fhxb', period)
        fhxc = foyer_fiscal('fhxc', period)
        fhxe = foyer_fiscal('fhxe', period)
        fhxf = foyer_fiscal('fhxf', period)
        fhxg = foyer_fiscal('fhxg', period)
        fhxh = foyer_fiscal('fhxh', period)
        fhxi = foyer_fiscal('fhxi', period)
        fhxl = foyer_fiscal('fhxl', period)
        fhxm = foyer_fiscal('fhxm', period)
        fhxn = foyer_fiscal('fhxn', period)
        fhxo = foyer_fiscal('fhxo', period)
        fhxq = foyer_fiscal('fhxq', period)
        fhxr = foyer_fiscal('fhxr', period)
        fhxs = foyer_fiscal('fhxs', period)
        fhxt = foyer_fiscal('fhxt', period)
        fhya = foyer_fiscal('fhya', period)

        # 70 % - à partir de 2015
        fhyd = foyer_fiscal('fhyd', period)
        fhxk = foyer_fiscal('fhxk', period)
        fhxp = foyer_fiscal('fhxp', period)
        fhxu = foyer_fiscal('fhxu', period)
        fhyb = foyer_fiscal('fhyb', period)

        ri_soc_65 = (fhyc
            + fhxq
            + fhxr
            + fhxs
            + fhxt
            + fhxa
            + fhxb
            + fhxc
            + fhxe
            + fhxf
            + fhxg
            + fhxh
            + fhxi
            + fhxl
            + fhxm
            + fhxn
            + fhxo
            + fhya)

        ri_soc_70 = (fhyd
            + fhxu
            + fhxk
            + fhxp
            + fhyb)

        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc
        P2010 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc

        base_70 = min_(P.partie_non_retro_plaf_abs, ri_soc_70 * (1 - P.retrocession_taux))
        base_65 = min_(P2010.partie_non_retro_plaf_abs - base_70, ri_soc_65 * (1 - P2010.retrocession_taux))

        rc_70 = base_70 * P.retrocession_taux / (1 - P.retrocession_taux)
        rc_65 = base_65 * P2010.retrocession_taux / (1 - P2010.retrocession_taux)

        return base_70 + base_65 + rc_70 + rc_65

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2020
        '''
        # 65 % - avant 2015
        fhxf = foyer_fiscal('fhxf', period)
        fhxg = foyer_fiscal('fhxg', period)
        fhxh = foyer_fiscal('fhxh', period)
        fhxi = foyer_fiscal('fhxi', period)
        fhxl = foyer_fiscal('fhxl', period)
        fhxm = foyer_fiscal('fhxm', period)
        fhxn = foyer_fiscal('fhxn', period)
        fhxo = foyer_fiscal('fhxo', period)
        fhxq = foyer_fiscal('fhxq', period)
        fhxr = foyer_fiscal('fhxr', period)
        fhxs = foyer_fiscal('fhxs', period)
        fhxt = foyer_fiscal('fhxt', period)
        fhya = foyer_fiscal('fhya', period)
        fhyc = foyer_fiscal('fhyc', period)

        # 70 % - à partir de 2015
        fhye = foyer_fiscal('fhye', period)
        fhxk = foyer_fiscal('fhxk', period)
        fhxp = foyer_fiscal('fhxp', period)
        fhxu = foyer_fiscal('fhxu', period)
        fhyb = foyer_fiscal('fhyb', period)
        fhyd = foyer_fiscal('fhyd', period)

        ri_soc_65 = (fhyc
            + fhxq
            + fhxr
            + fhxs
            + fhxt
            + fhxf
            + fhxg
            + fhxh
            + fhxi
            + fhxl
            + fhxm
            + fhxn
            + fhxo
            + fhya)

        ri_soc_70 = (fhye
            + fhyd
            + fhxu
            + fhxk
            + fhxp
            + fhyb)

        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc
        P2010 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc

        base_70 = min_(P.partie_non_retro_plaf_abs, ri_soc_70 * (1 - P.retrocession_taux))
        base_65 = min_(P2010.partie_non_retro_plaf_abs - base_70, ri_soc_65 * (1 - P2010.retrocession_taux))

        rc_70 = base_70 * P.retrocession_taux / (1 - P.retrocession_taux)
        rc_65 = base_65 * P2010.retrocession_taux / (1 - P2010.retrocession_taux)

        return base_70 + base_65 + rc_70 + rc_65

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2021
        '''
        # 65 % - avant 2015
        fhxl = foyer_fiscal('fhxl', period)
        fhxm = foyer_fiscal('fhxm', period)
        fhxn = foyer_fiscal('fhxn', period)
        fhxo = foyer_fiscal('fhxo', period)
        fhxq = foyer_fiscal('fhxq', period)
        fhxr = foyer_fiscal('fhxr', period)
        fhxs = foyer_fiscal('fhxs', period)
        fhxt = foyer_fiscal('fhxt', period)
        fhya = foyer_fiscal('fhya', period)
        fhyc = foyer_fiscal('fhyc', period)

        # 70 % - à partir de 2015
        fhyf = foyer_fiscal('fhyf', period)
        fhxp = foyer_fiscal('fhxp', period)
        fhxu = foyer_fiscal('fhxu', period)
        fhye = foyer_fiscal('fhye', period)
        fhyb = foyer_fiscal('fhyb', period)
        fhyd = foyer_fiscal('fhyd', period)

        ri_soc_65 = (fhyc
            + fhxq
            + fhxr
            + fhxs
            + fhxt
            + fhxl
            + fhxm
            + fhxn
            + fhxo
            + fhya)

        ri_soc_70 = (fhyf
            + fhye
            + fhyd
            + fhxu
            + fhxp
            + fhyb)

        P = parameters(period).impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc
        P2010 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.outremer_investissement.domsoc

        base_70 = min_(P.partie_non_retro_plaf_abs, ri_soc_70 * (1 - P.retrocession_taux))
        base_65 = min_(P2010.partie_non_retro_plaf_abs - base_70, ri_soc_65 * (1 - P2010.retrocession_taux))

        rc_70 = base_70 * P.retrocession_taux / (1 - P.retrocession_taux)
        rc_65 = base_65 * P2010.retrocession_taux / (1 - P2010.retrocession_taux)

        return base_70 + base_65 + rc_70 + rc_65
