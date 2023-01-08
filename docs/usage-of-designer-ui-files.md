# How to use UI designs into the application
The application UI is developed using Qt designer platform which generate `.ui` files, demonstrate your designs, that you will use next during functionality development phase.

And there are two ways to use those `.ui` files into your code:

### 1. Import them into the code file directly
```py
    from PyQt5.uic import loadUi

    loadUi('designer-ui-file.ui', self)
```

### 2. Inherit them as python class (used-in-project)
1. Convert the `.ui` file to `.py` file using `pyuic5`
```sh
    pyuic5.exe -o ui-python-class.py designer-ui-file.ui
```

2. Add the python class to inheritance list of the widget class:
```py
class WritingWindow(QMainWindow, Ui_WritingWindow):
```
