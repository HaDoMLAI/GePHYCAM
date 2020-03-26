# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""
#%%
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg

# import pyqtgraph.examples
# pyqtgraph.examples.run()


class MplWidget(QWidget):
    
    def __init__ (self, parent = None): 
        QWidget.__init__(self, parent)
        #-----------------------------------------------------
        ## Create window with GraphicsView widget
        self.win = pg.GraphicsLayoutWidget()
        self.win.show()  ## show widget alone in its own window
        view = self.win.addViewBox()
        ## lock the aspect ratio so pixels are always square
        view.setAspectLocked(True)
        ## Create image item
        self.img = pg.ImageItem(border='w')
        view.addItem(self.img)
        ## set layout
        vertical_layout = QVBoxLayout() 
        vertical_layout.addWidget(self.win)
        self.setLayout(vertical_layout)
    
    def imshow(self, imageData):
        self.img.setImage(imageData)



        

