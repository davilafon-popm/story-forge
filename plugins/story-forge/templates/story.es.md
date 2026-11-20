<!--
Plantilla "historia funcional detallada" (español).
Sin encabezados Markdown: la estructura se logra con etiquetas en negrita.
Dentro de un bloque, los saltos de línea se logran con dos espacios al final de la línea.
-->
**{KEY} – {Título corto del flujo}**  
**Épica:** {KEY} – {Nombre de la épica}  
**Producto / Mercado:** {team.product} – {market.name}  
**Canal:** {Mobile | Web | Ambos}

**Historia de usuario**

**Como** {tipo de cliente o usuario},  
**quiero** {acción o funcionalidad},  
**para** {beneficio o necesidad que resuelve}.

**Descripción funcional**

Uno o dos párrafos: punto de acceso (pantalla anterior, botón o menú), nombre exacto de cada pantalla u hoja como aparece en el diseño, valores por defecto, reglas que aplican y qué ocurre al avanzar. Si es una mejora, qué cambia frente al comportamiento actual.

**Alcance**

* Funcionalidad incluida, en frases cortas.

**Fuera de alcance**

* Funcionalidad excluida y la historia que la cubre (con su clave).
* Elementos visibles en el diseño sin funcionalidad definida en esta historia.

**Precondiciones**

* Condición de acceso, estado de sesión o de proceso, datos que el usuario debe tener.

**Referencias**

Diseño: {nombre del flujo y link al nodo del archivo original}  
Requerimiento: {link}  
Historias relacionadas: {clave, nombre y motivo; solo relaciones confirmadas}

**Dependencias**

* Servicios: cada servicio por su función, con su nombre del inventario o [Pendiente: nombre del servicio].
* Diseño: pantallas, hojas y estados requeridos.
* Otras historias: claves de las que depende.
* Configuraciones: textos, mensajes, parámetros, permisos.

**Criterios de aceptación**

1. Nombre corto del comportamiento

Dado que {contexto o condición inicial},  
cuando {acción del usuario o evento del sistema},  
entonces {resultado observable y verificable}.

* Regla, validación o detalle de este criterio. Aplica la regla *Desde posterior a Hasta*.
* Condición de habilitación o comportamiento adicional.

Referencia visual: imagen 01-descripcion.png

2. Siguiente comportamiento

(Mismo formato.)
