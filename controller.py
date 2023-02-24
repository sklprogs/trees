import sys
import PyQt5
import PyQt5.QtWidgets

import gui as gi



class Tree:
    
    def __init__(self):
        self.majors = []
        self.minors = {}
        self.gui = gi.Tree()
        self.set_bindings()
    
    def close(self):
        self.gui.close()
    
    def show(self):
        self.gui.show()
    
    def fill(self,dic):
        f = '[Trees] controller.Tree.fill'
        if not dic:
            print(f,'Empty!')
            return
        self.gui.fill(dic)
    
    def set_bindings(self):
        self.gui.bind('Space',self.test)
        self.gui.bind('Escape',self.close)
    
    def get_children(self,item):
        children = []
        if not item:
            print('empty!')
            return children
        rownum = self.gui.get_num(item)
        if not rownum:
            print('empty!')
            return children
        for i in range(rownum):
            subitem = self.gui.get_child(item,i,0)
            children.append(self.gui.get_text(subitem))
        return children
    
    def set_majors(self):
        self.majors = self.get_children(self.gui.get_root())
        print('Majors:',self.majors)
    
    def set_minors(self):
        if not self.majors:
            print('empty!')
            return
        root = self.gui.get_root()
        if not root:
            print('empty!')
            return
        for i in range(len(self.majors)):
            item = self.gui.get_child(root,i,0)
            self.minors[self.majors[i]] = self.get_children(item)
        print('Minors:',self.minors)
    
    def test(self):
        print('------------------------------')
        index_ = self.gui.get_index()
        print(f'Row #{index_.row()}. Column #{index_.column()}')
        item = self.gui.model.model.itemFromIndex(index_)
        self.gui.inspect_item(item)
        #self.gui.get_children(item)
        #self.gui.get_row()


if __name__ == '__main__':
    dic = {'Level1': ['Level1_item1','Level1_item2','Level1_item3']
          ,'Level2': ['Level2_item1','Level2_item2','Level2_item3'
                     ,'Level2_item4'
                     ]
          ,'Level3': ['Level3_item1','Level3_item2','Level3_item3']
          }
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    itree = Tree()
    itree.fill(dic)
    itree.gui.tree.expandAll()
    itree.show()
    itree.set_majors()
    itree.set_minors()
    sys.exit(app.exec_())
