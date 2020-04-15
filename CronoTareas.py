#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  CronoTareas, v.1.1
#  Sencilla aplicación para cronometrar tiempos asociados a tareas.
#  
#  Copyright April, 2020 fer <donanpher@gmail.com>
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
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

import sqlite3, sys, os
from sqlite3 import Error
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QListWidget, QLabel, QPushButton, QListWidgetItem, \
    QHBoxLayout, QLCDNumber, QMessageBox, QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit, QFrame
from PyQt5 import QtCore
from PyQt5 import QtGui
from ui_CronoTareas import *
BaseDeDatos = "CronoTareas.db"

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
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
                miQuery = "INSERT INTO Tareas (NombreTarea, Tag, FechaAlta) \
                            VALUES ('" + modifTarea + "', '" + modifTag + "', '" + self.strAhora + "')"
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

    def AnhadirItem(self, nuevoID, nuevaTarea, nuevoTag):
        self.nuevoID = nuevoID
        self.nuevaTarea = nuevaTarea
        self.nuevoTag = nuevoTag
        miItem = QListWidgetItem()
        miCustomWidget = MiTimer(self.nuevoID, self.nuevaTarea, self.nuevoTag)
        miItem.setSizeHint(miCustomWidget.sizeHint())
        self.ui.listWidgetTareas.addItem(miItem) # añade el item al final de la lista
        #self.ui.listWidgetTareas.insertItem(0, miItem) # inserta el item en primer lugar de la lista
        self.ui.listWidgetTareas.setItemWidget(miItem, miCustomWidget)
        self.ui.listWidgetTareas.setStyleSheet( "QListWidget::item { border-bottom: 1px solid black; }" ) # esta es una línea que separa líneas
        self.show()

    def MostrarTabla(self, miQuery):
        try:
            conn = sqlite3.connect(BaseDeDatos)
            cur = conn.cursor()
            cur.execute(miQuery)
            registros = cur.fetchall()
            totalReg = len(registros) # total de registros de la query
            #elf.ui.tableWidgetNotas.setRowCount(totalReg) # dimensionamos el widget en filas
            recNum = 0
            for registro in registros:
                self.AnhadirItem(str(registro[0]), registro[1], registro[2])
                recNum += 1

        except Error as e:
            self.ui.statusbar.showMessage(str(e), 10000)
        finally:
            conn.close()
    
    def Recargar(self):
        self.ui.listWidgetTareas.clear()
        self.MostrarTabla("SELECT * FROM Tareas ORDER BY FechaAlta DESC, IDTarea DESC;")


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
                        FechaAlta   TEXT (20)  \
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
                       FechaAlta \
                        ) \
                        VALUES ( \
                            'Tarea 1', \
                            'Test Tareas', \
                            '2020-04-12 12:16:08' \
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

    # esta es la linea, con la colección de widgets, que se pinta dentro de la lista
    def __init__(self, miID, miTarea, miTag, parent=None):
        super(MiTimer, self).__init__(parent)
        self.miID = miID
        self.miTarea = miTarea
        self.miTag = miTag
        self.altoWidgets = 25
        self.anchoBotones = 75
        self.tiempoActual = QtCore.QTime(0,0,0)
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
        self.miDisplay = QLCDNumber()
        self.miDisplay.setDigitCount(8)
        self.miDisplay.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.miDisplay.setFixedWidth(self.anchoBotones + 30)
        self.miDisplay.setFixedHeight(30)
        # self.font = QtGui.QFont()
        # self.font.setBold(True)
        # self.miDisplay.setFont(self.font)

        self.showlcd()
        self.timer.timeout.connect(self.showlcd)
        self.miLayOut = QHBoxLayout()
        self.miLayOut.addWidget(self.IDTarea)
        self.miLayOut.addWidget(self.NombreTarea)
        self.miLayOut.addWidget(self.Tag)
        self.miLayOut.addWidget(self.botonIniciar)
        self.miLayOut.addWidget(self.botonParar)
        self.miLayOut.addWidget(self.miDisplay)
        self.setLayout(self.miLayOut)

    def IniciarCrono(self):
        # La idea de todo esto es que si se está en modo monocrono, sólo se pueda tener activo uno, los que están en pausa no están activos.
        # En el modo multicrono, se permite que estén activos todos los cronos que se quieran.
        # Si se permiten varios cronos simultáneos, o si no se permiten pero que sólo haya uno activo o que el pulsado sea de Pausa o Continuar
        # (esta condición me llevó unas cuantas horas/sesiones elaborarla)
        if (w.PermitirCronosSimultaneos) or (
            (not w.PermitirCronosSimultaneos) and (
                (not MiTimer.hayUnCronoActivo) or (self.botonIniciar.text() == "Pause") or (self.botonIniciar.text() == "Continuar")
                )
            ):
            # en qué modo se pincha el botón iniciar? (Start|Pause|Continue)
            if self.botonIniciar.text() == "Start":
                self.timer.start(1000) # pongo en marcha el Timer
                MiTimer.hayUnCronoActivo = True
                MiTimer.numCronosActivos += 1
                self.miDisplay.setStyleSheet("QLCDNumber {color: red;}")
                self.icon3 = QtGui.QIcon()
                self.icon3.addPixmap(QtGui.QPixmap(":/miprefijo/images/pause.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.botonIniciar.setText("Pause")
                self.botonIniciar.setIcon(self.icon3)        
                print("CRONOS ACTIVOS: ", str(MiTimer.numCronosActivos)), 
                print("")
            elif self.botonIniciar.text() =="Pause":
                self.timer.stop() # detengo el timer
                MiTimer.hayUnCronoActivo = False
                self.icon4 = QtGui.QIcon()
                self.icon4.addPixmap(QtGui.QPixmap(":/miprefijo/images/continue.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.botonIniciar.setText("Continue")
                self.botonIniciar.setIcon(self.icon4)        
                self.miDisplay.setStyleSheet("QLCDNumber {color: green;}")
                print("CRONOS ACTIVOS: ", str(MiTimer.numCronosActivos)), 
                print("")
            else: # self.botonIniciar.text() == Continue":
                self.timer.start(1000) # reanudo el Timer que estaba en pausa
                MiTimer.hayUnCronoActivo = True
                self.miDisplay.setStyleSheet("QLCDNumber {color: red;}")
                self.icon3 = QtGui.QIcon()
                self.icon3.addPixmap(QtGui.QPixmap(":/miprefijo/images/pause.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.botonIniciar.setText("Pause")
                self.botonIniciar.setIcon(self.icon3)        
                print("CRONOS ACTIVOS: ", str(MiTimer.numCronosActivos)), 
                print("")
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
        #if self.Pausa: # si está en marcha un crono sin haber habido una pausa 
        MiTimer.numCronosActivos -= 1
        print("CRONOS ACTIVOS: ", str(MiTimer.numCronosActivos)), 
        print("")
        self.timer.stop()
        self.miDisplay.setStyleSheet("QLCDNumber {color: black;}")
        #self.tiempoFinal = self.ui.lcdNumber.value()
        cadena = str(self.tiempoActual.hour()) + ":" \
                + str(self.tiempoActual.minute()) + ":"  \
                + str(self.tiempoActual.second())
        # #QMessageBox.about(self, "Información", cadena)
        # buttonReply = QMessageBox.question(self, 'Guardar Crono Actual', "¿Quieres guardar el estado de este Crono?:\n" 
        #                                     + cadena, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # if buttonReply == QMessageBox.Yes:
        #     pass
        # else:
        #     pass
        self.tiempoActual = QtCore.QTime(0,0,0)
        self.miDisplay.display(self.tiempoActual.toString('hh:mm:ss'))
        self.Pausa = False
        self.botonIniciar.setText("Start")
        self.icon1 = QtGui.QIcon()
        self.icon1.addPixmap(QtGui.QPixmap(":/miprefijo/images/play.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.botonIniciar.setIcon(self.icon1)        

        self.miDisplay.setStyleSheet("QLCDNumber {color: black;}")

        # si hay más de un crono activo, deshabilito el check (para evitar inconsistencias)
        if MiTimer.numCronosActivos > 1:
            w.ui.checkBoxMultiCrono.setEnabled(False)
        else:
            w.ui.checkBoxMultiCrono.setEnabled(True)

    def GuardarEstadoCrono(self):
        pass

    def showlcd(self):
        # self.Ahora = datetime.now()
        # difSegundos = self.Ahora - self.horaInicio
        # segundos = datetime.strptime(str(difSegundos.seconds),"%S")
        # textoDisplay = datetime.strftime(segundos, "%H:%M:%S")
        self.tiempoActual = self.tiempoActual.addSecs(1)
        self.miDisplay.display(self.tiempoActual.toString('hh:mm:ss'))
        #text2 = Ahora.toString('hh:mm:ss')
        # hay que poner el lcdNumber.digitCount = 8
        #self.ui.lcdNumber.display(textoDisplay) 
        #app.processEvents() # just this one line allows display of 'i'
        #self.ui.label.setText(textoDisplay)


if __name__=="__main__":         
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

