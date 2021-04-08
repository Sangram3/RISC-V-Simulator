import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from memory import *
from registers import *
from fetch import *
from decode import *
from execute import *
from mem import *
from control import *
from write_back import *
from RISCV_Sim import *

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
      self.setWindowTitle("RISC-V Simulator")
      self.setWindowIcon(QIcon("logo.png"))
      # self.setGeometry(300, 300,300,300)
      self.move(0,0)
      self.setStyleSheet("background: white;")  
      self.setStyleSheet("color: white;background: black")
      self.bt=QPushButton("",self)
      self.merged = []
      self.out_msg=[]
      self.out_step=[]
      self.memory={}
      self.register=[]
      self.file_mc=""
      # set reset step dump ##################################################
      self.first_frame = {}
      self.run_btn = QPushButton('Run')
      self.step_btn= QPushButton('Step')
      self.reset_btn= QPushButton('Reset')
      self.dump_btn= QPushButton('Dump')
      self.code_ended = 0
      self.index=0
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
            "Simulator": QtGui.QColor("brown"),
        }
      tabs.setTabBar(TabBar(d))
      tabs.addTab(self.EditorTabUI(), "Editor")
      tabs.addTab(self.CompilerTabUI(), "Simulator")
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
      filebox.addStretch(0)
      filebox.addWidget(self.f)
      filebox.addStretch(0)
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
      filebox.addStretch(2)
      btn.clicked.connect(self.getfile)
      layout.addLayout(filebox)
      self.editor = QPlainTextEdit()
      self.editor.setReadOnly(True)
      fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
      fixedfont.setPointSize(12)
      self.editor.setFont(fixedfont)
      layout.addWidget(self.editor)
      editorTab.setLayout(layout)
      return editorTab

   def getfile(self):
      path, _ = QFileDialog.getOpenFileName(self, "Open file", "", 
                             "MC documents (*.mc)")
      
      self.f.setText(str(path))
      
      if path:
            try:
                with open(path) as f:
                    text = f.read()
                    self.file_mc=path
                    print(path)
                    mem_mod.__init__(path)
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.editor.setPlainText(text)
   
   def CompilerTabUI(self):
      compilerTab = QWidget()
      layout = QHBoxLayout()
      lef_s = QVBoxLayout()
      run= QHBoxLayout()

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

      self.formLayout =QFormLayout()
      groupBox = QGroupBox("     clk                                 PC                                              Machine Code                                                 Basic Code")
     
      groupBox.setLayout(self.formLayout)
      scroll = QScrollArea()
      scroll.setWidget(groupBox)
      scroll.setWidgetResizable(True)
      scroll.setFixedHeight(500)
      scroll.setFixedWidth(1000)

      lef_s.addWidget(scroll)
      
      lef_s.addWidget(QLabel())
      lef_s.addWidget(QLabel())

      self.gB = QGroupBox("Output")
      self.vb= QFormLayout()
      
      
         
      self.gB.setLayout(self.vb)
      scr = QScrollArea()
      
      scr.setWidget(self.gB)
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
      layout.addStretch()

      compilerTab.setLayout(layout)
      return compilerTab

    
   def run_code(self):
      
       if self.code_ended == 0:
           self.code_ended = 1
           self.is_step_first_time = 0
           self.first_frame ,self.out_msg= run(self.out_msg)
           #print(self.out_msg)
           for key in self.first_frame:
              self.merged.append(QLabel("{}                {}                         {}                         {}".format(self.first_frame[key][0],self.first_frame[key][1],self.first_frame[key][2],self.first_frame[key][3])))
              self.formLayout.addRow(self.merged[-1])
           self.memory = mem_mod.get_mem()
           self.mem_pane_update()
           self.register = reg_mod.get_regs()
           self.reg_pane_update()
           for i in range(len(self.out_msg)):
              self.vb.addRow(QLabel(self.out_msg[i]))
              if(self.out_msg[i][0][0]=="W"):
                  self.vb.addRow(QLabel(" "))    
           self.gB.setLayout(self.vb)
       return 
       
   def step_code(self):
       if self.code_ended == 0:
           
           st,self.out_step = step(self.out_step)
           #print(self.out_step)
           if st==None:
               self.code_ended = 1
           else:
               self.merged.append(QLabel("{}                {}                         {}                         {}".format(st[0],st[1],st[2],st[3])))
               self.formLayout.addRow(self.merged[-1])
               self.memory = mem_mod.get_mem()
               self.mem_pane_update()
               self.register = reg_mod.get_regs()
               self.reg_pane_update()
               for i in range(len(self.out_step)):
                  self.vb.addRow(QLabel(self.out_step[i]))
                  if(self.out_msg[i][0][0]=="W"):
                     self.vb.addRow(QLabel(" "))    
               self.gB.setLayout(self.vb)
       
   def reset_code(self):

       for i in reversed(range(self.vb.count())): 
         self.vb.itemAt(i).widget().setParent(None)
       self.gB.setLayout(self.vb)

       if(self.file_mc!=""):
          mc_file= self.file_mc
       
       else:
          mc_file = "temp.mc"

       mem_mod.reset_mem()
       reg_mod.reset_regs()
       print(mc_file)
       mem_mod.__init__(mc_file)
       

       self.first_time = 1
       self.memory = mem_mod.get_mem()
       self.mem_pane_update()
       self.register = reg_mod.get_regs()
       self.reg_pane_update()
       self.code_ended = 0
       for i in self.merged:
           i.clear()
       for i in range(self.formLayout.count()):
            self.formLayout.itemAt(0).widget().close()
            self.formLayout.takeAt(0)
   def dump_code(self):
       path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
							"Text documents (*.txt);All files (*.*)")
       if not path:
          return
       self._save_to_path(path)

   def _save_to_path(self, path):

       text = mem_mod.code_ends()
       try:
           with open(path,'w')  as f:
               f.write(text)
       except Exception as e:
           pass
       else:
           self.path = path
               
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
               t.append(QLabel((hex(4*i).upper()+"    "))) 
            else:
               t.append(QLabel("00"))
               
         self.labels.append(t)
      
      add_l=QLabel("Address     ")
      add_l.setAlignment(Qt.AlignCenter)
      plus0 = QLabel(" +0 ")
      plus0.setAlignment(Qt.AlignCenter)
      plus1 = QLabel(" +1 ")
      plus1.setAlignment(Qt.AlignCenter)
      plus2 = QLabel(" +2 ")
      plus2.setAlignment(Qt.AlignCenter)
      plus3 = QLabel(" +4 ")
      plus3.setAlignment(Qt.AlignCenter)
      
      layout.addWidget(add_l, 0,0)
      layout.addWidget(plus0, 0,1)
      layout.addWidget(plus1, 0,2)
      layout.addWidget(plus2, 0,3)
      layout.addWidget(plus3, 0,4)
      

      for i in range(10):
         for j in range(5):
            self.labels[i][j].setAlignment(Qt.AlignCenter)
            if(j!=0):
               self.labels[i][j].setStyleSheet("border: 1px solid white;")   
            layout.addWidget(self.labels[i][j],i+1,j)
      
      #f_lay.addStretch(0)
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
      
      #f_lay.addStretch(0)
      f_lay.addLayout(nav_pane)
      

      jumpto = QHBoxLayout()
      jumpto.addWidget(QLabel("Jump to"))
      jump_add = QLineEdit()
      jumpto.addWidget(jump_add)
      self.jump_to=""
      jump_add.textChanged.connect(self.textChanged)
      jump_add.editingFinished.connect(self.jump_enterPress)

      #f_lay.addStretch(0)
      f_lay.addLayout(jumpto)
      #f_lay.addStretch(0)

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
               self.labels[i][j].setText(hex(4*i+(40*self.mem_page)).upper()+"    ")
            else:
               if(4*i+(40*self.mem_page)+j-1 in self.memory):
                  self.labels[i][j].setText(self.memory[4*i+(40*self.mem_page)+j-1].upper())
               elif(4*i+(40*self.mem_page)+j-1 < 0 or 4*i+(40*self.mem_page)+j-1> 2147483647):
                  self.labels[i][j].setText("--")
               else:
                  self.labels[i][j].setText("00")

   def RegisterTabUI(self):

      registerTab = QWidget()
      v= QVBoxLayout()

      gb = QGroupBox()

      self.reg_labels = [QLabel("0x00000000") for i in range(32)]
      
      layout = QVBoxLayout()

      for i in range(32):
         reg = QHBoxLayout()
         reg_name = QLabel("x"+str(i))
         reg_name.setMaximumSize(100, 50)
         reg_name.setAlignment(Qt.AlignCenter)
         reg_value = self.reg_labels[i]
         reg_value.setAlignment(Qt.AlignCenter)
         reg_value.setStyleSheet("border: 1px solid white;")   
         
         reg.addWidget(reg_name)
         reg.addWidget(reg_value)

         layout.addLayout(reg)
         layout.addWidget(QLabel(" "))

      gb.setLayout(layout)
      scr = QScrollArea()
      
      scr.setWidget(gb)
      scr.setWidgetResizable(True)
      scr.setFixedHeight(800)
      scr.setFixedWidth(400)

      v.addWidget(scr)
      registerTab.setLayout(v)
      return registerTab

   def reg_pane_update(self):
      for i in range(32):
         val = ''
         if(self.register[i]<0): 
            val = self.dec_to_2s(self.register[i],32)
         else:
            val = self.extend_hex(self.register[i],32)
         self.reg_labels[i].setText(val)

   def dec_to_2s(data, digits):
      return (hex(2**(digits*4) - data))
   
   def extend_hex(self,data, digits):
      ans =hex(data)[2:]
      if(len(hex(data)) < 10):
         for i in range(10- len(hex(data))):
            ans = "0"+ans
         return "0x" + ans
      else:
         return hex(data)
if __name__ == "__main__":
   app = QApplication(sys.argv)
   try:
    app.setStyleSheet("QLabel{font-size: 12pt;font-color: white;}")
   except:
    pass
   app.setStyle("fusion")
   custom_font = QFont()
   custom_font.setWeight(12);
   QApplication.setFont(custom_font, "QLabel")
   window = Window()
   
   window.showMaximized()
   sys.exit(app.exec_())
