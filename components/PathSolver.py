import os
from datetime import datetime
import ctypes.wintypes


class PathSolver():

    # Gets the path of the new created file in default dir
    def getNewFilePath(self):
        try:
            defaultPath = os.path.expanduser('~/My Documents/KEYBOARDCOWBOY/')
            filePath = os.path.join(defaultPath, self.getCurrentDateTime() + '.txt')

            with open(filePath, 'w') as f:
                f.write('\n')
                
        except:
            CSIDL_PERSONAL = 5       # My Documents
            SHGFP_TYPE_CURRENT = 0   # Get current, not default value

            buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

            filePath = os.path.join(buf.value, self.getCurrentDateTime() + '.txt')

            with open(filePath, 'w') as f:
                f.write('\n')
        
        if not os.path.exists(defaultPath):
            os.makedirs(defaultPath)
            
        return filePath


    def getCurrentDateTime(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M") # dd-mm-YY_H-M