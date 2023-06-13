#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


def get_dic():
    file = sh.objs.get_pdir().add('resources', 'example.json')
    code = sh.ReadTextFile(file).get()
    #dic = json.loads(code)
    #print(json.dumps(dic, sort_keys=True, indent=4))
    return json.loads(code)



class Model:
    
    def __init__(self, dic):
        self.dic = dic
    
    def parse_dic(self, value):
        for key in value:
            print('parse_dic:', key)
            self.parse_item(value[key])
    
    def parse_item(self, value):
        if isinstance(value, str):
            print('parse_item:', value)
        elif isinstance(value, list):
            print('parse_item: list')
            for item in value:
                self.parse_item(item)
        elif isinstance(value, dict):
            print('parse_item: dict')
            self.parse_dic(value)
    
    def run(self):
        self.parse_dic(self.dic)


if __name__ == '__main__':
    f = '[Trees] logic.__main__'
    sh.com.start()
    dic = get_dic()
    Model(dic).run()
    mes = _('Goodbye!')
    sh.objs.get_mes(f, mes, True).show_debug()
    sh.com.end()
