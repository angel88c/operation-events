# 📋 Especificación de Proyecto — Operation Events

> Generado con el workflow `/generate-spec` de Windsurf
> Fecha: 12/02/2026

---

## ⚡ 1. Visión del Proyecto

**Nombre:** Operation Events

**Descripción en una línea:**
> Aplicación para captura y análisis de eventos operativos registrados en producción.

**¿Quién lo va a usar?**
> Gerentes, Directivos, Ingenieros y Técnicos de ensamble.

**Problema que resuelve:**
> Actualmente los eventos se registran manualmente en SharePoint sin lógica de negocio, sin notificaciones automáticas, sin análisis gráfico ni filtros. Operation Events centraliza la captura, agrega notificaciones automáticas al responsable y dashboards con gráficos Pareto, tendencias e insights para análisis y toma de decisiones.

---

## ⚡ 2. Tech Stack

| Capa | Tecnología | Versión | Justificación |
|------|-----------|---------|---------------|
| **Frontend/UI** | Streamlit | 1.38+ | Rápido para prototipar dashboards internos |
| **Backend** | Python | 3.11+ | Ecosistema maduro para datos y APIs |
| **Base de datos** | Microsoft Lists (SharePoint) | vía MS Graph API | Mantener SharePoint como fuente de datos con acceso programático |
| **Autenticación** | MSAL (Microsoft 365) | 1.28+ | SSO corporativo ya configurado |
| **Gráficos** | Plotly | 5.18+ | Gráficos interactivos (Pareto, tendencias) |
| **Tablas** | AgGrid | 1.0+ | Tablas editables con filtros avanzados |
| **Notificaciones** | MS Graph API (email) | — | Envío de correos vía Outlook sin dependencias extra |
| **Despliegue** | Docker + docker-compose | — | Contenedorización para servidor interno |

**Dependencias clave (requirements.txt):**
```
streamlit>=1.38.0
msal>=1.28.0
pandas>=2.1.0
numpy>=1.26.0
streamlit-aggrid>=1.0.0
plotly>=5.18.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
email-validator>=2.1.0
python-dotenv>=1.0.0
requests>=2.31.0
httpx>=0.27.0
streamlit-option-menu>=0.3.12
openpyxl>=3.1.0
xlsxwriter>=3.1.0
```

---

## ⚡ 3. Requerimientos Funcionales

### RF-001: Captura de Eventos Operativos
- **Historia:** Como técnico/ingeniero, quiero registrar un evento operativo detectado en producción, para que quede documentado y se notifique al responsable.
- **Criterios de aceptación:**
  - [ ] Formulario con los siguientes campos:
    - Persona que detecta hallazgo (selector de usuarios M365)
    - Tipo de Impacto (selector dependiente del catálogo)
    - Causa (selector dinámico filtrado por Tipo de Impacto)
    - Número de Proyecto (texto, máximo 10 caracteres)
    - Número de Parte / Número de Plano (texto, máximo 15 caracteres)
    - Responsable (selector de usuarios M365)
    - Comentarios adicionales (texto, máximo 300 caracteres con contador)
    - Fecha de Hallazgo (automática, fecha y hora del día de captura)
  - [ ] La causa se filtra dinámicamente según el tipo de impacto seleccionado
  - [ ] Botón "Enviar y Guardar" guarda en Microsoft List y envía email al responsable
  - [ ] Validación de campos obligatorios antes de enviar
  - [ ] Mensaje de confirmación al guardar exitosamente
- **Prioridad:** 🔴 Alta
- **Datos de entrada:** Todos los campos del formulario
- **Resultado esperado:** Evento guardado en Microsoft List + email enviado al responsable

### RF-002: Gestión de Eventos
- **Historia:** Como gerente/ingeniero, quiero ver todos los eventos en una tabla editable, para dar seguimiento con acciones correctivas y preventivas.
- **Criterios de aceptación:**
  - [ ] Tabla con columnas provenientes de la captura: Responsable, Impacto, Causa
  - [ ] Campos adicionales editables:
    - Acción Correctiva (texto, máximo 300 caracteres)
    - Acción Preventiva (texto, máximo 300 caracteres)
    - Fecha Plan (formato dd/MM/AAAA)
    - Fecha Real de Cierre (formato dd/MM/AAAA)
    - Status (selector: Open, Closed, On Going, Cancelled)
  - [ ] Filtro por Responsable (driver) que sumariza todos los eventos
  - [ ] Re-asignación y edición de responsable
  - [ ] Definición si es interno o proveedor
  - [ ] Botón "Guardar" que persiste cambios en la base de datos (Microsoft List)
  - [ ] Visualización de toda la información de la base de datos
- **Prioridad:** 🔴 Alta
- **Datos de entrada:** Edición de campos en la tabla
- **Resultado esperado:** Cambios guardados en Microsoft List

### RF-003: Reportes y Análisis
- **Historia:** Como directivo/gerente, quiero ver gráficos y análisis de los eventos, para tomar decisiones basadas en datos.
- **Criterios de aceptación:**
  - [ ] Gráfico Pareto de Causas (barras de frecuencia + línea de % acumulado)
  - [ ] Gráfico de Tendencia Mensual de eventos (barras por mes)
  - [ ] Sección de Insights Importantes:
    - Top 3 Causas Críticas
    - Proyectos con Más Eventos
    - Recomendaciones
  - [ ] Botón "Exportar Reporte" (descarga en Excel)
  - [ ] Botón "Actualizar Datos" para refrescar desde la base de datos
  - [ ] Filtros por rango de fechas, tipo de impacto, proyecto, etc.
- **Prioridad:** 🔴 Alta
- **Datos de entrada:** Filtros de consulta
- **Resultado esperado:** Gráficos interactivos y reporte exportable

### RF-004: Configuración
- **Historia:** Como administrador, quiero gestionar los catálogos y conexiones, para mantener la app actualizada sin modificar código.
- **Criterios de aceptación:**
  - [ ] Prueba de conexión a SharePoint con indicador visual (éxito/fallo)
  - [ ] CRUD de catálogo de Tipos de Impacto (agregar, editar, eliminar)
  - [ ] CRUD de catálogo de Causas asociadas a cada Tipo de Impacto (agregar, editar, eliminar)
  - [ ] Los cambios en catálogos se reflejan inmediatamente en la pantalla de Captura
- **Prioridad:** 🟡 Media
- **Datos de entrada:** Valores de catálogos
- **Resultado esperado:** Catálogos actualizados y reflejados en toda la app

### RF-005: Notificaciones por Email
- **Historia:** Como responsable asignado, quiero recibir un email cuando me asignen un evento, para actuar de inmediato.
- **Criterios de aceptación:**
  - [ ] Al guardar un evento nuevo, se envía email al responsable vía MS Graph API
  - [ ] El email incluye: tipo de impacto, causa, número de proyecto, número de parte, comentarios y enlace a la app
  - [ ] El email tiene formato profesional y legible
- **Prioridad:** 🔴 Alta
- **Datos de entrada:** Datos del evento capturado
- **Resultado esperado:** Email recibido por el responsable con toda la información del evento

---

## ⚡ 4. Requerimientos No Funcionales

### Rendimiento
- **Tiempo de carga máximo:** < 3 segundos por pantalla
- **Usuarios concurrentes:** 1-5

### Seguridad
- **Autenticación requerida:** Sí — Microsoft 365 (MSAL)
- **Roles de usuario:** No aplica (todos los usuarios autenticados tienen acceso completo)
- **Datos sensibles:** No contiene datos personales sensibles, solo datos operativos de producción

### Compatibilidad
- **Navegadores:** Chrome, Edge
- **Dispositivos:** Desktop (no requiere responsive)

### Disponibilidad
- **Entorno:** Docker en servidor interno (intranet)
- **Uptime requerido:** Horario laboral

---

## ⚡ 5. Milestones

### 🏁 Milestone 1: Estructura base + Pantalla de Captura
**Objetivo:** La app muestra el formulario de captura funcional con los catálogos de Impacto/Causa y guarda en Microsoft List.
- [ ] Configurar navegación sidebar con 4 pantallas (Captura, Gestión, Reportes, Configuración)
- [ ] Crear formulario de captura con todos los campos según diseño
- [ ] Implementar relación dinámica Impacto → Causa con catálogos predefinidos
- [ ] Conectar con Microsoft List para guardar eventos
- [ ] Implementar selectores de personas desde M365
- [ ] Validaciones de campos (longitud máxima, campos obligatorios)
- **Criterio de éxito:** Se puede capturar un evento completo y verlo guardado en SharePoint/Microsoft List
- **Commit tag:** `v0.1-captura`

### 🏁 Milestone 2: Notificaciones por Email
**Objetivo:** Al guardar un evento, se envía email automático al responsable vía MS Graph API.
- [ ] Integrar envío de email vía MS Graph API
- [ ] Diseñar template del email con datos del evento
- [ ] Incluir enlace a la app en el email
- [ ] Validar que el email llega correctamente al responsable
- **Criterio de éxito:** El responsable recibe un email profesional con los datos del evento al guardarlo
- **Commit tag:** `v0.2-notificaciones`

### 🏁 Milestone 3: Pantalla de Gestión de Eventos
**Objetivo:** Tabla editable para dar seguimiento a eventos con acciones correctivas/preventivas.
- [ ] Tabla AgGrid con datos de la base de datos (Responsable, Impacto, Causa)
- [ ] Campos editables: Acción Correctiva, Acción Preventiva, Fecha Plan, Fecha Real de Cierre, Status
- [ ] Filtro por Responsable (driver) que sumariza eventos
- [ ] Re-asignación de responsable
- [ ] Definición interno/proveedor
- [ ] Botón "Guardar" que persiste cambios en Microsoft List
- **Criterio de éxito:** Se pueden editar eventos, asignar acciones, cambiar status y guardar cambios
- **Commit tag:** `v0.3-gestion`

### 🏁 Milestone 4: Pantalla de Reportes y Análisis
**Objetivo:** Dashboard con gráficos Pareto, tendencias e insights para toma de decisiones.
- [ ] Gráfico Pareto de Causas con Plotly (barras + línea % acumulado)
- [ ] Gráfico de Tendencia Mensual de eventos
- [ ] Sección de Insights: Top 3 causas críticas, proyectos con más eventos, recomendaciones
- [ ] Botón "Exportar Reporte" (Excel con openpyxl/xlsxwriter)
- [ ] Botón "Actualizar Datos" para refrescar desde la base de datos
- **Criterio de éxito:** Los gráficos muestran datos reales de Microsoft List y se puede exportar reporte
- **Commit tag:** `v0.4-reportes`

### 🏁 Milestone 5: Configuración + Versión Final
**Objetivo:** Pantalla de configuración completa y app lista para producción en Docker.
- [ ] Prueba de conexión a SharePoint con indicador visual
- [ ] CRUD de catálogo Tipos de Impacto
- [ ] CRUD de catálogo Causas (asociadas a cada Tipo de Impacto)
- [ ] Revisión general de todas las pantallas
- [ ] Pruebas de integración end-to-end
- [ ] Despliegue final en Docker
- **Criterio de éxito:** App completa funcionando en Docker con todas las pantallas operativas
- **Commit tag:** `v1.0-release`

---

## 💡 6. Estructura de Proyecto

```
streamlit-operation-events/
├── app.py                      # Punto de entrada principal
├── config/
│   ├── settings.py             # Configuración centralizada
│   ├── theme.py                # Estilos CSS personalizados
│   └── catalogs.py             # Catálogos de Impacto/Causa
├── pages/
│   ├── capture.py              # Pantalla de Captura de Eventos
│   ├── event_management.py     # Pantalla de Gestión de Eventos
│   ├── reports.py              # Pantalla de Reportes y Análisis
│   └── settings_page.py        # Pantalla de Configuración
├── components/
│   ├── navigation.py           # Sidebar con navegación
│   ├── forms.py                # Componentes de formulario reutilizables
│   ├── tables.py               # Componentes de tabla (AgGrid)
│   └── charts.py               # Componentes de gráficos (Plotly)
├── auth/
│   └── microsoft.py            # Autenticación MSAL + MS Graph
├── utils/
│   ├── sharepoint.py           # Conexión y CRUD con Microsoft List
│   ├── email_service.py        # Envío de emails vía MS Graph
│   └── validators.py           # Validaciones de formulario
├── specs/
│   └── operation-events.md     # Esta especificación
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 💡 7. Modelo de Datos

### Entidad: Evento Operativo (Microsoft List)
| Campo | Tipo | Descripción | Requerido | Restricción |
|-------|------|-------------|-----------|-------------|
| id | autonumérico | Identificador único del evento | Sí | Auto-generado |
| persona_detecta | texto | Persona que detecta el hallazgo (usuario M365) | Sí | Selector M365 |
| tipo_impacto | texto | Tipo de impacto del evento | Sí | Catálogo configurable |
| causa | texto | Causa asociada al tipo de impacto | Sí | Filtrada por tipo_impacto |
| numero_proyecto | texto | Número de proyecto | Sí | Máximo 10 caracteres |
| numero_parte | texto | Número de parte / número de plano | Sí | Máximo 15 caracteres |
| responsable | texto | Responsable asignado (usuario M365) | Sí | Selector M365 |
| comentarios | texto | Comentarios adicionales | No | Máximo 300 caracteres |
| fecha_hallazgo | fecha/hora | Fecha y hora de captura | Sí | Automática (día de captura) |
| accion_correctiva | texto | Acción correctiva definida | No | Máximo 300 caracteres |
| accion_preventiva | texto | Acción preventiva definida | No | Máximo 300 caracteres |
| fecha_plan | fecha | Fecha planeada de cierre | No | Formato dd/MM/AAAA |
| fecha_real_cierre | fecha | Fecha real de cierre | No | Formato dd/MM/AAAA |
| status | texto | Estado del evento | Sí | Open / Closed / On Going / Cancelled |
| tipo_origen | texto | Interno o Proveedor | No | Selector |

### Entidad: Catálogo de Impacto-Causa (Configuración)
| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| tipo_impacto | texto | Nombre del tipo de impacto | Sí |
| causa | texto | Causa asociada | Sí |
| activo | booleano | Si está activo en el catálogo | Sí |

---

## 💡 8. Reglas de Negocio

- **RN-001:** La causa solo puede seleccionarse después de elegir el tipo de impacto, y debe pertenecer al catálogo asociado a ese impacto.
- **RN-002:** La fecha de hallazgo se asigna automáticamente al momento de la captura y no es editable.
- **RN-003:** Al guardar un evento nuevo, se debe enviar obligatoriamente un email al responsable asignado.
- **RN-004:** El status inicial de todo evento nuevo es "Open".
- **RN-005:** Solo se puede establecer "Fecha Real de Cierre" cuando el status cambia a "Closed".
- **RN-006:** Los cambios en los catálogos de configuración se reflejan inmediatamente en el formulario de captura.
- **RN-007:** El número de proyecto no puede exceder 10 caracteres y el número de parte no puede exceder 15 caracteres.

---

## 💡 9. Integraciones Externas

| Servicio | Propósito | Autenticación | Documentación |
|----------|-----------|---------------|---------------|
| Microsoft Graph API | Obtener usuarios de Azure AD para selectores | OAuth2 (MSAL) | https://learn.microsoft.com/graph/api/ |
| Microsoft Graph API | Enviar emails de notificación vía Outlook | OAuth2 (MSAL) | https://learn.microsoft.com/graph/api/user-sendmail |
| SharePoint / Microsoft Lists | Almacenamiento de eventos operativos | OAuth2 (MSAL) | https://learn.microsoft.com/graph/api/resources/list |

---

## 💡 10. Diseño / UI

**Estilo general:** Profesional, limpio, colores corporativos azul y blanco. Interfaz tipo dashboard empresarial.

**Pantallas principales:**
1. **Captura de Datos Básicos:** Formulario con campos en layout de 2 columnas. Selectores desplegables para personas M365, tipo de impacto y causa. Contador de caracteres en comentarios. Fecha automática visible. Botón "Enviar y Guardar" centrado al final.
2. **Gestión de Eventos:** Tabla AgGrid con todas las columnas. Filtro superior por Responsable. Campos editables inline. Botón "Guardar" para persistir cambios.
3. **Reportes y Análisis:** Dos gráficos principales lado a lado (Pareto + Tendencia Mensual). Sección de Insights debajo con tarjetas (Top 3 Causas, Proyectos con más eventos, Recomendaciones). Botones "Exportar Reporte" y "Actualizar Datos" al final.
4. **Configuración:** Prueba de conexión a SharePoint con indicador. Tablas editables para catálogos de Tipo de Impacto y Causas asociadas.

---

## 💡 11. Catálogos Iniciales

### Tipo de Impacto → Causas

**Paro de Ensamble:**
- Falla de equipo
- Falta de material
- Material incorrecto
- Material en hold de calidad
- Instrucción de trabajo incorrecta / no disponible
- Falta de Personal
- Personal no capacitado
- Ausentismo
- Retraso en surtido interno
- Defecto detectado en Máquina
- Contención activa
- Cambio urgente de prioridad

**Retrabajo:**
- Defecto de material
- Especificación incorrecta
- Instrucción de trabajo no clara
- Método no estandarizado
- Error de ensamble
- Falta de capacitación
- Cambio Eng no implementado
- Criterio de aceptación incorrecto
- Defecto de proveedor

**Mejora del Proceso:**
- Tiempo ciclo alto
- Cuello de botella
- Alta tasa de defectos
- Variabilidad del proceso
- Riesgo ergonómico
- Riesgo de accidente
- Scrap elevado
- Uso excesivo de consumibles
- Exceso de movimiento
- Layout ineficiente
- Proceso no estandarizado
- Secuencia ineficiente
- Falta de trazabilidad
- Registro manual
- Abasto ineficiente
- Inventario innecesario

**Falta de Material:**
- Error en MRP
- Demanda mayor al forecast
- Inventario incorrecto en sistema
- Ubicación incorrecta
- Error de surtido
- Proveedor on hold
- Retraso de proveedor
- Entrega incompleta
- Problema de capacidad
- Material on hold
- Rechazo de lote
- Cambio de PN sin stock
- Retraso en transporte

---

## 📌 Notas Adicionales

- Esta app reemplaza el proceso manual de registro de eventos en SharePoint.
- Los datos existentes en SharePoint deben ser accesibles desde la app.
- La autenticación Microsoft 365 ya está configurada en el proyecto base.
- El proyecto ya cuenta con estructura de Streamlit, Docker y dependencias instaladas.

---

## ✅ Checklist Pre-Desarrollo

- [x] La visión del proyecto está clara (Sección 1)
- [x] El tech stack está definido y es simple (Sección 2)
- [x] Hay al menos 3 requerimientos funcionales (Sección 3) — 5 definidos
- [x] Los milestones están definidos y son testeables (Sección 5) — 5 milestones
- [x] El archivo está guardado en `specs/operation-events.md`
- [ ] Las reglas de Windsurf están configuradas (`.windsurf/rules/`)
