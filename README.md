<h1> CronoTareas </h1>  

![Python GPLv3](https://img.shields.io/badge/Python-v3.6.7-success) ![PyQt v5](https://img.shields.io/badge/PyQt-5-brightgreen) ![SQLite v3](https://img.shields.io/badge/SQLite-v.3-blueviolet) ![License GPLv3](https://img.shields.io/badge/License-GPLv3-red) 

## Cronometra la duración de tus Tareas.  
## <span style="color:grey"><i>Time the duration of your Tasks</i></span>
Hecha en Python 3.6.7 + PyQt5 + SQLite 3  
Versión para Linux, testada únicamente en Ubuntu Budgie 18.04.4 LTS  
<span style="color:grey">
<i>Made with Python 3.6.7 + PyQt5 + SQLite 3</i>  
<i>Linux version, tested only on Ubuntu Budgie 18.04.4 LTS</i>  
</span>  
Fernando Souto (donanpher@gmail.com)  
A Coruña (Galicia), Spain  
Abril 2020 (durante la cuarentena del #Coronavirus #SARS-CoV-2 #Covid-19)  
<span style="color:grey"><i>April 2020 (during the #Coronavirus # SARS-CoV-2 # Covid-19 quarantine)</i></span>  

---
![Screenshot](./images/Screenshot_CronoTareas.png)
---
## Instalación en Linux <span style="color:grey"><i>(Linux installation)</i></span>
* <a href="https://drive.google.com/file/d/1cgRqV5Qgp4uzodVLaAUIhtPUVwQF5riE/view?usp=sharing">Descargar CronoTareas.zip (46 MB)</a>
* Descomprimelo en una nueva carpeta, por ejemplo /opt/cronotareas/
* Ejecuta CronoTareas
---
* <span style="color:grey"><i><a href="https://drive.google.com/file/d/1cgRqV5Qgp4uzodVLaAUIhtPUVwQF5riE/view?usp=sharing">Download CronoTareas.zip (46 MB)</a></i> </span>  
* <span style="color:grey"><i>Unzip it into a new folder, for example /opt/cronotareas/</i> </span>  
* <span style="color:grey"><i>Run CronoTareas</i> </span>  

## Descripción General <span style="color:grey"><i>(General Description)</i></span>
Aplicación para llevar el control de tiempo de distintas tareas.  
Se pueden añadir tantas tareas como se quiera, iniciarlas, pausarlas o detenerlas.  
<span style="color:grey"><i>Application to take time control on your tasks</i></span>  
<span style="color:grey"><i>You can add as many tasks as you want, start, pause, or stop them</i></span>  

### <b>Funciones:</b>  <span style="color:grey"><i>(Functions)</i></span>
* Botón `Start`: Inicia una tarea y guarda la fecha y hora de ese inicio.  
* Botón `Pause`: Pausa la tarea y guarda la fecha y hora de esa pausa.
* Botón `Continue`: Reanuda la tarea y guarda la fecha y hora de la reanudación.  
* Botón `Stop`: Detiene la tarea y pregunta si se desea guardar el estado actual del Crono para una continuación posterior.  
* Cada combinación de ('Start' + 'Pause') o ('Continue' + 'Pause') genera un tramo de tiempo que queda almacenado en la base de datos.  
* En la pestaña de Informes se pueden consultar todos estos tramos de tiempo.  
* La elección entre guardar el Crono o no, no tiene repercusión en los informes. Es sólo a efectos visuales.  
---
* <span style="color:grey"><i>Button `Start`: Starts a task and saves its date & time</i> </span>  
* <span style="color:grey"><i>Button `Pause`: Pauses the task and saves its date & time</i></span>  
* <span style="color:grey"><i>Button `Continue`: Resumes the task and save the date and time of the resume</i></span>  
* <span style="color:grey"><i>Button `Stop`: Stop the task and ask if you want to save the current state of the Chrono for a later continuation</i></span>  
* <span style="color:grey"><i>Each combination of ('Start' + 'Pause') or ('Continue' + 'Pause') generates a stretch of time that is stored in the database</i></span>  
* <span style="color:grey"><i>In the Reports tab (Informes) you can see all these time sections</i></span>  
* <span style="color:grey"><i>The choice between saving the Chrono or not has no impact on the reports. It is only for visual purposes.</i></span>  
  
### <b>Tareas/Tags:</b>  <span style="color:grey"><i>(Tasks/Tags)</i></span>
* Nombre de Tarea: Se refiere a una tarea particular y concreta dentro de un proyecto. Por ejemplo, elaborar documentación, codificar conexión a base de datos, etc.  
* Tag: Está a un nivel superior, se refiere al proyecto o cliente. Por ejemplo, Cliente X o Proyecto Y.  
Resumiendo: Los Tags incluyen Tareas.  
---
* <span style="color:grey"><i>Task Name: Refers to a particular and concrete task within a project. For example, preparing documentation, coding database connection, etc.</i></span>  
* <span style="color:grey"><i>Tag: It is at a higher level, it refers to the project or client. For example, Client X or Project Y</i></span>  
<span style="color:grey"><i>Summarizing: Tags include Tasks</i></span>  

### <b>Tipos de Tareas:</b> (<i>recomendaciones de uso</i>):  <span style="color:grey"><i>(Types of Tasks, recommendations of use)</i></span>
* Tareas recurrentes: Son tareas que se repiten en el tiempo, por ejemplo, ir a tomar un café. Al terminar la tarea, vuelvo a poner el crono a cero.  
* Tareas independientes: Son únicas y no se vuelven a repetir. En este tipo de tareas suelo guardar el crono para la siguiente vez, así veo continuamente el tiempo total acumulado.  
---
* <span style="color:grey"><i>Recurring tasks: These are tasks that are repeated over time, for example, going for a coffee. At the end of the task, I reset the clock to zero.</i></span>  
* <span style="color:grey"><i>Independent tasks: They are unique and do not happen again. In this type of tasks I usually save the chrono for the next time, so I can continuously see the total accumulated time</i></span>  

### <b>Cronómetros:</b>  <span style="color:grey">(<i>Chronometers (Timers)</i>)</span>
* La aplicación por defecto se inicia en modo mono-cronómetro, aunque se puede activar el modo multi-cronómetro en el checkbox.  
* Se pueden tener tantos cronómetros activos como se quiera.  
---
* <span style="color:grey"><i>The application by default starts in mono-chrono mode, although you can activate the multi-chrono mode at checkbox</i></span>  
* <span style="color:grey"><i>You can have as many timers (chronos) as you want</i></span>  

### <b>Informes:</b>  <span style="color:grey"><i>(Reports)</i></span>
* Los informes resumen se basan todos en los tramos de tiempo generados por cada inicio, pausa y reanudación del Cronómetro.  
* El estado del Cronómetro en ningún momento se tiene en cuenta para generar informes.  
* Dada la posibilidad que se tiene de modificar un crono, existe la posibilidad de un descuadre entre el tiempo total del crono y el tiempo que sale en los informes.  
No se recomienda la modificación de los cronos por este motivo, si se hace es sólo a efectos visuales.  
* Exportación de informes a archivo CSV.  
---
* <span style="color:grey"><i>Summary reports are all based on the time frames generated by each start, pause, and restart of the timer</i></span>  
* <span style="color:grey"><i>The status of the Timer (Chrono) is never taken into account when generating reports</i></span>  
* <span style="color:grey"><i>Given the possibility that you can to modify a chrono, there is the possibility of an imbalance between the total time of the chrono and the time that appears in the reports</i></span>  
* <span style="color:grey"><i>The modification of the chrono is not recommended for this reason, if you do so, is only for visual purposes</i></span>  
* <span style="color:grey"><i>Exporting reports to CSV file</i></span>  

---
## Versiones  

### 14-04-2020 [v.1.0] Funcionalidad básica
	La aplicación funciona correctamente, dándole buen uso, pero tiene inconsistencias a la hora de marcar/desmarcar el checkbox estando activos uno o varios de los cronos...(pendiente de corregir)
	
	- [x] Se crea una opción para permitir, o no, el funcionamiento de varios cronos simultaneos (por defecto lógicamente no,  porque "no se pueden hacer varias tareas simultanemente" pero por si se quiere, se habilita la opción.)

### 15-04-2020 [v.1.1] Nuevas características y corrección de errores
	- [x] Si durante el funcionamiento de varios cronos se deschecka el checkBox, este ya no surte efecto.
			Solución: deshabilitar checkBox durante el funcionamiento de varios cronos
	- [x] Al agregar tarea, se añade a la BD. la fecha y hora actuales
	- [x] Añadido botón para recargar toda la lista

### 16-04-2020 [v.1.2] Nuevas características y corrección de errores
	En esta versión, conviven 2 tipos de Crono: el basado en QTime (máx. 24 horas de registro) y el basado en DateTime (sin límites).
	Esta versión es de prueba, funcional pero no recomendable por la innecesidad de tener 2 cronos simultaneos, aparte tema estética...
	En la siguiente versión 1.3. quedará sólo el basado en DateTime.
	- [x] Mostrar total de tareas
	- [x] Cambio importante en el LCDDisplay: ahora el tiempo lo controlo con diferencias de datetime.now(), en vez de usar QTime.
		Esto supone que ahora ya no estoy limitado en el Display a 24 horas, sino que puedo mostrar días también.
		Yo no sabía que en un LCDDisplay se podía mostrar cualquier cosa. Fue gracias al descubrimiento de un Custom LCDDisplay el que me hizo ver la luz y motivarme a
		hacer el cambio, que además coincide con mi idea inicial de uso del DateTime. 
		Desde aqui agradezco este descubrimiento a Juan Carlos Paco (https://gist.github.com/juancarlospaco/c0fb15281d56dc6eb2f4)
		De este repositorio tomé la idea y le copio, con permiso y por comodidad, la función seconds_time_to_human_string() que convierte segundos a una 'lectura humana'.
	- [x] Se deshabilita el botón Reset mientras esté en funcionamiento un crono o mientra no se haya iniciado ninguno
	- [x] Se añade un label con el Total de Tareas
	- [x] Hacer la ventana de la aplicación fija en cuanto a tamaño, que no se pueda expandir ni contraer. También centrarla en el escritorio.
	- [x] Añadir ToolTips...  al botón Reset y al botón Recargar lista

### 16-04-2020 [v.1.3] Nuevas características y corrección de errores
	Versión totalmente operativa y funcional.
	Ya definitivamente se usa DateTime para controlar el tiempo
	Así mismo, también se guarda y se restaura el estado del Crono (al pulsar Reset y responder 'Sí' a guardar)
	- [x] Limpiar todo el código con restos del LCDDisplay que no uso. (sólo lo #comento, no lo elimino todavía hasta la v.1.4)
	- [X] Guardar estado de todos los cronos, fechas/horas de inicio/fin, etc. en BD.

### 19-04-2020 [v.1.4] Nuevas características y corrección de errores
	- [x] Botón Modificar ahora también permite modificar el Crono.
	- [x] Pongo el límite del tamaño de cada cada campo, en los LineEdit que se usan para modificar una tarea.
	- [x] Al hacer click en el logo, muestro un diálogo de créditos.
	- [x] Buscar el límite del Display, por lo pronto representa sin problemas '99D 23:59:59' incluso sigue sumando sin contratiempo.
			Eso supone un total de 8.639.999 seg. que, si sobrepasa eso, le muestro una advertencia.
	- [x] Ancheo la ventana para que quepa mejor todo.
	- [x] Cuando se quiere modificar una tarea, le pongo una máscara al line edit del crono, y esta máscara incluye, aunque sea, cero diás.
			Esto es así para permitir modificar una tarea de sólo horas añadiéndole días.
	- [x] Descarto el tema de la máscara y pongo un SpinBox (para los días) + un TimeEdit (para las horas)
	- [x] Botón Buscar para filtrar por Tarea o Tag...podría también filtrarse por Fecha Alta, pero no la estoy mostrarndo en el list...

### 21-04-2020 [v.1.5] Nuevas características y corrección de errores
	Esta nueva versión ya la considero bastante estable, con muchas mejoras y "libre de errores".
	- [x] Si se pulsa Buscar y hay un crono activo (en marcha o en pausa), se le advierte al usuario de que debe detenerlo antes (Stop).
	- [x] Cambio el nombre del botón 'Reset' por el de 'Stop' (y su icono), porque llevaba a confusión.  
			La idea de este botón, que sólo está habilitado cuando se hace una pausa, es la de que cuando se pulse,  
			se pregunta si se quiere guardar el estado actual para continuar en otro momento.  
			Si no se guarda, se pone a cero.
	- [x] Si un crono está activo, y se pulsa Modificar, saco una advertencia para que detenga el crono, después modifique y vuelva a inicialo.
	- [x] Al dar un alta, no recargo la lista, guardo el registro en BD. e inserto un item sin necesidad de recargar toda la lista.
	- [x] Creo un label con el mismo contenido que el Crono, pero oculto, para poder acceder más facilmente a dicha información.
	- [x] Fix!: GuardarEstadoTareas -> Si está en marcha un crono y se modifica la tarea, este se restaura: Arreglado, ya no!

### 23-04-2020 [v.1.6] Nuevas características y corrección de errores
	- [x] Guardar parciales de cada inicio parada del crono.
	- [x] Añado a la creación de la tabla DetalleTareas, la cláusula 'ON DELETE CASCADE', para que al eliminar una tarea, se elimine su detalle.
	- [x] Se me coló en la versión anterior (v.1.5), que el botón Eliminar quedó deshabilitado (el signal lo dejé conectado a otro slot de prueba)
	- [x] A pesar de tener puesto en la tabla DetalleTareas, la eliminación en cascada, no veo que funcione. Lo hago por código entonces.
	- [x] Desarrollar todo el tema de los Informes. Hecho, aunque no está del todo depurado: pasan cosas raras, como que si ejecuto un informe
			a veces no muestra el total de horas y minutos y otras veces sí, simplemente ejecutándolo por segunda vez. ¡¿!?

### 25-04-2020 [v.1.7] Nuevas características y corrección de errores
	- [x] Ahora las queries se hacen correctamente: query = "SELECT * FROM Tabla WHERE Campo = ?", y despues: cur.execute(query, (valor,))
	- [x] En los informes, ahora se muestra una sola columna 'Tiempo' con la diferencia entre el inicio y el fin. También una última fila con los 'Totales'.
	- [x] Botón 'Exportar', para generar un archivo de texto .csv con los datos del informe seleccionado.

### 26-04-2020 [v.1.8] Corrección de errores
	- [x] Corregido que no se pueda recargar la lista de tareas mientras haya un crono activo.
	- [x] Al eliminar una tarea, se elimina de la BD. y después el item de la lista, ya no se elimina la lista y se vuelve a cargar. Así los cronos pueden seguir funcionando.
	- [x] Al iniciarse la aplicación, compruebo si hay algún campo con FechaHoraFin vacío, y si lo hay le pongo la FechaHoraInicio
	- [x] Capturo la señal de cierre de la aplicación para preguntar al usuario si desea salir, y además si lo hace habiendo un crono activo se lo advierto.
			Además, si aún así sale de la aplicación sin parar el crono, yo le pongo la fecha-hora actual al campo FechaHoraFin.
	- [x] Hago el primer 'freeze' a la aplicación. Le paso el pyinstaller y la situo en /opt/CronoTareas:
		`$ pyinstaller --onefile --icon=./images/cronotareas.png --windowed --add-data="CronoTareas.db:." CronoTareas.py`
	- [x] Corregido pequeño error al Crear BD.: nombre de campo FechaHoraFina (mal), FechaHoraFin(bien).

### 27-04-2020 [v.1.9] Corrección de errores
	- [ ] Permitir editar la FechaHoraIni y Fin de las tareas.
	- [ ] Iniciar CronoTareas con argumentos, para que cada vez que se inicie ponga en ejecución una tarea.
	- [x] Crear un mejor texto descriptivo de esta aplicación para poner en este readme.md. Versión intl.(inglés) incluida.
	- [ ] Poner un botón 'Help' con la ayuda de la app.
	- [ ] Traducir la aplicación a versión internacional (inglés).