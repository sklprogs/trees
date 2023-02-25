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
    
    def test(self):
        self.move_up()
        self.set_majors()
        self.set_minors()
    
    def move_item_up(self):
        rowno1 = self.gui.get_cur_row()
        rowno2 = rowno1 - 1
        cur_index = self.gui.get_cur_index()
        cur_item = self.gui.get_item(cur_index)
        parent_item = self.gui.get_parent(cur_item)
        parent_index = self.gui.get_index_by_item(parent_item)
        index1 = self.gui.get_index(rowno1,parent_index)
        index2 = self.gui.get_index(rowno2,parent_index)
        item1 = self.gui.get_item(index1)
        item2 = self.gui.get_item(index2)
        '''
        item1 = self.gui.get_item_by_row(rowno1)
        item2 = self.gui.get_item_by_row(rowno2)
        '''
        if not item1 or not item2:
            print('item empty!')
            return
        text1 = self.gui.get_text(item1)
        text2 = self.gui.get_text(item2)
        self.gui.set_text(item1,text2)
        self.gui.set_text(item2,text1)
        '''
        cur_index = self.gui.get_cur_index()
        if not cur_index:
            print('cur index empty!')
            return
        cur = self.gui.get_item(cur_index)
        if not cur:
            print('cur item empty!')
            return
        rowno = self.gui.get_row(cur_index)
        prev_index = self.gui.get_index(rowno-1,cur_index)
        if not prev_index:
            print('prev_index empty!')
            return
        prev = self.gui.get_item(prev_index)
        if not prev:
            print('prev item empty!')
            return
        cur_text = self.gui.get_text(cur)
        prev_text = self.gui.get_text(prev)
        self.gui.set_text(cur,prev_text)
        self.gui.set_text(prev,cur_text)
        '''
    
    def move_up(self):
        rowno = self.gui.get_cur_row()
        if rowno == 0:
            print('Create new group first')
        else:
            self.move_item_up()
    
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
        rownum = self.gui.get_row_num(item)
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
    #itree.set_majors()
    #itree.set_minors()
    sys.exit(app.exec_())
