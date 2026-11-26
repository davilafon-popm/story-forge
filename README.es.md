# story-forge

**Historias de usuario casi finales a partir de requerimientos y diseños — en cualquier idioma y con cualquier gestor de tickets, wiki y herramienta de diseño.**

[English](README.md) · Licencia: [Apache 2.0](LICENSE) · Estado: versión inicial (0.2.0)

story-forge es un método para product owners, empaquetado como plugin de Claude. Convierte un ticket, su requerimiento y su diseño en una historia detallada con criterios de aceptación numerados, servicios nombrados, una imagen del diseño bajo cada criterio y los estándares de tu equipo aplicados. Después la revisa, la publica en el ticket que indiques y aprende de los bugs de cada sprint.

## Novedades de 0.2.0

**Las imágenes del diseño llegan al ticket sin elegir archivos.** Con Claude in Chrome conectado, story-forge carga por sí mismo las imágenes de cada historia en la página del ticket, las verifica byte a byte e inserta cada una debajo de su criterio. Antes, el Product Owner muchas veces tenía que seleccionar las PNG en un selector de archivos en cada historia. Por qué pasaba y cómo funciona: [docs/image-upload.es.md](docs/image-upload.es.md). Lista completa: [CHANGELOG.md](CHANGELOG.md).

## Por qué

La mayor parte del tiempo de un PO en una historia no es redactar: es confirmar el alcance, buscar textos en el diseño, exportar pantallas, aplicar reglas no escritas del equipo y responder cada sprint las mismas preguntas de QA. story-forge vuelve esos pasos explícitos, repetibles y mejorables.

## Cómo se ve una historia

Extracto del ejemplo ficticio de [`examples/`](examples/):

```
5. Confirmación exitosa

Dado que el usuario revisó el resumen en "Confirmar",
cuando toca "Programar" y el servicio Registro de programaciones confirma el registro,
entonces el sistema muestra "¡Listo!" con el texto "Tu transferencia quedó programada.".

* Sin confirmación del servicio no se muestra la pantalla de éxito.

Referencia visual: imagen 04-listo.png
```

Cada historia llega con una **tabla de decisiones** (qué se decidió y con qué fuente), como máximo N **preguntas bloqueantes** con respuesta recomendada, el resultado de la **revisión** y **casos de prueba** sugeridos.

## Qué hace

| Paso | Skill | Qué obtienes |
|---|---|---|
| Configurar | `sf-setup` | Perfil del equipo: herramientas, mercados, idiomas, alternativas, modelos |
| Revisar alcance | `sf-precheck` | Confirmación de que ticket, requerimiento y diseño son del mismo flujo |
| Leer el diseño | `sf-design-reader` | Textos, controles, notas y un PNG por pantalla, con alternativas ante cuotas |
| Redactar | `sf-write-story` | Historia casi final, tabla de decisiones y máximo N preguntas bloqueantes |
| Flujo completo | `sf-backlog` | Épica e historias, con una sola ronda de revisión |
| Revisar | `sf-lint` | Hallazgos por criterio con severidad y corrección |
| Publicar | `sf-publish` | La historia en el ticket, con cada imagen bajo su criterio |
| Investigar | `sf-research` | Datos externos con fuente (normativa, prácticas, documentación) |
| Aprender | `sf-retro` | Reglas nuevas para tu base de conocimiento a partir de los bugs |
| Orquestar | `sf-workflow` | Todo lo anterior, con subagentes y el modelo adecuado en cada paso |

## Principios

- **Agnóstico a las herramientas.** Las skills hablan de gestor de tickets, wiki y herramienta de diseño; tu perfil dice cuáles (Jira, Azure DevOps, Linear, Confluence, Notion, Figma, Penpot…). Ver [CONNECTORS.md](plugins/story-forge/CONNECTORS.md).
- **Cualquier idioma.** Idioma de la historia, etiquetas y palabras Dado/cuando/entonces salen del perfil y de `templates/i18n.yaml`.
- **Alternativas para cada paso frágil.** Cuotas, permisos e interfaces cambian; cada paso tiene alternativas ordenadas. Ver la [matriz de opciones](plugins/story-forge/reference/options-matrix.md).
- **Varios mercados.** Países, marcas o unidades con bases de conocimiento y datos separados.
- **Control humano.** Nada se escribe en tu gestor o wiki sin que lo pidas o apruebes.
- **Aprende.** Las retros convierten bugs y correcciones en reglas.

## Alcance y requisitos

- **Agnóstico a tus herramientas, no a la IA.** story-forge es un plugin de Claude: usa skills, subagentes (opcionales) y, para algunas alternativas, el navegador de la app de Claude o Claude in Chrome. Tu gestor de tickets, wiki y herramienta de diseño pueden ser cualquiera con conector, API o alternativa manual.
- **Conectores** de tu gestor y tu wiki en tu espacio de Claude (o las estrategias `manual`).
- **Python 3.10+** solo si usas los scripts de diseño: `pip install -r requirements.txt`.
- **Madurez.** El método se usó en proyectos reales (Jira, Confluence, Figma) antes de empaquetarse; story-forge 0.1.0 como tal es nuevo. Cuéntanos qué funciona y qué falla con tus herramientas.

## Instalación

**Claude Code**

```
/plugin install story-forge --marketplace davilafon-popm/story-forge
```

Esa sola línea funciona en Claude Code 2.1.275 o posterior. En versiones anteriores, usa dos pasos:

```
/plugin marketplace add davilafon-popm/story-forge
/plugin install story-forge@story-forge
```

**Claude (Cowork / escritorio)**: comprime la carpeta `plugins/story-forge` (su contenido en la raíz del zip), cámbiale el nombre a `story-forge.plugin` y agrégalo como plugin. Tu organización también puede distribuirlo desde su catálogo.

El plugin necesita su carpeta completa (plantillas, base de conocimiento, referencias): no se admite subir skills sueltas.

Luego di "configura story-forge". La skill `sf-setup` hace unas preguntas y escribe tu perfil. Guía paso a paso: [docs/getting-started.es.md](docs/getting-started.es.md).

## Contribuir

Mejoras al método, nuevos idiomas, adaptadores de herramientas y reglas iniciales son bienvenidos. Lee [CONTRIBUTING.es.md](CONTRIBUTING.es.md). Nunca incluyas datos reales de una empresa en ejemplos o reglas. Problemas de seguridad: ver [SECURITY.md](SECURITY.md). Quién decide qué: ver [GOVERNANCE.es.md](GOVERNANCE.es.md) — cada Product Owner puede cambiar su propia implementación salvo que su organización no lo permita.

## Aviso

story-forge es un proyecto independiente. No está afiliado, respaldado ni patrocinado por Anthropic, Atlassian, Figma, Microsoft, Notion, Linear ni ningún otro proveedor mencionado; los nombres de productos solo describen compatibilidad. Algunas alternativas opcionales automatizan la interfaz web de un proveedor o leen un formato de archivo no oficial: eres responsable de usarlas conforme a los términos de servicio de cada herramienta y a las políticas de tu organización, y pueden dejar de funcionar cuando el proveedor cambie su producto.

## Autor

Método y skills originales de **David Dávila**. Ver [NOTICE](NOTICE).
