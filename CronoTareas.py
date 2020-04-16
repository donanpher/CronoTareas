#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  CronoTareas, v.1.3
#  Sencilla aplicación para cronometrar tiempos asociados a tareas.
#  Creada usando Python 3.6.7 + PyQt5
#  
#  Copyright April, 2020 Fer <donanpher@gmail.com>
#  (durante la cuarentena del #Coronavirus #SARS-CoV-2 #Covid-19)
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  

import sqlite3, sys, os
from sqlite3 import Error
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QListWidget, QLabel, QPushButton, QListWidgetItem, \
    QHBoxLayout, QLCDNumber, QMessageBox, QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit, QFrame, QDesktopWidget
from PyQt5 import QtCore
from PyQt5 import QtGui
from ui_CronoTareas import *
BaseDeDatos = "CronoTareas.db"

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(676, 487)
        self.center() # este método es para centrar la ventana en la pantalla
        # si no existe la BD en el directorio de la app., la creamos e insertamos un registro de muestra
        if not os.path.isfile(BaseDeDatos):
            self.CrearDB()
            self.mensajeBarraDeEstado = "No se encontró Base de Datos, creada una nueva!"
        else:
            self.mensajeBarraDeEstado = "Base de Datos cargada"
        #self.ui.statusbar.showMessage(self.mensajeBarraDeEstado, 5000)
        self.miFont = QtGui.QFont()
        self.miFont.setFamily("Gallaecia Castelo")
        self.miFont.setPointSize(10)
        #self.miFont.setBold(True)
        self.ui.statusbar.setFont(self.miFont)
        
        # esta variable depende de widget checkBoxMultiCrono y se usa para permitir o no la simultaneidad de los cronos
        # normalmente sería lógico que sólo un crono funcione a la vez, pero por si se quiere que no, se da la opción.
        self.PermitirCronosSimultaneos = self.ui.checkBoxMultiCrono.isChecked()
        self.ui.statusbar.showMessage("Modo: Mono Crono")
        # conexión de los botones con sus respectivos slots
        self.ui.pushButtonAgregarTarea.clicked.connect(self.AgregarTarea)
        self.ui.pushButtonEliminarTarea.clicked.connect(self.EliminarTarea)
        #self.ui.pushButtonEliminarTarea.clicked.connect(self.GuardarEstadoTareas) # PROVISIONAL
        self.ui.pushButtonModificarTarea.clicked.connect(self.ModificarTarea)
        self.ui.pushButtonRecargar.clicked.connect(self.Recargar)
        self.ui.listWidgetTareas.itemDoubleClicked.connect(self.ModificarTarea)
        self.ui.checkBoxMultiCrono.stateChanged.connect(self.CronosSimultaneos)

        # Inicialización de la lista de tareas
        self.MostrarTabla("SELECT * FROM Tareas ORDER BY FechaAlta DESC, IDTarea DESC;")
        self.ui.labelTotalTareas.setText("Total Tareas: " + str(self.ui.listWidgetTareas.count()))

    def CronosSimultaneos(self):
        self.PermitirCronosSimultaneos = not self.PermitirCronosSimultaneos
        if self.PermitirCronosSimultaneos:
            self.ui.statusbar.showMessage("Modo: Multi Crono")
        else:
            self.ui.statusbar.showMessage("Modo: Mono Crono")

    def AgregarTarea(self):
        #QMessageBox.about(self, "Información", "Agregando Tarea")
        dlg = CustomDialog(self)
        if dlg.exec_():
            #self.AnhadirItem("999", dlg.miLineEditTareaDialog.text(), dlg.miLineEditTagDialog.text())
            try:
                # esta es la fecha y hora del momento actual para guardarla en la BD. al dar un alta
                self.Ahora = datetime.now()
                self.strAhora = datetime.strftime(self.Ahora, "%Y-%m-%d %H:%M:%S")
                # modificamos en la BD.
                conn = sqlite3.connect(BaseDeDatos)
                cur = conn.cursor()
                modifTarea = dlg.miLineEditTareaDialog.text()
                modifTag = dlg.miLineEditTagDialog.text()
                miQuery = "INSERT INTO Tareas (NombreTarea, Tag, FechaAlta, Crono) \
                            VALUES ('" + modifTarea + "', '" + modifTag + "', '" + self.strAhora + "', '00:00:00')"
                cur.execute(miQuery)
                conn.commit()
                # ahora borramos todo el contenido del listWidget para volver a cargarlo con los datos actualizados
                self.ui.listWidgetTareas.clear()
                self.MostrarTabla("SELECT * FROM Tareas ORDER BY FechaAlta DESC, IDTarea DESC;")
                self.ui.statusbar.showMessage("Se ha añadido una nueva Tarea", 5000)
            except Error as e:
                self.ui.statusbar.showMessage(str(e), 10000)
            finally:
                conn.close()
        else:
            self.ui.statusbar.showMessage("Añadir Tarea nueva cancelado", 5000)
            
    def ModificarTarea(self):
        filaModificar = self.ui.listWidgetTareas.currentRow()

        if filaModificar == -1:
            self.ui.statusbar.showMessage("Selecciona la fila que quieres modificar.", 5000)
            QMessageBox.about(self, "Información", "Selecciona la fila que quieres modificar.")
        else:
            ItemModificar = self.ui.listWidgetTareas.currentItem()
            miWidget = self.ui.listWidgetTareas.itemWidget(ItemModificar)
            # estos son los datos de la fila seleccionada actualmente
            elID = miWidget.IDTarea.text()
            laTarea = miWidget.NombreTarea.text()
            elTag = miWidget.Tag.text()
            # llamamos al diálogo para captar los datos con la modificación
            dlg = CustomDialog(self)
            dlg.miLineEditTareaDialog.setText(laTarea)
            dlg.miLineEditTagDialog.setText(elTag)
            if dlg.exec_():
                modifTarea = dlg.miLineEditTareaDialog.text()
                modifTag = dlg.miLineEditTagDialog.text()
                try:
                    # modificamos en la BD.
                    conn = sqlite3.connect(BaseDeDatos)
                    cur = conn.cursor()
                    miQuery = "UPDATE Tareas SET NombreTarea = '" + modifTarea + "', Tag = '" + modifTag + "' WHERE IDTarea = " + elID
                    cur.execute(miQuery)
                    conn.commit()
                    # ahora borramos todo el contenido del listWidget para volver a cargarlo con los datos actualizados
                    self.ui.listWidgetTareas.clear()
                    self.MostrarTabla("SELECT * FROM Tareas ORDER BY FechaAlta DESC, IDTarea DESC;")
                    self.ui.statusbar.showMessage("Tarea modificada", 5000)
                except Error as e:
                    self.ui.statusbar.showMessage(str(e), 10000)
                finally:
                    conn.close()
            else:
                self.ui.statusbar.showMessage("Modificar Tarea Cancelado", 5000)
                #print("Ha pulsado Cancel!")
    
    def EliminarTarea(self):
        filaModificar = self.ui.listWidgetTareas.currentRow()

        if filaModificar == -1:
            self.ui.statusbar.showMessage("Selecciona la fila que quieres eliminar.", 5000)
            QMessageBox.about(self, "Información", "Selecciona la fila que quieres eliminar.")
        else:
            ItemModificar = self.ui.listWidgetTareas.currentItem()
            miWidget = self.ui.listWidgetTareas.itemWidget(ItemModificar)
            # estos son los datos de la fila seleccionada actualmente
            elID = miWidget.IDTarea.text()
            laTarea = miWidget.NombreTarea.text()
            elTag = miWidget.Tag.text()
            laNota = "IDTarea: " + elID + "\nTarea: " + laTarea + "\nTag: " + elTag
            # llamamos a un diálogo de Aceptar/Cancelar para confirmar eliminación
            buttonReply = QMessageBox.question(self, 'Eliminar Tarea', "¿Quieres eliminar esta Tarea?:\n" + laNota, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                try:
                    conn = sqlite3.connect(BaseDeDatos)
                    cur = conn.cursor()
                    miQuery = "DELETE FROM Tareas WHERE IDTarea = " + elID
                    cur.execute(miQuery)
                    conn.commit()
                    # ahora borramos todo el contenido del listWidget para volver a cargarlo con los datos actualizados
                    self.ui.listWidgetTareas.clear()
                    self.MostrarTabla("SELECT * FROM Tareas ORDER BY FechaAlta DESC, IDTarea DESC;")
                    self.ui.statusbar.showMessage("Tarea eliminada", 5000)
                except Error as e:
                    self.ui.statusbar.showMessage(str(e), 10000)
                finally:
                    conn.close()
            else:
                self.ui.statusbar.showMessage("Eliminar Tarea Cancelado", 5000)

    def GuardarEstadoTareas(self):
        # Cada vez que se hace un alta/modificación/eliminación, se hace un .clear (se vacía el listWidget) y se vuelve a cargar desde la BD.
        # Si hay cronos activos, al hacer lo anterior, se pierde la información del crono actual
        # Por todo lo anterior, hay que guardar el estado actual de todos los cronos antes de recargar la lista.
        totalFilas = self.ui.listWidgetTareas.count()
        # for elemento in range(totalFilas):
        #     jaja = self.ui.listWidgetTareas.item(elemento)
        print("a ver")
            #print(jaja.IDTarea.text())
        self.ui.listWidgetTareas.itemWidget.setCurrentRow(2)
            # ItemModificar = self.ui.listWidgetTareas.currentItem()
            # miWidget = self.ui.listWidgetTareas.itemWidget(ItemModificar)
            # elID = miWidget.IDTarea.text()
            # laTarea = miWidget.NombreTarea.text()
            # elTag = miWidget.Tag.text()
            # print(elID, laTarea)

        # ItemModificar = self.ui.listWidgetTareas.currentItem()
        # miWidget = self.ui.listWidgetTareas.itemWidget(ItemModificar)
        # # estos son los datos de la fila seleccionada actualmente
        # elID = miWidget.IDTarea.text()
        # laTarea = miWidget.NombreTarea.text()
        # elTag = miWidget.Tag.text()

    def AnhadirItem(self, nuevoID, nuevaTarea, nuevoTag, nuevoCrono):
        # Un Item es cada fila de la lista de tareas
        # Este método es llamado por el método MostrarTabla, para ir añadiendo todos los reg. de la BD.
        self.nuevoID = nuevoID
        self.nuevaTarea = nuevaTarea
        self.nuevoTag = nuevoTag
        self.nuevoCrono = nuevoCrono
        miItem = QListWidgetItem()
        miCustomWidget = MiTimer(self.nuevoID, self.nuevaTarea, self.nuevoTag, self.nuevoCrono)
        miItem.setSizeHint(miCustomWidget.sizeHint())
        self.ui.listWidgetTareas.addItem(miItem) # añade el item al final de la lista
        #self.ui.listWidgetTareas.insertItem(0, miItem) # inserta el item en primer lugar de la lista
        self.ui.listWidgetTareas.setItemWidget(miItem, miCustomWidget)
        self.ui.listWidgetTareas.setStyleSheet( "QListWidget::item { border-bottom: 1px solid black; }" ) # esta es una línea que separa líneas
        self.show()

    def MostrarTabla(self, miQuery):
        # Carga en la lista de tareas todos los registros de la BD.
        try:
            conn = sqlite3.connect(BaseDeDatos)
            cur = conn.cursor()
            cur.execute(miQuery)
            registros = cur.fetchall()
            totalReg = len(registros) # total de registros de la query
            #elf.ui.tableWidgetNotas.setRowCount(totalReg) # dimensionamos el widget en filas
            recNum = 0
            for registro in registros:
                self.AnhadirItem(str(registro[0]), registro[1], registro[2], registro[4]) # estos son los campos
                recNum += 1

        except Error as e:
            self.ui.statusbar.showMessage(str(e), 10000)
        finally:
            conn.close()
    
    def Recargar(self):
        # Vacía y vuelve a cargar la lista de tareas a partir de la BD.
        self.ui.listWidgetTareas.clear()
        self.MostrarTabla("SELECT * FROM Tareas ORDER BY FechaAlta DESC, IDTarea DESC;")
    
    def center(self):
        # Para centrar la ventana en el escritorio
        # geometry of the main window
        qr = self.frameGeometry()
        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def CrearDB(self):
        # Si no existe la BD en el directorio activo, la creamos e insertamos un registro de muestra
        try:
            conn = sqlite3.connect(BaseDeDatos)
            cur = conn.cursor()
            # Creamos la tabla Tareas
            laQuery = "CREATE TABLE Tareas ( \
                        IDTarea     INTEGER   PRIMARY KEY AUTOINCREMENT \
                                            UNIQUE \
                                            NOT NULL, \
                        NombreTarea TEXT (30), \
                        Tag         TEXT (20), \
                        FechaAlta   TEXT (20),  \
                        Crono       TEXT (20)  \
                    );"
            cur.execute(laQuery)
            conn.commit()
            # Creamos la tabla DetalleTareas
            laQuery = "CREATE TABLE DetalleTareas ( \
                        IDDetalle       INTEGER   PRIMARY KEY AUTOINCREMENT \
                                                UNIQUE \
                                                NOT NULL, \
                        IDTarea         INTEGER   REFERENCES Tareas (IDTarea)  \
                                                NOT NULL, \
                        FechaHoraInicio TEXT (20), \
                        FechaHoraFina   TEXT (20)  \
                    );"
            cur.execute(laQuery)
            conn.commit()
            # Insertamos un registro inicial en ambas tablas
            laQuery = "INSERT INTO Tareas ( \
                       NombreTarea, \
                       Tag, \
                       FechaAlta, \
                       Crono \
                        ) \
                        VALUES ( \
                            'Tarea 1', \
                            'Test Tareas', \
                            '2020-04-12 12:16:08', \
                            '00:00:00' \
                        );"
            cur.execute(laQuery)
            conn.commit()
            laQuery = "INSERT INTO DetalleTareas ( \
                              IDTarea, \
                              FechaHoraInicio, \
                              FechaHoraFina \
                          ) \
                          VALUES ( \
                              1, \
                              '2020-04-12 12:18:25', \
                              '2020-04-12 13:16:08' \
                          );"
            cur.execute(laQuery)
            conn.commit()
            conn.close()
        except ValueError as e:
            print(str(e))

class CustomDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("Añadir Tarea")
        self.miEtiqueta = QLabel("Nombre de la Tarea")
        self.miLineEditTareaDialog = QLineEdit("")
        self.miEtiqueta2 = QLabel("Tag de la Tarea")
        self.miLineEditTagDialog = QLineEdit("")
        
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.miEtiqueta)
        self.layout.addWidget(self.miLineEditTareaDialog)
        self.layout.addWidget(self.miEtiqueta2)
        self.layout.addWidget(self.miLineEditTagDialog)

        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

class MiTimer(QWidget):
    hayUnCronoActivo = False # para controlar si hay activo algún crono y poder permitir un segundo o no en función del checkbox
    # mismo tema anterior pero para solucionar el tema de que estando desmarcado el check (permitir varios cronos),
    # si se marca el check de no permitir, se descontrola el tema
    # lo que trato de hacer ahora es que, si se permiten varios cronos + se inicia más de un crono, entonces deshabilito el check.
    numCronosActivos = 0 

    # esta es la linea (WidgetItem), con la colección de widgets (dentro de un QHBoxLayout), que se pinta dentro de la lista.
    def __init__(self, miID, miTarea, miTag, miCrono, parent=None):
        super(MiTimer, self).__init__(parent)
        self.miID = miID
        self.miTarea = miTarea
        self.miTag = miTag
        self.miCrono = miCrono
        self.altoWidgets = 25
        self.anchoBotones = 75
        # self.tiempoActual = QtCore.QTime(0,0,0)
        self.tiempoActual2Ini = datetime.now()
        self.tiempoActual2Fin = datetime.now()
        self.segundosAcumulado = 0.0 # cuando se hace una pausa, hay que guardar aqui el tiempo transcurrido hasta ese momento para sumarselo después a la reanudación.
        #self.tiempoFinal = QTime(0,0,0)
        self.timer = QtCore.QTimer(self)
        self.IDTarea = QLabel(self.miID)
        self.IDTarea.setFrameShape(QFrame.StyledPanel)
        self.IDTarea.setFixedWidth(30)
        self.NombreTarea = QLabel(self.miTarea)
        self.NombreTarea.setFrameShape(QFrame.StyledPanel)
        # self.NombreTarea.setFrameShadow(QFrame.Sunken)
        # self.NombreTarea.setLineWidth(3)
        # self.NombreTarea.setFixedHeight(altoWidgets)
        # self.Tag.setFixedHeight(altoWidgets)
        self.Tag = QLabel(self.miTag)
        self.Tag.setFrameShape(QFrame.StyledPanel)
        self.Tag.setFixedWidth(self.anchoBotones + 20)
        self.botonIniciar= QPushButton("Start")
        self.botonIniciar.setFixedWidth(self.anchoBotones + 15)
        self.icon1 = QtGui.QIcon()
        self.icon1.addPixmap(QtGui.QPixmap(":/miprefijo/images/play.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.botonIniciar.setIcon(self.icon1)        
        self.botonIniciar.clicked.connect(self.IniciarCrono)
        #t = Thread(target=self.IniciarCrono)
        #t.start()
        self.botonParar= QPushButton("Reset")
        self.icon2 = QtGui.QIcon()
        self.icon2.addPixmap(QtGui.QPixmap(":/miprefijo/images/refresh.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.botonParar.setIcon(self.icon2)        
        self.botonParar.setFixedWidth(self.anchoBotones)
        self.botonParar.clicked.connect(self.PararCrono)
        self.botonParar.setEnabled(False)
        self.botonParar.setToolTip('<b>Resetea</b> el Crono y también pregunta si se desea <br><b>Guardar su estado</b>.')
        # self.miDisplay = QLCDNumber()
        # self.miDisplay.setDigitCount(8)
        # self.miDisplay.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        # self.miDisplay.setFixedWidth(self.anchoBotones + 30)
        # self.miDisplay.setFixedHeight(30)
        # self.font = QtGui.QFont()
        # self.font.setBold(True)
        # self.miDisplay.setFont(self.font)
        ###########################################################################################################################
        self.miSegundoDisplay = QLCDNumber()
        self.miSegundoDisplay.setDigitCount(12)
        self.miSegundoDisplay.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.miSegundoDisplay.setFixedWidth(self.anchoBotones + 80)
        self.miSegundoDisplay.setFixedHeight(30)
        self.miSegundoDisplay.display(self.miCrono)
        ###########################################################################################################################
        #self.showlcd()
        self.timer.timeout.connect(self.showlcd) # método que se ejecuta con cada Timer
        self.miLayOut = QHBoxLayout()
        self.miLayOut.addWidget(self.IDTarea)
        self.miLayOut.addWidget(self.NombreTarea)
        self.miLayOut.addWidget(self.Tag)
        self.miLayOut.addWidget(self.botonIniciar)
        self.miLayOut.addWidget(self.botonParar)
        # self.miLayOut.addWidget(self.miDisplay)
        self.miLayOut.addWidget(self.miSegundoDisplay)
        self.setLayout(self.miLayOut)

    def IniciarCrono(self):
        # La idea de todo esto es que si se está en modo monocrono, sólo se pueda tener activo uno, los que están en pausa no están activos.
        # En el modo multicrono, se permite que estén activos todos los cronos que se quieran.
        # Lo que no se puede dar es que, si se está en modo multicrono y con varios cronos activos, se pueda pasar al modo monocrono.
        # Condición:
        # Si se permiten varios cronos simultáneos, o si no se permiten pero que sólo haya uno activo o que el pulsado sea de Pausa o Continuar
        # (sólo esta condición me llevó unas cuantas horas/sesiones elaborarla)
        if (w.PermitirCronosSimultaneos) or (
            (not w.PermitirCronosSimultaneos) and (
                (not MiTimer.hayUnCronoActivo) or (self.botonIniciar.text() == "Pause") or (self.botonIniciar.text() == "Continuar")
                )
            ):
            # en qué modo se pincha el botón iniciar? (Start|Pause|Continue)
            if self.botonIniciar.text() == "Start":
                self.timer.start(1000) # pongo en marcha el Timer
                #self.tiempoActual2Ini = datetime.now() - timedelta(days=2) # le resto 2 días
                self.tiempoActual2Ini = datetime.now()
                self.tiempoActual2Fin = datetime.now()
                # Si se ha restaurado un cronómetro de una vez anterior
                if self.miCrono != "00:00:00":
                    # hay que convertir la cadena horaria a segundos
                    sumar = self.ConvertirCadena_a_Segundos(self.miCrono)
                    self.segundosAcumulado = float(sumar)
                else:
                    self.segundosAcumulado = 0
                MiTimer.hayUnCronoActivo = True
                MiTimer.numCronosActivos += 1
                # self.miDisplay.setStyleSheet("QLCDNumber {color: red;}")
                self.miSegundoDisplay.setStyleSheet("QLCDNumber {color: red;}")
                self.icon3 = QtGui.QIcon()
                self.icon3.addPixmap(QtGui.QPixmap(":/miprefijo/images/pause.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.botonIniciar.setText("Pause")
                self.botonIniciar.setIcon(self.icon3)    
                self.botonParar.setEnabled(False) # deshabilitamos el botón Reset    
                # print("CRONOS ACTIVOS: ", str(MiTimer.numCronosActivos)), 
                # print("")
            elif self.botonIniciar.text() =="Pause":
                self.timer.stop() # detengo el timer
                MiTimer.hayUnCronoActivo = False
                self.icon4 = QtGui.QIcon()
                self.icon4.addPixmap(QtGui.QPixmap(":/miprefijo/images/continue.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.botonIniciar.setText("Continue")
                self.botonIniciar.setIcon(self.icon4)        
                # self.miDisplay.setStyleSheet("QLCDNumber {color: green;}")
                self.miSegundoDisplay.setStyleSheet("QLCDNumber {color: green;}")
                # al hacer una pausa, hay que guardar los segundos transcurridos hasta este momento para añadirselos al reanudar el crono
                self.tiempoActual2Fin = datetime.now() ##################
                self.segundosAcumulado += (self.tiempoActual2Fin - self.tiempoActual2Ini).seconds ####################
                self.botonParar.setEnabled(True) # deshabilitamos el botón Reset  
                # print("ini: ", str(self.tiempoActual2Ini))
                # print("fin: ", str(self.tiempoActual2Fin))
                # print("acum seg: ", str(self.segundosAcumulado))
                # print("----------------------------")

                # print("CRONOS ACTIVOS: ", str(MiTimer.numCronosActivos))
                # print("")
            else: # self.botonIniciar.text() == Continue":
                self.timer.start(1000) # reanudo el Timer que estaba en pausa
                MiTimer.hayUnCronoActivo = True
                self.tiempoActual2Ini = datetime.now()
                # self.miDisplay.setStyleSheet("QLCDNumber {color: red;}")
                self.miSegundoDisplay.setStyleSheet("QLCDNumber {color: red;}") ###############################
                self.icon3 = QtGui.QIcon()
                self.icon3.addPixmap(QtGui.QPixmap(":/miprefijo/images/pause.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.botonIniciar.setText("Pause")
                self.botonIniciar.setIcon(self.icon3)
                self.botonParar.setEnabled(False) # habilitamos el botón Reset    
                # print("CRONOS ACTIVOS: ", str(MiTimer.numCronosActivos)), 
                # print("")
        else:
            QMessageBox.about(self, "Información", "No se puede activar más de un Crono a la vez." \
                                + "\nPuedes activar esta opción en la pantalla principal.")

        # Si el check está en modo monocrono, se deja habilitado para permitir conmutar a modo multicrono
        # Si el check está en modo multicron, se deshabilita si hay más de un crono activo
        # ***PENDIENTE: Pendiente de comprobar más a fondo toda la casuística ...
        if w.PermitirCronosSimultaneos: # modo multicrono
            if MiTimer.numCronosActivos > 1:
                w.ui.checkBoxMultiCrono.setEnabled(False)
            else:
                w.ui.checkBoxMultiCrono.setEnabled(True)
        else: # modo monocrono
                w.ui.checkBoxMultiCrono.setEnabled(True)

    def PararCrono(self):
        # Botón Reset: se pone a cero, pero preguntamos si desea guardar este crono para más adelante
        MiTimer.hayUnCronoActivo = False
        MiTimer.numCronosActivos -= 1
        if MiTimer.numCronosActivos < 0:
            MiTimer.numCronosActivos = 0
        
        # print("CRONOS ACTIVOS: ", str(MiTimer.numCronosActivos)), 
        # print("")

        self.timer.stop()
        # self.miDisplay.setStyleSheet("QLCDNumber {color: black;}")
        self.miSegundoDisplay.setStyleSheet("QLCDNumber {color: black;}") ###################################
        
        # Ya no: todo lo de abajo, porque siempre que se pulse el Reset es porque viene de una Pausa (en los otros momentos está deshabilitado)
        # # Al parar el crono tengo que distinguir si el crono está en marcha (label=Pause) o parado (label=Continue)
        # # para no sumar 2 veces a segundosAcumulado el tiempo transcurrido entre que se puso en Pausa y se le da a Reset
        # if self.botonIniciar.text() == "Pause": # el crono está en marcha y se pulsa el botón reset directamente
        #     self.tiempoActual2Fin = datetime.now() ##############################
        #     self.segundosAcumulado += (self.tiempoActual2Fin - self.tiempoActual2Ini).seconds
        # elif self.botonIniciar.text() == "Continue": # el crono está en pausa, por tanto al segundosAcumulado ya se le incrementó en la pausa
        #     pass
        # else: # el crono todavía no ha iniciado
        #     pass

        # Presentamos los datos de la medición del tiempo y preguntamos si los quiere guardar para retomarlos en otra sesión.
        # cadena = str(self.tiempoActual.hour()) + ":" \
        #         + str(self.tiempoActual.minute()) + ":"  \
        #         + str(self.tiempoActual.second())
        cadena2 = self.seconds_time_to_human_string(self.segundosAcumulado)
        # #QMessageBox.about(self, "Información", cadena)
        # Preguntamos si se desea guardar el estado actual del crono para un uso posterior.
        buttonReply = QMessageBox.question(self, 'Guardar Crono Actual', "¿Quieres guardar el estado de este Crono?:\n" 
                                             + cadena2, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            # guardamos en BD. el estado de este crono.
            self.GuardarEstadoCrono(cadena2)
        # print("Cadena: ", cadena)
        # print("Cadena2: ", cadena2)
        
        # Ponemos todo a cero
        # self.tiempoActual = QtCore.QTime(0,0,0)
        # self.miDisplay.display(self.tiempoActual.toString('hh:mm:ss'))
        self.segundosAcumulado = 0
        self.miSegundoDisplay.display(self.seconds_time_to_human_string(self.segundosAcumulado)) #####################################
        
        self.Pausa = False
        self.botonIniciar.setText("Start")
        self.botonIniciar.setIcon(self.icon1)
        self.botonParar.setEnabled(False) # deshabilitamos el botón Reset  
        self.icon1 = QtGui.QIcon()
        self.icon1.addPixmap(QtGui.QPixmap(":/miprefijo/images/play.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # self.miDisplay.setStyleSheet("QLCDNumber {color: black;}")
        self.miSegundoDisplay.setStyleSheet("QLCDNumber {color: black;}") ###########################

        # si hay más de un crono activo, deshabilito el check (para evitar inconsistencias)
        if MiTimer.numCronosActivos > 1:
            w.ui.checkBoxMultiCrono.setEnabled(False)
        else:
            w.ui.checkBoxMultiCrono.setEnabled(True)
    
    def GuardarEstadoCrono(self, elCrono):
        print("ID: ", self.IDTarea.text())
        print("Estado: ", elCrono)
        print("")
        try:
            # modificamos en la BD.
            conn = sqlite3.connect(BaseDeDatos)
            cur = conn.cursor()
            miQuery = "UPDATE Tareas SET Crono = '" + elCrono + "' WHERE IDTarea = " + self.IDTarea.text()
            cur.execute(miQuery)
            conn.commit()
            # ahora borramos todo el contenido del listWidget para volver a cargarlo con los datos actualizados
            w.ui.listWidgetTareas.clear()
            w.MostrarTabla("SELECT * FROM Tareas ORDER BY FechaAlta DESC, IDTarea DESC;")
            w.ui.statusbar.showMessage("Crono guardado", 5000)
        except Error as e:
            self.ui.statusbar.showMessage(str(e), 10000)
        finally:
            conn.close()

    def showlcd(self):
        # Esto es lo que se ejecuta con cada evento del TimeOut del Timer (1 seg.)
        # self.Ahora = datetime.now()
        # difSegundos = self.Ahora - self.horaInicio
        # segundos = datetime.strptime(str(difSegundos.seconds),"%S")
        # textoDisplay = datetime.strftime(segundos, "%H:%M:%S")
        # self.tiempoActual = self.tiempoActual.addSecs(1)
        # self.miDisplay.display(self.tiempoActual.toString('hh:mm:ss'))
        self.tiempoActual2Fin = datetime.now()
        #self.totalSegundos = (self.tiempoActual2Fin - self.tiempoActual2Ini 
        #                    + timedelta(seconds=self.segundosAcumulado)).total_seconds() ############################
        self.totalSegundos = (self.tiempoActual2Fin - self.tiempoActual2Ini).seconds + self.segundosAcumulado ############################
        self.miSegundoDisplay.display(self.seconds_time_to_human_string(self.totalSegundos))
        # print("INI: ", str(self.tiempoActual2Ini))
        # print("FIN: ", str(self.tiempoActual2Fin))
        # print("ACUM SEG: ", str(self.segundosAcumulado))
        # print("----------------------------")
        #text2 = Ahora.toString('hh:mm:ss')
        # hay que poner el lcdNumber.digitCount = 8
        #self.ui.lcdNumber.display(textoDisplay) 
        #app.processEvents() # just this one line allows display of 'i'
        #self.ui.label.setText(textoDisplay)

    def ConvertirCadena_a_Segundos(self, cadena):
        # Convertimos una cadena de fecha/hora a segundos
        # Este procedimiento es necesario para poder restaurar un crono guardado de una vez anterior (es llamado desde el botón Start)
        # Lo primero que hay que saber es la longitud de la cadena 
        # Puede ser una cadena normal '00:00:00' o la ampliada '00d 00:00:00' que también muestra los días
        segundosDevolver = 0
        Dias = 0
        if len(cadena) != 8: # cadena por defecto '00:00:00', # cadena extendida que incluye días '27D 00:00:00'
            Dias = Horas = int(cadena[-12:-10])
        Horas = int(cadena[-8:-6])
        Minutos = int(cadena[-5:-3])
        Segundos = int(cadena[-2:])

        # hh = Dias * 86400
        # mm = Horas * 3600
        # ss = Minutos * 60

        #***CONTINUAR AQUI:
        #*** ¡¡¡ DA DISTINTO para el caso de '30D 23:59:50' (segundosDevolver2 da 50 seg. menos) !!! ***
        segundosDevolver = (Dias * 86400) + (Horas * 3600) + (Minutos * 60) + Segundos
        # segundosDevolver2 = hh + mm + ss

        return float(segundosDevolver)

    def seconds_time_to_human_string(self, time_on_seconds=0):
        """Calculate time, with precision from seconds to days."""
        minutes, seconds = divmod(int(time_on_seconds), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        human_time_string = ""
        if days:
            human_time_string += "%02dD " % days
        if hours:
            human_time_string += "%02d" % hours
        else:
            human_time_string += "00"
        if minutes:
            human_time_string += ":%02d" % minutes
        else:
            human_time_string += ":00"
        human_time_string += ":%02d" % seconds
        return human_time_string
    


if __name__=="__main__":         
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

