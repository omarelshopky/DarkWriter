import os
from datetime import datetime
import ctypes.wintypes

class PathSolver():

    # Gets the path of the new created file in default dir
    def getNewFilePath(self):
        try:
            try:
                defaultPath = os.path.expanduser('~/My Documents/KEYBOARDCOWBOY/')

                # print(defaultPath)

                if not os.path.exists(defaultPath):
                    os.makedirs(defaultPath)
                
                filePath = os.path.join(defaultPath, self.getCurrentDateTime() + '.txt')
                    
            except Exception as e:
                print(str(e))

                CSIDL_PERSONAL = 5       # My Documents
                SHGFP_TYPE_CURRENT = 0   # Get current, not default value

                buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

                defaultPath = buf.value + '\KEYBOARDCOWBOY'

                if not os.path.exists(defaultPath):
                    os.mkdir(defaultPath, 0o777)

                filePath = os.path.join(defaultPath, self.getCurrentDateTime() + '.txt')

        except Exception as e:
            print(str(e))
        
        return filePath


    def getCurrentDateTime(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M") # dd-mm-YY_H-M

