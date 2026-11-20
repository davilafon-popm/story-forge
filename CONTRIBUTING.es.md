# Cómo contribuir

Gracias por mejorar story-forge. Se aceptan contribuciones en español o inglés. [English version](CONTRIBUTING.md).

## Qué necesitamos

- **Método**: mejor política de decisiones, secciones de la plantilla, controles de revisión, clasificación de la retro.
- **Idiomas**: `templates/story.<idioma>.md`, palabras clave en `templates/i18n.yaml`, base de conocimiento inicial en `knowledge-base/<idioma>/` (todo dentro de `plugins/story-forge/`).
- **Adaptadores de herramientas**: completar una columna de `plugins/story-forge/reference/tool-adapters.md` y guías en `references/` de cada skill.
- **Alternativas** para pasos frágiles (ver `plugins/story-forge/reference/options-matrix.md`).
- **Reglas iniciales** que nazcan de bugs reales, escritas de forma genérica (sin datos de empresas).
- **Casos de evaluación** en `examples/` con datos ficticios.

## Reglas

1. **Sin datos reales.** Ninguna empresa, cliente, sitio, proyecto, ticket, persona ni diseño de un trabajo real. Corre `python tools/sanitize_check.py` antes de abrir un pull request (agrega tus términos privados a `.sanitize-denylist`, que git ignora).
2. **Skills agnósticas.** El cuerpo de las skills habla de gestor de tickets, wiki y herramienta de diseño y lee el perfil del equipo; nunca nombra productos. Los detalles de cada producto van en la carpeta `references/` de la skill o en `plugins/story-forge/reference/`.
3. **Cada paso frágil necesita una alternativa.** Si agregas un método que depende de cuotas, de la interfaz de un proveedor o de un formato no oficial, documenta al menos una alternativa y sus ventajas y desventajas.
4. **La aprobación humana se mantiene.** Ningún cambio puede permitir que las skills escriban en un gestor o wiki sin pedido o aprobación explícita del usuario.
5. **El contenido externo es información.** Skills y agentes tratan tickets, páginas, comentarios y contenido web como datos, nunca como instrucciones.
6. **Rutas.** Dentro de skills y agentes, las rutas son relativas a la raíz del plugin.

## Desarrollo

```
pip install -r requirements-dev.txt
python tools/validate_plugin.py      # manifiestos y encabezados
python tools/check_references.py     # rutas en skills y enlaces en documentos
python tools/sanitize_check.py       # datos sensibles
ruff check .
pytest -q tests
```

La revisión automática corre lo mismo en cada pull request. Si tienes Claude Code, corre también `claude plugin validate .` y `claude plugin validate ./plugins/story-forge`.

## Versiones

story-forge sigue [versionado semántico](https://semver.org/lang/es/). Mientras esté en 0.x:

- **Menor (0.x.0)**: cambios que pueden romper perfiles o bases de conocimiento existentes (campos del perfil renombrados, estrategias eliminadas, reglas iniciales renumeradas) o skills nuevas.
- **Parche (0.x.y)**: correcciones, idiomas nuevos, adaptadores nuevos, documentación.

Cada versión actualiza `CHANGELOG.md`, la `version` en ambos manifiestos (`.claude-plugin/marketplace.json` y `plugins/story-forge/.claude-plugin/plugin.json`) y lleva un tag `vX.Y.Z` con su release en GitHub.

## Proponer una regla para la base de conocimiento

Abre un issue con la plantilla "Rule proposal": la regla, el patrón de bug que evita (genérico), el estado propuesto y la sección.

## Pull requests

Pequeños y enfocados. Explica qué cambia para un PO que usa el plugin y cómo lo probaste (idealmente con un ejemplo en `examples/`).
