#! /usr/bin/env python
'''Open a variable in the DGFIP website in a browser.'''


import argparse
import logging
import os
import re
import sys
import webbrowser


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)

DEFAULT_YEAR = 2013


def inspect_dgfip_variable(variable, year, browser_name):
    # Attention les liens changent entre la version simplifiée
    matched = re.match('^f[1-8][a-z]{2}', variable)
    assert matched is not None, 'Invalid variable: {}'.format(variable)
    section_number = variable[1]
    case = variable[2:4].upper()
    log.info('section %s, case %s', section_number, case)
    url_base = 'http://www3.impots.gouv.fr/simulateur/calcul_impot/' + str(year + 1) + '/aides/'
    url_section = {
        '2': 'capitaux_mobiliers.htm',
        '3': 'gains_c.htm',
        '4': 'fonciers.htm',
        # '5': "charges_s.htm",
        '6': 'charges.htm',
        '7': 'reductions.htm',
        '8': 'autres_imputations.htm',
        }.get(section_number)
    assert url_section is not None, 'Unhandled section number: {}'.format(section_number)
    url = url_base + url_section
    if section_number not in ('3', '4'):
        url += '#' + case

    browser = webbrowser.get(browser_name)
    browser.open_new_tab(url)


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('variable_name', help = 'Name of the variable to inspect. Example: "f7wr"')
    parser.add_argument('--browser', dest = 'browser_name', default = 'chromium', help = 'Open links in this browser')
    parser.add_argument('--min-year', default = None, help = 'Year to start from', type = int)
    parser.add_argument('--max-year', default = None, help = 'Year to stop to', type = int)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = 'Increase output verbosity')
    parser.add_argument('--year', default = None, help = 'Inspect the variable for the given year', type = int)
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    if args.year and (args.min_year or args.max_year):
        parser.error('year and {min,max}-year arguments cannot be used together')

    if args.min_year or args.max_year:
        if args.min_year and args.max_year:
            for year in range(args.max_year, args.min_year, -1):
                try:
                    inspect_dgfip_variable(args.variable_name, year, args.browser_name)
                except ValueError:
                    log.error('Variable "%s" not found', args.variable_name)
        else:
            parser.error('Please give min and max year')
    else:
        year = args.year or DEFAULT_YEAR
        try:
            inspect_dgfip_variable(args.variable_name, year, args.browser_name)
        except ValueError:
            log.error('Variable "%s" not found', args.variable_name)


if __name__ == '__main__':
    sys.exit(main())
