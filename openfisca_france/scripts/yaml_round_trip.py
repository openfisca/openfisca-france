# -*- coding: utf-8 -*-

import sys
import pprint
import io
from ruamel.yaml import YAML, RoundTripRepresenter

def my_represent_none(self, data):
    return self.represent_scalar(u'tag:yaml.org,2002:null', u'null')

RoundTripRepresenter.add_representer(type(None), my_represent_none)

yaml = YAML()
yaml.default_flow_style = False
yaml.width = 1000

def roundTrip(path):
    with io.open(path, 'r', encoding='utf8') as f:
        try:
            data = yaml.load(f)
            with io.open(path, 'w', encoding='utf8') as f:
                yaml.dump(data, f)
        except Exception as e:
            raise e


if __name__ == "__main__":
    for p in sys.argv[1:]:
        roundTrip(p)
