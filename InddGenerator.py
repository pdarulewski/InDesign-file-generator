from pprint import pprint
import sys
import traceback
import logging
import os
import win32com.client as client

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('indd_generator')

class InddGenerator:
    __filenames = []
    __fileformats= []
    __data = None
    __destination = None
    __month = None

    def __init__(self, data, destination, month):
        self.__data = data
        self.__destination = destination
        self.__month = month

    def generate_indd_files(self):
        try:
            app = client.Dispatch('InDesign.Application.CC.2018')
            for filename, fileformat in zip(self.__filenames, self.__fileformats):
                self.__generate_indd_file(filename, fileformat, app)
            logger.info('%s', 'All indd files were generated.')
        except Exception:
            logger.error("An error occurred while generating indd files.")
            traceback.print_exc()
            sys.exit()

    def __generate_indd_file(self, filename, fileformat, app):
        idPortrait = 1751738216
        myDocument = app.Documents.Add()
        try:
            if("b2" in fileformat):
                myDocument.DocumentPreferences.PageHeight = "684mm"
                myDocument.DocumentPreferences.PageWidth = "484mm"
            elif("a2" in fileformat):
                myDocument.DocumentPreferences.PageHeight = "594mm"
                myDocument.DocumentPreferences.PageWidth = "420mm"
            elif("a3" in fileformat):
                myDocument.DocumentPreferences.PageHeight = "420mm"
                myDocument.DocumentPreferences.PageWidth = "297mm"
            else: # for fb / b1
                myDocument.DocumentPreferences.PageHeight = "1000mm"
                myDocument.DocumentPreferences.PageWidth = "707mm"

            myDocument.DocumentPreferences.PageOrientation = idPortrait

            myDocument.DocumentPreferences.DocumentBleedBottomOffset = "5mm"
            myDocument.DocumentPreferences.DocumentBleedTopOffset = "5mm"
            myDocument.DocumentPreferences.DocumentBleedInsideOrLeftOffset = "5mm"
            myDocument.DocumentPreferences.DocumentBleedOutsideOrRightOffset = "5mm"

            myDocument.DocumentPreferences.SlugBottomOffset = "0mm"
            myDocument.DocumentPreferences.SlugTopOffset = "0mm"
            myDocument.DocumentPreferences.SlugInsideOrLeftOffset = "0mm"
            myDocument.DocumentPreferences.SlugRightOrOutsideOffset = "0mm"

            myDocument.MarginPreferences.Left = "12.7mm"
            myDocument.MarginPreferences.Right = "12.7mm"
            myDocument.MarginPreferences.Top = "12.7mm"
            myDocument.MarginPreferences.Bottom = "12.7mm"
            
            myDocument.DocumentPreferences.FacingPages = False

            myDocument.DocumentPreferences.PagesPerDocument = 1

        except Exception as e:
            print(e)
        try:
            myFile = self.__destination + '\\' + self.__month
            if not os.path.exists(myFile):
                os.makedirs(myFile)
            myFile = myFile + '\\' + filename
            myDocument = myDocument.Save(myFile)
            myDocument.Close()
            logger.info('%s', myFile + ' was generated.')
        except Exception:
            logger.critical("An error occurred while generating indd files.")
            traceback.print_exc()

    def parse_file_properties(self):
        for city in self.__data['cities']:
            for event in city['events']:
                formats = ""
                self.__fileformats.append([])
                for shape in event['format']:
                    self.__fileformats[-1].append(shape)
                    formats += shape + "_"
                self.__filenames.append(
                    str(event['date']).replace(".", "_") + "_" + event['title'].replace(" ", "_") +
                    "_" + formats + city['city'] + ".indd")
        
