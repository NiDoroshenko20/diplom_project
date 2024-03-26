from PySide6 import QtWidgets, QtCore, QtGui
from src.client.dialog_forms.login_form import LoginForm
from src.client.dialog_forms.register_form import RegisterForm



class AuthorizationMenu(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(AuthorizationMenu, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()
    
    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.login_button = QtWidgets.QPushButton(text='Login')
        self.register_button = QtWidgets.QPushButton(text='Register')
    
    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)

        self.main_h_layout.addWidget(self.login_button)
        self.main_h_layout.addWidget(self.register_button)

        self.main_h_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        self.login_button.clicked.connect(self.on_login_button_click)
        self.register_button.clicked.connect(self.on_register_button_click)

    def open_login_dialog(self) -> None:
        LoginForm(self.parent)
    
    def open_register_dialog(self) -> None:
        RegisterForm(self.parent)

    def on_login_button_click(self) -> None:
        self.open_login_dialog()

    def on_register_button_click(self) -> None:
        self.open_register_dialog()