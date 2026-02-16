---
description: Genera una especificación de proyecto paso a paso usando el template de vibe coding
---

# Workflow: Generar Especificación de Proyecto

Este workflow te guía paso a paso para crear la especificación de tu proyecto.
Windsurf te hará preguntas y generará el archivo de spec automáticamente.

## Pasos

1. **Pregunta al usuario** la siguiente información en orden, esperando respuesta entre cada pregunta:

   a. **Nombre y descripción:** "¿Cómo se llama tu proyecto y qué hace en una oración?"
   
   b. **Usuarios:** "¿Quién va a usar esta aplicación?"
   
   c. **Problema:** "¿Qué problema resuelve? ¿Cómo se hace actualmente sin esta app?"

2. **Propón el tech stack** basándote en la respuesta del usuario:
   - Empieza con el stack más simple posible
   - Si el proyecto está dentro de este workspace, sugiere Streamlit + Python
   - Presenta 2-3 opciones de stack y recomienda la más simple
   - Espera confirmación del usuario antes de continuar

3. **Requerimientos funcionales** — Pregunta al usuario:
   "Describe las 3-5 cosas más importantes que tu app debe hacer. No te preocupes por el formato, solo descríbelas en tus palabras."
   
   Luego, convierte las respuestas del usuario en requerimientos formales con formato RF-XXX, incluyendo:
   - Historia de usuario
   - Criterios de aceptación
   - Prioridad
   - Muestra el resultado al usuario y pide confirmación

4. **Requerimientos no funcionales** — Pregunta:
   - "¿Necesita autenticación/login?"
   - "¿Cuántas personas la usarán al mismo tiempo?"
   - "¿Dónde se va a ejecutar? (tu computadora / servidor / nube)"
   - "¿Maneja datos sensibles?"

5. **Milestones** — Basándote en los requerimientos, propón 3-5 milestones:
   - Milestone 1 siempre debe ser lo mínimo funcional (algo visible en pantalla)
   - Cada milestone debe ser testeable independientemente
   - El último milestone debe ser la versión completa
   - Presenta los milestones al usuario y ajusta según feedback

6. **Genera el archivo de especificación:**
   - Copia el template de `SPEC_TEMPLATE.md`
   - Llena todas las secciones con la información recopilada
   - Guarda como `specs/[nombre-proyecto].md`
   - Muestra un resumen al usuario

7. **Checklist final** — Verifica con el usuario:
   - "¿La visión del proyecto está clara?"
   - "¿El tech stack es suficientemente simple?"
   - "¿Los milestones son realistas y testeables?"
   - "¿Falta algún requerimiento importante?"

8. **Siguiente paso** — Pregunta al usuario:
   "Tu spec está lista. ¿Quieres que empecemos con el Milestone 1?"

## Notas para Windsurf

- Habla en español
- Usa lenguaje simple, sin jerga técnica
- Si el usuario no sabe algo, sugiere la opción más simple
- No generes código durante este workflow, solo la especificación
- Si el usuario ya tiene un proyecto existente, analiza la estructura antes de proponer el stack
