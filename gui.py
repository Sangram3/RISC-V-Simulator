import sys

from PyQt5.QtWidgets import *

class Window(QWidget):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("QTabWidget Example")
      self.resize(4000, 3000)
      # Create a top-level layout
      layout = QVBoxLayout()
      self.setLayout(layout)
      # Create the tab widget with two tabs
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

      for i in range(5):
         lef_s.addWidget(QLabel("Inst"))  
         lef_s.addStretch()
      self.Output= QLabel("Output")
      lef_s.addWidget(self.Output)
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
      layout.addWidget(QLabel("Address"),0,0)
      layout.addWidget(QLabel("+0"),0,1)
      layout.addWidget(QLabel("+1"),0,2)
      layout.addWidget(QLabel("+2"),0,3)
      layout.addWidget(QLabel("+4"),0,4)

      for i in range(10):
         for j in range(5):
            if(j==0):
               layout.addWidget(QLabel("0x0"),i+1,j) 
            else:
               layout.addWidget(QLabel("00"),i+1,j)
      
      memoryTab.setLayout(layout)
      return memoryTab

   def RegisterTabUI(self):

      registerTab = QWidget()
      layout = QVBoxLayout()

      
      for i in range(32):
         reg = QHBoxLayout()
         reg.addWidget(QLabel("x"+str(i+1)))
         reg.addWidget(QLabel("0x0"))
         layout.addLayout(reg)

      registerTab.setLayout(layout)
      return registerTab

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = Window()
   window.show()
   sys.exit(app.exec_())
