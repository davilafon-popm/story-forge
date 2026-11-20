**AND-101 – Programar transferencia recurrente a cuenta de terceros**  
**Épica:** AND-100 – Transferencias programadas  
**Producto / Mercado:** App Andina – Perú  
**Canal:** Mobile

**Historia de usuario**

**Como** cliente con cuentas de terceros inscritas,  
**quiero** programar una transferencia recurrente,  
**para** no repetir manualmente pagos periódicos.

**Descripción funcional**

Desde "Programar transferencia" el usuario elige "Cuenta de origen", "Cuenta destino" (solo terceros inscritos), "Monto" y "Recurrente". Al tocar "Continuar" pasa a "Recurrencia", donde define "Frecuencia" (Semanal, Quincenal o Mensual), "Fecha de inicio" (desde el día siguiente) y, opcionalmente, "Fecha de fin". En "Confirmar" revisa el resumen y al tocar "Programar" el servicio Registro de programaciones registra la programación; solo con su confirmación se muestra "¡Listo!".

**Alcance**

* Programación recurrente a cuentas de terceros inscritas.
* Validación de fechas, del límite diario y del máximo de programaciones activas.
* Confirmación y manejo de errores del registro.

**Fuera de alcance**

* Programación de única vez (cubierta en AND-102).
* Edición y cancelación de programaciones (cubiertas en AND-103).
* Historial de programaciones.

**Precondiciones**

* Sesión iniciada.
* Al menos una cuenta de origen activa y una cuenta de terceros inscrita.

**Referencias**

Diseño: Programar transferencia – nodo de la sección en el archivo original  
Requerimiento: Programadas › Cuentas a terceros › Recurrente  
Historias relacionadas: AND-102 (única vez, comparte pantallas P1 y P3)

**Dependencias**

* Servicios: Consulta de límites (límite diario del cliente); Registro de programaciones (alta de la programación); consulta de programaciones activas: [Pendiente: nombre del servicio].
* Diseño: P1 Programar transferencia, P2 Recurrencia, P3 Confirmar, P4 ¡Listo!, P5 Error.
* Otras historias: AND-102.
* Configuraciones: mensaje de límite de programaciones (ver preguntas).

**Criterios de aceptación**

1. Selección de recurrencia

Dado que el usuario completó origen, destino y monto en "Programar transferencia",  
cuando selecciona "Recurrente" y toca "Continuar",  
entonces el sistema muestra "Recurrencia" con las frecuencias "Semanal", "Quincenal" y "Mensual".

* "Continuar" permanece deshabilitado hasta completar los campos obligatorios.

Referencia visual: imagen 01-programar.png

2. Validación de fechas

Dado que el usuario está en "Recurrencia",  
cuando ingresa una "Fecha de fin (opcional)" igual o anterior a la "Fecha de inicio",  
entonces el sistema muestra "La fecha de fin debe ser posterior a la de inicio." y no permite continuar.

* La fecha de inicio mínima es el día siguiente.

Referencia visual: imagen 02-recurrencia-error-fechas.png

3. Monto mayor al límite diario

Dado que el usuario ingresó un monto,  
cuando el servicio Consulta de límites indica que supera el límite diario,  
entonces el sistema no permite continuar y muestra [Pendiente: mensaje de límite diario].

Referencia visual: sin pantalla en el diseño

4. Límite de programaciones activas

Dado que el cliente tiene 12 programaciones activas,  
cuando intenta programar una nueva,  
entonces el sistema no permite continuar y muestra el mensaje de límite (ver pregunta 2).

* Regla tomada de la nota de diseño "Máximo 12 programaciones activas por cliente".

Referencia visual: sin pantalla en el diseño

5. Confirmación exitosa

Dado que el usuario revisó el resumen en "Confirmar",  
cuando toca "Programar" y el servicio Registro de programaciones confirma el registro,  
entonces el sistema muestra "¡Listo!" con el texto "Tu transferencia quedó programada.".

* Sin confirmación del servicio no se muestra la pantalla de éxito.

Referencia visual: imagen 04-listo.png

6. Error al registrar la programación

Dado que el usuario tocó "Programar",  
cuando el servicio Registro de programaciones responde con error o no responde,  
entonces el sistema muestra "No pudimos programar tu transferencia." con el botón "Reintentar".

* No se muestra el estado de éxito ni se registra la programación. Aplica la regla *Estado de error con Reintentar*.

Referencia visual: imagen 05-error.png

**Decisiones tomadas**

| Decisión | Fuente |
|---|---|
| Máximo 12 programaciones activas | Nota de diseño |
| Fecha de inicio mínima: día siguiente | Requerimiento |
| El límite diario se valida al continuar desde P1 | Supuesto |

**Preguntas bloqueantes**

1. ¿Aplica comisión a las transferencias programadas? → Recomiendo: la misma de una transferencia inmediata a terceros.
2. ¿Qué mensaje se muestra al alcanzar 12 programaciones activas? → Recomiendo: "Alcanzaste el máximo de 12 transferencias programadas activas."

**Revisión (sf-lint):** 0 bloquea · 0 corregir · 1 sugerencia (criterio 3: pedir pantalla de límite diario al diseño).
