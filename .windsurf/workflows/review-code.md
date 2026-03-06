---
description: Revisa el código del proyecto buscando duplicados, redundancias y problemas
---

# Workflow: Revisar Código

Revisa el codebase buscando problemas de calidad, duplicados y redundancias.

## Pasos

1. **Analiza la estructura del proyecto:**
   - Lista todos los archivos y su propósito
   - Identifica archivos que no pertenecen a la estructura esperada

2. **Busca problemas:**
   - Código duplicado entre archivos
   - Imports sin usar
   - Variables o funciones no utilizadas
   - Credenciales o secrets hardcodeados
   - Archivos vacíos o sin propósito

3. **Presenta los hallazgos:**
   - Lista cada problema encontrado con su ubicación
   - Clasifica por severidad: 🔴 Crítico / 🟡 Medio / 🟢 Bajo
   - **NO corrijas nada automáticamente**

4. **Pide confirmación:**
   - "Encontré [N] problemas. ¿Quieres que corrija alguno?"
   - Corrige solo lo que el usuario apruebe, uno a la vez

## Notas para Windsurf

- Este workflow es para auditoría, no para cambios masivos
- Nunca elimines código sin aprobación explícita
- Si encuentras algo que no entiendes, pregunta antes de reportarlo como problema
