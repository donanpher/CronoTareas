# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_CronoTareas.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(788, 487)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/miprefijo/images/cronotareas.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.labelCronoTareas = QtWidgets.QLabel(self.centralwidget)
        self.labelCronoTareas.setGeometry(QtCore.QRect(87, 17, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.labelCronoTareas.setFont(font)
        self.labelCronoTareas.setObjectName("labelCronoTareas")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(92, 43, 670, 3))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(721, 43, 40, 17))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        font.setPointSize(7)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.labelCronoTareas_2 = QtWidgets.QLabel(self.centralwidget)
        self.labelCronoTareas_2.setGeometry(QtCore.QRect(105, 41, 530, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCronoTareas_2.sizePolicy().hasHeightForWidth())
        self.labelCronoTareas_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelCronoTareas_2.setFont(font)
        self.labelCronoTareas_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelCronoTareas_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.labelCronoTareas_2.setScaledContents(False)
        self.labelCronoTareas_2.setWordWrap(True)
        self.labelCronoTareas_2.setObjectName("labelCronoTareas_2")
        self.tabWidgetTareas = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidgetTareas.setGeometry(QtCore.QRect(20, 90, 740, 370))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        self.tabWidgetTareas.setFont(font)
        self.tabWidgetTareas.setStyleSheet("")
        self.tabWidgetTareas.setObjectName("tabWidgetTareas")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.labelCronoTareas_3 = QtWidgets.QLabel(self.tab_1)
        self.labelCronoTareas_3.setGeometry(QtCore.QRect(12, 2, 601, 20))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelCronoTareas_3.setFont(font)
        self.labelCronoTareas_3.setObjectName("labelCronoTareas_3")
        self.pushButtonAgregarTarea = QtWidgets.QPushButton(self.tab_1)
        self.pushButtonAgregarTarea.setGeometry(QtCore.QRect(47, 298, 100, 29))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        self.pushButtonAgregarTarea.setFont(font)
        self.pushButtonAgregarTarea.setStyleSheet("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/miprefijo/images/agregar.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonAgregarTarea.setIcon(icon1)
        self.pushButtonAgregarTarea.setObjectName("pushButtonAgregarTarea")
        self.pushButtonModificarTarea = QtWidgets.QPushButton(self.tab_1)
        self.pushButtonModificarTarea.setGeometry(QtCore.QRect(152, 298, 100, 29))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        self.pushButtonModificarTarea.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/miprefijo/images/modificar.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonModificarTarea.setIcon(icon2)
        self.pushButtonModificarTarea.setObjectName("pushButtonModificarTarea")
        self.pushButtonEliminarTarea = QtWidgets.QPushButton(self.tab_1)
        self.pushButtonEliminarTarea.setGeometry(QtCore.QRect(256, 298, 100, 29))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        self.pushButtonEliminarTarea.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/miprefijo/images/eliminar.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonEliminarTarea.setIcon(icon3)
        self.pushButtonEliminarTarea.setObjectName("pushButtonEliminarTarea")
        self.listWidgetTareas = QtWidgets.QListWidget(self.tab_1)
        self.listWidgetTareas.setGeometry(QtCore.QRect(12, 42, 710, 230))
        self.listWidgetTareas.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidgetTareas.setMidLineWidth(1)
        self.listWidgetTareas.setAlternatingRowColors(True)
        self.listWidgetTareas.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listWidgetTareas.setObjectName("listWidgetTareas")
        self.checkBoxMultiCrono = QtWidgets.QCheckBox(self.tab_1)
        self.checkBoxMultiCrono.setGeometry(QtCore.QRect(470, 302, 250, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBoxMultiCrono.setFont(font)
        self.checkBoxMultiCrono.setChecked(False)
        self.checkBoxMultiCrono.setObjectName("checkBoxMultiCrono")
        self.labelCronoTareas_4 = QtWidgets.QLabel(self.tab_1)
        self.labelCronoTareas_4.setGeometry(QtCore.QRect(22, 24, 20, 20))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.labelCronoTareas_4.setFont(font)
        self.labelCronoTareas_4.setObjectName("labelCronoTareas_4")
        self.labelCronoTareas_5 = QtWidgets.QLabel(self.tab_1)
        self.labelCronoTareas_5.setGeometry(QtCore.QRect(59, 24, 50, 20))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.labelCronoTareas_5.setFont(font)
        self.labelCronoTareas_5.setObjectName("labelCronoTareas_5")
        self.labelCronoTareas_6 = QtWidgets.QLabel(self.tab_1)
        self.labelCronoTareas_6.setGeometry(QtCore.QRect(265, 24, 50, 20))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.labelCronoTareas_6.setFont(font)
        self.labelCronoTareas_6.setObjectName("labelCronoTareas_6")
        self.pushButtonRecargar = QtWidgets.QPushButton(self.tab_1)
        self.pushButtonRecargar.setGeometry(QtCore.QRect(11, 298, 30, 29))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        self.pushButtonRecargar.setFont(font)
        self.pushButtonRecargar.setStyleSheet("")
        self.pushButtonRecargar.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/miprefijo/images/recargar.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonRecargar.setIcon(icon4)
        self.pushButtonRecargar.setObjectName("pushButtonRecargar")
        self.labelTotalTareas = QtWidgets.QLabel(self.tab_1)
        self.labelTotalTareas.setGeometry(QtCore.QRect(12, 273, 250, 20))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelTotalTareas.setFont(font)
        self.labelTotalTareas.setObjectName("labelTotalTareas")
        self.labelCronoTareas_7 = QtWidgets.QLabel(self.tab_1)
        self.labelCronoTareas_7.setGeometry(QtCore.QRect(546, 24, 50, 20))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.labelCronoTareas_7.setFont(font)
        self.labelCronoTareas_7.setObjectName("labelCronoTareas_7")
        self.pushButtonBuscar = QtWidgets.QPushButton(self.tab_1)
        self.pushButtonBuscar.setGeometry(QtCore.QRect(362, 298, 100, 29))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        self.pushButtonBuscar.setFont(font)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/miprefijo/images/buscar.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonBuscar.setIcon(icon5)
        self.pushButtonBuscar.setObjectName("pushButtonBuscar")
        self.labelSumaCronos = QtWidgets.QLabel(self.tab_1)
        self.labelSumaCronos.setGeometry(QtCore.QRect(445, 273, 250, 20))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelSumaCronos.setFont(font)
        self.labelSumaCronos.setText("")
        self.labelSumaCronos.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelSumaCronos.setObjectName("labelSumaCronos")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/miprefijo/images/tareas2.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidgetTareas.addTab(self.tab_1, icon6, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.comboBoxInformes = QtWidgets.QComboBox(self.tab_2)
        self.comboBoxInformes.setGeometry(QtCore.QRect(150, 10, 281, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBoxInformes.setFont(font)
        self.comboBoxInformes.setObjectName("comboBoxInformes")
        self.comboBoxInformes.addItem("")
        self.comboBoxInformes.addItem("")
        self.comboBoxInformes.addItem("")
        self.comboBoxInformes.addItem("")
        self.tableWidgetInformes = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidgetInformes.setGeometry(QtCore.QRect(14, 38, 710, 290))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableWidgetInformes.setFont(font)
        self.tableWidgetInformes.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidgetInformes.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidgetInformes.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableWidgetInformes.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidgetInformes.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidgetInformes.setObjectName("tableWidgetInformes")
        self.tableWidgetInformes.setColumnCount(4)
        self.tableWidgetInformes.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetInformes.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetInformes.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetInformes.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetInformes.setHorizontalHeaderItem(3, item)
        self.labelTotalTareas_2 = QtWidgets.QLabel(self.tab_2)
        self.labelTotalTareas_2.setGeometry(QtCore.QRect(18, 10, 140, 20))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelTotalTareas_2.setFont(font)
        self.labelTotalTareas_2.setObjectName("labelTotalTareas_2")
        self.pushButtonExportar = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonExportar.setGeometry(QtCore.QRect(626, 4, 100, 29))
        font = QtGui.QFont()
        font.setFamily("Gallaecia Castelo")
        font.setPointSize(10)
        self.pushButtonExportar.setFont(font)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/miprefijo/images/exportar.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonExportar.setIcon(icon7)
        self.pushButtonExportar.setObjectName("pushButtonExportar")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/miprefijo/images/informes2.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidgetTareas.addTab(self.tab_2, icon8, "")
        self.labelIcono = QtWidgets.QLabel(self.centralwidget)
        self.labelIcono.setGeometry(QtCore.QRect(16, 8, 60, 60))
        self.labelIcono.setStyleSheet("border-image: url(:/miprefijo/images/cronotareas.png);")
        self.labelIcono.setText("")
        self.labelIcono.setObjectName("labelIcono")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidgetTareas.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidgetTareas, self.pushButtonAgregarTarea)
        MainWindow.setTabOrder(self.pushButtonAgregarTarea, self.pushButtonModificarTarea)
        MainWindow.setTabOrder(self.pushButtonModificarTarea, self.pushButtonEliminarTarea)
        MainWindow.setTabOrder(self.pushButtonEliminarTarea, self.pushButtonBuscar)
        MainWindow.setTabOrder(self.pushButtonBuscar, self.pushButtonRecargar)
        MainWindow.setTabOrder(self.pushButtonRecargar, self.listWidgetTareas)
        MainWindow.setTabOrder(self.listWidgetTareas, self.checkBoxMultiCrono)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Crono Tareas"))
        self.labelCronoTareas.setText(_translate("MainWindow", "Crono Tareas"))
        self.label.setText(_translate("MainWindow", "v.1.9"))
        self.labelCronoTareas_2.setText(_translate("MainWindow", "Cronometra la duración de tus Tareas y genera informes resumen de las mismas"))
        self.labelCronoTareas_3.setText(_translate("MainWindow", "Añade nuevas tareas, selecciona una fila para modificar o eliminar"))
        self.pushButtonAgregarTarea.setText(_translate("MainWindow", "&Añadir"))
        self.pushButtonModificarTarea.setText(_translate("MainWindow", "&Modificar"))
        self.pushButtonEliminarTarea.setText(_translate("MainWindow", "&Eliminar"))
        self.checkBoxMultiCrono.setText(_translate("MainWindow", "Permitir varios cronos simultaneos"))
        self.labelCronoTareas_4.setText(_translate("MainWindow", "ID"))
        self.labelCronoTareas_5.setText(_translate("MainWindow", "Tarea"))
        self.labelCronoTareas_6.setText(_translate("MainWindow", "Tag"))
        self.pushButtonRecargar.setToolTip(_translate("MainWindow", "Recargar lista de Tareas"))
        self.labelTotalTareas.setText(_translate("MainWindow", "Total Tareas: "))
        self.labelCronoTareas_7.setText(_translate("MainWindow", "Crono"))
        self.pushButtonBuscar.setText(_translate("MainWindow", "&Buscar"))
        self.tabWidgetTareas.setTabText(self.tabWidgetTareas.indexOf(self.tab_1), _translate("MainWindow", "&Tareas"))
        self.comboBoxInformes.setCurrentText(_translate("MainWindow", "--- Selecciona un informe ---"))
        self.comboBoxInformes.setItemText(0, _translate("MainWindow", "--- Selecciona un informe ---"))
        self.comboBoxInformes.setItemText(1, _translate("MainWindow", "01 Detalle de Tareas por Tag"))
        self.comboBoxInformes.setItemText(2, _translate("MainWindow", "02 Detalle de Tags por Tarea"))
        self.comboBoxInformes.setItemText(3, _translate("MainWindow", "03 Todas las Tareas (por Fecha inicio)"))
        item = self.tableWidgetInformes.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Tag"))
        item = self.tableWidgetInformes.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Tarea"))
        item = self.tableWidgetInformes.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Inicio"))
        item = self.tableWidgetInformes.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Fin"))
        self.labelTotalTareas_2.setText(_translate("MainWindow", "Selecciona informe:"))
        self.pushButtonExportar.setText(_translate("MainWindow", "E&xportar"))
        self.tabWidgetTareas.setTabText(self.tabWidgetTareas.indexOf(self.tab_2), _translate("MainWindow", "&Informes"))

import mirecurso_rc
