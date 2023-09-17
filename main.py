# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from PyQt6.QtWidgets import QApplication
from modules.Configuration import OpenFile
from modules.Operations import Preparation
from datetime import date, timedelta, datetime


def main():
    # Prompt user to select the data file to process
    app = QApplication(sys.argv)
    of = OpenFile()
    of.show()
    of.close()
    app.exit()

    # Load data file into preparation class
    prep = Preparation(of.file_loc)
    print(prep.df)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
