# 🏭 Operation Events

Aplicación para **captura y análisis de eventos operativos** registrados en producción. Centraliza la captura de hallazgos, envía notificaciones automáticas al responsable y ofrece dashboards con gráficos Pareto, tendencias e insights para toma de decisiones.

**Usuarios:** Gerentes, Directivos, Ingenieros y Técnicos de ensamble.

---

## ✨ Funcionalidades

| Pantalla | Descripción |
|---|---|
| **📝 Captura** | Formulario de registro de eventos con selección dinámica de Tipo de Impacto → Causa, selector de usuarios M365, y guardado en Microsoft Lists |
| **📋 Gestión de Eventos** | Tabla AgGrid editable con filtros por responsable, status y tipo de impacto. Guardado de cambios directo a SharePoint |
| **📊 Reportes y Análisis** | Pareto de causas e impactos, tendencia mensual, eventos por proyecto, insights automáticos, métricas de eficiencia y exportación a Excel |
| **⚙️ Configuración** | Prueba de conexión a SharePoint, CRUD de catálogos (Tipos de Impacto y Causas), perfil de usuario |

### Características adicionales

- **Notificaciones por email** — Envío automático al responsable vía MS Graph API con template HTML
- **Autenticación Microsoft 365** — SSO corporativo con MSAL (OAuth2)
- **Catálogos editables** — Tipos de impacto y causas configurables con persistencia en JSON
- **Despliegue Docker** — Dockerfile + docker-compose con Nginx y SSL

---

## 🛠️ Tech Stack

| Capa | Tecnología |
|---|---|
| **Frontend/UI** | Streamlit 1.38+ |
| **Backend** | Python 3.11+ |
| **Base de datos** | Microsoft Lists (SharePoint) vía MS Graph API |
| **Autenticación** | MSAL (Microsoft 365 / Azure AD) |
| **Tablas** | streamlit-aggrid |
| **Gráficos** | Plotly |
| **Email** | MS Graph API (Mail.Send) |
| **Configuración** | pydantic-settings + .env |
| **Despliegue** | Docker + Nginx |

---

## 📁 Estructura del Proyecto

```
streamlit-operation-events/
├── app.py                      # 🏠 Punto de entrada principal
├── requirements.txt            # 📦 Dependencias Python
├── Dockerfile                  # � Imagen Docker
├── docker-compose.yml          # 🐳 Orquestación con Nginx
├── .env.example                # 🔑 Template de variables de entorno
├── .streamlit/
│   └── config.toml             # Configuración de Streamlit (puerto 3001, tema)
│
├── auth/                       # 🔐 Autenticación
│   ├── microsoft.py            # MSAL OAuth2 flow, login UI, sesión
│   └── graph_users.py          # Consulta de usuarios M365 vía Graph API
│
├── config/                     # ⚙️ Configuración
│   ├── settings.py             # Pydantic Settings (carga desde .env)
│   ├── catalogs.py             # Catálogos de Impacto/Causa con CRUD y persistencia JSON
│   └── theme.py                # Paleta de colores, CSS personalizado
│
├── components/                 # 🧩 Componentes reutilizables
│   ├── tables.py               # Wrapper AgGrid
│   ├── charts.py               # Gráficos Plotly con tema consistente
│   ├── forms.py                # Formularios con validación
│   ├── cards.py                # Tarjetas de métricas
│   └── navigation.py           # Sidebar, header, menú de usuario
│
├── pages/                      # 📄 Pantallas de la aplicación
│   ├── capture.py              # Captura de eventos (RF-001)
│   ├── event_management.py     # Gestión de eventos con AgGrid (RF-002)
│   ├── reports.py              # Reportes y análisis (RF-003)
│   └── settings_page.py        # Configuración (RF-004)
│
├── utils/                      # 🛠️ Utilidades
│   ├── sharepoint.py           # CRUD Microsoft Lists vía Graph API
│   ├── email.py                # Envío de notificaciones por email
│   └── helpers.py              # Formateadores (moneda, números, porcentajes)
│
├── specs/
│   └── operation-events.md     # Especificación completa del proyecto
│
└── nginx/                      # 🌐 Configuración Nginx (reverse proxy + SSL)
    ├── nginx.conf
    └── generate-cert.sh
```

---

## 🚀 Inicio Rápido

### 1. Clonar e instalar

```bash
git clone https://github.com/angel88c/operation-events.git
cd operation-events
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
copy .env.example .env          # Windows
# cp .env.example .env          # macOS/Linux
```

Edita `.env` con tus credenciales. **Para desarrollo sin autenticación Microsoft:**

```env
ENABLE_AUTH=false
```

### 3. Ejecutar

```bash
streamlit run app.py
```

La app se abrirá en [http://localhost:3001](http://localhost:3001).

---

## 🔐 Configuración de Microsoft 365

### Azure Portal

1. Ir a [Azure Portal](https://portal.azure.com) → **Azure Active Directory** → **App registrations**
2. **New registration**
   - **Name:** Operation Events
   - **Supported account types:** Single tenant
   - **Redirect URI:** Web → `http://localhost:3001`
3. Copiar **Application (client) ID** y **Directory (tenant) ID**
4. **Certificates & secrets** → New client secret → Copiar el **Value**
5. **API permissions** → Agregar:
   - `User.Read` — Perfil del usuario
   - `User.Read.All` (Application) — Selector de usuarios
   - `Sites.ReadWrite.All` (Application) — Lectura/escritura en Microsoft Lists
   - `Mail.Send` (Application) — Envío de notificaciones por email
6. **Grant admin consent** para los permisos de aplicación

### Variables de entorno requeridas

```env
AZURE_CLIENT_ID=tu-client-id
AZURE_CLIENT_SECRET=tu-client-secret
AZURE_TENANT_ID=tu-tenant-id
AZURE_REDIRECT_URI=http://localhost:3001

SHAREPOINT_SITE_ID=tu-site-id
SHAREPOINT_LIST_ID=tu-list-id
SHAREPOINT_DOMAIN=tuempresa.sharepoint.com
USER_DOMAIN=tuempresa.com

EMAIL_SENDER=notificaciones@tuempresa.com
APP_URL=http://localhost:3001
```

---

## 🐳 Despliegue con Docker

### Build y ejecución directa

```bash
docker build -t operation-events .
docker run -p 3001:3001 --env-file .env operation-events
```

### Con Docker Compose (incluye Nginx + SSL)

```bash
# Generar certificado SSL autofirmado
bash nginx/generate-cert.sh

# Levantar servicios
docker-compose up --build -d

# Ver logs
docker-compose logs -f
```

Acceso:
- **Local:** https://localhost
- **Red:** https://192.168.100.90

---

## 📊 Catálogos de Impacto y Causas

Los catálogos vienen preconfigurados con 4 tipos de impacto y sus causas asociadas:

| Tipo de Impacto | Causas |
|---|---|
| **Paro de Ensamble** | 12 causas (falla de equipo, falta de material, etc.) |
| **Retrabajo** | 9 causas (defecto de material, error de ensamble, etc.) |
| **Mejora del Proceso** | 16 causas (tiempo ciclo alto, cuello de botella, etc.) |
| **Falta de Material** | 13 causas (error en MRP, retraso de proveedor, etc.) |

Los catálogos se pueden editar desde **Configuración → Catálogos** y se persisten en `config/catalogs.json`.

---

## 📋 Dependencias principales

| Paquete | Propósito |
|---|---|
| `streamlit` | Framework web |
| `msal` | Autenticación Microsoft 365 |
| `pandas` / `numpy` | Manejo de datos |
| `streamlit-aggrid` | Tablas editables avanzadas |
| `plotly` | Gráficos interactivos |
| `pydantic-settings` | Configuración tipada |
| `requests` | Cliente HTTP para Graph API |
| `xlsxwriter` | Exportación a Excel |

---

## 📌 Versiones

| Tag | Milestone | Descripción |
|---|---|---|
| `v0.1-captura` | M1 | Estructura base + Pantalla de Captura |
| `v0.2-notificaciones` | M2 | Notificaciones por email vía MS Graph API |
| `v0.3-gestion` | M3 | Gestión de Eventos con AgGrid editable |
| `v0.4-reportes` | M4 | Reportes con Pareto, tendencias, insights y Excel |
| `v1.0-release` | M5 | Configuración completa + CRUD catálogos + Docker |

---

## 📄 Licencia

MIT — Uso libre para proyectos internos.
