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
	- [ ] Guardar estado de todos los cronos, fechas/horas de inicio/fin, etc. en BD.
	- [ ] Fix!: GuardarEstadoTareas -> Si está en marcha un crono y se modifica la tarea, este se restaura.
	- [ ] Mostrar total de tareas
	- [ ] Si durante el funcionamiento de varios cronos se deschecka el checkBox, este ya no surte efecto.
			Solución: deshabilitar checkBox durante el funcionamiento de varios cronos
	- [ ] Deshabilitar botón de Modificar durante el funcionamiento de su cron
	- [ ] Desarrollar todo el tema de los Informes.




