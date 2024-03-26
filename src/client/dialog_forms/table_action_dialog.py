from PySide6 import QtWidgets, QtCore, QtGui
from src.server.service import RouterManager


class TableAction(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget, router: RouterManager) -> None:
        super().__init__(parent)
        self.parent = parent
        self.router = router
        self.__init_ui()
        self.__setting_ui()
        self.exec_()
    
    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.input_layout = QtWidgets.QHBoxLayout()
        self.labels_layout = QtWidgets.QVBoxLayout()
        self.line_edits_layout = QtWidgets.QVBoxLayout()
        self.confirm_button = QtWidgets.QPushButton('Подтвердить')

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)
        
        self.main_v_layout.addLayout(self.input_layout)

        self.input_layout.addLayout(self.labels_layout)
        self.input_layout.addLayout(self.line_edits_layout)

        for column in self.router.database_model._meta.sorted_field_names:
            if column == 'id':
                continue
            self.labels_layout.addWidget(QtWidgets.QLabel(column))
            line_edit = QtWidgets.QLineEdit()
            line_edit.setObjectName(column)
            self.line_edits_layout.addWidget(line_edit)

        self.main_v_layout.addWidget(self.confirm_button, 0, QtCore.Qt.AlignmentFlag.AlignRight)

        self.confirm_button.clicked.connect(self.confirm_button_clicked)

    def validate_line_edits(self) -> bool:
        layout = self.line_edits_layout
        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            widget: QtWidgets.QLineEdit = item.widget()

            if widget:
                if widget.text() == '':
                    return False
            
        return True

    def confirm_button_clicked(self) -> None:
        if not self.validate_line_edits():
            self.parent.parent.show_message(
                text='Одно или несколько полей пустые',
                error=True
            )
            return
        self.hide()