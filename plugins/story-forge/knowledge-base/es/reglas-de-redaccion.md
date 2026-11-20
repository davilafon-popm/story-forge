# Reglas de redacción de historias de usuario

**Estado:** VIGENTE · **Última actualización:** AAAA-MM-DD · **Mercado:** {nombre}

Reglas para redactar historias. Se citan por nombre y se actualizan con las correcciones que se repiten (ver sf-retro). Este es el conjunto inicial de story-forge: ajústalo a tu equipo; cambia el origen cuando una regla nazca de un ticket propio.

## A. Fuentes y textos

| Nombre | Regla | Origen |
|---|---|---|
| Textos literales del diseño | **Usar los textos literales del diseño** (títulos, botones, mensajes, etiquetas), aunque parezcan provisionales. Si parecen provisionales, se usan igual y se anota la observación; no se reemplazan por un pendiente. | Conjunto inicial |
| Revisar antes de dejar pendiente | **Revisar el diseño y este estándar antes de dejar un pendiente.** Si el diseño ya muestra el comportamiento (un modal, una pantalla de error, un estado deshabilitado), se describe. | Conjunto inicial |
| Las notas del diseño son reglas | **Las notas de desarrollo del diseño son reglas de negocio.** Se incorporan como criterios y se cita la nota. Si contradicen el requerimiento, se registra como pendiente; no se elige una de las dos. | Conjunto inicial |
| Los datos de ejemplo no son requisitos | **Los datos de ejemplo del diseño no son requisitos.** Teléfonos enmascarados, montos, nombres y fechas de muestra no se convierten en reglas. | Conjunto inicial |

## B. Comportamientos y bordes

| Nombre | Regla | Origen |
|---|---|---|
| Aplicar comportamientos estándar | **Aplicar los comportamientos estándar.** Si la historia incluye filtros, listados, descargas, formularios o estados vacíos, incluye las reglas vigentes que apliquen o las cita por su nombre ("Aplica las reglas *Desde posterior a Hasta* y *Dos estados vacíos*"). | Conjunto inicial |
| Definir los bordes | **Definir los bordes.** Cada historia indica qué pasa con datos vacíos, errores de conexión o de servicio y valores límite. Lo que no se pueda definir queda como pendiente explícito, nunca en silencio. | Conjunto inicial |
| Declarar excepciones | **Declarar las excepciones.** "Excepción a la regla *Descarga de lo que se ve*: …". | Conjunto inicial |

## C. Pendientes y relaciones

| Nombre | Regla | Origen |
|---|---|---|
| Pendientes solo para decisiones de negocio | **Los pendientes son solo para decisiones de negocio reales:** montos, límites, comisiones, temas regulatorios o legales, alcance entre historias y contradicciones entre fuentes. Cada pendiente incluye una propuesta recomendada. | Conjunto inicial |
| Solo historias relacionadas confirmadas | **No listar historias relacionadas sin confirmar.** | Conjunto inicial |
| Vacío detectado por QA | **Vacío detectado por QA.** Si QA reporta un comportamiento que ni la historia ni el estándar definen, no se trata como fallo de desarrollo: se registra como "Por definir" en el estándar y, una vez decidido, se ajusta la historia o se gestiona como cambio. | Conjunto inicial |

## D. Imágenes

| Nombre | Regla | Origen |
|---|---|---|
| Una imagen por criterio | **Una imagen de la pantalla debajo de cada criterio.** La referencia visual es la imagen, insertada en la descripción del ticket bajo su criterio; nunca adjuntos sueltos. Si no hay pantalla para un criterio, se dice explícitamente. | Conjunto inicial |
