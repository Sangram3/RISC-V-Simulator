import sys

from PyQt5.QtWidgets import *

class Window(QWidget):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("QTabWidget Example")
      self.resize(300, 200)
      
      layout = QVBoxLayout()
      self.setLayout(layout)
      
      tabs = QTabWidget()
      tabs.addTab(self.EditorTabUI(), "Editor")
      tabs.addTab(self.CompilerTabUI(), "Compiler")
      layout.addWidget(tabs)

   def EditorTabUI(self):
      editorTab = QWidget()
      layout = QVBoxLayout()
      
      self.fn='File'
      filebox = QHBoxLayout()
      self.f=QLabel("File")
      filebox.addWidget(self.f)
      filebox.addStretch()

      btn = QPushButton("Select File")
      filebox.addWidget(btn)
      filebox.addStretch()

      btn.clicked.connect(self.getfile)
      
      layout.addLayout(filebox)
      layout.addWidget(QTextEdit())
      
      editorTab.setLayout(layout)
      return editorTab

   def getfile(self):
      fname = QFileDialog.getOpenFileName(self, 'Open file', 'D:\\4th_Sem\CS204\Project',"Machine Cdde files (*.mc)")
      print(str(fname[0]))
      self.f.setText(str(fname[0]))
   

   def CompilerTabUI(self):
      compilerTab = QWidget()
      layout = QHBoxLayout()
      lef_s = QVBoxLayout()

      run= QHBoxLayout()
      run.addWidget(QPushButton("Run"))
      run.addStretch()
      run.addWidget(QPushButton("Step"))
      run.addStretch()
      run.addWidget(QPushButton("Reset"))
      run.addStretch()
      run.addWidget(QPushButton("Dump"))
      run.addStretch()

      lef_s.addLayout(run)
      layout.addStretch()

      formLayout =QFormLayout()
      groupBox = QGroupBox("Machine Code Input")
      labelLis = []
      comboList = []
      labelLis.append(QLabel("PC    "))
      comboList.append(QLabel("Instruction"))
         
      for i in  range(100):
         labelLis.append(QLabel("0x0      "))
         comboList.append(QLabel("Inst"))
         formLayout.addRow(labelLis[i], comboList[i])

      groupBox.setLayout(formLayout)
      scroll = QScrollArea()
      
      scroll.setWidget(groupBox)
      scroll.setWidgetResizable(True)
      scroll.setFixedHeight(700)
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
      scr.setFixedWidth(700)
      
      lef_s.addWidget(scr)
      lef_s.addStretch()
      
      layout.addLayout(lef_s)
      layout.addStretch()

      tabs = QTabWidget()
      tabs.addTab(self.MemoryTabUI(), "Memory")
      tabs.addTab(self.RegisterTabUI(), "Register")
      layout.addWidget(tabs)
      layout.addStretch()

      compilerTab.setLayout(layout)
      return compilerTab

   def MemoryTabUI(self):
      memoryTab = QWidget()
      layout = QGridLayout()
      layout.addWidget(QLabel("Address"),0,0,1,2)
      layout.addWidget(QLabel("+0"),0,1,1,2)
      layout.addWidget(QLabel("+1"),0,2,1,2)
      layout.addWidget(QLabel("+2"),0,3,1,2)
      layout.addWidget(QLabel("+4"),0,4,1,2)

      for i in range(10):
         for j in range(5):
            if(j==0):
               layout.addWidget(QLabel("0x0"),i+1,j,1,2) 
            else:
               layout.addWidget(QLabel("00"),i+1,j,1,2)
      
      memoryTab.setLayout(layout)
      return memoryTab

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
   window = Window()
   window.show()
   sys.exit(app.exec_())
