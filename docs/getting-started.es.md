# Primeros pasos

1. **Instala** el plugin (ver README).
2. **Configura**: di "configura story-forge". Responde las preguntas (gestor de tickets, wiki, herramienta de diseño, idioma, mercados, alternativas). El perfil se guarda como `story-forge.profile.yaml` en tu carpeta de trabajo o en tu Proyecto de Claude.
3. **Base de conocimiento**: si tu equipo aún no tiene reglas escritas, acepta crear el conjunto inicial (`knowledge-base/es/`) en tu wiki o como archivos markdown. Ajusta los valores entre llaves.
4. **Mapa de flujos**: agrega los flujos en los que trabajas al mapa flujo → fuentes (requerimiento y link de diseño por flujo y canal).
5. **Primera historia**: "escribe la historia ABC-123" (agrega los links de requerimiento y diseño si no están en el mapa). Responde las preguntas bloqueantes y revisa el borrador.
6. **Publica**: "actualiza ABC-123 con esta historia".
7. **Retro**: al cierre del sprint, "haz la retro de historias del sprint N" y aprueba las reglas que valga la pena conservar.

## Pruébalo sin datos reales

Usa `examples/es-scheduled-transfer/`: dale el requerimiento y el resumen de diseño a `sf-write-story` y compara el resultado con `expected-story.md` usando `sf-lint`.

## Consejos

- Deja el modelo más capaz en la conversación principal; los subagentes usan modelos más económicos donde la calidad es igual.
- Para publicar las imágenes sin elegir archivos, conecta Claude in Chrome e inicia sesión en tu gestor de tickets en Chrome; deja `browser-extension` primero en `publishing.images_inline`. Detalle: [image-upload.es.md](image-upload.es.md).
- Si la cuota de diseño es escasa, pon `local-file` primero para textos y `browser-export` o `designer-export` primero para imágenes.
- Lee la línea de consumo al final de cada ejecución y ajusta `agents.routing`.
