# Digimind Data Fetch

Automatización para descargar reportes de Digimind usando Selenium.

## Setup local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar credenciales
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar
export DIGIMIND_EMAIL="tu_email@gmail.com"
export DIGIMIND_PASSWORD="tu_password"
python test_selenium.py
```

## ¿Dónde ejecutar esto?

### ❌ **Lambda NO recomendado**
- Chrome pesa ~200MB, Lambda tiene límite de 250MB
- Timeout de 15 minutos (puede no ser suficiente)
- Necesitas layers customizados para Chrome/ChromeDriver
- Complejidad alta

### ✅ **Opciones recomendadas:**

#### 1. **GitHub Actions** (GRATIS y fácil)
```bash
# Ya está configurado en .github/workflows/fetch-report.yml
# Solo añade secrets en tu repo:
# Settings > Secrets > Actions > New secret
# - DIGIMIND_EMAIL
# - DIGIMIND_PASSWORD
```

Se ejecuta automáticamente cada día a las 8 AM UTC. También puedes ejecutar manualmente desde Actions tab.

#### 2. **Cron local** (tu Mac/servidor)
```bash
# Hacer ejecutable
chmod +x run_cron.sh

# Editar crontab
crontab -e

# Ejecutar todos los días a las 8 AM
0 8 * * * /Users/clopca/dev/github/onclusive-data-fetch/run_cron.sh
```

#### 3. **Docker + cron** (servidor propio)
```bash
cd docker
docker-compose up --build
```

#### 4. **EC2 con cron** (AWS, ~$5-10/mes)
- Crear EC2 t3.micro
- Instalar Python + Chrome
- Configurar cron
- Más control que Lambda

#### 5. **ECS Fargate Task scheduled** (AWS, ~$10-20/mes)
- Usar el Dockerfile incluido
- Crear ECS Task scheduled con EventBridge
- Mejor que Lambda para este uso

#### 6. **Railway / Render / Fly.io** (Plataformas modernas)
- Soportan Docker
- Tienen cron jobs integrados
- ~$5-10/mes

## Uso

### Test rápido (con navegador visible)
```python
from fetch_selenium import DigimindSeleniumFetcher

with DigimindSeleniumFetcher("email", "password", headless=False) as fetcher:
    fetcher.fetch(
        title="test",
        topic_id=1,
        start_date="2025-11-12T23:00:00.000Z",
        end_date="2025-11-13T22:59:59.999Z",
        output_file="report.csv",
        num_mentions=38345,
        date_range_type="TODAY"
    )
```

### Producción (headless)
```python
with DigimindSeleniumFetcher("email", "password", headless=True) as fetcher:
    fetcher.fetch(...)
```

## Estructura

```
.
├── fetch_report.py       # Versión con cookies manuales (deprecated)
├── fetch_selenium.py     # ✅ Versión con Selenium (usar esta)
├── test_selenium.py      # Script de prueba
├── run_cron.sh          # Script para cron
├── docker/
│   ├── Dockerfile       # Imagen con Chrome
│   └── docker-compose.yml
└── .github/
    └── workflows/
        └── fetch-report.yml  # GitHub Actions
```

## Recomendación final

**Para empezar rápido:** GitHub Actions (gratis, cero infraestructura)

**Para producción seria:** ECS Fargate scheduled task o EC2 con cron

**NO uses Lambda** a menos que quieras sufrir con layers de Chrome.

