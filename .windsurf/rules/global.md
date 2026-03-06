# Reglas Globales de Windsurf — Vibe Coding (Peter Yang's 12 Rules)

> Estas reglas aplican a TODAS las conversaciones en este proyecto.
> Están basadas en las 12 reglas de vibe coding de Peter Yang.

---

## 🧠 Regla 1: Planifica antes de codear (Reglas 1, 4, 5)

- **SIEMPRE** explica tu plan antes de escribir código. No codees sin confirmación del usuario.
- Cuando el usuario pida una funcionalidad nueva, responde con:
  1. Qué vas a hacer (en lenguaje simple)
  2. Qué archivos vas a modificar o crear
  3. Posibles riesgos o efectos secundarios
- Si hay múltiples formas de implementar algo, presenta **2-3 opciones empezando por la más simple**.
- Pregunta al usuario cuál prefiere antes de proceder.

## 🧱 Regla 2: Simplicidad ante todo (Reglas 2, 5, 6)

- **Haz lo más simple primero.** No sobre-ingenieres.
- No agregues librerías, dependencias o abstracciones innecesarias.
- Usa módulos y archivos separados en lugar de un solo archivo monolítico.
- Si una solución requiere más de 100 líneas en un solo archivo, considera dividirla.
- **NUNCA** cambies el tech stack sin aprobación explícita del usuario.

## 🎯 Regla 3: Solo cambios solicitados (Reglas 6, 9)

- **Solo modifica lo que el usuario pidió.** No hagas cambios "de mejora" no solicitados.
- No refactorices código existente a menos que el usuario lo pida.
- No cambies estilos, nombres de variables o estructura sin razón.
- Si detectas un problema en código existente, **repórtalo** pero no lo corrijas sin permiso.
- Limita cada cambio al **mínimo número de archivos posible**.

## 🚫 Regla 4: No duplicar código (Regla 3c)

- Antes de crear una función nueva, **busca en el codebase** si ya existe algo similar.
- Reutiliza componentes, utilidades y configuraciones existentes.
- Si necesitas funcionalidad similar a algo existente, extiéndelo en lugar de duplicarlo.
- Mantén la configuración centralizada en `config/settings.py`.

## 📁 Regla 5: Respeta la estructura del proyecto

- Sigue la estructura de directorios existente:
  - `pages/` — Páginas y vistas de la aplicación
  - `components/` — Componentes reutilizables de UI
  - `utils/` — Funciones auxiliares y helpers
  - `auth/` — Lógica de autenticación
  - `config/` — Configuración y settings
  - `specs/` — Especificaciones del proyecto
- **NUNCA** crees archivos en la raíz del proyecto sin justificación.
- Los nuevos archivos deben ir en el directorio que corresponda según su función.
- Usa nombres descriptivos en snake_case para archivos Python.

## 🧪 Regla 6: Cambios incrementales y testeables (Reglas 6, 8)

- Implementa **un paso a la vez**. No hagas cambios masivos.
- Cada cambio debe ser **verificable inmediatamente** por el usuario.
- Después de cada cambio, indica al usuario **exactamente cómo probarlo**.
- Si un cambio involucra múltiples archivos, explica el orden de verificación.

## 📋 Regla 7: Sigue la especificación (Regla 1)

- Si existe un archivo de especificación en `specs/`, **síguelo estrictamente**.
- No implementes funcionalidades que no estén en la spec sin preguntar.
- Referencia el número de requerimiento (RF-XXX) cuando implementes algo.
- Respeta los milestones: no avances al siguiente sin completar el actual.

## 🔒 Regla 8: Seguridad y configuración

- **NUNCA** hardcodees credenciales, API keys o secrets en el código.
- Usa variables de entorno (`.env`) para toda configuración sensible.
- Verifica que `.env` esté en `.gitignore`.
- Mantén un `.env.example` actualizado con las variables necesarias (sin valores reales).

## 💬 Regla 9: Comunicación clara

- Usa español para comunicarte con el usuario (a menos que pida otro idioma).
- Cuando expliques código, usa **lenguaje simple** sin jerga innecesaria.
- Si el usuario pide que expliques algo, hazlo como si hablaras con alguien no técnico.
- Incluye emojis solo si el usuario los usa primero.

## 🔄 Regla 10: Control de versiones (Regla 10)

- Al completar un milestone, sugiere al usuario hacer commit con el tag correspondiente.
- Formato de commit sugerido: `feat: [milestone] - [descripción breve]`
- Si un cambio rompe algo, sugiere revertir antes de intentar arreglar en cascada.

## ⚠️ Regla 11: Manejo de errores

- No ignores errores silenciosamente. Siempre maneja excepciones con mensajes claros.
- Los mensajes de error deben ser útiles para el usuario final, no solo para desarrolladores.
- Usa `st.error()`, `st.warning()`, `st.info()` apropiadamente en Streamlit.

## 📐 Regla 12: Consistencia de código

- Sigue el estilo del código existente en el proyecto.
- Si el proyecto usa `width='stretch'` en lugar de `use_container_width`, mantén esa convención.
- Respeta los patrones de importación existentes.
- Mantén la consistencia en nombres: si el proyecto usa español para variables de UI, continúa así.
