##
## CREATION DES VARIABLES DE BASE
##

# "DomLog" - art. 199 undecies A CGI
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class ri_iom_domlog_non_plaf_pg0809(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "RI DomLog non-plafonnées (plaf. spéc.), plaf. global de 2008/09"
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhqb = foyer_fiscal('fhqb', period)
        fhqc = foyer_fiscal('fhqc', period)
        fhqt = foyer_fiscal('fhqt', period)
        fhoa = foyer_fiscal('fhoa', period)
        fhoh = foyer_fiscal('fhoh', period)
        fhol = foyer_fiscal('fhol', period)
        fhoo = foyer_fiscal('fhoo', period)
        fhos = foyer_fiscal('fhos', period)

        return fhqb + fhqc + fhqt + fhoa + fhoh + fhol + fhoo + fhos


class ri_iom_domlog_40_pg0809(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "RI DomLog plaf. 40K/15% - plaf. glob. de 2008/09"
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        PB = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.rici_iom.plafond.plafond_de_base
        PPG = parameters('2009-01-01').impot_revenu.calcul_credits_impots.plaf_nich.plafonnement_des_niches
        PG = PPG.plafond_1 + PPG.taux * foyer_fiscal('rni', period)

        fhql = foyer_fiscal('fhql', period)
        fhqm = foyer_fiscal('fhqm', period)
        fhob = foyer_fiscal('fhob', period)
        fhom = foyer_fiscal('fhom', period)

        ri = min_(PB,
            PG,
            fhql + fhqm + fhob + fhom)

        return ri


class ri_iom_domlog_40_pg10(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "RI DomLog plaf. 40K/15% - plaf. glob. de 2010"
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        PB = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.rici_iom.plafond
        PPG = parameters('2010-01-01').impot_revenu.calcul_credits_impots.plaf_nich.plafonnement_des_niches
        PG = PPG.plafond_1 + PPG.taux * foyer_fiscal('rni', period)

        utilise = foyer_fiscal('ri_iom_domlog_40_pg0809', period)

        fhqd = foyer_fiscal('fhqd', period)
        fhoc = foyer_fiscal('fhoc', period)
        fhon = foyer_fiscal('fhon', period)
        fhod = foyer_fiscal('fhod', period)
        fhua = foyer_fiscal('fhua', period)
        fhuh = foyer_fiscal('fhuh', period)
        fhuo = foyer_fiscal('fhuo', period)
        fhva = foyer_fiscal('fhva', period)

        ri = min_(PB - utilise,
            PG - utilise,
            fhqd + fhoc + fhon + fhod + fhua + fhuh + fhuo + fhva)

        return ri


class ri_iom_domlog_36_pg0809(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "RI DomLog plaf. 36K/13% - plaf. glob. de 2008/09"
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhoi = foyer_fiscal('fhoi', period)
        fhop = foyer_fiscal('fhop', period)

        return fhoi + fhop


class ri_iom_domlog_36_pg10(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "RI DomLog plaf. 36K/13% - plaf. glob. de 2010"
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhoj = foyer_fiscal('fhoj', period)
        fhoq = foyer_fiscal('fhoq', period)
        fhoe = foyer_fiscal('fhoe', period)
        fhub = foyer_fiscal('fhub', period)
        fhui = foyer_fiscal('fhui', period)
        fhup = foyer_fiscal('fhup', period)
        fhvb = foyer_fiscal('fhvb', period)

        return fhoj + fhoq + fhoe + fhub + fhui + fhup + fhvb


class ri_iom_domlog_36_pg11(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "RI DomLog plaf. 36K/13% - plaf. glob. de 2011"
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhok = foyer_fiscal('fhok', period)
        fhor = foyer_fiscal('fhor', period)
        fhof = foyer_fiscal('fhof', period)
        fhuc = foyer_fiscal('fhuc', period)
        fhuj = foyer_fiscal('fhuj', period)
        fhuq = foyer_fiscal('fhuq', period)
        fhvc = foyer_fiscal('fhvc', period)

        return fhok + fhor + fhof + fhuc + fhuj + fhuq + fhvc


class ri_iom_domlog_306_pg0809(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "RI DomLog plaf. 30.6K/11% - plaf. glob. de 2008/09"
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhot = foyer_fiscal('fhot', period)

        return fhot


class ri_iom_domlog_306_pg10(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "RI DomLog plaf. 30.6K/11% - plaf. glob. de 2010"
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhou = foyer_fiscal('fhou', period)
        fhog = foyer_fiscal('fhog', period)
        fhud = foyer_fiscal('fhud', period)
        fhuk = foyer_fiscal('fhuk', period)
        fhur = foyer_fiscal('fhur', period)
        fhvd = foyer_fiscal('fhvd', period)

        return fhou + fhog + fhud + fhuk + fhur + fhvd


class ri_iom_domlog_306_pg11(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "RI DomLog plaf. 30.6K/11% - plaf. glob. de 2011"
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhov = foyer_fiscal('fhov', period)
        fhox = foyer_fiscal('fhox', period)
        fhue = foyer_fiscal('fhue', period)
        fhul = foyer_fiscal('fhul', period)
        fhus = foyer_fiscal('fhus', period)
        fhve = foyer_fiscal('fhve', period)

        return fhov + fhox + fhue + fhul + fhus + fhve


class ri_iom_domlog_306_pg12(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "RI DomLog plaf. 30.6K/11% - plaf. glob. de 2012"
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhow = foyer_fiscal('fhow', period)
        fhoy = foyer_fiscal('fhoy', period)
        fhuf = foyer_fiscal('fhuf', period)
        fhum = foyer_fiscal('fhum', period)
        fhut = foyer_fiscal('fhut', period)
        fhvf = foyer_fiscal('fhvf', period)

        return fhow + fhoy + fhuf + fhum + fhut + fhvf


class ri_iom_domlog_306_pg13(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "RI DomLog plaf. 30.6K/11% - plaf. glob. de 2013"
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhoz = foyer_fiscal('fhoz', period)
        fhug = foyer_fiscal('fhug', period)
        fhun = foyer_fiscal('fhun', period)
        fhuu = foyer_fiscal('fhuu', period)
        fhvg = foyer_fiscal('fhvg', period)

        return fhoz + fhug + fhun + fhuu + fhvg

# "DomEnt" - art. 199 undecies B CGI
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class doment_loc_non_plaf(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhpm = foyer_fiscal('fhpm', period)
        fhrj = foyer_fiscal('fhrj', period)

        return fhpm + fhrj


class doment_loc_pg0809_ps40_tr50(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhpn = foyer_fiscal('fhpn', period)

        return fhpn


class doment_loc_pg10_ps40_tr50(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhps = foyer_fiscal('fhps', period)

        return fhps


class doment_loc_pg0809_ps40_tr60(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhpo = foyer_fiscal('fhpo', period)

        return fhpo


class doment_loc_pg10_ps40_tr60(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhpt = foyer_fiscal('fhpt', period)

        return fhpt


class doment_loc_pg10_ps36_tr5263(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhaa = foyer_fiscal('fhaa', period)
        fhsa = foyer_fiscal('fhsa', period)

        return fhaa + fhsa


class doment_loc_pg11_ps36_tr5263(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhpx = foyer_fiscal('fhpx', period)
        fhaf = foyer_fiscal('fhaf', period)
        fhsf = foyer_fiscal('fhsf', period)

        return fhpx + fhaf + fhsf


class doment_loc_pg10_ps36_tr625(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhab = foyer_fiscal('fhab', period)
        fhsb = foyer_fiscal('fhsb', period)

        return fhab + fhsb


class doment_loc_pg11_ps36_tr625(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhpy = foyer_fiscal('fhpy', period)
        fhag = foyer_fiscal('fhag', period)
        fhsg = foyer_fiscal('fhsg', period)

        return fhpy + fhag + fhsg


class doment_loc_pg0809_ps306_tr5263(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhrk = foyer_fiscal('fhrk', period)

        return fhrk


class doment_loc_pg10_ps306_tr5263(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhrp = foyer_fiscal('fhrp', period)
        fhsk = foyer_fiscal('fhsk', period)
        fhak = foyer_fiscal('fhak', period)
        fhbi = foyer_fiscal('fhbi', period)

        return fhrp + fhsk + fhak + fhbi


class doment_loc_pg11_ps306_tr5263(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhru = foyer_fiscal('fhru', period)
        fhsp = foyer_fiscal('fhsp', period)
        fhap = foyer_fiscal('fhap', period)
        fhbn = foyer_fiscal('fhbn', period)

        return fhru + fhsp + fhap + fhbn


class doment_loc_pg12_ps306_tr5263(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhdi = foyer_fiscal('fhdi', period)
        fhnu = foyer_fiscal('fhnu', period)
        fhsu = foyer_fiscal('fhsu', period)
        fhau = foyer_fiscal('fhau', period)
        fhbs = foyer_fiscal('fhbs', period)
        fhci = foyer_fiscal('fhci', period)

        return fhdi + fhnu + fhsu + fhau + fhbs + fhci


class doment_loc_pg13_ps306_tr5263(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhdn = foyer_fiscal('fhdn', period)
        fhsz = foyer_fiscal('fhsz', period)
        fhba = foyer_fiscal('fhba', period)
        fhbx = foyer_fiscal('fhbx', period)
        fhcn = foyer_fiscal('fhcn', period)

        return fhdn + fhsz + fhba + fhbx + fhcn


class doment_loc_pg0809_ps306_tr625(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhrl = foyer_fiscal('fhrl', period)

        return fhrl


class doment_loc_pg10_ps306_tr625(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhrq = foyer_fiscal('fhrq', period)
        fhsl = foyer_fiscal('fhsl', period)
        fhal = foyer_fiscal('fhal', period)
        fhbj = foyer_fiscal('fhbj', period)

        return fhrq + fhsl + fhal + fhbj


class doment_loc_pg11_ps306_tr625(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhrv = foyer_fiscal('fhrv', period)
        fhsq = foyer_fiscal('fhsq', period)
        fhaq = foyer_fiscal('fhaq', period)
        fhbo = foyer_fiscal('fhbo', period)

        return fhrv + fhsq + fhaq + fhbo


class doment_loc_pg12_ps306_tr625(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhdj = foyer_fiscal('fhdj', period)
        fhnv = foyer_fiscal('fhnv', period)
        fhsv = foyer_fiscal('fhsv', period)
        fhav = foyer_fiscal('fhav', period)
        fhbt = foyer_fiscal('fhbt', period)
        fhcj = foyer_fiscal('fhcj', period)

        return fhdj + fhnv + fhsv + fhav + fhbt + fhcj


class doment_loc_pg13_ps306_tr625(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhdo = foyer_fiscal('fhdo', period)
        fhta = foyer_fiscal('fhta', period)
        fhbb = foyer_fiscal('fhbb', period)
        fhby = foyer_fiscal('fhby', period)
        fhco = foyer_fiscal('fhco', period)

        return fhdo + fhta + fhbb + fhby + fhco


class doment_loc_pg13_ps306_tr56(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhds = foyer_fiscal('fhds', period)
        fhcc = foyer_fiscal('fhcc', period)
        fhcs = foyer_fiscal('fhcs', period)

        return fhds + fhcc + fhcs


class doment_loc_pg13_ps306_tr66(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhdt = foyer_fiscal('fhdt', period)
        fhcd = foyer_fiscal('fhcd', period)
        fhct = foyer_fiscal('fhct', period)

        return fhdt + fhcd + fhct


class doment_propre_pg0809_ps40(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhpp = foyer_fiscal('fhpp', period)

        return fhpp


class doment_propre_pg10_ps40(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhpu = foyer_fiscal('fhpu', period)

        return fhpu


class doment_propre_pg0809_ps100(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhpr = foyer_fiscal('fhpr', period)

        return fhpr


class doment_propre_pg10_ps100(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhpw = foyer_fiscal('fhpw', period)

        return fhpw


class doment_propre_pg10_ps36(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhsc = foyer_fiscal('fhsc', period)
        fhac = foyer_fiscal('fhac', period)

        return fh


class doment_propre_pg11_ps36(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhrg = foyer_fiscal('fhrg', period)
        fhsh = foyer_fiscal('fhsh', period)
        fhah = foyer_fiscal('fhah', period)

        return fh


class doment_propre_pg10_ps90(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhse = foyer_fiscal('fhse', period)
        fhae = foyer_fiscal('fhae', period)

        return fh


class doment_propre_pg11_ps90(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhri = foyer_fiscal('fhri', period)
        fhsj = foyer_fiscal('fhsj', period)
        fhaj = foyer_fiscal('fhaj', period)

        return fh


class doment_propre_pg0809_ps306(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhrm = foyer_fiscal('fhrm', period)

        return fhrm


class doment_propre_pg10_ps306(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhrr = foyer_fiscal('fhrr', period)
        fhsm = foyer_fiscal('fhsm', period)
        fham = foyer_fiscal('fham', period)
        fhbk = foyer_fiscal('fhbk', period)

        return fhrr + fhsm + fham + fhbk


class doment_propre_pg11_ps306(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhrw = foyer_fiscal('fhrw', period)
        fhsr = foyer_fiscal('fhsr', period)
        fhar = foyer_fiscal('fhar', period)
        fhbp = foyer_fiscal('fhbp', period)

        return fhrw + fhsr + fhar + fhbp


class doment_propre_pg12_ps306(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhdk = foyer_fiscal('fhdk', period)
        fhnw = foyer_fiscal('fhnw', period)
        fhsw = foyer_fiscal('fhsw', period)
        fhaw = foyer_fiscal('fhaw', period)
        fhbu = foyer_fiscal('fhbu', period)
        fhck = foyer_fiscal('fhck', period)

        return fhdk + fhnw + fhsw + fhaw + fhbu + fhck


class doment_propre_pg13_ps306(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhdp = foyer_fiscal('fhdp', period)
        fhdu = foyer_fiscal('fhdu', period)
        fhtb = foyer_fiscal('fhtb', period)
        fhbe = foyer_fiscal('fhbe', period)
        fhbz = foyer_fiscal('fhbz', period)
        fhce = foyer_fiscal('fhce', period)
        fhcp = foyer_fiscal('fhcp', period)
        fhcu = foyer_fiscal('fhcu', period)

        return fhdp + fhdu + fhtb + fhbe + fhbz + fhce + fhcp + fhcu


class doment_propre_pg0809_ps765(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhro = foyer_fiscal('fhro', period)

        return fhro


class doment_propre_pg10_ps765(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhrt = foyer_fiscal('fhrt', period)
        fhso = foyer_fiscal('fhso', period)
        fhao = foyer_fiscal('fhao', period)
        fhbm = foyer_fiscal('fhbm', period)

        return fhrt + fhso + fhao + fhbm


class doment_propre_pg11_ps765(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhry = foyer_fiscal('fhry', period)
        fhst = foyer_fiscal('fhst', period)
        fhat = foyer_fiscal('fhat', period)
        fhbr = foyer_fiscal('fhbr', period)

        return fhry + fhst + fhat + fhbr


class doment_propre_pg12_ps765(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhdm = foyer_fiscal('fhdm', period)
        fhny = foyer_fiscal('fhny', period)
        fhsy = foyer_fiscal('fhsy', period)
        fhay = foyer_fiscal('fhay', period)
        fhbw = foyer_fiscal('fhbw', period)
        fhcm = foyer_fiscal('fhcm', period)

        return fhdm + fhny + fhsy + fhay + fhbw + fhcm


class doment_propre_pg13_ps765(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhdr = foyer_fiscal('fhdr', period)
        fhdw = foyer_fiscal('fhdw', period)
        fhtd = foyer_fiscal('fhtd', period)
        fhbg = foyer_fiscal('fhbg', period)
        fhcb = foyer_fiscal('fhcb', period)
        fhcg = foyer_fiscal('fhcg', period)
        fhcr = foyer_fiscal('fhcr', period)
        fhcw = foyer_fiscal('fhcw', period)

        return fhdr + fhdw + fhtd + fhbg + fhcb + fhcg + fhcr + fhcw

# "DomSoc" - art. 199 undecies C CGI
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class domsoc_pg0809_tr65(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhqj = foyer_fiscal('fhqj', period)

        return fhqj


class domsoc_pg10_tr65(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhxq = foyer_fiscal('fhxq', period)
        fhqs = foyer_fiscal('fhqs', period)
        fhra = foyer_fiscal('fhra', period)
        fhxa = foyer_fiscal('fhxa', period)
        fhxf = foyer_fiscal('fhxf', period)
        fhxl = foyer_fiscal('fhxl', period)

        return fhxq + fhqs + fhra + fhxa + fhxf + fhxl


class domsoc_pg11_tr65(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhxr = foyer_fiscal('fhxr', period)
        fhqw = foyer_fiscal('fhqw', period)
        fhrb = foyer_fiscal('fhrb', period)
        fhxb = foyer_fiscal('fhxb', period)
        fhxg = foyer_fiscal('fhxg', period)
        fhxm = foyer_fiscal('fhxm', period)

        return fhxr + fhqw + fhrb + fhxb + fhxg + fhxm


class domsoc_pg12_tr65(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhxs = foyer_fiscal('fhxs', period)
        fhqx = foyer_fiscal('fhqx', period)
        fhrc = foyer_fiscal('fhrc', period)
        fhxc = foyer_fiscal('fhxc', period)
        fhxh = foyer_fiscal('fhxh', period)
        fhxn = foyer_fiscal('fhxn', period)

        return fhxs + fhqx + fhrc + fhxc + fhxh + fhxn


class domsoc_pg13_tr65(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhxt = foyer_fiscal('fhxt', period)
        fhrd = foyer_fiscal('fhrd', period)
        fhxe = foyer_fiscal('fhxe', period)
        fhxi = foyer_fiscal('fhxi', period)
        fhxo = foyer_fiscal('fhxo', period)

        return fhxt + fhrd + fhxe + fhxi + fhxo


class domsoc_tr70(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        fhxu = foyer_fiscal('fhxu', period)
        fhxk = foyer_fiscal('fhxk', period)
        fhxp = foyer_fiscal('fhxp', period)

        return fhxu + fhxk + fhxp

##
## CREATION DES VARIABLES DE BASE
##

P09 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.rici_iom.plafond
P11 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.rici_iom.plafond
P12 = parameters('2012-01-01').impot_revenu.calcul_reductions_impots.rici_iom.plafond
P13 = parameters('2013-01-01').impot_revenu.calcul_reductions_impots.rici_iom.plafond

# Partie I (II) : Non-rétrocédée

## Plafond I.A (C) : € 40K

### Dispositif I.A.1 (3) : DomLog (art. 199 undecies A CGI)

class rl_40_0809(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        P09 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.rici_iom.plafond
        ri_iom_domlog_40_pg0809 = foyer_fiscal('ri_iom_domlog_40_pg0809', period)

        return fmin_(P09.plafond_de_base, ri_iom_domlog_40_pg0809)











### Dispositif I.A.2 (3) : DomSoc (art. 199 undecies C CGI)

# ---

### Dispositif I.A.3 (3) : DomEnt (art. 199 undecies B CGI)
### (ordre décroissant par taux de rétrocession)

# ---

## Plafond I.B (C) : € 36K

### Dispositif I.B.1 (3) : DomLog (art. 199 undecies A CGI)

# ---

### Dispositif I.B.2 (3) : DomSoc (art. 199 undecies C CGI)

# ---

### Dispositif I.B.3 (3) : DomEnt (art. 199 undecies B CGI)
### (ordre décroissant par taux de rétrocession)

# ---

## Plafond I.C (C) : € 30.6K

### Dispositif I.C.1 (3) : DomLog (art. 199 undecies A CGI)

# ---

### Dispositif I.C.2 (3) : DomSoc (art. 199 undecies C CGI)

# ---

### Dispositif I.C.3 (3) : DomEnt (art. 199 undecies B CGI)
### (ordre décroissant par taux de rétrocession)

# ---

# Partie II (II) : Rétrocédée

## Plafond II.A (C) : € 40K

### Dispositif II.A.1 (3) : DomLog (art. 199 undecies A CGI)

# ---

### Dispositif II.A.2 (3) : DomSoc (art. 199 undecies C CGI)

# ---

### Dispositif II.A.3 (3) : DomEnt (art. 199 undecies B CGI)
### (ordre décroissant par taux de rétrocession)

# ---

## Plafond II.B (C) : € 36K

### Dispositif II.B.1 (3) : DomLog (art. 199 undecies A CGI)

# ---

### Dispositif II.B.2 (3) : DomSoc (art. 199 undecies C CGI)

# ---

### Dispositif II.B.3 (3) : DomEnt (art. 199 undecies B CGI)
### (ordre décroissant par taux de rétrocession)

# ---

## Plafond II.C (C) : € 30.6K

### Dispositif II.C.1 (3) : DomLog (art. 199 undecies A CGI)

# ---

### Dispositif II.C.2 (3) : DomSoc (art. 199 undecies C CGI)

# ---

### Dispositif II.C.3 (3) : DomEnt (art. 199 undecies B CGI)
### (ordre décroissant par taux de rétrocession)

# ---

