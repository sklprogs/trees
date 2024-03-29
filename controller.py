import sys
import PyQt5
import PyQt5.QtWidgets

import gui as gi

#from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh



class Tree:
    ''' Drag-and-drop/navigation strategy:
        We assume that:
        - major is a root item, it has no parent and is not indented;
        - minor is a non-root item, it has a non-empty parent and is indented;
        - group1 is an item/group to be moved;
        - group2 is a group over which major/minor group1 is dropped;
        - index1 is the index of the initially selected row;
        - index2 is the index where group1 is to be dropped;
        - index2 > index1 if group1 is moved top to bottom and index1 > index2
          otherwise;
        - item1 is an item having the index of index1;
        - item2 is an item having the index of index2.
        Variants:
        - indices are the same: report that no action is required;
        - both index1 and index2 are root entries:
        
        and index2 is the index of the minor/major where group1 was dropped)
        
        
          - index1 and index2 have the same parent: this should happen only if
            index1 == index2 but we skip this variant above;
          - parents of index1 and index2 have the same title (note that
            a shared title does not make them refer to the same node): merge
            groups by inserting all minors of group2 into group1 at the start
            of group1;
          - parents of index1 and index2 have different titles: 
            insert entire group2 
          - ↓ (index1 precedes index2): put index1 and its children after last
            child of index2;
          - ↑ (index2 precedes index1): put index1 and its children ahead of
            first child of index2;
        - both index1 and index2 are non-root entries:
          - index1 and index2 have the same parent:
            - ↓ (index1 precedes index2): put index1 after index2;
            - ↑ (index2 precedes index1): put index1 ahead of index2;
          - index1 and index2 have a different parent:
            - ↓ (index1 precedes index2): duplicate index1 parent after ;
            - ↑ (index2 precedes index1): ?;
        - index1 is a root entry and index2 is a non-root entry:
          - ↓ (index1 precedes index2): 
    '''
    def __init__(self):
        self.majors = []
        self.minors = {}
        self.index1 = None
        self.index2 = None
        self.gui = gi.Tree()
        self.set_bindings()
    
    def select_mode(self, index1, index2):
        # Select same-level or multilevel strategy
        if not index1 or not index2:
            print('empty!')
            return
        item1 = self.gui.get_item(index1)
        item2 = self.gui.get_item(index2)
        if not item1 or not item2:
            print('empty!')
            return
        parent1 = self.gui.get_parent(item1)
        parent2 = self.gui.get_parent(item2)
        if parent1 == parent2:
            print('Same-level strategy')
        else:
            if parent1 is None:
                parent1 = item1
            if parent2 is None:
                parent2 = item2
            print('Multilevel strategy')
            children = self.get_children(parent1)
            print('Move what:',children)
            parent2_index = self.gui.get_index_by_item(parent2)
            rowno2 = self.gui.get_row(index2)
            # Insert before, delete later since row numbers will change
            children = children[::-1]
            for i in range(len(children)):
                self.gui.insert_row(rowno2, parent2_index)
                item = self.gui.get_item(index2)
                self.gui.set_text(item,children[i])
            # Referring to deleted items will cause an error
            self.gui.remove_item(index1)
    
    def insert_same_level(self):
        # Insert an item at the same level as the currently selected item
        index_ = self.gui.get_cur_index()
        rowno = self.gui.get_row(index_)
        item = self.gui.get_item(index_)
        parent_item = self.gui.get_parent(item)
        if not parent_item:
            parent_item = self.gui.get_root()
        parent_index = self.gui.get_index_by_item(parent_item)
        self.gui.insert_row(rowno, parent_index)
    
    def add_indices(self):
        if not self.index1:
            self.index1 = self.gui.get_cur_index()
            print('1st index added')
            return
        if not self.index2:
            self.index2 = self.gui.get_cur_index()
            print('2nd index added')
            if self.index1 == self.index2:
                print('Same index!')
            return
        print('lazy')
    
    def remove_empty_majors(self):
        f = 'remove_empty_majors'
        empty = []
        rownum = self.gui.get_row_num(self.gui.get_root())
        for rowno in range(rownum):
            major_index = self.gui.get_root_index(rowno)
            if not self.gui.has_children(major_index):
                empty.append(major_index)
        if not empty:
            print(f, 'empty!')
            return
        for index_ in empty:
            item = self.gui.get_item(index_)
            mes = 'Removing empty "{}"'.format(self.gui.get_text(item))
            print(f,mes)
            self.gui.remove_item(index_)
    
    def get_empty_parent_index(self, minor_index):
        minor_item = self.gui.get_item(minor_index)
        parent_item = self.gui.get_parent(minor_item)
        if not parent_item:
            return
        return self.gui.get_index_by_item(parent_item)
    
    def divide(self):
        f = '[Trees] controller.Tree.divide'
        if not self.index1 or not self.index2:
            print(f,'empty!')
            return
        # Get initial selection
        minor1_item = self.gui.get_item(self.index1)
        major1_item = self.gui.get_parent(minor1_item)
        if not major1_item:
            print(f, 'Copy instead of dividing')
            return
        minor1_text = self.gui.get_text(minor1_item)
        major1_text = self.gui.get_text(major1_item)
        # Get final selection
        minor2_item = self.gui.get_item(self.index2)
        major2_item = self.gui.get_parent(minor2_item)
        if not major2_item:
            print(f,'Use another strategy')
            return
        minor2_text = self.gui.get_text(minor2_item)
        major2_text = self.gui.get_text(major2_item)
        print('Minor1:', minor1_text)
        print('Major1:', major1_text)
        print('Minor2:', minor2_text)
        print('Major2:', major2_text)
        if major1_text == major2_text:
            print(f, 'Use another strategy')
            return
        major2_children = self.get_children(major2_item)
        print('major2_children:', major2_children)
        list1, list2 = sh.List(major2_children).split_by_item(minor2_text)
        print('list1:', list1)
        print('list2:', list2)
        major2_index = self.gui.get_index_by_item(major2_item)
        major2_rowno = self.gui.get_row(major2_index)
        print('major2_rowno:', major2_rowno)
        self.gui.remove_group(major2_rowno)
        # Do this before deleting the minor
        #empty_parent_index = self.get_empty_parent_index(self.index1)
        self.gui.remove_item(self.index1)
        major21 = self.gui.insert_child (parent = self.gui.get_root()
                                        ,rowno = major2_rowno
                                        ,text = major2_text
                                        )
        for child in list1:
            self.gui.add_child(major21, child)
        major22 = self.gui.insert_child (parent = self.gui.get_root()
                                        ,rowno = major2_rowno + 1
                                        ,text = major1_text
                                        )
        minor22_item = self.gui.add_child(major22, minor1_text)
        minor22_index = self.gui.get_index_by_item(minor22_item)
        major23 = self.gui.insert_child (parent = self.gui.get_root()
                                        ,rowno = major2_rowno + 2
                                        ,text = major2_text
                                        )
        for child in list2:
            self.gui.add_child(major23, child)
        self.gui.set_cur_index(minor22_index)
        self.gui.expand_all()
        self.remove_empty_majors()
        #if empty_parent_index:
        #    self.gui.remove_item(empty_parent_index)
        # Old indices left after deleting rows will cause a segfault
        self.index1 = self.index2 = None
        #self.gui.remove_children(major2_rowno+3)
        #self.gui.remove_major(major2_rowno+3)
    
    def add_major(self, text='Level2'):
        # Add a root level if necessary
        index_ = self.gui.get_cur_index()
        item = self.gui.get_item(index_)
        parent_item = self.gui.get_parent(item)
        if parent_item:
            parent_text = self.gui.get_text(parent_item)
        else:
            parent_text = self.gui.get_text(item)
            parent_item = item
        if text == parent_text:
            print('No need to insert a major')
        else:
            parent_index = self.gui.get_index_by_item(parent_item)
            parent_rowno = self.gui.get_row(parent_index)
            root_item = self.gui.get_root()
            new_parent = self.gui.insert_child(root_item, parent_rowno, text)
            children = self.get_children(parent_item)
            for child in children:
                self.gui.add_child(new_parent, child)
    
    def test(self):
        '''
        index1 = self.gui.get_root_index(0)
        index2 = self.gui.get_cur_index()
        self.select_mode(index1, index2)
        '''
        #self.add_major()
        self.divide()
    
    def test1(self):
        # Works: Both are root items
        # Level 1..5..2
        rowno1 = 4
        rowno2 = 1
        index1 = self.gui.get_root_index(rowno1)
        index2 = self.gui.get_root_index(rowno2)
        self.move_item(index1,index2)
    
    def has_expanded(self):
        row_num = self.gui.get_row_num(self.gui.get_root())
        for rowno in range(row_num):
            if self.gui.is_expanded(self.gui.get_root_index(rowno)):
                return True
    
    def expand_or_collapse_all(self):
        if self.has_expanded():
            self.gui.collapse_all()
        else:
            self.gui.expand_all()
    
    def expand_or_collapse(self):
        index_ = self.gui.get_cur_index()
        if index_ is None:
            print('empty!')
            return
        if self.gui.is_expanded(index_):
            self.gui.set_expanded(index_, False)
        else:
            self.gui.set_expanded(index_, True)
    
    def move_up(self):
        index1 = self.gui.get_cur_index()
        if index1 is None:
            print('empty!')
            return
        ''' Do not use 'QTreeView.indexAbove' since it can return both major or
            minor.
        '''
        rowno1 = self.gui.get_row(index1)
        if rowno1 == 0:
            print('lazy!')
            return
        rowno2 = rowno1 - 1
        self._move_by_row(index1, rowno1, rowno2)
    
    def move_down(self):
        index1 = self.gui.get_cur_index()
        if index1 is None:
            print('empty!')
            return
        ''' Do not use 'QTreeView.indexBelow' since it can return both major or
            minor.
        '''
        rowno1 = self.gui.get_row(index1)
        item1 = self.gui.get_item(index1)
        if item1 is None:
            print('empty!')
            return
        parent1 = self.gui.get_parent(item1)
        if parent1 is None:
            parent1 = self.gui.get_root()
        if parent1 is None:
            print('empty!')
            return
        rownum = self.gui.get_row_num(parent1)
        if rowno1 == rownum - 1:
            print('lazy!')
            return
        rowno2 = rowno1 + 1
        self._move_by_row(index1, rowno1, rowno2)
    
    def _move_by_row(self, index1, rowno1, rowno2):
        item1 = self.gui.get_item(index1)
        if item1 is None:
            print('empty!')
            return
        parent1 = self.gui.get_parent(item1)
        if parent1 is None:
            parent1 = self.gui.get_root()
        if parent1 is None:
            print('empty!')
            return
        parent_index = self.gui.get_index_by_item(parent1)
        if parent_index is None:
            print('empty!')
            return
        index2 = self.gui.get_index(rowno2, parent_index)
        self.move_item(index1, index2)
    
    def move_item(self, index1, index2):
        if index1 is None or index2 is None:
            print('empty!')
            return
        item1 = self.gui.get_item(index1)
        item2 = self.gui.get_item(index2)
        if item1 is None or item2 is None:
            print('empty!')
            return
        parent = self.gui.get_parent(item1)
        rowno1 = self.gui.get_row(index1)
        rowno2 = self.gui.get_row(index2)
        print('rowno1:', rowno1, ', rowno2:', rowno2)
        if parent:
            print('Mode: minor')
            self.gui.insert(parent, rowno1, rowno2)
        else:
            print('Mode: major')
            self.gui.insert(self.gui.get_root(), rowno1, rowno2)
        self.gui.set_cur_index(index2)
    
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
        self.gui.bind('Escape', self.close)
        self.gui.bind('Shift+Up', self.move_up)
        self.gui.bind('Shift+Down', self.move_down)
        self.gui.bind('Space', self.expand_or_collapse)
        self.gui.bind('Ctrl+A', self.expand_or_collapse_all)
        self.gui.bind('Return', self.test)
        self.gui.bind('a', self.add_indices)
    
    def get_children(self, item):
        children = []
        if not item:
            print('empty!')
            return children
        rownum = self.gui.get_row_num(item)
        if not rownum:
            print('empty!')
            return children
        for i in range(rownum):
            subitem = self.gui.get_child(item, i, 0)
            if not subitem:
                print('Avoid None')
                continue
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
            item = self.gui.get_child(root, i, 0)
            self.minors[self.majors[i]] = self.get_children(item)
        print('Minors:',self.minors)


if __name__ == '__main__':
    dic = {'Level1': ['Level1_item1', 'Level1_item2', 'Level1_item3']
          ,'Level2': ['Level2_item1', 'Level2_item2', 'Level2_item3'
                     ,'Level2_item4'
                     ]
          ,'Level3': ['Level3_item1', 'Level3_item2', 'Level3_item3']
          ,'Level4': ['Level4_item1', 'Level4_item2']
          ,'Level5': ['Level5_item1', 'Level5_item2', 'Level5_item3'
                     ,'Level5_item4', 'Level5_item5'
                     ]
          }
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    itree = Tree()
    itree.fill(dic)
    itree.gui.tree.expandAll()
    #itree.show()
    itree.gui.showMaximized()
    #itree.set_majors()
    #itree.set_minors()
    sys.exit(app.exec_())
