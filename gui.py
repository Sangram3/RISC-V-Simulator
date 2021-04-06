import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

class TabBar(QtWidgets.QTabBar):
    def __init__(self, colors, parent=None):
        super(TabBar, self).__init__(parent)
        self.mColors = colors

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            if opt.text in self.mColors:
                opt.palette.setColor(
                    QtGui.QPalette.Button, self.mColors[opt.text]
                )
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt)

class Window(QtWidgets.QTabWidget):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("QTabWidget Example")
      self.setGeometry(300, 300,300,300)
      self.move(0,0)
      self.setStyleSheet("background: white;")  
      self.setStyleSheet("color: white;background: black")
      self.bt=QPushButton("",self)

      self.memory={}
      self.register=[]
      # set reset step dump ##################################################
      
      self.run_btn = QPushButton('Run')
      self.run_btn.setEnabled(False)
      self.step_btn= QPushButton('Step')
      self.step_btn.setEnabled(False)
      self.reset_btn= QPushButton('Reset')
      self.reset_btn.setEnabled(False)
      self.dump_btn= QPushButton('Dump')
      self.dump_btn.setEnabled(False)
     
      self.run_btn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : green;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}"
                             )
      
      self.step_btn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : purple;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}"
                             )
      
      self.reset_btn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : blue;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}"
                             ) 
      self.dump_btn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #000080;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}"
                             )
      
      ########################################################################
      layout = QVBoxLayout()
      self.setLayout(layout)
      # Editor Compiler#######################################################
      tabs = QTabWidget()
      d = {
            "Editor": QtGui.QColor("blue"),
            "Compiler": QtGui.QColor("brown"),
        }
      tabs.setTabBar(TabBar(d))
      tabs.addTab(self.EditorTabUI(), "Editor")
      tabs.addTab(self.CompilerTabUI(), "Compiler")
      layout.addWidget(tabs)
      ########################################################################

   def EditorTabUI(self):
      editorTab = QWidget()
      layout = QVBoxLayout()
      editorTab.setAutoFillBackground(True)
      palette = editorTab.palette()
      palette.setColor(editorTab.backgroundRole(), QtCore.Qt.blue)
      editorTab.setPalette(palette)
      self.fn='File'
      filebox = QHBoxLayout()
      self.f=QLabel("File")
      filebox.addWidget(self.f)
      filebox.addStretch()

      btn = QPushButton("Select File")
      btn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #000080;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : brown;"
                             "}"
                             )
      filebox.addWidget(btn)
      # filebox.addStretch()

      btn.clicked.connect(self.getfile)
      
      layout.addLayout(filebox)
      layout.addWidget(QTextEdit())
      
      editorTab.setLayout(layout)
      return editorTab

   def getfile(self):
      fname = QFileDialog.getOpenFileName(self, 'Open file', 'D:\\4th_Sem\CS204\Project',"Machine Cdde files (*.mc)")
      print(str(fname[0]))
      self.f.setText(str(fname[0]))
   
   def assemble_clicked(self):
      self.bt.hide()
      self.run_btn.setEnabled(True)
      self.step_btn.setEnabled(True)
      self.reset_btn.setEnabled(True)
      self.dump_btn.setEnabled(True)

   def CompilerTabUI(self):
      compilerTab = QWidget()
      layout = QHBoxLayout()
      lef_s = QVBoxLayout()

      run= QHBoxLayout()

      self.bt=QPushButton("Assemble and Simulate from the editor")
      run.addWidget(self.bt)
      run.addStretch()
      self.bt.clicked.connect(self.assemble_clicked)

      run.addWidget(self.run_btn)
      run.addStretch()
      
      run.addWidget(self.step_btn)
      run.addStretch()
      
      run.addWidget(self.reset_btn)
      run.addStretch()
      
      run.addWidget(self.dump_btn)
      run.addStretch()

      self.run_btn.clicked.connect(self.run_code)      
      self.step_btn.clicked.connect(self.step_code)      
      self.reset_btn.clicked.connect(self.reset_code)      
      self.dump_btn.clicked.connect(self.dump_code)      

    

      lef_s.addLayout(run)
      layout.addStretch()

      formLayout =QFormLayout()
      groupBox = QGroupBox("Machine Code Input")
      labelLis = []
      comboList = []
      basic_codes = []
      labelLis.append(QLabel("PC    "))
      comboList.append(QLabel("Instruction"))
      basic_codes.append(QLabel("Basic Code"))
      
      for i in  range(15):
         labelLis.append(QLabel("0x0      "))
         comboList.append(QLabel("Inst"))
         basic_codes.append(QLabel("add x11 x12 x13"))
         formLayout.addRow(labelLis[i], basic_codes[i])

      groupBox.setLayout(formLayout)
      scroll = QScrollArea()
      scroll.setWidget(groupBox)
      scroll.setWidgetResizable(True)
      scroll.setFixedHeight(300)
      scroll.setFixedWidth(1000)

      lef_s.addWidget(scroll)

      gB = QGroupBox("Output")
      vb= QFormLayout()
         
      for i in range(100):
         vb.addRow(QLabel(str(i)))   
      gB.setLayout(vb)
      scr = QScrollArea()
      
      scr.setWidget(gB)
      scr.setWidgetResizable(True)
      scr.setFixedHeight(250)
      scr.setFixedWidth(1000)
      
      lef_s.addWidget(scr)
      lef_s.addStretch()
      
      layout.addLayout(lef_s)
      layout.addStretch()


      Tabs = QTabWidget()
      D = {
             "Memory": QtGui.QColor("blue"),
             "Register": QtGui.QColor("purple"),
         }
      Tabs.setTabBar(TabBar(D))
      Tabs.addTab(self.MemoryTabUI(), "Memory")
      Tabs.addTab(self.RegisterTabUI(), "Register")
      layout.addWidget(Tabs)
      
      # tabs = QTabWidget()
   
      # tabs.addTab(self.MemoryTabUI(), "Memory")
      # tabs.addTab(self.RegisterTabUI(), "Register")
      # layout.addWidget(tabs)
      layout.addStretch()

      compilerTab.setLayout(layout)
      return compilerTab

   def run_code(self):
       # run()
       print("run clicked")
       
   def step_code(self):
       # step()
       print("step clicked")
       
   def reset_code(self):
       # reset()
       print("reset clicked")
       
   def dump_code(self):
       # dump()
       print("dump clicked")
       
   def MemoryTabUI(self):
      memoryTab = QWidget()
      f_lay = QVBoxLayout()
      layout = QGridLayout()
      
      self.labels=[]
      self.mem_page = 0

      for i in range(10):
         t = []
         for j in range(5):
            if(j==0):
               t.append(QLabel(hex(4*i))) 
            else:
               t.append(QLabel("00"))
               
         self.labels.append(t)
      
      
      layout.addWidget(QLabel("Address"),0,0,1,1)
      layout.addWidget(QLabel("+0"),0,1,1,2)
      layout.addWidget(QLabel("+1"),0,2,1,2)
      layout.addWidget(QLabel("+2"),0,3,1,2)
      layout.addWidget(QLabel("+4"),0,4,1,2)
      

      for i in range(10):
         for j in range(5):
            if(j==0):
               layout.addWidget(self.labels[i][j],i+1,j,1,1)   
            layout.addWidget(self.labels[i][j],i+1,j,1,2)
      
      f_lay.addLayout(layout)
      
      nav_pane = QHBoxLayout()

      self.jump = QComboBox()
      self.jump.addItems(["--Choose--","Text","Data","Heap","Stack"])
      self.jump.currentIndexChanged.connect(self.selectionchange)


      up = QPushButton("UP")
      up.clicked.connect(self.UP_onclick)

      down = QPushButton("DOWN")
      down.clicked.connect(self.DOWN_onclick)

      nav_pane.addWidget(QLabel("Jump"))
      nav_pane.addWidget(self.jump)
      nav_pane.addWidget(up)
      nav_pane.addWidget(down) 
      f_lay.addLayout(nav_pane)
      f_lay.addStretch()

      jumpto = QHBoxLayout()
      jumpto.addWidget(QLabel("Jump to"))
      jump_add = QLineEdit()
      jumpto.addWidget(jump_add)
      self.jump_to=""
      jump_add.textChanged.connect(self.textChanged)
      jump_add.editingFinished.connect(self.jump_enterPress)

      f_lay.addLayout(jumpto)

      memoryTab.setLayout(f_lay)
      return memoryTab

   def DOWN_onclick(self):
      self.mem_page+=1
      self.mem_pane_update()
   
   def UP_onclick(self):
      if(self.mem_page>0):
         self.mem_page-=1
         self.mem_pane_update()

   def textChanged(self, address):
      self.jump_to = address

   def jump_enterPress(self):
      if(self.jump_to != "" and int(self.jump_to, 16) >= 0 and int(self.jump_to, 16)<= 2147483647):
         self.mem_page = int(int(self.jump_to, 16)/40)
         self.mem_pane_update()


   def selectionchange(self,i):
      pg = [0, 0, 6710886, 6711705, 53687090]
      if(i>0):
         self.mem_page = pg[i]
      self.mem_pane_update()

   def mem_pane_update(self):
      for i in range(10):
         for j in range(5):
            if(j==0):
               self.labels[i][j].setText(hex(4*i+(40*self.mem_page)))
            else:
               if(4*i+(40*self.mem_page)+j-1 in self.memory):
                  self.labels[i][j].setText(self.memory[4*i+(40*self.mem_page)+j-1])
               elif(4*i+(40*self.mem_page)+j-1 < 0 or 4*i+(40*self.mem_page)+j-1> 2147483647):
                  self.labels[i][j].setText("--")
               else:
                  self.labels[i][j].setText("00")

   def RegisterTabUI(self):

      registerTab = QWidget()
      v= QVBoxLayout()

      gb = QGroupBox()

      layout = QVBoxLayout()
      for i in range(32):
         reg = QHBoxLayout()
         reg.addWidget(QLabel("x"+str(i+1)))
         reg.addWidget(QLabel("0x0"))
         layout.addLayout(reg)

      gb.setLayout(layout)
      scr = QScrollArea()
      
      scr.setWidget(gb)
      scr.setWidgetResizable(True)
      scr.setFixedHeight(700)
      scr.setFixedWidth(200)

      v.addWidget(scr)
      registerTab.setLayout(v)
      return registerTab

if __name__ == "__main__":
   app = QApplication(sys.argv)
   app.setStyleSheet("QLabel{font-size: 12pt;font-color: white;}")
   app.setStyle("fusion")
   custom_font = QFont()
   custom_font.setWeight(12);
   QApplication.setFont(custom_font, "QLabel")
   window = Window()
   
   window.show()
   sys.exit(app.exec_())
