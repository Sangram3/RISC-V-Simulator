import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from memory_p import *
from registers_p import *
from fetch_p import *
from decode_p import *
from execute_p import *
from mem_p import *
from write_back_p import *
from RISCV_Sim_p import *
from Pipeline import *

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
      self.setStyleSheet("color: white;background: black; font-family: Consolas;")
      self.bt=QPushButton("",self)
      self.merged = []
      self.out_msg=[]
      self.out_step=[]
      self.memory={}
      self.register=[]
      self.file_mc=""
      self.pipelined = 0
      self.forwarding = 0

      self.all_pip_regs = 0
      self.inst_pip_regs = 0
      self.inst_num = 0

      self.flowchartarr = [['F'], ['D','F'], ['E', 'D', 'F'], ['M', 'D', 'D'], ['W', 'D', 'D'], ['D', 'D'], ['E', 'E', 'F'], ['M', 'M', 'D', 'F'], ['W', 'W', 'E'], ['M'], ['W']]

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
      self.tabs = QTabWidget()
      d = {
            "Editor": QtGui.QColor("blue"),
            "Simulator": QtGui.QColor("brown"),
            "Flow Chart": QtGui.QColor("red"),
        }
      self.tabs.setTabBar(TabBar(d))
      self.tabs.addTab(self.EditorTabUI(), "Editor")
      self.tabs.addTab(self.CompilerTabUI(), "Simulator")
      layout.addWidget(self.tabs)
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
      filebox.addSpacerItem(QSpacerItem(10,10,QSizePolicy.Expanding))
      self.f=QLabel("File")
      filebox.addWidget(self.f)
      filebox.addSpacerItem(QSpacerItem(100,10,QSizePolicy.Expanding))
      btn = QPushButton("Select File")
      btn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #000080; font-size: 15px; color: white;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : brown;  font-size: 15px; color: white;"
                             "}"
                             )
      filebox.addWidget(btn)
      
      knobs = QGroupBox("Knobs")
      knobs.setStyleSheet("background-color: white; font-size: 20px; font-family: Consolas; color: Black;")
      self.cb_layout = QVBoxLayout()
      pipelining_cb = QCheckBox("Pipelining", self)
      pipelining_cb.setStyleSheet("QCheckBox"
                                 "{"
                                 "color: Black; font-size: 20px; font-family: Consolas;"
                                 "}")
                                 
      '''
                                 "QCheckBox::indicator"
                                 "{"
                                 "background-color:white;"
                                 "}"
                                 )
      '''
      pipelining_cb.stateChanged.connect(self.pipelining_ed)
      self.cb_layout.addWidget(pipelining_cb)
      
      filebox.addSpacerItem(QSpacerItem(400,10,QSizePolicy.Expanding))
      
      knobs.setLayout(self.cb_layout)
      filebox.addWidget(knobs)

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
                    mem_mod.__init__(path)
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.editor.setPlainText(text)
   
   def CompilerTabUI(self):
      compilerTab = QWidget()
      layout = QHBoxLayout()
      lef_s = QVBoxLayout()
      self.run= QHBoxLayout()

      self.run.addWidget(self.run_btn)
      self.run.addStretch()
      
      self.run.addWidget(self.step_btn)
      self.run.addStretch()
      
      self.run.addWidget(self.reset_btn)
      self.run.addStretch()
      
      self.run.addWidget(self.dump_btn)
      self.run.addStretch()

      self.run_btn.clicked.connect(self.run_code)      
      self.step_btn.clicked.connect(self.step_code)      
      self.reset_btn.clicked.connect(self.reset_code)      
      self.dump_btn.clicked.connect(self.dump_code)      

      lef_s.addLayout(self.run)
      layout.addStretch()

      self.formLayout = self.pane_type()
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

   def pane_type(self):
      if(self.pipelined == 0):
         return QFormLayout()
      else:
         return QGridLayout()


   def pipelining_ed(self, state):
      if state == Qt.Checked:
         self.run.stretch(4)
         forwarding_cb = QCheckBox("Forwarding", self)
         forwarding_cb.setStyleSheet("QCheckBox"
                                 "{"
                                 "color: Black; font-size: 20px; font-family: Consolas;"
                                 "}"
                                 )

         forwarding_cb.stateChanged.connect(self.forwarding_ed)
         self.cb_layout.addWidget(forwarding_cb)
         
         print_reg_cb = QCheckBox("Print Register Values at the End of Each Cycle", self)
         print_reg_cb.setStyleSheet("QCheckBox"
                                 "{"
                                 "color: Black; font-size: 20px; font-family: Consolas;"
                                 "}"
                                 )
                                 
         print_reg_cb.stateChanged.connect(self.print_reg_ed)
         self.cb_layout.addWidget(print_reg_cb)
         
         print_pip_cb = QCheckBox("Print Pipeline Register Values", self)
         print_pip_cb.setStyleSheet("QCheckBox"
                                 "{"
                                 "color: Black; font-size: 20px; font-family: Consolas;"
                                 "}"
                                 )
                                 
         print_pip_cb.stateChanged.connect(self.print_pip_ed)
         self.cb_layout.addWidget(print_pip_cb)
         
         
         self.pipelined = 1
         if(self.run.count()>6):
            self.run.itemAt(2).widget().setHidden(True)

      else:
         self.pipelined = 0
         self.forwarding = 0
         self.run.itemAt(2).widget().setHidden(False)

         if (self.cb_layout.count() > 1):
            for i in range(self.cb_layout.count()-1):
               i = self.cb_layout.count()-1-i
               try:
                  self.cb_layout.itemAt(i).widget().deleteLater()
               except:
                  self.cb_layout.itemAt(i).layout().deleteLater()
               

   def forwarding_ed(self, state):
      if state == Qt.Checked:
         self.forwarding = 1
      else:
         self.forwarding = 0

   def print_reg_ed(self, state):
      pass

   def print_pip_ed(self, state):
      if(state == Qt.Checked and self.cb_layout.count()<6):
         self.all_pip_regs=1
         x=QHBoxLayout()
         ec = QRadioButton("At the end of each Cycle")
         x.addSpacerItem(QSpacerItem(20,10))
         x.addWidget(ec)
         ec.but = 0
         ec.toggled.connect(self.onClicked)
         
         y=QHBoxLayout()
         ci = QRadioButton("Certain Cycle's")
         ci.but = 1
         ci.toggled.connect(self.onClicked)
         inst_no = QLineEdit()
         inst_no.textChanged.connect(self.inst_num_changed)
         y.addSpacerItem(QSpacerItem(20,10))
         y.addWidget(ci)
         y.addWidget(inst_no)

         self.cb_layout.addLayout(x)
         self.cb_layout.addLayout(y)
         
      else:
         self.all_pip_regs = 0
         self.cb_layout.itemAt(5).deleteLater()
         self.cb_layout.itemAt(4).deleteLater()

   def inst_num_changed(self, inst):
      self.inst_num = inst
      
   def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            if(radioButton.but == 0):
               self.all_pip_regs = 1
               self.inst_pip_regs = 0
            else:
               self.all_pip_regs = 0
               self.inst_pip_regs = 1  

   def run_code(self):
       if(self.pipelined == 1 and self.tabs.count()==2):
           self.tabs.addTab(self.FlowChartTabUI(), "Flow Chart")
       elif(self.pipelined == 0 and self.tabs.count()==3):
           self.tabs.removeTab(self.tabs.count()-1)
           
       if(self.pipelined == 0):  
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

       elif(self.pipelined == 1):  
         if self.code_ended == 0:
            self.code_ended = 1
            execute_cycle_util()
            
            self.memory = mem_mod.get_mem()
            self.mem_pane_update()
            self.register = reg_mod.get_regs()
            self.reg_pane_update()

            for i in range(self.formLayout.count()):
               self.formLayout.itemAt(i).widget().deleteLater()
            
            row=0
            if(self.all_pip_regs == 1):
               buf_type = ["FD",'DE', 'EM', 'MW']
               for i in range(len(gui_util_obj.buffers_pane)):
                  x = QLabel("Cycle: "+ str(i+1))
                  x.setStyleSheet("background-color: blue")
                  print(self.formLayout)
                  self.formLayout.addWidget(x)
                  row+=1
                  for j in range(len(gui_util_obj.buffers_pane[i])):
                     y = QLabel(buf_type[j] +" Interstate Buffer")
                     y.setStyleSheet("background-color: green")
                     self.formLayout.addWidget(y)
                     self.formLayout.addWidget(QLabel("Mneumonic: "+ str(gui_util_obj.buffers_pane[i][j].mne)))
                     row+=1
                     self.formLayout.addWidget(QLabel("rs1: "+ str(gui_util_obj.buffers_pane[i][j].rs1)))
                     row+=1
                     self.formLayout.addWidget(QLabel("rs2: "+ str(gui_util_obj.buffers_pane[i][j].rs2)))
                     row+=1
                     self.formLayout.addWidget(QLabel("rd: "+ str(gui_util_obj.buffers_pane[i][j].rd)))
                     row+=1
                        
            elif(self.inst_pip_regs == 1):
               buf_type = ["FD",'DE', 'EM', 'MW']
               i = int(self.inst_num) - 1
               x = QLabel("Cycle: "+ str(i+1))
               x.setStyleSheet("background-color: blue")
               self.formLayout.addWidget(x)
               row+=1
               for j in range(len(gui_util_obj.buffers_pane[i])):
                  y = QLabel(buf_type[j] +" Interstate Buffer")
                  y.setStyleSheet("background-color: green")
                  self.formLayout.addWidget(y)
                  self.formLayout.addWidget(QLabel("Mneumonic: "+ str(gui_util_obj.buffers_pane[i][j].mne)))
                  row+=1
                  self.formLayout.addWidget(QLabel("rs1: "+str(gui_util_obj.buffers_pane[i][j].rs1)))
                  row+=1
                  self.formLayout.addWidget(QLabel("rs2: "+str(gui_util_obj.buffers_pane[i][j].rs2)))
                  row+=1
                  self.formLayout.addWidget(QLabel("rd: "+str(gui_util_obj.buffers_pane[i][j].rd)))
                  row+=1
                  self.formLayout.addWidget(QLabel())
            self.refresh_table()  
         return 


   def FlowChartTabUI(self):
      ui = QWidget()
      win = QVBoxLayout()
     
      self.form_B = QGroupBox()
      self.horiz_b= QHBoxLayout()
      
      self.table = QTableWidget()
      self.horiz_b.addWidget(self.table)

      self.form_B.setLayout(self.horiz_b)
      scr = QScrollArea()
      
      scr.setWidget(self.form_B)
      scr.setWidgetResizable(True)
      scr.setFixedHeight(900)
      scr.setFixedWidth(1700)

      win.addWidget(scr)
      ui.setLayout(win)
      
      return ui

   def refresh_table(self):
      print(pipeline_obj.pipeline)
      print(gui_util_obj.matrix)
      print(gui_util_obj.left_pane)
      count_i = 0
      self.table.setColumnCount(len(pipeline_obj.pipeline)+1)
      self.table.setRowCount(len(gui_util_obj.left_pane))
      for i in gui_util_obj.left_pane:
         self.table.setItem(count_i,0, QTableWidgetItem(str(i)))
         count_i+=1
      
      
      self.table.horizontalHeader().setVisible(False)
      self.table.verticalHeader().setVisible(False)

      inst = 0
      for i in range(len(pipeline_obj.pipeline)):
         if(len(pipeline_obj.pipeline[i])!=0):
            for j in range(len(pipeline_obj.pipeline[i])):
               x =  QTableWidgetItem(str(pipeline_obj.pipeline[i][j]))
               self.table.setItem(j+inst,i+1, x)
               if(self.forwarding ==1 and j in gui_util_obj.data_hazards and gui_util_obj.data_hazards[j] == i):
                  x.setBackground(QtGui.QColor("red"))
            if( pipeline_obj.pipeline[i][0] == 'W'):
               inst+=1   
      
      self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
      
   def step_code(self):
       if self.code_ended == 0:
           try:
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
           except:
               pass
       
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
							"MC documents (*.mc)")
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
            val = self.dec_to_2s(self.register[i],8)
         else:
            val = self.extend_hex(self.register[i],8)
         self.reg_labels[i].setText(val)

   def dec_to_2s(self,data, digits):
      return (hex(2**(digits*4) + data))
   
   def extend_hex(self,data, digits):
      ans =hex(data)[2:]
      if(len(hex(data)) < digits+2):
         for i in range(digits+2- len(hex(data))):
            ans = "0"+ans

         return "0x" + ans
      else:
         return hex(data)
if __name__ == "__main__":
   app = QApplication(sys.argv)
   try:
    app.setStyleSheet("QLabel{font-size: 12pt;}")
   except:
    pass
   app.setStyle("fusion")
   custom_font = QFont()
   custom_font.setWeight(12);
   QApplication.setFont(custom_font, "QLabel")
   window = Window()
   
   window.showMaximized()
   sys.exit(app.exec_())
