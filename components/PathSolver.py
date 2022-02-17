import os
from datetime import datetime


class PathSolver():

    # Gets the path of the new created file in default dir
    def getNewFilePath(self):
        defaultPath = os.path.expanduser('~/Documents/DarkTurkeyWriter/')
        
        filePath = os.path.join(defaultPath, self.getCurrentDateTime() + '.txt')
        if not os.path.exists(defaultPath):
            os.makedirs(defaultPath)
            
        return filePath


    def getCurrentDateTime(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M") # dd-mm-YY_H-M