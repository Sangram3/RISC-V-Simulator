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
      layout.addWidget(QTextEdit())
      editorTab.setLayout(layout)
      return editorTab

   def CompilerTabUI(self):
      compilerTab = QWidget()
      layout = QHBoxLayout()
      lef_s = QVBoxLayout()

      run= QHBoxLayout()
      run.addWidget(QPushButton("Run"))
      run.addWidget(QPushButton("Step"))
      run.addWidget(QPushButton("Reset"))
      run.addWidget(QPushButton("Dump"))
      
      lef_s.addLayout(run)
      for i in range(20):
         lef_s.addWidget(QLabel("Inst"))  
      
      layout.addLayout(lef_s)

      tabs = QTabWidget()
      tabs.addTab(self.MemoryTabUI(), "Memory")
      tabs.addTab(self.RegisterTabUI(), "Register")
      layout.addWidget(tabs)

      compilerTab.setLayout(layout)
      return compilerTab

   def MemoryTabUI(self):
      memoryTab = QWidget()
      layout = QVBoxLayout()
      layout.addWidget(QLabel("Memory"))
      memoryTab.setLayout(layout)
      return memoryTab

   def RegisterTabUI(self):

      registerTab = QWidget()
      layout = QVBoxLayout()
      layout.addWidget(QLabel("Registers"))
      registerTab.setLayout(layout)
      return registerTab

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = Window()
   window.show()
   sys.exit(app.exec_())
