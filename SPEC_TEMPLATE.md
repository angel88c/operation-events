# 📋 Especificación de Proyecto — Vibe Coding con Windsurf

> **Instrucciones:** Copia este archivo como `specs/NOMBRE_PROYECTO.md` y llena cada sección.
> Las secciones marcadas con ⚡ son **obligatorias**. Las marcadas con 💡 son opcionales pero recomendadas.
> Enfócate en **QUÉ** quieres que haga la app, no en **CÓMO** implementarlo.

---

## ⚡ 1. Visión del Proyecto

**Nombre:** [Nombre de tu aplicación]

**Descripción en una línea:**
> [Describe tu app en una sola oración. Ej: "Dashboard interno para monitorear ventas en tiempo real"]

**¿Quién lo va a usar?**
> [Ej: "Equipo de ventas de 15 personas", "Clientes externos", "Solo yo"]

**Problema que resuelve:**
> [Ej: "Actualmente los reportes se generan manualmente en Excel y toman 2 horas"]

---

## ⚡ 2. Tech Stack

> **Regla:** Mantén el stack lo más simple posible. Menos tecnologías = menos errores.

| Capa | Tecnología | Versión | Justificación |
|------|-----------|---------|---------------|
| **Frontend/UI** | [Ej: Streamlit] | [Ej: 1.41+] | [Ej: Rápido para prototipar dashboards] |
| **Backend** | [Ej: Python] | [Ej: 3.11+] | |
| **Base de datos** | [Ej: SQLite / Ninguna] | | [Ej: Solo lectura de APIs] |
| **Autenticación** | [Ej: MSAL / Ninguna] | | |
| **APIs externas** | [Ej: Microsoft Graph] | | |
| **Despliegue** | [Ej: Docker / localhost] | | |

**Dependencias clave (requirements.txt):**
```
# Lista las librerías principales que necesitas
# Ej:
# streamlit>=1.41
# pandas>=2.0
# plotly>=5.0
```

> 💡 **Tip:** Si no estás seguro del stack, deja esta sección vacía y usa el workflow
> `/generate-spec` — Windsurf te ayudará a elegir el stack más simple.

---

## ⚡ 3. Requerimientos Funcionales

> **Instrucciones:** Describe cada funcionalidad como una historia de usuario.
> Formato: "Como [rol], quiero [acción], para [beneficio]"

### RF-001: [Nombre de la funcionalidad]
- **Historia:** Como [rol], quiero [acción], para [beneficio].
- **Criterios de aceptación:**
  - [ ] [Criterio 1: Qué debe pasar cuando...]
  - [ ] [Criterio 2: Qué debe pasar cuando...]
- **Prioridad:** 🔴 Alta / 🟡 Media / 🟢 Baja
- **Datos de entrada:** [Qué información necesita el usuario proporcionar]
- **Resultado esperado:** [Qué debe ver/obtener el usuario]

### RF-002: [Nombre de la funcionalidad]
- **Historia:** Como [rol], quiero [acción], para [beneficio].
- **Criterios de aceptación:**
  - [ ] [Criterio 1]
  - [ ] [Criterio 2]
- **Prioridad:** 🔴 Alta / 🟡 Media / 🟢 Baja
- **Datos de entrada:** [...]
- **Resultado esperado:** [...]

> 📝 Agrega tantos RF-XXX como necesites. Copia el bloque de arriba.

---

## ⚡ 4. Requerimientos No Funcionales

### Rendimiento
- **Tiempo de carga máximo:** [Ej: < 3 segundos]
- **Usuarios concurrentes:** [Ej: 1-5 / 10-50 / 100+]

### Seguridad
- **Autenticación requerida:** [Sí/No]
- **Roles de usuario:** [Ej: Admin, Viewer / No aplica]
- **Datos sensibles:** [Ej: "Contiene datos de clientes, requiere encriptación"]

### Compatibilidad
- **Navegadores:** [Ej: Chrome, Edge]
- **Dispositivos:** [Ej: Solo desktop / Responsive]

### Disponibilidad
- **Entorno:** [Ej: Solo localhost / Intranet / Internet]
- **Uptime requerido:** [Ej: Horario laboral / 24x7]

---

## ⚡ 5. Milestones (Máximo 5)

> **Regla:** Cada milestone debe ser **testeable independientemente**.
> Avanza al siguiente milestone solo cuando el actual funcione al 100%.
> Haz commit a Git al completar cada milestone.

### 🏁 Milestone 1: [Nombre — Lo mínimo funcional]
**Objetivo:** [Ej: "La app muestra la pantalla de login y autentica con Azure AD"]
- [ ] [Tarea 1.1]
- [ ] [Tarea 1.2]
- [ ] [Tarea 1.3]
- **Criterio de éxito:** [Cómo sabes que está listo]
- **Commit tag:** `v0.1-milestone1`

### 🏁 Milestone 2: [Nombre]
**Objetivo:** [...]
- [ ] [Tarea 2.1]
- [ ] [Tarea 2.2]
- **Criterio de éxito:** [...]
- **Commit tag:** `v0.2-milestone2`

### 🏁 Milestone 3: [Nombre]
**Objetivo:** [...]
- [ ] [Tarea 3.1]
- [ ] [Tarea 3.2]
- **Criterio de éxito:** [...]
- **Commit tag:** `v0.3-milestone3`

### 🏁 Milestone 4: [Nombre]
**Objetivo:** [...]
- [ ] [Tarea 4.1]
- [ ] [Tarea 4.2]
- **Criterio de éxito:** [...]
- **Commit tag:** `v0.4-milestone4`

### 🏁 Milestone 5: [Nombre — Versión final]
**Objetivo:** [...]
- [ ] [Tarea 5.1]
- [ ] [Tarea 5.2]
- **Criterio de éxito:** [...]
- **Commit tag:** `v1.0-release`

---

## 💡 6. Estructura de Proyecto

> Deja esta sección vacía si quieres que Windsurf la proponga.
> Si ya tienes una estructura, documéntala aquí para que Windsurf la respete.

```
mi-proyecto/
├── app.py                  # Punto de entrada
├── config/
│   └── settings.py         # Configuración centralizada
├── pages/
│   └── ...                 # Páginas/vistas
├── components/
│   └── ...                 # Componentes reutilizables
├── utils/
│   └── ...                 # Funciones auxiliares
├── auth/
│   └── ...                 # Autenticación (si aplica)
├── specs/
│   └── ...                 # Especificaciones del proyecto
├── requirements.txt
├── .env.example
└── README.md
```

---

## 💡 7. Modelo de Datos

> Describe las entidades principales de tu aplicación.
> No necesitas SQL ni esquemas técnicos — solo describe los datos en lenguaje natural.

### Entidad: [Nombre — Ej: "Usuario"]
| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| [nombre] | [texto/número/fecha/booleano] | [Para qué sirve] | [Sí/No] |
| [email] | [texto] | [Correo del usuario] | [Sí] |

### Entidad: [Nombre — Ej: "Venta"]
| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| [...] | [...] | [...] | [...] |

---

## 💡 8. Reglas de Negocio

> Describe las reglas que la aplicación debe cumplir SIEMPRE.
> Estas son restricciones lógicas, no funcionalidades.

- **RN-001:** [Ej: "Un usuario solo puede ver los datos de su propia región"]
- **RN-002:** [Ej: "Los descuentos no pueden superar el 30% sin aprobación de gerente"]
- **RN-003:** [Ej: "Las fechas de entrega deben ser al menos 3 días hábiles después del pedido"]

---

## 💡 9. Integraciones Externas

| Servicio | Propósito | Autenticación | Documentación |
|----------|-----------|---------------|---------------|
| [Ej: Microsoft Graph API] | [Ej: Obtener usuarios de Azure AD] | [Ej: OAuth2 / API Key] | [URL de docs] |
| [Ej: SendGrid] | [Ej: Enviar notificaciones por email] | [API Key] | [URL] |

---

## 💡 10. Diseño / UI

> Incluye screenshots, wireframes o mockups si los tienes.
> Si no, describe la interfaz en lenguaje natural.

**Estilo general:** [Ej: "Minimalista, colores corporativos azul y blanco"]

**Pantallas principales:**
1. **[Nombre pantalla]:** [Descripción de qué muestra y qué puede hacer el usuario]
2. **[Nombre pantalla]:** [...]

> 💡 **Tip:** Puedes adjuntar imágenes en la carpeta `specs/mockups/` y referenciarlas aquí.

---

## 📌 Notas Adicionales

> Cualquier contexto extra que Windsurf deba conocer.
> Ej: "Esta app reemplaza un proceso manual en Excel", "Los datos vienen de SAP", etc.

---

## ✅ Checklist Pre-Desarrollo

Antes de empezar a codear, verifica:

- [ ] La visión del proyecto está clara (Sección 1)
- [ ] El tech stack está definido y es simple (Sección 2)
- [ ] Hay al menos 3 requerimientos funcionales (Sección 3)
- [ ] Los milestones están definidos y son testeables (Sección 5)
- [ ] El archivo está guardado en `specs/NOMBRE_PROYECTO.md`
- [ ] Las reglas de Windsurf están configuradas (`.windsurf/rules/`)
