---
description: Implementa un milestone específico de la especificación del proyecto paso a paso
---

# Workflow: Implementar Milestone

Este workflow guía la implementación de un milestone de la especificación.

## Pasos

1. **Lee la especificación del proyecto:**
   - Busca el archivo de spec en `specs/`
   - Si hay múltiples specs, pregunta al usuario cuál usar
   - Identifica el milestone actual (el primero que no esté completado)

2. **Presenta el plan de implementación:**
   - Lista las tareas del milestone
   - Para cada tarea, explica:
     - Qué archivos se crearán o modificarán
     - Qué funcionalidad se agregará
     - Cómo se puede probar
   - **NO codees todavía.** Espera confirmación del usuario.

3. **Implementa tarea por tarea:**
   - Implementa UNA tarea a la vez
   - Después de cada tarea, indica al usuario cómo probarla
   - Espera confirmación de que funciona antes de continuar
   - Si algo falla, arréglalo antes de avanzar

4. **Verificación del milestone:**
   - Al completar todas las tareas, verifica el criterio de éxito del milestone
   - Pide al usuario que haga una prueba completa
   - Si todo funciona, sugiere hacer commit:
     ```
     git add .
     git commit -m "feat: [milestone] - [descripción]"
     git tag [commit-tag-del-milestone]
     ```

5. **Limpieza post-milestone:**
   - Revisa si hay código duplicado o redundante
   - Verifica que no haya imports sin usar
   - Actualiza el checklist del milestone en la spec (marca tareas como completadas)

6. **Siguiente paso:**
   - "Milestone [N] completado ✅. ¿Quieres continuar con el Milestone [N+1]?"

## Notas para Windsurf

- Sigue las reglas globales en `.windsurf/rules/global.md`
- Referencia los números de requerimiento (RF-XXX) en cada cambio
- No avances al siguiente milestone sin completar el actual
- Cada cambio debe ser el mínimo necesario
- Prioriza reutilizar código existente
