# Imágenes del diseño en el ticket sin elegir archivos

[English](image-upload.md) · Nuevo en 0.2.0

## El problema

Cada historia lleva una imagen del diseño debajo de cada criterio de aceptación. Sacar las imágenes de la herramienta de diseño ya estaba automatizado, pero el último paso seguía necesitando a una persona: en muchos equipos el Product Owner tenía que abrir un selector de archivos y elegir las PNG en cada historia.

Ese paso no es un fallo de una sesión. Las imágenes están en disco y el gestor de tickets las necesita dentro de una página web o a través de su API. Cada vía habitual puede estar cerrada:

- **El navegador de la app de Claude** puede llamar al gestor desde la página del ticket, pero no puede poner un archivo en una página. Solo una persona puede elegir archivos en el selector.
- **Los conectores del gestor** pueden no subir adjuntos (algunas versiones solo leen y escriben texto).
- **La red de Claude** puede no llegar a la API del gestor, porque la lista de dominios permitidos de la organización no lo incluye. Entonces tampoco sirve un script con token.

## La solución: Claude in Chrome

Claude in Chrome (la extensión del navegador) tiene la herramienta `file_upload`, que carga archivos en un campo de archivo de una página, sin selector. story-forge 0.2.0 la usa como primera estrategia de publicación (`browser-extension`):

1. Claude abre el ticket en Chrome, donde ya tienes sesión en el gestor.
2. Carga las PNG de la historia en un campo de archivo oculto de la página.
3. Compara nombre, tamaño y SHA-256 de cada archivo con los originales.
4. Desde la misma página, las sube con la API de adjuntos del gestor y escribe la descripción con cada imagen debajo de su criterio.
5. Verifica el ticket y quita el campo.

Probado en Jira Cloud el 2026-11-25: los archivos llegaron a la página idénticos byte a byte a los originales.

## Qué necesitas

- Claude in Chrome instalado, conectado y con sesión en la **misma organización** que tu conversación de Claude.
- Tu gestor de tickets abierto en Chrome con tu sesión (Claude nunca escribe contraseñas; si la sesión vence, te pide que entres).
- `browser-extension` primero en `publishing.images_inline` de tu perfil (el valor por defecto desde 0.2.0).

Conviene saber:

- `file_upload` acepta archivos del espacio de trabajo de la sesión de Claude, no rutas de tus carpetas. El paso de imágenes ya deja las PNG ahí; si solo están en tu carpeta, Claude las copia primero.
- Máximo 3,8 MB por llamada. Una PNG de pantalla pesa entre 25 y 80 KB, así que una historia entera cabe en una llamada.

## Si no puedes usar la extensión

Las demás estrategias siguen disponibles, en el orden de tu perfil: `api-token` (un token en una variable de entorno, cuando la red de Claude llega al gestor), `browser-session` (tú eliges los archivos), `wiki-page` y `manual`. Ver [la matriz de opciones](../plugins/story-forge/reference/options-matrix.md).
