#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
 CronoTareas, v.2.3
 Sencilla aplicación para cronometrar tiempos asociados a tareas.
 Creada usando Python 3.6.7 + PyQt5
    Fecha Inicio: 14-04-2020
    Fecha Fin (v.1.8): 26-04-2020
    Tiempo empleado: 13 días, a 4 horas/día (aprox.) = 52 horas (más o menos...)
    Es mi segunda aplicación hecha con PyQt5
    Si hubiese tenido CronoTareas, sabría el tiempo exacto que me llevó.

 Copyright April, 2020 Fer <donanpher@gmail.com>
 (durante la cuarentena del #Coronavirus #SARS-CoV-2 #Covid-19)
 
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 """
#  

import sqlite3, sys, os
from sqlite3 import Error
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QListWidget, QLabel, QPushButton, QListWidgetItem, \
    QHBoxLayout, QLCDNumber, QMessageBox, QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit, QFrame, QDesktopWidget, \
    QSpinBox, QTimeEdit, QComboBox, QTableWidgetItem, QFileDialog, QDateEdit, QCheckBox, qApp
from PyQt5 import QtCore
from PyQt5 import QtGui
from ui_CronoTareas import *

#########################################################
__author__ = "Fernando Souto"
__email_ = "donanpher@gmail.com"
__copyright__ = "Copyright (c) April 2020 Fernando Souto"
__license__ = "GPLv3"
__version__ = "2.2"
#########################################################

BaseDeDatos = "CronoTareas.db"

class AppWindow(QMainWindow):
    def __init__(self, argus):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(788, 487)
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
        
        # esta variable depende del widget checkBoxMultiCrono y se usa para permitir o no la simultaneidad de los cronos
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
        self.ui.labelIcono.mouseReleaseEvent = self.MuestraCreditos # mousePressEvent() , mouseReleaseEvent() , mouseDoubleClickEvent()
        self.ui.pushButtonBuscar.clicked.connect(self.BuscarTareas)
        self.ui.pushButtonExportar.clicked.connect(self.Exportar)
        #self.ui.comboBoxInformes.currentIndexChanged.connect(self.Informes) # esta señal es cuando cambia el elemento seleccionado
        self.ui.comboBoxInformes.activated.connect(self.Informes) # esta señal es cuando se pincha el elemento, aunque no haya cambiado la selección
        #---------------------------------------------------
        # Este es el punto rojo que se enciende cuando hay algún crono en marcha
        self.ui.label_Punto1.setVisible(False)

        # Chequeo inicial de la BD.: se comprueba que si hay un campo FechaHoraIni con datos, no haya uno FechaHoraFin sin ellos, y si lo hay igualar ambas fechas
        # Esto puede suceder si durante el funcionamiento de un crono, el usuario sale de la app. sin más, lo que después puede provocar un error en los listados.
        # ya no!: si el usuario cierra en la X, se le advierte, y si sigue pasando del tema, le pongo yo la fecha del momento.
        self.ComprobarBD("") # no le pasamos ninguna fecha porque no la sabemos

        # Inicialización de la lista de tareas
        miTupla = () # la tupla va vacía
        self.MostrarTabla("SELECT * FROM Tareas WHERE Mostrar = 1 ORDER BY FechaAlta DESC, IDTarea DESC;", miTupla)
        #self.ui.labelTotalTareas.setText("Total Tareas: " + str(self.ui.listWidgetTareas.count()))
        
    def PonerEnMarchaTarea(self, idEjecutar):
        # Si vienen argumentos con la app, o sea, el ID de la Tarea que queremos poner en marcha según se inicie la app.
        # hay que recorrer todo el listWidget hasta encontrar ese ID, posicionarnos, y pulsar el botón.
        totalFilas = self.ui.listWidgetTareas.count()
        for n in range(0, totalFilas):
            self.ui.listWidgetTareas.setCurrentRow(n)
            ItemModificar = self.ui.listWidgetTareas.currentItem()
            miWidget = self.ui.listWidgetTareas.itemWidget(ItemModificar)
            # estos son los datos de la fila seleccionada actualmente
            elID = miWidget.IDTarea.text()
            if int(elID) == int(idEjecutar):
                miWidget.botonIniciar.click() # pulsamos el botón 'Start' correspondiente al ID de tarea con que se ha iniciado la app.
                break # no me gustan los break!!!


    def CronosSimultaneos(self):
        # Esto muestra en la barra de estado el modo en el que nos encontramos: monoCrono (por defecto) o multiCrono (seleccionable)
        self.PermitirCronosSimultaneos = not self.PermitirCronosSimultaneos
        if self.PermitirCronosSimultaneos:
            self.ui.statusbar.showMessage("Modo: Multi Crono")
        else:
            self.ui.statusbar.showMessage("Modo: Mono Crono")

    def AgregarTarea(self):
        # Agrega una nueva tarea, tanto a la BD. como a la lista de tareas.
        dlg = CustomDialog(self)
        if dlg.exec_():
            try:
                # esta es la fecha y hora del momento actual para guardarla en la BD. al dar un alta
                self.Ahora = datetime.now()
                self.strAhora = datetime.strftime(self.Ahora, "%Y-%m-%d %H:%M:%S")
                # modificamos en la BD.
                conn = sqlite3.connect(BaseDeDatos)
                cur = conn.cursor()
                # estos son los valores que hay en el CustomDialog
                modifTarea = dlg.miLineEditTareaDialog.text()
                modifTag = dlg.miLineEditTagDialog.text()
                modifDias = str(dlg.miSpinDias.value())
                modifHora = dlg.miTimeEditHoras.time().toString()
                if len(modifDias) ==1: # si el día sólo tiene un dígito, le añadimos el cero delante
                    modifDias = "0" + modifDias
                modifDias = modifDias + "D " # le ponemos el formato nuestro que estamos usando en el display
                #miQuery = "INSERT INTO Tareas (NombreTarea, Tag, FechaAlta, Crono) \
                #            VALUES ('" + modifTarea + "', '" + modifTag + "', '" + self.strAhora + "', '" + modifDias + modifHora + "')"
                miQuery = "INSERT INTO Tareas (NombreTarea, Tag, FechaAlta, Crono) VALUES (?, ?, ?, ?)"
                cur.execute(miQuery, (modifTarea, modifTag, self.strAhora, modifDias + modifHora,))
                conn.commit()
                # necesitamos saber cuál es el ID asignado (es autonumérico).
                if cur.rowcount != 1:
                    print("Algo falló al insertar")
                else:
                    elID = cur.lastrowid
                # miQuery = "SELECT Max(IDTarea) FROM Tareas"
                # cur.execute(miQuery)
                # elRegistro = cur.fetchone()
                # elID = elRegistro[0]
                #
                # ahora insertamos un item en la lista con esta alta
                miItem = QListWidgetItem()
                self.ui.listWidgetTareas.insertItem(0, miItem) # inserta el item en primer lugar de la lista
                miCustomWidget = MiTimer(str(elID), modifTarea, modifTag, modifDias + modifHora, modifDias + modifHora, "1")
                miItem.setSizeHint(miCustomWidget.sizeHint())
                #self.ui.listWidgetTareas.addItem(miItem) # añade el item al final de la lista
                self.ui.listWidgetTareas.setItemWidget(miItem, miCustomWidget)
                self.ui.listWidgetTareas.setStyleSheet( "QListWidget::item { border-bottom: 1px solid black; }" ) # esta es una línea que separa líneas
                self.show()
                self.ui.statusbar.showMessage("Se ha añadido una nueva Tarea", 5000)
            except Error as e:
                self.ui.statusbar.showMessage(str(e), 10000)
            finally:
                conn.close()
        else:
            self.ui.statusbar.showMessage("Añadir Tarea nueva cancelado", 5000)
            
    def ModificarTarea(self):
        # Modificar la tarea seleccionada, bien dándole al botón modificar o haciendo doble-click en la fila
        filaModificar = self.ui.listWidgetTareas.currentRow()

        if filaModificar == -1: # si no hay seleccionada ninguna fila
            self.ui.statusbar.showMessage("Selecciona la fila que quieres modificar.", 5000)
            QMessageBox.about(self, "Información", "Selecciona la fila que quieres modificar.")
        else: # hay una fila seleccionada
            ItemModificar = self.ui.listWidgetTareas.currentItem()
            miWidget = self.ui.listWidgetTareas.itemWidget(ItemModificar)
            # Para poder modificar una fila, no puede estar el crono activo
            if miWidget.botonIniciar.text() != "Start":
                QMessageBox.about(self, "Información", "Para poder modificar una Tarea, el Crono no puede estar activo. \
                                                        \nPulsa Stop, guarda el Crono, modifica Tarea y vuelve a iniciarla.")
            else: # no hay ningún crono activo
                # estos son los datos de la fila seleccionada actualmente
                elID = miWidget.IDTarea.text()
                laTarea = miWidget.NombreTarea.text()
                elTag = miWidget.Tag.text()
                elCrono = miWidget.labelCrono.text()
                elMostrar = miWidget.labelMostrar.text()
                # llamamos al diálogo para captar los datos con la modificación
                dlg = CustomDialog(self)
                dlg.setWindowTitle("Modificar Tarea")
                dlg.miLabelIDDialog.setText("ID: " + elID)
                dlg.miLineEditTareaDialog.setText(laTarea)
                dlg.miLineEditTagDialog.setText(elTag)
                dlg.miCheckArchivada.setChecked(not int(elMostrar))
                # El crono por defecto siempre va a incluir días, aunque sean cero.
                # esto lo hago así porque si el crono sólo incluye hora y deseamos añadir días, no podríamos hacerlo
                if len(elCrono) == 8:
                    losDias = 0
                    laHora = elCrono
                else:
                    losDias = int(elCrono[:2])
                    laHora = elCrono[-8:]
                dlg.miSpinDias.setValue(losDias)
                horaQTime = QtCore.QTime(int(laHora[:2]),int(laHora[3:5]),int(laHora[6:])) 
                dlg.miTimeEditHoras.setTime(horaQTime)
                # Abrimos un cuadro de diálogo, que muestra los datos actuales de la tarea, para poder modificarla.
                if dlg.exec_():
                    modifTarea = dlg.miLineEditTareaDialog.text()
                    modifTag = dlg.miLineEditTagDialog.text()
                    modifDias = str(dlg.miSpinDias.value())
                    modifHora = dlg.miTimeEditHoras.time().toString()
                    if len(modifDias) == 1: # si el día sólo tiene un dígito, le añadimos el cero delante
                        modifDias = "0" + modifDias
                    modifDias = modifDias + "D " # le ponemos el formato nuestro que estamos usando en el display
                    if dlg.miCheckArchivada.isChecked():
                        modifMostrar = 0
                    else:
                        modifMostrar = 1

                    try: # hay que guardar en BD. las modificaciones
                        # modificamos en la BD.
                        conn = sqlite3.connect(BaseDeDatos)
                        cur = conn.cursor()
                        #         + "' WHERE IDTarea = " + elID
                        miQuery = "UPDATE Tareas SET NombreTarea = ?, Tag = ?, Crono = ?, Mostrar = ? WHERE IDTarea = ?"
                        cur.execute(miQuery, (modifTarea, modifTag, modifDias + modifHora, modifMostrar, elID,))
                        conn.commit()
                        #Se debe de guardar el estado actual de cosas y sólo modificar lo que se ha tocado.
                        ItemModificar = self.ui.listWidgetTareas.currentItem()
                        miWidget = self.ui.listWidgetTareas.itemWidget(ItemModificar)
                        # estos son los datos de la fila seleccionada actualmente
                        elID = miWidget.IDTarea.text()
                        miWidget.NombreTarea.setText(modifTarea)
                        miWidget.Tag.setText(modifTag)
                        miWidget.miCrono = modifDias + modifHora
                        miWidget.miSegundoDisplay.display(modifDias + modifHora)
                        miWidget.labelCrono.setText(modifDias + modifHora)
                        miWidget.labelMostrar.setText(str(modifMostrar))
                        if modifMostrar == 0: # si se archiva la tarea, se elimina de la lista
                            self.ui.listWidgetTareas.takeItem(filaModificar)

                        self.ui.statusbar.showMessage("Tarea modificada", 5000)
                    except Error as e:
                        self.ui.statusbar.showMessage(str(e), 10000)
                    finally:
                        conn.close()
                else: # Ha pulsado Cancel!
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
            
            # llamamos a un diálogo de Aceptar/Cancelar (con checkBox!!!) para confirmar eliminación
            self.msgBox = QMessageBox()
            self.msgBox.setText("Eliminar Tarea")
            self.msgBox.setInformativeText("¿Quieres eliminar de la lista esta Tarea?:\n" + laNota)
            self.msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.msgBox.setIcon(QMessageBox.Question)
            eliminarEnBD = QCheckBox("Eliminar también en la Base de Datos")
            self.msgBox.setCheckBox(eliminarEnBD)
            buttonReply = self.msgBox.exec_()
            #buttonReply = QMessageBox.question(self, 'Eliminar Tarea', "¿Quieres eliminar esta Tarea?:\n" + laNota, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # msg.setIcon(QMessageBox.Information,QMessageBox.Question,QMessageBox.Warning,QMessageBox.Critical)            
            if buttonReply == QMessageBox.Yes:
                # eliminamos de la lista sólo el item actual, sin necesidad de vaciar lista y volver a cargarla. Así los cronos pueden seguir funcionando.
                self.ui.listWidgetTareas.takeItem(filaModificar)
                conn = sqlite3.connect(BaseDeDatos)
                cur = conn.cursor()
                # Si además también hay que eliminarlo de la BD.
                if self.msgBox.checkBox().isChecked():
                    try:
                        # A pesar de tener puesto en la tabla DetalleTareas, la eliminación en cascada, no veo que funcione.
                        # Por tanto, tengo que hacerlo manualmente desde aqui.
                        # Primero, en DetalleTareas
                        #miQuery = "DELETE FROM DetalleTareas WHERE IDTarea = " + elID
                        miQuery = "DELETE FROM DetalleTareas WHERE IDTarea = ?"
                        cur.execute(miQuery, (elID,))
                        conn.commit()
                        # Después, en Tareas
                        miQuery = "DELETE FROM Tareas WHERE IDTarea = ?"
                        cur.execute(miQuery, (elID,))
                        conn.commit()
                    except Error as e:
                        self.ui.statusbar.showMessage(str(e), 10000)
                    finally:
                        conn.close()
                else: # se elimina de la lista, pero no de la BD.
                    # Hay que actualizar en la BD. para que no se muestre en la lista más
                    try:
                        miQuery = "UPDATE Tareas SET Mostrar = ? WHERE IDTarea = ?"
                        cur.execute(miQuery, (0, elID,))
                        conn.commit()
                    except Error as e:
                        self.ui.statusbar.showMessage(str(e), 10000)
                    finally:
                        conn.close()

                self.ui.statusbar.showMessage("Tarea eliminada", 5000)
            else:
                self.ui.statusbar.showMessage("Eliminar Tarea Cancelado", 5000)

    def BuscarTareas(self):
        # Si hay un crono activo, no dejamos buscar porque al hacerlo se aplica un filtro a la lista y esta se recarga.
        if MiTimer.numCronosActivos > 0:
            QMessageBox.about(self, "Información", "No se pueden hacer búsquedas mientras haya un Crono activo. Detén Cronos (Stop) antes de hacer una búsqueda.")
        else:
            # llamamos al diálogo para captar los datos de la búsqueda
            dlg = CustomDialogBuscar(self)
            if dlg.exec_():
                campoDondeBuscar = dlg.miComboCampos.itemText(dlg.miComboCampos.currentIndex())
                if campoDondeBuscar == "Tarea":
                    campoDondeBuscar = "NombreTarea"
                queBuscar = dlg.miLineEditBuscar.text()
                try:
                    conn = sqlite3.connect(BaseDeDatos)
                    cur = conn.cursor()
                    tuplaBuscar = ("%" + queBuscar + "%",)
                    #miQuery = "SELECT * FROM Tareas WHERE " + campoDondeBuscar + " LIKE '%" + queBuscar + "%' ORDER BY FechaAlta DESC, IDTarea DESC;"
                    miQuery = "SELECT * FROM Tareas WHERE " + campoDondeBuscar + " LIKE ? ORDER BY FechaAlta DESC, IDTarea DESC"
                    cur.execute(miQuery, tuplaBuscar)
                    #cur.execute(miQuery)
                    registros = cur.fetchall()
                    totalReg = len(registros) # total de registros de la query
                    if totalReg == 0:
                        QMessageBox.about(self, "Información", "No se han encontrado Tareas coincidentes.")
                        self.ui.statusbar.showMessage("No hay Tareas con los criterios de busqueda suministrados.", 5000)
                    else:
                        self.ui.statusbar.showMessage("Registros encontrados: " + str(totalReg), 5000)
                except Error as e:
                    self.ui.statusbar.showMessage(str(e), 10000)
                finally:
                    conn.close()
                
                # no me deja ejecutar esta query, aun estando cerrada la conexión: "sqlite3.Warning: You can only execute one statement at a time."
                # ya sé porque era: tenía abierto el SQLite Studio.
                if totalReg > 0:
                    self.ui.listWidgetTareas.clear()
                    self.MostrarTabla(miQuery, tuplaBuscar)

            else:
                self.ui.statusbar.showMessage("Buscar Tarea Cancelado", 5000)

    def GuardarEstadoTareas(self):
        # ***** Esto de momento queda en Stand-by, pues creo que no lo voy a necesitar. *****
        # Cada vez que se hace un alta/modificación/eliminación, se hace un .clear (se vacía el listWidget) y se vuelve a cargar desde la BD.
        # Si hay cronos activos, al hacer lo anterior, se pierde la información del crono actual
        # Por todo esto, hay que guardar el estado actual de todos los cronos antes de recargar la lista.
        totalFilas = self.ui.listWidgetTareas.count()
        for n in range(0, totalFilas):
            self.ui.listWidgetTareas.setCurrentRow(n)
            ItemModificar = self.ui.listWidgetTareas.currentItem()
            miWidget = self.ui.listWidgetTareas.itemWidget(ItemModificar)
            # estos son los datos de la fila seleccionada actualmente
            elID = miWidget.IDTarea.text()
            elCrono = miWidget.miCrono

    def AnhadirItem(self, nuevoID, nuevaTarea, nuevoTag, nuevoCrono, nuevoLabelCrono, nuevoLabelMostrar):
        # Un Item es cada fila de la lista de tareas
        # Este método es llamado por el método MostrarTabla, para ir añadiendo todos los reg. de la BD.
        self.nuevoID = nuevoID
        self.nuevaTarea = nuevaTarea
        self.nuevoTag = nuevoTag
        self.nuevoCrono = nuevoCrono
        self.nuevoLabelCrono = nuevoLabelCrono
        self.nuevoMostrar = nuevoLabelMostrar
        miItem = QListWidgetItem()
        miCustomWidget = MiTimer(self.nuevoID, self.nuevaTarea, self.nuevoTag, self.nuevoCrono, self.nuevoLabelCrono, self.nuevoMostrar)
        miItem.setSizeHint(miCustomWidget.sizeHint())
        self.ui.listWidgetTareas.addItem(miItem) # añade el item al final de la lista
        #self.ui.listWidgetTareas.insertItem(0, miItem) # inserta el item en primer lugar de la lista
        self.ui.listWidgetTareas.setItemWidget(miItem, miCustomWidget)
        self.ui.listWidgetTareas.setStyleSheet( "QListWidget::item { border-bottom: 1px solid black; }" ) # esta es una línea que separa líneas
        self.show()

    def MostrarTabla(self, miQuery, tuplaQuery):
        # Carga en la lista de tareas todos los registros de la BD.
        try:
            conn = sqlite3.connect(BaseDeDatos)
            cur = conn.cursor()
            if len(tuplaQuery) == 0: # es una query sin argumentos
                cur.execute(miQuery)
            else: # es una query con argumentos
                cur.execute(miQuery, tuplaQuery)
            registros = cur.fetchall()
            totalReg = len(registros) # total de registros de la query
            #elf.ui.tableWidgetNotas.setRowCount(totalReg) # dimensionamos el widget en filas
            recNum = 0
            sumaCronos = 0 # aquí vamos acumulando los segundos de cada crono para después mostrarlos en el label al pié de la lista
            for registro in registros: # Campos: ID, Tarea, Tag, Crono, LabelCrono, Mostrar
                self.AnhadirItem(str(registro[0]), registro[1], registro[2], registro[4], registro[4], str(registro[5])) # estos son los campos
                recNum += 1
                sumaCronos += MiTimer.ConvertirCadena_a_Segundos(self, registro[4]) # la función de conversión, está en la clase MiTimer
            # mostramos la suma de los cronos en el label (previamente convertida a formato humano)
            self.ui.labelSumaCronos.setText("Suma Cronos: " + MiTimer.seconds_time_to_human_string(self, sumaCronos))
        except Error as e:
            self.ui.statusbar.showMessage(str(e), 10000)
            print(str(e))
        finally:
            conn.close()
            self.ui.labelTotalTareas.setText("Total Tareas: " + str(self.ui.listWidgetTareas.count()))

    def Informes(self):
        # Cuando se selecciona un informe en el combo que hay en la pestaña informes
        informeSeleccionado = self.ui.comboBoxInformes.itemText(self.ui.comboBoxInformes.currentIndex())
        if informeSeleccionado[:2] == "01": # Detalle de Tareas por Tag
            # Abrimos un diálogo para pedir los datos del Tag
            dlg = CustomDialogInformes(self)
            dlg.miEtiqueta.setText("Selecciona el Tag")
            if dlg.exec_():
                elemElegido = dlg.miCombo.itemText(dlg.miCombo.currentIndex())
                self.InformesDetalle("Tag", elemElegido, "")
                #self.InformesDetalle("Tag", elemElegido)
            else: # Ha pulsado Cancel!
                pass
                #self.ui.statusbar.showMessage("Cancelado por usuario", 5000)
        elif informeSeleccionado[:2] == "02": # Detalle de Tags por Tarea
            # Abrimos un diálogo para pedir los datos del Tag
            dlg = CustomDialogInformes(self)
            dlg.miEtiqueta.setText("Selecciona la Tarea")
            if dlg.exec_():
                elemElegido = dlg.miCombo.itemText(dlg.miCombo.currentIndex())
                self.InformesDetalle("NombreTarea", elemElegido, "")
            else: # Ha pulsado Cancel!
                pass
                #self.ui.statusbar.showMessage("Cancelado por usuario", 5000)
        elif informeSeleccionado[:2] == "03": # Todas las Tareas por FechaInicio
            # Abrimos un diálogo para pedir los datos del Tag
            dlg = CustomDialogInformes2(self)
            #dlg.miEtiqueta.setText("Selecciona Fecha Desde-Hasta")
            if dlg.exec_():
                fechaIni = dlg.fechaDesde.date()
                fechaFin = dlg.fechaHasta.date()
                # a la fecha-hasta, se le añaden 23:59:59, porque si no, no cogería los registros de esa fecha, que sí incluyen horas y por tanto son mayores.
                self.InformesDetalle("TodasTareas", fechaIni.toString("yyyy-MM-dd"), fechaFin.toString("yyyy-MM-dd") + " 23:59:59")
            else: # Ha pulsado Cancel!
                pass
                #self.ui.statusbar.showMessage("Cancelado por usuario", 5000)
        
        else: #"--- Selecciona un informe ---":
            pass
            #QMessageBox.about(self, "Información", informeSeleccionado)

    def InformesDetalle(self, campo, valor, valor2):
        try:
            conn = sqlite3.connect(BaseDeDatos)
            cur = conn.cursor()
            if campo == "Tag":
                self.tuplaQuery = (valor,)
                self.queryInformes = "SELECT T.NombreTarea, T.Tag, DT.FechaHoraInicio, DT.FechaHoraFin, \
                                Cast ((JulianDay(DT.FechaHoraFin) - JulianDay(DT.FechaHoraInicio)) * 24 * 60 * 60 As Integer) Total \
                                FROM Tareas T, DetalleTareas DT ON T.IDTarea = DT.IDTarea \
                                WHERE T.Tag = ? \
                                ORDER BY T.FechaAlta, DT.FechaHoraInicio"
            elif campo == "NombreTarea":
                self.tuplaQuery = (valor,)
                self.queryInformes = "SELECT T.Tag, T.NombreTarea, DT.FechaHoraInicio, DT.FechaHoraFin, \
                                Cast ((JulianDay(DT.FechaHoraFin) - JulianDay(DT.FechaHoraInicio)) * 24 * 60 * 60 As Integer) Total \
                                FROM Tareas T, DetalleTareas DT ON T.IDTarea = DT.IDTarea \
                                WHERE T.NombreTarea = ? \
                                ORDER BY T.FechaAlta, DT.FechaHoraInicio"
            else: # TodasTareas (Todas las Tareas por FechaInicio)
                self.tuplaQuery = (valor, valor2,)
                self.queryInformes = "SELECT T.NombreTarea, T.Tag, DT.FechaHoraInicio, DT.FechaHoraFin, \
                                Cast ((JulianDay(DT.FechaHoraFin) - JulianDay(DT.FechaHoraInicio)) * 24 * 60 * 60 As Integer) Total \
                                FROM Tareas T, DetalleTareas DT ON T.IDTarea = DT.IDTarea \
                                WHERE DT.FechaHoraInicio BETWEEN ? AND ? \
                                ORDER BY DT.FechaHoraInicio"

            cur.execute(self.queryInformes, self.tuplaQuery)
            registros = cur.fetchall()
            totalReg = len(registros) # total de registros de la query
            if totalReg > 0:
                totalReg += 1 # añadimos una fila para representar los totales
            self.ui.tableWidgetInformes.clear()
            self.ui.tableWidgetInformes.setRowCount(totalReg) # dimensionamos el widget en filas
            self.ui.tableWidgetInformes.setColumnCount(5)
            recNum = 0
            totalSegundos = 0
            # recorremos toda la query en filas (registros) y tupla (campos)
            for tupla in registros:
                colNum = 0
                for columna in tupla:
                    if colNum == 4: # vamos sumando los segundos
                        if columna is None: # por si nos viene un valor nulo, sobretodo si no hay fechafin
                            unaColumna = QTableWidgetItem(MiTimer.seconds_time_to_human_string(self, 0)) # convierto los segundos en formato humano
                            unaColumna.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter) # alineación derecha
                        else:
                            totalSegundos += int(columna)
                            unaColumna = QTableWidgetItem(MiTimer.seconds_time_to_human_string(self, columna)) # convierto los segundos en formato humano
                            unaColumna.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter) # alineación derecha
                    else:
                        unaColumna = QTableWidgetItem(str(columna))
                    self.ui.tableWidgetInformes.setItem(recNum, colNum, unaColumna)
                    #self.ui.tableWidgetInformes.item(recNum, colNum).setText(str(columna))
                    colNum += 1
                recNum += 1
            
            if recNum > 0: # Añadimos una fila con los Totales
                unaColumna = QTableWidgetItem("TOTALES")
                self.ui.tableWidgetInformes.setItem(recNum, 3, unaColumna)
                unaColumna = QTableWidgetItem(MiTimer.seconds_time_to_human_string(self, totalSegundos))
                unaColumna.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter) # alineación derecha
                self.ui.tableWidgetInformes.setItem(recNum, 4, unaColumna)

            # Geometría de la tabla (distinta en función del informe seleccionado)
            if campo == "NombreTarea":
                self.ui.tableWidgetInformes.setHorizontalHeaderLabels(("Tag","Tarea","Inicio","Fin","Tiempo"))
                self.ui.tableWidgetInformes.setColumnWidth(0,100) # ancho columna Tag
                self.ui.tableWidgetInformes.setColumnWidth(1,190) # ancho columna Tarea
            else: #campo == "Tag" or "TodasTareas"
                self.ui.tableWidgetInformes.setHorizontalHeaderLabels(("Tarea","Tag","Inicio","Fin","Tiempo"))
                self.ui.tableWidgetInformes.setColumnWidth(0,190) # ancho columna Tarea
                self.ui.tableWidgetInformes.setColumnWidth(1,100) # ancho columna Tag
            
            self.ui.tableWidgetInformes.setColumnWidth(2,150) # ancho columna HoraInicio
            self.ui.tableWidgetInformes.setColumnWidth(3,150) # ancho columna HoraFin
            self.ui.tableWidgetInformes.setColumnWidth(4,80) # ancho columna Tiempo
            self.ui.tableWidgetInformes.resizeRowsToContents() # ajuste alto de fila a su contenido
            self.ui.tabWidgetTareas.update()
            #self.ui.tableWidgetInformes.horizontalHeaderItem().setTextAlignment(AlignHCenter)

        except Error as e:
            QMessageBox.about(self, "Información", str(e))
        finally:
            conn.close()

    def Exportar(self):
        # Exportar datos del informe actualmente seleccionado, a un archivo de texto .csv (el csv lo hago yo a pelo, no uso ningún import...es tan simple...)
        # Primero intentamos acceder al atributo de clase self.queryInformes, que no existirá si no se ha ejecutado antes un informe
        # esto lo hago así para evitar que se pulse el botón exportar sin haber generado previamente un informe
        try: 
            if self.queryInformes:
                pass
            # preguntamos al usuario dónde y con que nombre guardar el archivo de datos.
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fichero, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Text Files (*.csv)", options=options)
            if fichero:
                #print(fichero) # nos devuelve la ruta completa + nombre de archivo
                try: # si ya se ha ejecutado el informe, iniciamos la conexión a la BD.
                    conn = sqlite3.connect(BaseDeDatos)
                    cur = conn.cursor()
                    cur.execute(self.queryInformes, self.tuplaQuery)
                    registros = cur.fetchall()
                    nombresDeCampo = [description[0] for description in cur.description] # estos son los nombres de los campos que van a ir en el encabezado del fichero
                    totalReg = len(registros) # total de registros de la query
                    recNum = 0
                    contenidoFichero = "" # aqui es donde vamos a meter todo lo que vamos a escribir en el fichero
                    for jj in nombresDeCampo: # añadimos una primera fila con los nombres de los campos
                        contenidoFichero += jj + "\t" # usamos el tabulador como delimitador de campos
                    contenidoFichero += "\n"
                    for fila in registros: # recorremos todos los registros
                        #for campo in registro: # recorremos todos los campos
                        for campo, valor in zip(nombresDeCampo, fila): # accedo mejor a través de los nombres de los campos para saber cuando llego a la columna Total
                            print(campo, str(valor))
                            if campo == "Total": # si es el campo Total (el total de segundos), lo convertimos a formato humano hh:mm:ss
                                contenidoFichero += str(MiTimer.seconds_time_to_human_string(self, valor)) + "\t"
                            else:
                                contenidoFichero += str(valor) + "\t" # delimitamos los campos con un tabulador
                        contenidoFichero += "\n" # nueva línea
                        recNum += 1
                    # ahora guardamos fichero
                    with open(fichero, "wt") as fiche:
                        fiche.write(contenidoFichero)
                    QMessageBox.about(self, "Información", "Informe exportado en:\n" + fichero)
                except Error as e:
                    self.ui.statusbar.showMessage(str(e), 10000)
                    print(str(e))
                finally:
                    conn.close()
                    self.ui.statusbar.showMessage("Exportados ", 5000)
            else:
                print("Guardar fichero: cancelado") # si el usuario cancela

        except AttributeError:
            QMessageBox.about(self, "Información", str(AttributeError))


    def ActualizarLista(self, miQuery, miCampo):
        # Es para actualizar el listWidget, sólo para el registro-campo especificado.
        pass

    def Recargar(self):
        # Vacía y vuelve a cargar la lista de tareas a partir de la BD.
        if MiTimer.numCronosActivos > 0:
            QMessageBox.about(self, "Información", "Para poder recargar la lista de Tareas, no puede haber ningún Crono activo. \
                                                    \nPulsa Stop, guarda el Crono, modifica Tarea y vuelve a iniciarla.")
        else:        
            self.ui.listWidgetTareas.clear()
            self.MostrarTabla("SELECT * FROM Tareas WHERE Mostrar = 1 ORDER BY FechaAlta DESC, IDTarea DESC;", ()) # le pasamos una tupla vacía
    
    def ComprobarBD(self, ahora):
        # Chequeo inicial de la BD.: se comprueba que si hay un campo FechaHoraIni con datos, no haya uno FechaHoraFin sin ellos, y si lo hay igualar ambas fechas
        # Esto puede suceder si durante el funcionamiento de un crono, el usuario sale de la app. sin más, lo que después puede provocar un error en los listados.
        # Ya he tomado medidas para que esto no pase, pero por si las moscas...
        try:
            conn = sqlite3.connect(BaseDeDatos)
            cur = conn.cursor()
            if ahora == "":
                miQuery = "UPDATE DetalleTareas SET FechaHoraFin = FechaHoraInicio WHERE FechaHoraFin is null"
                cur.execute(miQuery)
            else:
                miQuery = "UPDATE DetalleTareas SET FechaHoraFin = ? WHERE FechaHoraFin is null"
                cur.execute(miQuery, (ahora,))
            conn.commit()
        except Error as e:
            self.ui.statusbar.showMessage(str(e), 10000)
            print(str(e))
        finally:
            conn.close()

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
    
    def closeEvent(self, event):
        # Si el usuario cierra en la X la aplicación, le pedimos confirmación sólo si hay un crono activo. 
        # Si no, pues nada que objetar...(no le voy a andar tocando los webos para confirmar que quiere cerrar, ya, sin preguntas, la aplicación)
        if MiTimer.hayUnCronoActivo: # si además hay un crono activo, se lo advertimos
            advertencia = "Atención: hay un Crono que sigue activo\n\n"

            buttonReply = QMessageBox.question(self, 'Salir de la aplicación', advertencia + "¿Quieres salir de CronoTareas?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if buttonReply == QMessageBox.Yes:
                ahora = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                self.ComprobarBD(ahora) # hacemos una depuración por si queda una fechafin sin poner y le ponemos la actual.
                event.accept()
            else:
                event.ignore()
    
    def MuestraCreditos(self, jj):
        QMessageBox.about(self, "Información", 
                            "Fer ha hecho esta simple aplicación \
                            \ndonanpher@gmail.com \
                            \nAbril 2020 (durante la cuarentena del: \
                            \n#Coronavirus #SARS-CoV-2 #Covid-19)")
        
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
                        Crono       TEXT (20),  \
                        Mostrar     INTEGER   DEFAULT (1) \
                    );"
            cur.execute(laQuery)
            conn.commit()
            # Creamos la tabla DetalleTareas
            laQuery = "CREATE TABLE DetalleTareas ( \
                        IDDetalle       INTEGER   PRIMARY KEY AUTOINCREMENT \
                                                UNIQUE \
                                                NOT NULL, \
                        IDTarea         INTEGER   REFERENCES Tareas (IDTarea) ON DELETE CASCADE \
                                                NOT NULL, \
                        FechaHoraInicio TEXT (20), \
                        FechaHoraFin    TEXT (20)  \
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
                              FechaHoraFin \
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
    # Este custom dialog lo uso para dar de alta una tarea o para modificarla
    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Añadir Tarea")
        self.miLabelIDDialog = QLabel("ID: ")
        self.miEtiqueta = QLabel("Nombre de la Tarea")
        self.miLineEditTareaDialog = QLineEdit("")
        self.miLineEditTareaDialog.setMaxLength(30)
        self.miEtiqueta2 = QLabel("Tag de la Tarea")
        self.miLineEditTagDialog = QLineEdit("")
        self.miLineEditTagDialog.setMaxLength(20)
        self.miEtiquetaDias = QLabel("Días")
        self.miSpinDias = QSpinBox()
        self.miEtiquetaHoras = QLabel("Horas")
        self.miTimeEditHoras = QTimeEdit()
        self.miTimeEditHoras.setDisplayFormat("HH:mm:ss")
        self.miCheckArchivada = QCheckBox("Tarea archivada")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.miLabelIDDialog)
        self.layout.addWidget(self.miEtiqueta)
        self.layout.addWidget(self.miLineEditTareaDialog)
        self.layout.addWidget(self.miEtiqueta2)
        self.layout.addWidget(self.miLineEditTagDialog)
        self.layout.addWidget(self.miEtiquetaDias)
        self.layout.addWidget(self.miSpinDias)
        self.layout.addWidget(self.miEtiquetaHoras)
        self.layout.addWidget(self.miTimeEditHoras)
        self.layout.addWidget(self.miCheckArchivada)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

class CustomDialogBuscar(QDialog):
    # Este custom dialog lo uso para Buscar Tareas.
    def __init__(self, *args, **kwargs):
        super(CustomDialogBuscar, self).__init__(*args, **kwargs)
        self.setWindowTitle("Buscar Tareas")
        self.miEtiqueta = QLabel("Seleccionar campo donde buscar:")
        self.miComboCampos = QComboBox()
        self.miComboCampos.addItem("Tarea")
        self.miComboCampos.addItem("Tag")
        self.miEtiqueta2 = QLabel("Texto a buscar:")
        self.miLineEditBuscar = QLineEdit("")
        self.miLineEditBuscar.setMaxLength(20) #***CONTINUAR AQUI: CAMBIAR AQUI EN FUNCIÓN DEL CAMPO SOBRE EL QUE SE BUSQUE

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.miEtiqueta)
        self.layout.addWidget(self.miComboCampos)
        self.layout.addWidget(self.miEtiqueta2)
        self.layout.addWidget(self.miLineEditBuscar)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class CustomDialogInformes(QDialog):
    # Este custom dialog lo uso pedir datos para los informes
    def __init__(self, *args, **kwargs):
        super(CustomDialogInformes, self).__init__(*args, **kwargs)
        self.setWindowTitle("Introducir datos para Informe")
        self.miEtiqueta = QLabel()
        self.miCombo = QComboBox()
        
        # esto lo hago así porque no sé como pasarle argumentos al CustomDialog.
        informe = w.ui.comboBoxInformes.itemText(w.ui.comboBoxInformes.currentIndex())
        if informe[:2] == "01": # Detalle de Tareas por Tag
            campo = "Tag"
        else: # Detalle de Tareas por Tarea
            campo = "NombreTarea"

        listaDeTags = self.CargarElementos(campo)
        if len(listaDeTags) > 0:
            for elemento in listaDeTags:
                self.miCombo.addItem(elemento)

            QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            
            self.buttonBox = QDialogButtonBox(QBtn)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

            self.layout = QVBoxLayout()
            self.layout.addWidget(self.miEtiqueta)
            self.layout.addWidget(self.miCombo)
            self.layout.addWidget(self.buttonBox)
            self.setLayout(self.layout)
        else:
            QMessageBox.about(self, "Información", "No hay ningún Tag en la Base de Datos.")
    
    def CargarElementos(self, campo):
        # Lo uso en Informes para cargar el Combo con los Tags distintos que haya en la BD.
        listaValores = []
        try:
            conn = sqlite3.connect(BaseDeDatos)
            cur = conn.cursor()
            miQuery = "SELECT DISTINCT(" + campo + ") FROM Tareas ORDER BY " + campo
            cur.execute(miQuery)
            registros = cur.fetchall()
            totalReg = len(registros) # total de registros de la query
            if totalReg > 0:
                for registro in registros:
                    listaValores.append(registro[0]) # añadimos cada registro a la lista
        except Error as e:
            self.ui.statusbar.showMessage(str(e), 10000)
        finally:
            conn.close()
            return listaValores


class CustomDialogInformes2(QDialog):
    # Este custom dialog lo uso pedir datos para el informe3 que pide fechas desde-hasta
    def __init__(self, *args, **kwargs):
        super(CustomDialogInformes2, self).__init__(*args, **kwargs)
        self.setWindowTitle("Introducir datos para Informe")
        self.labelFechaDesde = QLabel("Fecha Desde")
        self.fechaDesde = QDateEdit()
        self.fechaDesde.setDisplayFormat("yyyy-MM-dd")
        self.fechaDesde.setDate(QtCore.QDate.currentDate())
        self.labelFechaHasta = QLabel("Fecha Hasta")
        self.fechaHasta = QDateEdit()
        self.fechaHasta.setDisplayFormat("yyyy-MM-dd")
        self.fechaHasta.setDate(QtCore.QDate.currentDate())

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.labelFechaDesde)
        self.layout.addWidget(self.fechaDesde)
        self.layout.addWidget(self.labelFechaHasta)
        self.layout.addWidget(self.fechaHasta)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class MiTimer(QWidget):
    # MiTimer es cada uno de los listItems (filas) que hay en el listWidget. Se instancia tantas veces como tareas haya en la lista.
    # A su vez, cada listItem se compone de varios widgets: 
    # el ID, la Tarea, el Tag, botón Iniciar/Pausar/Continue, botón Reset, el LCDDisplay (Crono) y labelCrono (un duplicado del Crono).
    hayUnCronoActivo = False # para controlar si hay activo algún crono y poder permitir un segundo o no en función del checkbox
    # mismo tema anterior pero para solucionar el tema de que estando desmarcado el check (permitir varios cronos),
    # si se marca el check de no permitir, se descontrola el tema
    # lo que trato de hacer ahora es que, si se permiten varios cronos + se inicia más de un crono, entonces deshabilito el check.
    numCronosActivos = 0 
    lucesDuenho = 0 # para que sólo un Crono pueda llevar este control (el dueño es el ID del Crono que tiene el control)
    visibilidadLuz = False # para controlar la visibilidad de la luz

    # esta es la linea (WidgetItem), con la colección de widgets (dentro de un QHBoxLayout), que se pinta dentro de la lista.
    def __init__(self, miID, miTarea, miTag, miCrono, miLabelCrono, miMostrar, parent=None):
        super(MiTimer, self).__init__(parent)
        self.miID = miID
        self.miTarea = miTarea
        self.miTag = miTag
        self.miCrono = miCrono
        self.miLabelCrono = miLabelCrono
        self.miMostrar = miMostrar
        self.altoWidgets = 25
        self.anchoBotones = 75
        self.haSidoAdvertido = False # esto es para cuando se sobrepasa el límite teórico del Crono, en que muestro una advertencia (ver showlcd())
        # self.tiempoActual = QtCore.QTime(0,0,0)
        self.tiempoActual2Ini = datetime.now()
        self.tiempoActual2Fin = datetime.now()
        self.segundosAcumulado = 0.0 # cuando se hace una pausa, hay que guardar aqui el tiempo transcurrido hasta ese momento para sumarselo después a la reanudación.
        #self.tiempoFinal = QTime(0,0,0)
        self.timer = QtCore.QTimer(self)
        
        # Widgets del itemWidget (elementos de cada fila de la lista)
        #---------------------------------------------------
        self.IDTarea = QLabel(self.miID)
        self.IDTarea.setFrameShape(QFrame.StyledPanel)
        self.IDTarea.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.IDTarea.setFixedWidth(32)
        #---------------------------------------------------
        self.NombreTarea = QLabel(self.miTarea)
        self.NombreTarea.setFrameShape(QFrame.StyledPanel)
        #---------------------------------------------------
        self.Tag = QLabel(self.miTag)
        self.Tag.setFrameShape(QFrame.StyledPanel)
        self.Tag.setFixedWidth(self.anchoBotones + 20)
        #---------------------------------------------------
        self.botonIniciar= QPushButton("Start")
        self.botonIniciar.setFixedWidth(self.anchoBotones + 15)
        self.icon1 = QtGui.QIcon()
        self.icon1.addPixmap(QtGui.QPixmap(":/miprefijo/images/play.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.botonIniciar.setIcon(self.icon1)        
        self.botonIniciar.clicked.connect(self.IniciarCrono)
        #---------------------------------------------------
        # Pensé que iba a necesitar Threads, pero parece que no hacen falta (una complicación menos!)
        #t = Thread(target=self.IniciarCrono)
        #t.start()
        self.botonParar= QPushButton(" Stop")
        self.icon2 = QtGui.QIcon()
        self.icon2.addPixmap(QtGui.QPixmap(":/miprefijo/images/guardar1.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.botonParar.setIcon(self.icon2)        
        self.botonParar.setFixedWidth(self.anchoBotones)
        self.botonParar.clicked.connect(self.PararCrono)
        self.botonParar.setEnabled(False)
        self.botonParar.setToolTip('<b>Para el Crono</b> y también pregunta si se desea <b>Guardar su estado</b>,<br>o Resetearlo.')
        #---------------------------------------------------
        self.miSegundoDisplay = QLCDNumber()
        self.miSegundoDisplay.setDigitCount(12)
        self.miSegundoDisplay.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.miSegundoDisplay.setFixedWidth(self.anchoBotones + 80)
        self.miSegundoDisplay.setFixedHeight(30)
        self.miSegundoDisplay.display(self.miCrono)
        #---------------------------------------------------
        # Añado un label que va a contener lo mismo que el Crono, pero no va a ser visible.
        # El motivo es para poder acceder a su valor, porque no consigo acceder al valor del Crono, ni con .value ni con hostias benditas...
        self.labelCrono = QLabel(self.miLabelCrono)
        self.labelCrono.setVisible(False) # oculto este label, porque sólo lo tengo para acceder a su información, que es la misma que el crono.
        #self.labelCrono.setFrameShape(QFrame.StyledPanel)
        #---------------------------------------------------
        # Este label es el que indica si una tarea está archivada o no (pero lo ponemos oculto)
        self.labelMostrar = QLabel(self.miMostrar)
        self.labelMostrar.setVisible(False)
        #---------------------------------------------------
        #self.showlcd()
        self.timer.timeout.connect(self.showlcd) # método que se ejecuta con cada Timer (1 seg.)
        self.miLayOut = QHBoxLayout()
        self.miLayOut.addWidget(self.IDTarea)
        self.miLayOut.addWidget(self.NombreTarea)
        self.miLayOut.addWidget(self.Tag)
        self.miLayOut.addWidget(self.botonIniciar)
        self.miLayOut.addWidget(self.botonParar)
        self.miLayOut.addWidget(self.miSegundoDisplay)
        self.miLayOut.addWidget(self.labelCrono)
        self.miLayOut.addWidget(self.labelMostrar)
        self.setLayout(self.miLayOut)

    def IniciarCrono(self):
        # La idea de todo esto es que si se está en modo monocrono, sólo se pueda tener activo uno, los que están en pausa no están activos.
        # En el modo multicrono, se permite que estén activos todos los cronos que se quieran.
        # Lo que no se puede dar es que, si se está en modo multicrono y con varios cronos activos, se pueda pasar al modo monocrono.
        # Condición: (telita lo que me costó llegar a ella...)
        # Si se permiten varios cronos simultáneos, o si no se permiten pero que sólo haya uno activo o que el pulsado sea de Pausa o Continuar
        # (sólo esta condición me llevó un buen rato elaborarla)
        if (w.PermitirCronosSimultaneos) or (
            (not w.PermitirCronosSimultaneos) and (
                (not MiTimer.hayUnCronoActivo) or (self.botonIniciar.text() == "Pause") # or (self.botonIniciar.text() == "Continuar") # tenía puesto este OR
                )
            ):
            # en qué modo se pincha el botón iniciar? (Start|Pause|Continue)
            if self.botonIniciar.text() == "Start":
                self.timer.start(1000) # pongo en marcha el Timer
                # --- pijada de las luces ---
                # asigno el ID de Tarea actual como dueño del control de las luces rojas
                if self.lucesDuenho == 0: 
                    self.lucesDuenho = int(self.IDTarea.text())
                    w.ui.label_Punto1.setVisible(True) # enciendo la luz
                # ---------------------------
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
                self.miSegundoDisplay.setStyleSheet("QLCDNumber {color: red;}")
                self.icon3 = QtGui.QIcon()
                self.icon3.addPixmap(QtGui.QPixmap(":/miprefijo/images/pause.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.botonIniciar.setText("Pause")
                self.botonIniciar.setIcon(self.icon3)    
                self.botonParar.setEnabled(False) # deshabilitamos el botón Stop
                # guardamos el momento actual en la tabla DetalleTareas
                self.GuardarParcialCrono(int(self.IDTarea.text()), datetime.strftime(self.tiempoActual2Ini, "%Y-%m-%d %H:%M:%S"), 1)
            elif self.botonIniciar.text() =="Pause":
                self.timer.stop() # detengo el timer
                MiTimer.hayUnCronoActivo = False
                # --- pijada de las luces ---
                # si este Crono estaba llevando el control de la luces, pues ya no.
                if self.lucesDuenho == int(self.IDTarea.text()): 
                    self.lucesDuenho = 0 
                    w.ui.label_Punto1.setVisible(False) # apago la luz
                # ---------------------------
                self.icon4 = QtGui.QIcon()
                self.icon4.addPixmap(QtGui.QPixmap(":/miprefijo/images/continue.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.botonIniciar.setText("Continue")
                self.botonIniciar.setIcon(self.icon4)        
                self.miSegundoDisplay.setStyleSheet("QLCDNumber {color: green;}")
                # al hacer una pausa, hay que guardar los segundos transcurridos hasta este momento para añadirselos al reanudar el crono
                self.tiempoActual2Fin = datetime.now()
                self.segundosAcumulado += (self.tiempoActual2Fin - self.tiempoActual2Ini).seconds
                self.botonParar.setEnabled(True) # deshabilitamos el botón Stop  
                # guardamos el momento actual en la tabla DetalleTareas
                self.GuardarParcialCrono(int(self.IDTarea.text()), datetime.strftime(self.tiempoActual2Fin, "%Y-%m-%d %H:%M:%S"), 2)
            else: # self.botonIniciar.text() == Continue":
                self.timer.start(1000) # reanudo el Timer que estaba en pausa
                MiTimer.hayUnCronoActivo = True
                self.tiempoActual2Ini = datetime.now()
                # --- pijada de las luces ---
                # asigno el ID de Tarea actual como dueño del control de las luces rojas (si no está en uso)
                if self.lucesDuenho == 0: 
                    self.lucesDuenho = int(self.IDTarea.text()) 
                    w.ui.label_Punto1.setVisible(True) # enciendo la luz
                # ---------------------------
                # self.miDisplay.setStyleSheet("QLCDNumber {color: red;}")
                self.miSegundoDisplay.setStyleSheet("QLCDNumber {color: red;}")
                self.icon3 = QtGui.QIcon()
                self.icon3.addPixmap(QtGui.QPixmap(":/miprefijo/images/pause.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.botonIniciar.setText("Pause")
                self.botonIniciar.setIcon(self.icon3)
                self.botonParar.setEnabled(False) # habilitamos el botón Stop
                # guardamos el momento actual en la tabla DetalleTareas
                self.GuardarParcialCrono(int(self.IDTarea.text()), datetime.strftime(self.tiempoActual2Ini, "%Y-%m-%d %H:%M:%S"), 3)

        else:
            QMessageBox.about(self, "Información", "No se puede activar más de un Crono a la vez." \
                                + "\nPuedes activar esta opción en la pantalla principal.")

        # Si el check está en modo monocrono, se deja habilitado para permitir conmutar a modo multicrono
        # Si el check está en modo multicrono, se deshabilita si hay más de un crono activo
        # ***PENDIENTE: Pendiente de comprobar más a fondo toda la casuística ... (no sé todavía si podría quedar algún resquicio por el que me puedan romper el tema)
        if w.PermitirCronosSimultaneos: # modo multicrono
            if MiTimer.numCronosActivos > 1:
                w.ui.checkBoxMultiCrono.setEnabled(False)
            else:
                w.ui.checkBoxMultiCrono.setEnabled(True)
        else: # modo monocrono
                w.ui.checkBoxMultiCrono.setEnabled(True)

    def PararCrono(self):
        # Botón Stop: se pone a cero, pero preguntamos si desea guardar este crono para más adelante
        MiTimer.hayUnCronoActivo = False # los en pausa no se consideran activos
        MiTimer.numCronosActivos -= 1 # restamos 1 al número de cronos activos (los en pausa sí que se consideran activos en este caso)
        if MiTimer.numCronosActivos < 0:
            MiTimer.numCronosActivos = 0
        
        self.timer.stop()

        self.miSegundoDisplay.setStyleSheet("QLCDNumber {color: black;}")
        
        cadena2 = self.seconds_time_to_human_string(self.segundosAcumulado)
        # Preguntamos si se desea guardar el estado actual del crono para un uso posterior.
        buttonReply = QMessageBox.question(self, 'Guardar Crono Actual', "¿Quieres guardar el estado actual de este Crono?:\n" 
                                             + cadena2, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # Si queremos guardar el estado actual para seguir en otra ocasión
        if buttonReply == QMessageBox.Yes:
            # guardamos en BD. el estado de este crono.
            self.GuardarEstadoCrono(cadena2)
            self.miCrono = cadena2
            #self.miSegundoDisplay.display(self.seconds_time_to_human_string(self.segundosAcumulado))
            #self.labelCrono.setText(self.seconds_time_to_human_string(self.segundosAcumulado))
        else: # No se desea guardar el estado de este crono
            # también guardamos, pero puesto a cero
            self.GuardarEstadoCrono(self.seconds_time_to_human_string(0))
            self.miCrono = "00:00:00"
            # Ponemos todo a cero
            self.segundosAcumulado = 0
            self.miSegundoDisplay.display(self.seconds_time_to_human_string(self.segundosAcumulado))
            self.labelCrono.setText(self.seconds_time_to_human_string(self.segundosAcumulado))
        
        self.Pausa = False
        self.botonIniciar.setText("Start")
        self.botonIniciar.setIcon(self.icon1)
        self.botonParar.setEnabled(False) # deshabilitamos el botón Reset

        self.icon1 = QtGui.QIcon()
        self.icon1.addPixmap(QtGui.QPixmap(":/miprefijo/images/play.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.miSegundoDisplay.setStyleSheet("QLCDNumber {color: black;}") ###########################

        # si hay más de un crono activo, deshabilito el check (para evitar inconsistencias)
        if MiTimer.numCronosActivos > 1:
            w.ui.checkBoxMultiCrono.setEnabled(False)
        else:
            w.ui.checkBoxMultiCrono.setEnabled(True)
    
    def GuardarEstadoCrono(self, elCrono):
        try:
            # modificamos en la BD.
            conn = sqlite3.connect(BaseDeDatos)
            cur = conn.cursor()
            #miQuery = "UPDATE Tareas SET Crono = '" + elCrono + "' WHERE IDTarea = " + self.IDTarea.text()
            miQuery = "UPDATE Tareas SET Crono = ? WHERE IDTarea = ?"
            cur.execute(miQuery, (elCrono, self.IDTarea.text(),))
            conn.commit()
            # ahora borramos todo el contenido del listWidget para volver a cargarlo con los datos actualizados
            #w.ui.listWidgetTareas.clear()
            #w.MostrarTabla("SELECT * FROM Tareas ORDER BY FechaAlta DESC, IDTarea DESC;")
            w.ui.statusbar.showMessage("Crono guardado", 5000)
        except Error as e:
            w.ui.statusbar.showMessage(str(e), 5000)
            QMessageBox.about(self, "Información", str(e))
        finally:
            conn.close()

    def showlcd(self):
        # Esto es lo que se ejecuta con cada evento TimeOut del Timer (1 seg.)
        self.tiempoActual2Fin = datetime.now()
        self.totalSegundos = (self.tiempoActual2Fin - self.tiempoActual2Ini).seconds + self.segundosAcumulado
        
        # --- pijada de las luces ---
        # si somos el dueño de las luces, somos quien tenemos el control de ellas
        if self.lucesDuenho == int(self.IDTarea.text()):
            w.ui.label_Punto1.setVisible(self.visibilidadLuz)
            self.visibilidadLuz = not self.visibilidadLuz
        # si no somos dueños de la luz, en cualquier momento podemos pasar a serlo, cuando se pare el crono que llevaba el control
        elif self.lucesDuenho == 0: # asigno el ID de Tarea actual como dueño del control de las luces rojas
            self.lucesDuenho = int(self.IDTarea.text())
            w.ui.label_Punto1.setVisible(True) # enciendo la luz
        # ---------------------------

        # Si se llega al supuesto límite del LCDDisplay ('99D 23:59:59' = 8.639.999 seg), muestro un mensaje y pregunto si desea continuar
        if (self.totalSegundos >= 8639999) and (not self.haSidoAdvertido): # '99D 23:59:59'
            self.haSidoAdvertido = True
            # Para empezar, detengo el Crono
            self.timer.stop()
            MiTimer.hayUnCronoActivo = False
            self.icon4 = QtGui.QIcon()
            self.icon4.addPixmap(QtGui.QPixmap(":/miprefijo/images/continue.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.botonIniciar.setText("Continue")
            self.botonIniciar.setIcon(self.icon4)        
            self.miSegundoDisplay.setStyleSheet("QLCDNumber {color: green;}")
            # al hacer una pausa, hay que guardar los segundos transcurridos hasta este momento para añadirselos al reanudar el crono
            self.tiempoActual2Fin = datetime.now()
            self.segundosAcumulado += (self.tiempoActual2Fin - self.tiempoActual2Ini).seconds
            self.botonParar.setEnabled(True) # deshabilitamos el botón Stop  

            # llamamos a un diálogo de Aceptar/Cancelar para confirmar eliminación
            textoMostrar = "Estás a punto de cruzar un límite no explorado.\n"
            textoMostrar += "Esta Tarea lleva: 2.400 horas!\n"
            textoMostrar += "Más alla de esto, no he probado el Crono,\n"
            textoMostrar += "puede que siga funcionando sin problemas,\n"
            textoMostrar += "pero lo dejo bajo tu responsabilidad.\n"
            textoMostrar += "Te recuerdo que la Jornada Anual de Trabajo\n"
            textoMostrar += "en España es de +/- 1.800 horas. \n"
            textoMostrar += "¿De verdad no puedes crear subtareas?\n"
            textoMostrar += "En fin, tú mismo...\n"
            textoMostrar += "\n"
            textoMostrar += "¿Deseas continuar?"
            buttonReply = QMessageBox.question(self, 'Advertencia!', textoMostrar , QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # Si quiere seguir adelante, pues avanti...
            if buttonReply == QMessageBox.Yes:
                self.timer.start(1000) # reanudo el Timer que estaba en pausa
                MiTimer.hayUnCronoActivo = True
                self.tiempoActual2Ini = datetime.now()
                # self.miDisplay.setStyleSheet("QLCDNumber {color: red;}")
                self.miSegundoDisplay.setStyleSheet("QLCDNumber {color: red;}")
                self.icon3 = QtGui.QIcon()
                self.icon3.addPixmap(QtGui.QPixmap(":/miprefijo/images/pause.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.botonIniciar.setText("Pause")
                self.botonIniciar.setIcon(self.icon3)
                self.botonParar.setEnabled(False) # habilitamos el botón Reset    

        # Este es el Crono que se muestra en pantalla (y el oculto)
        self.miSegundoDisplay.display(self.seconds_time_to_human_string(self.totalSegundos))
        self.labelCrono.setText(self.seconds_time_to_human_string(self.totalSegundos))

    def GuardarParcialCrono(self, idtarea, tiempo, accion):
        # Guardamos en la tabla DetalleTareas, cada vez que se inicia, pausa, reanuda y detiene un crono.
        # Esto es para la pestaña de Informes, para poder sacar listados detallados de toda la actividad.
        # Soy consciente de que pueden producirse descuadres, porque al permitir poder modificar un crono,
        # se puede poner lo que se quiera y ya no coincidirá con la realidad, pero eso lo dejo a criterio
        # del usuario de la aplicación.
        # Las acciones son: 1=Start, 2=Pause, 3=Continue
        try:
            # modificamos en la BD.
            conn = sqlite3.connect(BaseDeDatos)
            cur = conn.cursor()
            if accion == 1 or accion == 3: # si es Start o Continue, damos de alta un nuevo registro
                #miQuery = "INSERT INTO DetalleTareas (IDTarea, FechaHoraInicio) VALUES (" + str(idtarea) + ", '" + tiempo + "')"
                miQuery = "INSERT INTO DetalleTareas (IDTarea, FechaHoraInicio) VALUES (?, ?)"
                cur.execute(miQuery, (str(idtarea), tiempo,))
            else: # es una pausa, por lo tanto hay que actualizar el último registro introducido
                #miQuery = "SELECT Max(IDDetalle) FROM DetalleTareas WHERE IDTarea = " + str(idtarea)
                miQuery = "SELECT Max(IDDetalle) FROM DetalleTareas WHERE IDTarea = ?"
                cur.execute(miQuery, (str(idtarea),))
                elRegistro = cur.fetchone()
                elID = elRegistro[0]              
                #miQuery = "UPDATE DetalleTareas SET FechaHoraFin = '" + tiempo + "' WHERE IDDetalle =" + str(elID)
                miQuery = "UPDATE DetalleTareas SET FechaHoraFin = ? WHERE IDDetalle = ?"
                cur.execute(miQuery, (tiempo, str(elID),))
            
            conn.commit()
        except Error as e:
            w.ui.statusbar.showMessage(str(e), 5000)
            QMessageBox.about(self, "Información", str(e))
        finally:
            conn.close()
    
    """
    WARNING!!!
    GENERAL FAILURE READING HARD DISK!
    (...)
    ¿Quién coño es el General Failure, y qué hace leyendo mi disco duro?
    (...)
    """
    
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
    w = AppWindow(sys.argv) # le pasamos los argumentos al init
    w.show()
    qApp.processEvents() # esto lo añado para poder ejecutar el argumento pasado (poner en marcha un crono directamente en el inicio de la app)
    # https://stackoverflow.com/questions/46739079/execute-long-running-code-at-program-startup-after-complete-gui-is-rendered
    # Si se inicia la app. con argumentos, es el ID de la Tarea que hay que poner en marcha directamente.
    if len(sys.argv) > 1:
        idEjecutar = sys.argv[1]
        w.PonerEnMarchaTarea(idEjecutar)

    sys.exit(app.exec_())


"""
#
﻿#                         ''~``
#                        ( o o )
#+------------------.oooO--(_)--Oooo.------------------+
#|                                                     |
#|                                                     |
#|                  Fernando Souto                     |
#|               donanpher@gmail.com                   |
#|                    Abril 2020                       |
#|                                                     |
#|                    .oooO                            |
#|                    (   )   Oooo.                    |
#+---------------------\ (----(   )--------------------+
#                       \_)    ) /
#                             (_/
#
"""
