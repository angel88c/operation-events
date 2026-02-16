# 🚀 Guía Rápida: Vibe Coding con Windsurf

> Basado en las [12 reglas de vibe coding de Peter Yang](https://creatoreconomy.so/p/12-rules-to-vibe-code-without-frustration)

---

## ¿Qué es esto?

Un sistema de templates y reglas para que puedas **crear aplicaciones con Windsurf de forma ordenada y sin frustraciones**. Tú te enfocas en **qué** quieres construir, Windsurf se encarga del **cómo**.

---

## Estructura del sistema

```
.windsurf/
├── rules/
│   └── global.md              ← Reglas que Windsurf sigue SIEMPRE
└── workflows/
    ├── generate-spec.md       ← /generate-spec  → Crea tu spec paso a paso
    ├── implement-milestone.md ← /implement-milestone → Implementa un milestone
    └── review-code.md         ← /review-code → Audita tu código

SPEC_TEMPLATE.md               ← Template para copiar y llenar manualmente
specs/                          ← Carpeta donde van tus especificaciones
```

---

## 🏁 Cómo empezar (2 opciones)

### Opción A: Guiado (recomendado para principiantes)

1. Abre Windsurf y escribe:
   ```
   /generate-spec
   ```
2. Windsurf te hará preguntas sobre tu proyecto
3. Al terminar, tendrás tu spec lista en `specs/`
4. Luego escribe:
   ```
   /implement-milestone
   ```
5. Windsurf implementará tu app milestone por milestone

### Opción B: Manual (para quienes prefieren escribir)

1. Copia `SPEC_TEMPLATE.md` a `specs/mi-proyecto.md`
2. Llena las secciones marcadas con ⚡ (obligatorias)
3. Dile a Windsurf:
   ```
   Lee la spec en specs/mi-proyecto.md e implementa el Milestone 1
   ```

---

## 📏 Las 12 Reglas Resumidas

| # | Regla | Cómo aplica aquí |
|---|-------|-------------------|
| 1 | **Empieza con vibe PMing** | Usa `/generate-spec` para crear tu spec con ayuda de AI |
| 2 | **Stack simple** | El template te obliga a justificar cada tecnología |
| 3 | **Reglas y documentación** | `.windsurf/rules/global.md` controla el comportamiento de AI |
| 4 | **Pide plan, no código** | Las reglas globales obligan a Windsurf a explicar antes de codear |
| 5 | **Pide opciones simples** | Las reglas priorizan la solución más simple siempre |
| 6 | **Pasos pequeños** | Los milestones dividen el proyecto en bloques testeables |
| 7 | **Usa imágenes** | La spec tiene sección para mockups y screenshots |
| 8 | **Testea cada cambio** | `/implement-milestone` verifica después de cada tarea |
| 9 | **Revierte sin miedo** | Las reglas sugieren revertir antes de arreglar en cascada |
| 10 | **Usa Git** | Cada milestone tiene un commit tag definido |
| 11 | **Usa tu voz** | Compatible con dictado por voz — las specs son lenguaje natural |
| 12 | **Pide explicaciones** | Usa `/review-code` para entender y limpiar tu código |

---

## 💡 Tips para escribir buenas specs

### ✅ Haz esto
- Describe funcionalidades como **historias de usuario**: "Como [rol], quiero [acción], para [beneficio]"
- Define **criterios de aceptación** claros: "El usuario debe ver un mensaje de éxito"
- Mantén los milestones **pequeños y testeables**
- Incluye **ejemplos concretos** de datos de entrada y salida esperada

### ❌ Evita esto
- No escribas código en la spec (eso lo hace Windsurf)
- No uses jerga técnica si no la dominas
- No hagas milestones gigantes con 20 tareas
- No dejes secciones obligatorias (⚡) vacías

---

## 🔄 Flujo de trabajo recomendado

```
1. Crear spec          →  /generate-spec
2. Implementar M1      →  /implement-milestone
3. Probar M1           →  Tú pruebas manualmente
4. Commit M1           →  git commit + tag
5. Implementar M2      →  /implement-milestone
6. ...repetir...
7. Revisar código      →  /review-code
8. Release final       →  git tag v1.0-release
```

---

## ❓ Prompts útiles para Windsurf

| Situación | Prompt |
|-----------|--------|
| Empezar proyecto | `/generate-spec` |
| Implementar siguiente paso | `/implement-milestone` |
| Algo se rompió | "Revierte el último cambio" |
| No entiendes el código | "Explica cómo funciona [archivo] en términos simples" |
| Quieres opciones | "Dame 3 opciones para [funcionalidad], empezando por la más simple. No codees." |
| Limpiar código | `/review-code` |
| Agregar funcionalidad | "Según la spec RF-XXX, implementa [funcionalidad]" |
| Verificar estado | "¿En qué milestone estamos y qué falta?" |

---

## 📂 Ejemplo rápido

Supongamos que quieres un dashboard de ventas:

1. Ejecutas `/generate-spec`
2. Respondes las preguntas:
   - **Nombre:** "Dashboard de Ventas Regional"
   - **Usuarios:** "Equipo de ventas (10 personas)"
   - **Problema:** "Los reportes se hacen en Excel y toman 2 horas"
3. Windsurf genera `specs/dashboard-ventas-regional.md`
4. Ejecutas `/implement-milestone` y empiezas a construir

**Resultado:** Una app funcional, construida paso a paso, sin frustraciones.
