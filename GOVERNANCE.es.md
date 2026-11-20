# Gobernanza

[English](GOVERNANCE.md)

## Dos niveles

**1. El método (este repositorio).** La metodología de story-forge pertenece a su autor, David Dávila, quien mantiene este repositorio y decide qué entra en la versión compartida: skills, plantillas, la base de conocimiento inicial y la documentación. Cualquiera puede proponer cambios con issues y pull requests (ver [CONTRIBUTING.es.md](CONTRIBUTING.es.md)); el mantenedor los revisa y los integra.

**2. Cada implementación (tu equipo).** Cada Product Owner puede cambiar su propia implementación sin pedir permiso a nadie: el perfil del equipo, la base de conocimiento (reglas de redacción y comportamientos estándar), las plantillas y, si lo necesita, una copia (fork) de las skills. El único límite es su organización: si sus políticas exigen aprobación para estándares, plantillas o herramientas, esas políticas mandan.

## Cómo lo aplica el plugin

El perfil del equipo tiene una sección `governance`:

```yaml
governance:
  kb_changes: po               # po = aprueba el Product Owner | organization = requiere la aprobación indicada abajo
  approver: ""                 # rol o grupo que aprueba cuando kb_changes es organization
```

- Con `po` (valor por defecto), `sf-retro` y `sf-setup` preguntan al Product Owner y aplican lo que apruebe.
- Con `organization`, preparan la propuesta (texto de la regla, evidencia, página afectada) para el aprobador indicado y no cambian nada hasta que el Product Owner confirme que fue aprobada.
- En ambos casos, los cambios se escriben solo en la base de conocimiento del mercado al que pertenecen.

## Compartir mejoras con todos

Si un cambio de tu implementación puede servir a otros equipos, propónlo al repositorio sin datos de tu empresa: redacción genérica, ejemplos inventados, sin nombres de clientes, sistemas ni personas. Las reglas aceptadas se suman al conjunto inicial con origen "Comunidad".

## Licencia

Apache License 2.0. Puedes usar, modificar y redistribuir el método según sus términos, conservando la atribución del archivo [NOTICE](NOTICE).
