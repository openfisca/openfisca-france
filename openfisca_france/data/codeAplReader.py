# -*- coding:utf-8 -*-
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

"""
µSim, Logiciel libre de simulation du système socio-fiscal français
Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul


This file is part of µSim.

    µSim is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    µSim is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with µSim.  If not, see <http://www.gnu.org/licenses/>.
"""

import csv, pickle

codeDict = {}
fileName = 'zone_apl.csv'

code = csv.reader(open(fileName), delimiter = ";")

for row in code:
    codeDict.update({row[2]:(row[1],row[4])})

#print codeDict['75017']

outputFile = open("code_apl", 'wb')
pickle.dump(codeDict, outputFile)
outputFile.close()