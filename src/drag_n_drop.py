#!/usr/bin/python3
# See https://github.com/jimmykuu/PyQt-PySide-Cookbook/blob/master/tree/drop_indicator.md

'''
The MIT License (MIT)

Copyright (c) 2014 Jimmy Kuu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import sys
import PyQt5
import PyQt5.QtWidgets


class MyTreeView(PyQt5.QtWidgets.QTreeView):

    def __init__(self, parent=None):
        super(MyTreeView, self).__init__(parent)
        self.dropIndicatorRect = PyQt5.QtCore.QRect()

    def paintEvent(self, event):
        painter = PyQt5.QtGui.QPainter(self.viewport())
        self.drawTree(painter, event.region())
        # Originally it calls the inline function paintDropIndicator here
        self.paintDropIndicator(painter)

    def paintDropIndicator(self, painter):
        if self.state() == PyQt5.QtWidgets.QAbstractItemView.DraggingState:
            opt = PyQt5.QtWidgets.QStyleOption()
            opt.initFrom(self)
            opt.rect = self.dropIndicatorRect
            rect = opt.rect

            brush = PyQt5.QtGui.QBrush(PyQt5.QtGui.QColor(PyQt5.QtCore.Qt.black))

            if rect.height() == 0:
                pen = PyQt5.QtGui.QPen(brush, 2, PyQt5.QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(rect.topLeft(), rect.topRight())
            else:
                pen = PyQt5.QtGui.QPen(brush, 2, PyQt5.QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.drawRect(rect)



class MyTreeWidget(PyQt5.QtWidgets.QTreeWidget, MyTreeView):

    def startDrag(self, supportedActions):
        listsQModelIndex = self.selectedIndexes()
        if listsQModelIndex:
            dataQMimeData = self.model().mimeData(listsQModelIndex)
            dragQDrag = PyQt5.QtGui.QDrag(self)
            dragQDrag.setMimeData(dataQMimeData)
            defaultDropAction = PyQt5.QtCore.Qt.IgnoreAction
            if ((supportedActions & PyQt5.QtCore.Qt.CopyAction) \
            and (self.dragDropMode() != PyQt5.QtWidgets.QAbstractItemView.InternalMove)):
                defaultDropAction = PyQt5.QtCore.Qt.CopyAction
            dragQDrag.exec_(supportedActions, defaultDropAction)

    def dragMoveEvent(self, event):
        pos = event.pos()
        item = self.itemAt(pos)

        if item:
            # This always gets default column 0 index
            index = self.indexFromItem(item)

            rect = self.visualRect(index)
            rect_left = self.visualRect(index.sibling(index.row(), 0))
            # In case the section has been moved
            rect_right = self.visualRect (index.sibling(index.row()
                                         ,self.header().logicalIndex(self.columnCount() - 1))
                                         )

            self.dropIndicatorPosition = self.position(event.pos(), rect, index)

            if self.dropIndicatorPosition == self.AboveItem:
                self.dropIndicatorRect = PyQt5.QtCore.QRect (rect_left.left()
                                                      ,rect_left.top()
                                                      ,rect_right.right() - rect_left.left()
                                                      ,0
                                                      )
                event.accept()
            elif self.dropIndicatorPosition == self.BelowItem:
                self.dropIndicatorRect = PyQt5.QtCore.QRect (rect_left.left()
                                                            ,rect_left.bottom()
                                                            ,rect_right.right() - rect_left.left()
                                                            ,0
                                                            )
                event.accept()
            elif self.dropIndicatorPosition == self.OnItem:
                self.dropIndicatorRect = PyQt5.QtCore.QRect (rect_left.left()
                                                            ,rect_left.top()
                                                            ,rect_right.right() - rect_left.left()
                                                            ,rect.height()
                                                            )
                event.accept()
            else:
                self.dropIndicatorRect = PyQt5.QtCore.QRect()

            self.model().setData (index, self.dropIndicatorPosition
                                 ,PyQt5.QtCore.Qt.UserRole
                                 )

        # This is necessary or else the previously drawn rect won't be erased
        self.viewport().update()

    def dropEvent(self, event):
        pos = event.pos()
        item = self.itemAt(pos)

        if item is self.currentItem():
            PyQt5.QtWidgets.QTreeWidget.dropEvent(self, event)
            event.accept()
            return

        if item:
            index = self.indexFromItem(item)
            self.model().setData(index, 0, PyQt5.QtCore.Qt.UserRole)

        if event.source == self and event.dropAction() == PyQt5.QtCore.Qt.MoveAction \
        or self.dragDropMode() == PyQt5.QtWidgets.QAbstractItemView.InternalMove:

            topIndex = PyQt5.QtCore.QModelIndex()
            col = -1
            row = -1

            lst = [event, row, col, topIndex]

            if self.dropOn(lst):

                event, row, col, topIndex = lst

                idxs = self.selectedIndexes()
                indexes = []
                existing_rows = set()
                for i in idxs:
                    if i.row() not in existing_rows:
                        indexes.append(i)
                        existing_rows.add(i.row())

                if topIndex in indexes:
                    return

                dropRow = self.model().index(row, col, topIndex)
                taken = []

                indexes_reverse = indexes[:]
                indexes_reverse.reverse()
                i = 0
                for index in indexes_reverse:
                    parent = self.itemFromIndex(index)
                    if not parent or not parent.parent():
                        '''
                        if not parent or not isinstance (parent.parent()
                                                        ,PyQt5.QtWidgets.QTreeWidgetItem
                                                        ):
                        '''
                        taken.append(self.takeTopLevelItem(index.row()))
                    else:
                        taken.append(parent.parent().takeChild(index.row()))

                    i += 1
                    # break

                taken.reverse()

                for index in indexes:
                    if row == -1:
                        if topIndex.isValid():
                            parent = self.itemFromIndex(topIndex)
                            parent.insertChild(parent.childCount(), taken[0])
                            taken = taken[1:]

                        else:
                            self.insertTopLevelItem (self.topLevelItemCount()
                                                    ,taken[0]
                                                    )
                            taken = taken[1:]
                    else:
                        r = dropRow.row() if dropRow.row() >= 0 else row
                        if topIndex.isValid():
                            parent = self.itemFromIndex(topIndex)
                            parent.insertChild (min(r, parent.childCount())
                                               ,taken[0]
                                               )
                            taken = taken[1:]
                        else:
                            self.insertTopLevelItem (min(r, self.topLevelItemCount())
                                                    ,taken[0]
                                                    )
                            taken = taken[1:]

                event.accept()

        PyQt5.QtWidgets.QTreeWidget.dropEvent(self, event)
        self.expandAll()

    def position(self, pos, rect, index):
        r = PyQt5.QtWidgets.QAbstractItemView.OnViewport
        ''' margin*2 must be smaller than row height, or the drop onItem rect
            will no show up.
        '''
        margin = 10
        if pos.y() - rect.top() < margin:
            r = PyQt5.QtWidgets.QAbstractItemView.AboveItem
        elif rect.bottom() - pos.y() < margin:
            r = PyQt5.QtWidgets.QAbstractItemView.BelowItem

        # this rect is always the first column rect
        # elif rect.contains(pos, True):
        elif pos.y() - rect.top() > margin and rect.bottom() - pos.y() > margin:
            r = PyQt5.QtWidgets.QAbstractItemView.OnItem

        return r

    def dropOn(self, lst):

        event, row, col, index = lst

        root = self.rootIndex()

        if self.viewport().rect().contains(event.pos()):
            index = self.indexAt(event.pos())
            if not index.isValid() or not self.visualRect(index).contains(event.pos()):
                index = root

        if index != root:
            '''
            dropIndicatorPosition = self.position (event.pos()
                                                  ,self.visualRect(index)
                                                  ,index
                                                  )
            '''
            self.position(event.pos(), self.visualRect(index), index)
            if self.dropIndicatorPosition == self.AboveItem:
                print('dropon above')
                row = index.row()
                col = index.column()
                index = index.parent()

            elif self.dropIndicatorPosition == self.BelowItem:
                print('dropon below')
                row = index.row() + 1
                col = index.column()
                index = index.parent()

            elif self.dropIndicatorPosition == self.OnItem:
                print('dropon onItem')
                pass
            elif self.dropIndicatorPosition == self.OnViewport:
                pass
            else:
                pass

        else:
            self.dropIndicatorPosition = self.OnViewport

        lst[0], lst[1], lst[2], lst[3] = event, row, col, index

        # if not self.droppingOnItself(event, index):
        return True



class UI(PyQt5.QtWidgets.QDialog):

    def __init__(self, args=None, parent=None):
        super(UI, self).__init__(parent)
        self.layout1 = PyQt5.QtWidgets.QVBoxLayout(self)
        treeWidget = MyTreeWidget()

        treeWidget.setSelectionMode(PyQt5.QtWidgets.QAbstractItemView.ExtendedSelection)

        button1 = PyQt5.QtWidgets.QPushButton('Add')
        button2 = PyQt5.QtWidgets.QPushButton('Add Child')

        self.layout1.addWidget(treeWidget)

        self.layout2 = PyQt5.QtWidgets.QHBoxLayout()
        self.layout2.addWidget(button1)
        self.layout2.addWidget(button2)

        self.layout1.addLayout(self.layout2)

        treeWidget.setHeaderHidden(True)

        self.treeWidget = treeWidget
        self.button1 = button1
        self.button2 = button2
        self.button1.clicked.connect(lambda *x: self.addCmd())
        self.button2.clicked.connect(lambda *x: self.addChildCmd())

        HEADERS = ("script", "chunksize", "mem")
        self.treeWidget.setHeaderLabels(HEADERS)
        self.treeWidget.setColumnCount(len(HEADERS))

        self.treeWidget.setColumnWidth(0, 160)
        self.treeWidget.header().show()

        self.treeWidget.setDragDropMode(PyQt5.QtWidgets.QAbstractItemView.InternalMove)
        self.treeWidget.setStyleSheet('''
                                         QTreeView {
                                             show-decoration-selected: 1;
                                         }

                                         QTreeView::item:hover {
                                             background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
                                         }

                                         QTreeView::item:selected:active{
                                             background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
                                         }

                                         QTreeView::item:selected:!active {
                                             background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
                                         }
                                         ''')

        self.resize(500, 350)
        for i in range(6):
            item = self.addCmd(i)
            if i in (3, 4):
                self.addChildCmd()
                if i == 4:
                    self.addCmd(f'{i}-2', parent=item)

        self.treeWidget.expandAll()
        self.setStyleSheet("QTreeWidget::item{ height: 30px;  }")

    def addChildCmd(self):
        parent = self.treeWidget.currentItem()
        self.addCmd(parent=parent)
        self.treeWidget.setCurrentItem(parent)

    def addCmd(self, i=None, parent=None):
        'add a level to tree widget'

        root = self.treeWidget.invisibleRootItem()
        if not parent:
            parent = root

        if i is None:
            if parent == root:
                i = self.treeWidget.topLevelItemCount()
            else:
                i = str(parent.text(0))[7:]
                i = '%s-%s' % (i, parent.childCount() + 1)

        item = PyQt5.QtWidgets.QTreeWidgetItem(parent, ['script %s' % i, '1', '150'])

        self.treeWidget.setCurrentItem(item)
        self.treeWidget.expandAll()
        return item


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    gui = UI()
    gui.show()
    app.exec_()
