# CronoTareas
Sencilla aplicación para llevar el control del tiempo de tareas.  
Se pueden controlar tantas tareas como se quiera. Permite tener varios cronómetros activos al mismo tiempo. Esta característica también se puede desactivar para que esté activa sólamente una tarea a la vez.
Hecha en Python 3.6.7 + PyQt5
  
Fernando Souto (donanpher@gmail.com)  
A Coruña (Galicia), Spain  
Abril 2020 (durante la cuarentena del coronavirus COVID-19)  

---

<H2>Características</H2>

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
		Yo no sabía que en un LCDDisplay se podía mostrar cualquier cosa. Fue gracias al descubrimiento de un Custom LCDDisplay el que me hizo ver la luz y motivarme a hacer el cambio, que además coincide con mi idea inicial de uso del DateTime. 
		Desde aqui agradezco este descubrimiento a Juan Carlos Paco (https://gist.github.com/juancarlospaco/c0fb15281d56dc6eb2f4)
		De este repositorio tomé la idea y le copio, con permiso y por comodidad, la función seconds_time_to_human_string() que convierte segundos a una 'lectura humana'.
	- [x] Se deshabilita el botón Reset mientras esté en funcionamiento un crono o mientra no se haya iniciado ninguno
	- [x] Se añade un label con el Total de Tareas
	- [x] Hacer la ventana de la aplicación fija en cuanto a tamaño, que no se pueda expandir ni contraer. También centrarla en el escritorio.
	- [x] Añadir ToolTips...  al botón Reset y al botón Recargar lista

### 17-04-2020 [v.1.3] Nuevas características y corrección de errores
	Versión totalmente operativa y funcional.
	Ya definitivamente se usa DateTime para controlar el tiempo
	Así mismo, también se guarda y se restaura el estado del Crono (al pulsar Reset y responder 'Sí' a guardar)
	- [x] Limpiar todo el código con restos del LCDDisplay que no uso. (sólo lo #comento, no lo elimino todavía hasta la v.1.4)
	- [X] Guardar estado de todos los cronos, fechas/horas de inicio/fin, etc. en BD.
	- [ ] Buscar el límite del Display, por lo pronto representa sin problemas '99D 23:59:59' incluso sigue sumando sin contratiempo.
	- [ ] Deshabilitar botones Modificar y Eliminar durante el funcionamiento de un crono o mejor, guardar estado, recargar y continuar.
	- [ ] Fix!: GuardarEstadoTareas -> Si está en marcha un crono y se modifica la tarea, este se restaura.
	- [ ] Deshabilitar botón de Modificar durante el funcionamiento de su cron
	- [ ] Si se pulsa botón Añadir durante un crono, hay que guardar el estado y restaurarlo, pues después de un alta siempre hay una recarga.
	- [ ] Desarrollar todo el tema de los Informes.

