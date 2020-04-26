# CronoTareas
Sencilla aplicación para llevar el control del tiempo de tareas.  
Hecha en Python 3.6.7 + PyQt5  
Versión para Linux, testada en Ubuntu Budgie 18.04.4 LTS
  
Fernando Souto (donanpher@gmail.com)  
A Coruña (Galicia), Spain  
Abril 2020 (durante la cuarentena del #Coronavirus #SARS-CoV-2 #Covid-19)  

---
![](./images/Screenshot_CronoTareas.png)
---
## Descripción General
Aplicación para llevar un control de tiempo de distintas tareas.  
Se pueden añadir tantas tareas como se quiera, iniciarlas, pausarlas o detenerlas. Al detenerlas se le pregunta al usuario si desea guardar el Crono en su estado actual para continuar en otra ocasión o simplemente deternerlo y ponerlo a cero.  
Independiente de esto último, cada vez que se 'Start' o 'Continue' se guarda la Fecha-Hora de inicio, y cuando se 'Pause' o 'Stop' se guarda la Fecha-Hora de fin.  
Permite tener varios cronómetros activos al mismo tiempo. Esta característica también se puede desactivar para que esté activa sólamente una tarea a la vez.
Existen 2 campos para identificar cada tarea:  
	- *Nombre Tarea*: Normalmente está pensado para describir la tarea específica que se quiere controlar.  
	- *Tag*			: Su función es más general, por ejemplo, el nombre del proyecto, el cliente, etc.  
Es el usuario el que determinará la manera que más se adapte a sus necesidades.  
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
	- [ ] Crear un mejor texto descriptivo de esta aplicación para poner en este readme.md
	- [ ] Poner un botón 'Help' con la ayuda de la app.
	- [ ] Traducir la aplicación a versión internacional (inglés).
