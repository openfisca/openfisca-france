# -*- coding:utf-8 -*-


from __future__ import division

import numpy as np

from openfisca_core import decompositions


class OutNode(object):
    def __init__(self, code = '', desc = '', shortname = '', vals = 0, color = (0, 0, 0), typevar = 0, parent = None):
        self.parent = parent
        self.children = []
        self.code = code
        self.desc = desc
        self.color = color
        self.visible = 0
        self.typevar = typevar
        self._vals = vals
        self._taille = 0
        if shortname:
            self.shortname = shortname
        else:
            self.shortname = code

    def addChild(self, child):
        self.children.append(child)
        if child.color == (0, 0, 0):
            child.color = self.color
        child.setParent(self)

    def setParent(self, parent):
        self.parent = parent

    def child(self, row):
        return(self.children[row])

    def childCount(self):
        return len(self.children)

    def row(self):
        if self.parent is not None:
            return self.parent.children.index(self)

    def setLeavesVisible(self):
        for child in self.children:
            child.setLeavesVisible()
        if self.children:
            self.visible = 0
        else:
            self.visible = 1

    def partiallychecked(self):
        if self.children:
            a = True
            for child in self.children:
                a = a and (child.partiallychecked() or child.visible)
            return a
        return False

    def hideAll(self, keep = ['revenu_disponible']):
        if self.code in keep:
            self.visible = 1
        else:
            self.visible = 0
        for child in self.children:
            child.hideAll(keep = keep)

    def setHidden(self, changeParent = True):
        # les siblings doivent être dans le même
        if self.partiallychecked():
            self.visible = 0
            return
        for sibling in self.parent.children:
            sibling.visible = 0
            for child in sibling.children:
                child.setHidden(False)
        if changeParent:
            self.parent.visible = 1

    def setVisible(self, changeSelf = True, changeParent = True):
        if changeSelf:
            self.visible = 1
        if self.parent is not None:
            for sibling in self.parent.children:
                if not (sibling.partiallychecked() or sibling.visible == 1):
                    sibling.visible = 1
            if changeParent:
                self.parent.setVisible(changeSelf = False)

    def getVals(self):
        return self._vals

    def setVals(self, vals):
        dif = vals - self._vals
        self._vals = vals
        self._taille = len(vals)
        if self.parent:
            self.parent.setVals(self.parent.vals + dif)

    vals = property(getVals, setVals)

    def __getitem__(self, key):
        if self.code == key:
            return self
        for child in self.children:
            val = child[key]
            if val is not None:
                return val

    def log(self, tabLevel=-1):
        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "\t"

        output += "|------" + self.code + "\n"

        for child in self.children:
            output += child.log(tabLevel)

        tabLevel -= 1
        output += "\n"

        return output

    def __repr__(self):
        return self.log()

    def difference(self, other):
        self.vals -= other.vals
        for child in self.children:
            child.difference(other[child.code])

    def __iter__(self):
        return self.inorder()

    def inorder(self):
        for child in self.children:
            for x in child.inorder():
                yield x
        yield self

    @classmethod
    def init_from_decomposition_json(cls, simulation, decomposition_json):
        simulations = [simulation]
        root_node = decompositions.calculate(simulations, decomposition_json)
        self = cls()
        convert_to_out_node(self, root_node)
        return self


def convert_to_out_node(out_node, node):
    out_node.code = node['code']
    out_node.desc = node['name']
    if 'color' in node:
        out_node.color = node['color']
    else:
        out_node.color = [0, 0, 0]
    out_node.shortname = node['short_name']
    out_node.typv = 0
    if 'type' in node:
        out_node.typv = node['type']
    if node.get('children'):
        for child in node.get('children'):
            code = child['code']
            desc = child['name']
            if 'color' in child:
                color = child['color']
            else:
                color = [0, 0, 0]
            shortname = child['short_name']
            typv = 0
            if 'type' in child:
                typv = child['type']
            child_out_node = OutNode(
                code,
                desc,
                color = color,
                typevar = typv,
                shortname = shortname)
            out_node.addChild(child_out_node)
            convert_to_out_node(child_out_node, child)
    else:
        out_node.setVals(np.array(node['values']))
        return
