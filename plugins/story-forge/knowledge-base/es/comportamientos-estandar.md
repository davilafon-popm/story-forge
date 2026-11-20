# Comportamientos estándar

**Estado:** VIGENTE · **Última actualización:** AAAA-MM-DD · **Mercado:** {nombre}

Cada regla tiene un nombre corto y único, y las historias la citan por ese nombre ("Aplica la regla *Estado de error con Reintentar*"). Los nombres no dependen del orden: agregar, mover o borrar reglas nunca rompe una cita; si renombras una regla, busca las historias que la citan. Estados: **VIGENTE** (se aplica), **POR DEFINIR** (trae una propuesta; hasta decidirse, las historias la tratan como pendiente explícito) y **APROBADA – EN BACKLOG**.

Este es el conjunto inicial de story-forge, nacido de bugs reales de apps transaccionales. Los valores entre llaves los decide tu equipo. Borra las secciones que no apliquen y agrega las tuyas con la retro.

## 1. Filtro de rango de fechas (Desde / Hasta)

| Nombre | Regla | Estado | Origen |
|---|---|---|---|
| Periodo por defecto | Por defecto, el listado muestra los registros de los últimos {N} días; no carga vacío si existen registros en ese periodo. | POR DEFINIR | Conjunto inicial |
| Rango máximo | El rango consultable es de máximo {N} días. | POR DEFINIR | Conjunto inicial |
| Desde posterior a Hasta | Si el usuario selecciona "Desde" posterior a "Hasta", el sistema no borra "Hasta" y muestra un mensaje de validación. | VIGENTE | Conjunto inicial |
| Aplicar con ambas fechas | **Propuesta:** "Aplicar" se habilita solo cuando ambas fechas están seleccionadas. | POR DEFINIR | Conjunto inicial |

## 2. Filtro de rango de montos

| Nombre | Regla | Estado | Origen |
|---|---|---|---|
| Mínimo igual al máximo | Monto mínimo igual al máximo. **Propuesta:** permitirlo; devuelve los registros por ese monto exacto. | POR DEFINIR | Conjunto inicial |
| Un solo monto | Solo un monto ingresado. **Propuesta:** "Aplicar" deshabilitado hasta ingresar ambos. | POR DEFINIR | Conjunto inicial |

## 3. Estados sin datos y de error

| Nombre | Regla | Estado | Origen |
|---|---|---|---|
| Dos estados vacíos | El estado vacío distingue "no hay registros en el periodo" de "no hay resultados para la búsqueda o filtro", con mensajes diferentes. | VIGENTE | Conjunto inicial |
| Estado de error con Reintentar | Ante falla de conexión o error de servicio no se muestra el estado vacío: se muestra un estado de error con "Reintentar". | VIGENTE | Conjunto inicial |
| Pantalla de error genérica | Pantalla de error genérica: título, texto con el teléfono de atención del mercado y botón "Reintentar" (textos según el diseño). | POR DEFINIR | Conjunto inicial |

## 4. Idioma

| Nombre | Regla | Estado | Origen |
|---|---|---|---|
| Idioma seleccionado en todo | Todos los textos, mensajes, estados y reportes respetan el idioma seleccionado, incluidos los mensajes sin resultados. | VIGENTE | Conjunto inicial |

## 5. Descarga de reportes (PDF, XLS, CSV)

| Nombre | Regla | Estado | Origen |
|---|---|---|---|
| Reporte según diseño | Contenido y diseño de los reportes según el diseño aprobado, con todos sus campos. | VIGENTE | Conjunto inicial |
| CSV conserva tildes | El CSV usa una codificación que conserva tildes y ñ al abrirse en hojas de cálculo. | VIGENTE | Conjunto inicial |
| Encabezado XLS sin tapar datos | El encabezado o banner del XLS no cubre datos del reporte. | VIGENTE | Conjunto inicial |
| Descarga de lo que se ve | **Propuesta:** la descarga respeta filtros y búsqueda activos; el reporte contiene lo que el usuario ve. | POR DEFINIR | Conjunto inicial |

## 6. Listados de movimientos o registros

| Nombre | Regla | Estado | Origen |
|---|---|---|---|
| Fecha y hora por registro | Cada registro muestra fecha y hora. | VIGENTE | Conjunto inicial |
| Signos de abono y cargo uniformes | **Propuesta:** signos y colores de abono/cargo iguales en todos los productos. | POR DEFINIR | Conjunto inicial |

## 7. Habilitación de botones y acciones

| Nombre | Regla | Estado | Origen |
|---|---|---|---|
| Confirmar deshabilitado sin cambios | En formularios de actualización, el botón de confirmar permanece deshabilitado mientras no haya cambios. | VIGENTE | Conjunto inicial |
| Acciones por tipo de producto | **Propuesta:** una tabla por tipo de producto con las acciones visibles y habilitadas, referenciada desde las historias. | POR DEFINIR | Conjunto inicial |

## 8. Teclado

| Nombre | Regla | Estado | Origen |
|---|---|---|---|
| Campo activo visible con teclado | Al abrirse el teclado, el campo activo (incluido el de búsqueda) permanece visible. | VIGENTE | Conjunto inicial |

## 9. Consistencia entre listado y detalle

| Nombre | Regla | Estado | Origen |
|---|---|---|---|
| Detalle coincide con listado | Los valores del detalle (saldos, tasas, estados) coinciden con los del listado; el detalle no muestra cero cuando el listado muestra un valor. | VIGENTE | Conjunto inicial |

## 10. Flujos de alta u onboarding

| Nombre | Regla | Estado | Origen |
|---|---|---|---|
| Confirmar antes de salir | Al salir durante el flujo se muestra un modal de confirmación con opciones para salir o continuar (textos según el diseño). | VIGENTE | Conjunto inicial |
| Teléfono de atención en error de validación | Ante un error al validar datos del cliente se muestra la pantalla de error del flujo con el teléfono de atención del mercado. | VIGENTE | Conjunto inicial |
| Permisos obligatorios | Los permisos del sistema que el flujo requiere (cámara, ubicación…) son obligatorios para continuar y se piden con el diálogo nativo. | VIGENTE | Conjunto inicial |
