# Despliegue en EasyPanel sin Dominio

## Configuración Previa

1. **Configurar Streamlit para producción**:
   - El archivo `.streamlit/config.toml` ya está configurado con `address = "0.0.0.0"`
   - Puerto configurado a `3001`

2. **Variables de entorno**:
   - Copia `.env.example` a `.env`
   - Configura `ENABLE_AUTH=false` para despliegue sin autenticación

## Opción 1: Usar Docker Compose (Recomendado)

1. **Sube tu código a un repositorio Git** (GitHub, GitLab, etc.)

2. **En EasyPanel**:
   - Crea un nuevo sitio/aplicación
   - Selecciona "Docker Compose"
   - Usa el siguiente contenido:

```yaml
version: "3.8"

services:
  app:
    image: python:3.11-slim
    working_dir: /app
    command: ["streamlit", "run", "app.py"]
    ports:
      - "3001:3001"
    environment:
      - ENABLE_AUTH=false
      - STREAMLIT_SERVER_PORT=3001
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
      - STREAMLIT_SERVER_HEADLESS=true
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3001/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    # Instalar dependencias
    build_context: .
    build_commands:
      - "pip install --no-cache-dir -r requirements.txt"
```

## Opción 2: Usar Imagen Docker Pre-construida

1. **Construye y sube tu imagen a Docker Hub**:

```bash
# Construir imagen
docker build -t tu-usuario/streamlit-app .

# Subir a Docker Hub
docker push tu-usuario/streamlit-app
```

2. **En EasyPanel**:
   - Crea nuevo sitio
   - Selecciona "Docker"
   - Imagen: `tu-usuario/streamlit-app`
   - Puerto: `3001`
   - Variables de entorno:
     - `ENABLE_AUTH=false`
     - `STREAMLIT_SERVER_PORT=3001`
     - `STREAMLIT_SERVER_ADDRESS=0.0.0.0`

## Opción 3: Aplicación Python Directa

1. **En EasyPanel**:
   - Crea nuevo sitio
   - Selecciona "Python"
   - Versión: 3.11
   - Comando de inicio: `streamlit run app.py --server.port=3001 --server.address=0.0.0.0`
   - Variables de entorno:
     - `ENABLE_AUTH=false`

## Configuración de Red

EasyPanel te asignará automáticamente una URL como:
- `https://tu-app.tu-servidor.easypanel.host`

No necesitas configurar dominio personalizado.

## Verificación

Una vez desplegado, tu app será accesible en:
- `https://tu-app.tu-servidor.easypanel.host:3001`

## Troubleshooting

1. **Error 502**: Verifica que el puerto `3001` esté correctamente expuesto
2. **Error de importación**: Asegúrate de que todas las dependencias estén en `requirements.txt`
3. **Autenticación**: Configura `ENABLE_AUTH=false` para pruebas

## Notas Importantes

- La configuración actual deshabilita la autenticación de Microsoft 365
- Para producción, considera configurar un dominio personalizado y SSL
- Los datos se perderán si el contenedor se reinicia (considera agregar persistencia)
