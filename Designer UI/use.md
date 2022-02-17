# Use .ui file in Window
```py
    from PyQt5.uic import loadUi
    loadUi('file', self)
```

# Or convert them to python code using
```sh
    pyuic5.exe -o outFile uiFile
```

then add this file to inhert list like:
```py
class WritingWindow(QMainWindow, Ui_WritingWindow):
```
