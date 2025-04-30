import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
# You'll need to make this ui in QtDesigner
# And convert it to a .py file using the MakeUIPy.bat file
from batch_renamer_Jin_ui import Ui_MainWindow
import batch_renamer_Jin
# Add comment for testing

class BatchRenamerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # UI Setup
        super().__init__()
        super(Ui_MainWindow).__init__()
        self.setupUi(self)
        # Connect "Browse" button to get_filepath function
        self.browseBtn.clicked.connect(self.get_filepath)
        # Connect "Run" button to run_renamer function
        self.run.clicked.connect(self.run_renamer)

        # Instance the "back end"
        self.batch_renamer = batch_renamer_Jin.BatchRenamer()

        # Show UI normal vs maximized
        self.showNormal()


    def get_filepath(self):
        """
        Open a file dialog for browsing to a folder
        """
        self.filepath = QFileDialog().getExistingDirectory()
        self.set_filepath(self.filepath)


    def set_filepath(self, filepath_to_set):
        """
        Set lineEdit text for filepath
        """
        self.filePathLine.setText(filepath_to_set)
        self.update_list(filepath_to_set)


    def update_list(self, filepath_to_update):
        """
        Clear listwidget
        read files in filepath with os.walk
        Add files as new items
        """
        self.listWidget.clear()
        for root, dirs, files in os.walk(filepath_to_update):
            self.listWidget.addItems(files)

    # Add a function to gather and set parameters based upon UI
    # e.g. lineEdit.text() or radioButton.isChecked
    # remember that you may need to check to see if the result
    # was a tuple and correct like so:
    # self.filepath = self.filepathEdit.text()
    # if type(self.filepath) is tuple:
    #     self.filepath = self.filepath[0]

    def gather_and_set_parameters(self):
        self.new_folder = self.newFolderLine.text()
        self.copy_file = self.copyRadioBtn.isChecked()
        self.overwrite = self.forceOverride.isChecked()
        self.filetype = self.fileTypeLine.text()
        self.prefix = self.prefixLine.text()
        self.suffix = self.suffixLine.text()
        self.strings_to_find = self.stringsToFindLine.text()
        self.string_to_replace = self.stringsToReplaceLine.text()



    def run_renamer(self):
        """
        Run back end batch renamer using self.batch_renamer
        self.batch_renamer is an instance of the BatchRenamer class
        """
        # run gather_and_set_parameters function to set parameters
        self.gather_and_set_parameters()
        # unction call to Gather Parameters
        self.batch_renamer.process_folder(self.filepath,
                                          self.new_folder,
                                          self.copy_file,
                                          self.overwrite,
                                          self.filetype,
                                          self.strings_to_find,
                                          self.string_to_replace,
                                          self.prefix,
                                          self.suffix,
        )
        # If new_folder is used, change filepath to new_folder
        # Update List Widget
        if self.new_folder != "":
            self.set_filepath(self.new_folder)
        else:
            self.set_filepath(self.filepath)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BatchRenamerWindow()
    sys.exit(app.exec())
 
