# 🚀 Streamlit Professional Template

A **production-ready** Streamlit application template with Microsoft 365 authentication, advanced data tables, professional charts, validated forms, and a clean modular architecture — designed to be extended rapidly with AI assistants (Windsurf + Claude).

---

## ✨ Features

| Feature | Technology | Description |
|---|---|---|
| **Authentication** | MSAL (Microsoft 365 / Azure AD) | Full OAuth2 authorization code flow with user profile |
| **Data Tables** | streamlit-aggrid | Filtering, sorting, pagination, column visibility, CSV export |
| **Charts** | Plotly | Bar, line, area, pie, KPI indicators with consistent theming |
| **Form Validation** | Pydantic-style declarative | Text, email, number, date, select, multiselect, checkbox, regex |
| **Navigation** | streamlit-option-menu | Sidebar with icons, page routing, user menu |
| **Styling** | Custom CSS + Fluent Design | Metric cards, info cards, badges, consistent color palette |
| **Configuration** | pydantic-settings + .env | Typed settings with environment variable support |

---

## 📁 Project Structure

```
streamlit-template-ws/
├── app.py                      # 🏠 Main entry point
├── requirements.txt            # 📦 Python dependencies
├── .env.example                # 🔑 Environment variables template
├── .gitignore                  # Git ignore rules
├── .streamlit/
│   └── config.toml             # Streamlit server & theme config
│
├── auth/                       # 🔐 Authentication module
│   ├── __init__.py
│   └── microsoft.py            # MSAL OAuth2 flow, login UI, session management
│
├── config/                     # ⚙️ Configuration module
│   ├── __init__.py
│   ├── settings.py             # Pydantic Settings (loads from .env)
│   └── theme.py                # Color palette, chart colors, CSS injection
│
├── components/                 # 🧩 Reusable UI components
│   ├── __init__.py
│   ├── tables.py               # AgGrid wrapper with AgGridConfig
│   ├── charts.py               # Plotly chart library (bar, line, pie, area, KPI)
│   ├── forms.py                # Validated forms with FormField definitions
│   ├── cards.py                # Metric cards, info cards
│   └── navigation.py           # Sidebar, page header, user menu
│
├── pages/                      # 📄 Application pages
│   ├── __init__.py
│   ├── dashboard.py            # KPI metrics + charts overview
│   ├── data_explorer.py        # AgGrid table with filters & export
│   ├── forms_page.py           # Form validation demos (3 examples)
│   ├── charts_page.py          # Interactive chart gallery
│   └── settings_page.py        # Profile, environment, about
│
└── utils/                      # 🛠️ Utilities
    ├── __init__.py
    ├── helpers.py              # Formatters (currency, numbers, percentages)
    └── sample_data.py          # Sample data generators for demos
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
cd streamlit-template-ws
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
copy .env.example .env          # Windows
# cp .env.example .env          # macOS/Linux
```

Edit `.env` with your settings. **For development without Microsoft auth:**

```env
ENABLE_AUTH=false
```

### 3. Run

```bash
streamlit run app.py
```

The app will open at [http://localhost:8501](http://localhost:8501).

---

## 🔐 Microsoft 365 Authentication Setup

### Azure Portal Configuration

1. Go to [Azure Portal](https://portal.azure.com) → **Azure Active Directory** → **App registrations**
2. Click **New registration**
   - **Name:** Your app name
   - **Supported account types:** Accounts in this organizational directory only (Single tenant)
   - **Redirect URI:** Web → `http://localhost:8501`
3. Copy the **Application (client) ID** and **Directory (tenant) ID**
4. Go to **Certificates & secrets** → **New client secret** → Copy the **Value**
5. Go to **API permissions** → Add:
   - `User.Read`
   - `openid`
   - `profile`
   - `email`
6. Update your `.env`:

```env
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-secret-value
AZURE_TENANT_ID=your-tenant-id
AZURE_REDIRECT_URI=http://localhost:8501
ENABLE_AUTH=true
```

---

## 🧩 How to Extend

### Adding a New Page

1. Create `pages/my_page.py`:

```python
from components.navigation import render_page_header

def render() -> None:
    render_page_header("My Page", "Description here", icon="🆕")
    # Your page content...
```

2. Register in `components/navigation.py` → `PAGE_REGISTRY`:

```python
{"name": "My Page", "icon": "plus-circle"},
```

3. Add to the router in `app.py` → `PAGE_MAP`:

```python
"My Page": my_page.render,
```

### Using AgGrid Tables

```python
from components import render_aggrid_table, AgGridConfig

config = AgGridConfig(
    page_size=25,
    selection_mode="multiple",
    enable_export=True,
    column_config={
        "price": {"headerName": "Price ($)", "type": ["numericColumn"]},
    },
)
response = render_aggrid_table(df, config=config)
```

### Using Validated Forms

```python
from components.forms import validated_form, FormField

fields = [
    FormField(key="name", label="Name", type="text", required=True, min_length=2),
    FormField(key="email", label="Email", type="email", required=True),
    FormField(key="age", label="Age", type="number", min_value=18, max_value=120),
]

result = validated_form(fields, submit_label="Submit")
if result:
    st.success(f"Submitted: {result}")
```

### Using Charts

```python
from components import render_bar_chart, render_line_chart, render_pie_chart

render_bar_chart(df, x="category", y="revenue", title="Revenue by Category")
render_line_chart(df, x="date", y=["sales", "returns"], title="Trends")
render_pie_chart(df, names="region", values="total", title="Distribution")
```

---

## 🎨 Theming

All visual tokens are centralized in `config/theme.py`:

- **`theme.colors`** — Primary, secondary, success, warning, danger, etc.
- **`theme.chart_colors`** — Sequential, categorical, and diverging palettes
- **`theme.spacing`** — Consistent spacing values (xs through xxl)

Custom CSS is injected via `get_custom_css()` in `app.py` for metric cards, sidebar, buttons, and more.

---

## 🤖 Designed for AI-Assisted Development

This template is structured for optimal collaboration with AI coding assistants:

- **Clear module boundaries** — Each file has a single responsibility
- **Comprehensive docstrings** — Every module, class, and function is documented
- **Type hints everywhere** — Full type annotations for better AI understanding
- **Declarative patterns** — Forms and tables use config objects, not imperative code
- **Consistent naming** — Predictable file and function naming conventions
- **Sample data included** — AI can immediately test and iterate

### Recommended Workflow with Windsurf + Claude

1. Describe what you want to build
2. Reference the relevant component (e.g., "use the AgGrid table component")
3. AI reads the component's docstring and creates your page
4. Iterate with validation — forms auto-validate, charts auto-theme

---

## 📋 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web framework |
| `msal` | Microsoft authentication |
| `pandas` / `numpy` | Data handling |
| `streamlit-aggrid` | Advanced data tables |
| `plotly` | Interactive charts |
| `pydantic` / `pydantic-settings` | Settings & validation |
| `streamlit-option-menu` | Sidebar navigation |
| `requests` / `httpx` | HTTP client |
| `openpyxl` / `xlsxwriter` | Excel export |

---

## 📄 License

MIT — Use freely for your projects.
