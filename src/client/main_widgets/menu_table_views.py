from PySide6 import QtWidgets, QtCore, QtGui
from src.server.router import *
from src.client.dialog_forms.table_action_dialog import TableAction
from src.client.api.resolvers import add_action, upd_action, del_action
import settings
import typing
import threading
import time


class MenuTableViews(QtWidgets.QFrame):
    router: RouterManager = None
    dialog: TableAction = None
    add_signal: QtCore.Signal = QtCore.Signal(typing.Any, int, str)
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()
    
    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.table_layout = QtWidgets.QHBoxLayout()
        self.table: QtWidgets.QTableWidget = QtWidgets.QTableWidget()
        self.cancel_button = QtWidgets.QToolButton()
        self.buttons_layout = QtWidgets.QVBoxLayout()
        self.add_button = QtWidgets.QPushButton('Добавить')
        self.update_button = QtWidgets.QPushButton('Обновить')
        self.delete_button = QtWidgets.QPushButton('Удалить')
        self.button_group = QtWidgets.QButtonGroup()

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.addWidget(self.scroll_area)
        self.main_v_layout.addLayout(self.table_layout)

        self.buttons_layout.addWidget(self.add_button, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.buttons_layout.addWidget(self.update_button, 1, QtCore.Qt.AlignmentFlag.AlignTop)
        self.buttons_layout.addWidget(self.delete_button, 5, QtCore.Qt.AlignmentFlag.AlignTop)
        
        self.table_layout.addWidget(self.cancel_button, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.table_layout.addWidget(self.table, 1)
        self.table_layout.addLayout(self.buttons_layout)
        
        self.scroll_area.setWidgetResizable(True)   
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_layout)

        self.scroll_layout.addWidget(MenuTableViews.ModifyButton('clients'))
        self.scroll_layout.addWidget(MenuTableViews.ModifyButton('posts'))
        self.scroll_layout.addWidget(MenuTableViews.ModifyButton('services'))
        self.scroll_layout.addWidget(MenuTableViews.ModifyButton('visits'))
        self.scroll_layout.addWidget(MenuTableViews.ModifyButton('users'))
        self.scroll_layout.addWidget(MenuTableViews.ModifyButton('workers'))

        layout = self.scroll_layout
        for i in range(0, self.scroll_layout.count()):
            item = layout.itemAt(i)
            widget: MenuTableViews.ModifyButton = item.widget()

            if widget:
                if isinstance(widget, MenuTableViews.ModifyButton):
                    widget.setObjectName(widget.text())
                    self.button_group.addButton(widget)
                    for router in routers:
                        if widget.objectName() == router.object_name:
                            widget.set_router(router)
        
        self.switch_state(False)

        self.cancel_button.setFixedSize(22, 22)
        self.cancel_button.setIcon(QtGui.QPixmap(f'{settings.IMG_PATH}/cancel_reversed.png'))
        self.cancel_button.setIconSize(QtCore.QSize(22, 22))

        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.add_button.clicked.connect(self.add_button_clicked)
        self.update_button.clicked.connect(self.upd_button_clicked)
        self.delete_button.clicked.connect(self.del_button_clicked)
        self.button_group.buttonClicked.connect(self.button_clicked)
        self.add_signal.connect(self.add_item_in_table)
    
    def button_clicked(self, button: QtWidgets.QPushButton) -> None:
        self.router = button.router
        self.update_table(self.router)
        self.switch_state(True)
    
    def switch_state(self, switch: bool) -> None:
        self.table.hide() if not switch else self.table.show()
        self.add_button.hide() if not switch else self.add_button.show()
        self.update_button.hide() if not switch else self.update_button.show()
        self.delete_button.hide() if not switch else self.delete_button.show()
        self.cancel_button.hide() if not switch else self.cancel_button.show()
        self.scroll_area.show() if not switch else self.scroll_area.hide()
    
    def change_meta_data_table(self, router) -> None:
        self.table.setColumnCount(len(router.database_model._meta.sorted_field_names))
        self.table.setHorizontalHeaderLabels(router.database_model._meta.sorted_field_names)
        self.table.setRowCount(router.database_model.select().count())
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

    def update_table(self, router) -> None:
        thread = threading.Thread(target=self.fill_table, args=(router,))
        thread.start()
        thread.join()

    def fill_table(self, router) -> None:
        print("Worker is running in thread:", threading.current_thread().name)
        self.change_meta_data_table(router)
        for model in router.database_model.select():
            for j, column in enumerate(router.database_model._meta.sorted_field_names):
                self.add_signal.emit(model, j, column)
                time.sleep(0.05)
    
    @QtCore.Slot(typing.Any, int, str)
    def add_item_in_table(self, model: typing.Any, j: int, column: str) -> None:
        item = QtWidgets.QTableWidgetItem(str(eval(f'model.{column}')))
        self.table.setItem(model.id - 1, j, item)

    def cancel_button_clicked(self) -> None:
        self.router = None
        self.switch_state(False)

    def create_data(self, dialog: TableAction) -> str:
        data = '{'
        layout =  dialog.line_edits_layout

        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            widget: QtWidgets.QLineEdit = item.widget()
            if widget:
                if widget.objectName() == 'id':
                    continue
                data += f'"{widget.objectName()}": "{widget.text()}", ' if not i == layout.count() - 1 else f'"{widget.objectName()}": "{widget.text()}"'
        
        data += '}'

        return data


    def add_button_clicked(self) -> None:
        dialog = TableAction(self, self.router)
        
        data = self.create_data(dialog)

        add_action(self.router.object_name, data)

        self.update_table(self.router)

    def upd_button_clicked(self) -> None:
        if self.table.currentRow() == -1:
            self.parent.show_message(
                    text='Не выбрана запись',
                    error=True,
                    parent=self
                )
            return
    
        row = self.table.currentRow()
        id = self.table.model().index(row, 0).data()

        dialog = TableAction(self, self.router)

        data = self.create_data(dialog)

        upd_action(id, self.router.object_name, data)

        self.update_table(self.router)

    def del_button_clicked(self) -> None:
        if self.table.currentRow() == -1:
            self.parent.show_message(
                    text='Не выбрана запись',
                    error=True,
                    parent=self
                )
            return
        
        row = self.table.currentRow()
        id = self.table.model().index(row, 0).data()

        del_action(id, self.router.object_name)
        
        self.update_table(self.router)

    class ModifyButton(QtWidgets.QPushButton):
        router = None
        def set_router(self, router):
            self.router = router