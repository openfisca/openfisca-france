# -*- coding: utf-8 -*-

import sys
import pprint
import io
from ruamel.yaml import YAML, RoundTripRepresenter
import copy

def my_represent_none(self, data):
    return self.represent_scalar(u'tag:yaml.org,2002:null', u'null')

RoundTripRepresenter.add_representer(type(None), my_represent_none)

yaml = YAML()
yaml.default_flow_style = False
yaml.preserve_quotes = True
yaml.width = 1000

def migrate(path):
    with io.open(path, 'r', encoding='utf8') as f:
        try:
            data = yaml.load(f)
            tests = data if isinstance(data, list) else [ data ]

            for test in tests:
                if 'familles' not in test:
                    continue

                familles = test['familles']
                familles = familles if isinstance(familles, list) else [ familles ]

                asi = None
                for f in familles:
                    if 'asi' in f:
                        asi = f['asi']
                        del f['asi']

                if not asi:
                    continue

                if sum([abs(v) for v in asi.values()]):
                    individus = test['individus']
                    individus = individus if isinstance(individus, list) else [ individus ]
                    for i in individus:
                        i['asi'] = copy.deepcopy(asi)

            with io.open(path, 'w', encoding='utf8') as f:
                yaml.dump(data, f)
        except Exception as e:
            print (path)
            raise e


if __name__ == "__main__":
    for p in sys.argv[1:]:
        migrate(p)
