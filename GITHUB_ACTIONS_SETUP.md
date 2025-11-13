# GitHub Actions Setup

## Quick Start (5 minutos)

### 1. Sube el código a GitHub

```bash
cd /Users/clopca/dev/github/onclusive-data-fetch

git init
git add .
git commit -m "Add Digimind fetcher with GitHub Actions"

# Crea el repo en github.com primero, luego:
git remote add origin https://github.com/TU_USUARIO/onclusive-data-fetch.git
git branch -M main
git push -u origin main
```

### 2. Configura los secrets

1. Ve a tu repo en GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Añade:

| Name | Value |
|------|-------|
| `DIGIMIND_EMAIL` | `cristobal.callejon@gmail.com` |
| `DIGIMIND_PASSWORD` | tu contraseña |

### 3. Primera ejecución

1. Ve a la pestaña **Actions**
2. Click en **Fetch Digimind Report** (lado izquierdo)
3. Click **Run workflow** → **Run workflow**
4. Espera ~5 minutos
5. Cuando termine, baja a **Artifacts** y descarga el CSV

### 4. Verifica que funciona

Deberías ver algo así:

```
✓ Set up Python
✓ Install dependencies  
✓ Install Chrome
✓ Fetch report
  Logging in as cristobal.callejon@gmail.com...
  Login successful!
  Generating report: test-all-today
  Status: PROCESSING - Progress: 45%
  Status: COMPLETED - Progress: 100%
  Report downloaded to: digimind_report.csv
  Done!
✓ Upload report as artifact
```

## Workflows disponibles

Tienes 3 workflows para elegir:

### 1. Basic (solo descarga)
📄 `.github/workflows/fetch-report.yml` (YA ACTIVADO)

El CSV se guarda como artifact en GitHub por 30 días.

### 2. Con S3 (subida automática)
📄 `.github/workflows/fetch-with-s3.yml`

**Secrets adicionales necesarios:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` (ej: `eu-west-1`)
- `S3_BUCKET` (ej: `mi-bucket-reports`)

Sube automáticamente a `s3://tu-bucket/digimind-reports/YYYYMMDD_HHMMSS/`

### 3. Con Email (envía por correo)
📄 `.github/workflows/fetch-with-email.yml`

**Secrets adicionales necesarios:**
- `SMTP_USERNAME` (tu Gmail)
- `SMTP_PASSWORD` (App Password de Gmail, no tu contraseña normal)

Para crear App Password:
1. Ve a https://myaccount.google.com/security
2. Verificación en dos pasos → App Passwords
3. Genera una nueva para "Mail"
4. Usa ese password en el secret

## Horarios

Por defecto: **8 AM UTC cada día** = 9 AM Madrid (invierno) / 10 AM (verano)

Para cambiar el horario, edita el cron:

```yaml
schedule:
  - cron: '0 8 * * *'  # Formato: minuto hora día mes día-semana
```

Ejemplos:

```yaml
# Medianoche UTC
- cron: '0 0 * * *'

# Cada 6 horas
- cron: '0 */6 * * *'

# 9 AM UTC, solo lunes a viernes
- cron: '0 9 * * 1-5'

# 7 AM y 7 PM UTC
- cron: '0 7,19 * * *'
```

Usa https://crontab.guru/ para validar expresiones cron.

## Ejecutar manualmente

Puedes ejecutar el workflow cuando quieras:

1. **Actions** → **Fetch Digimind Report**
2. **Run workflow** → **Run workflow**

## Troubleshooting

### "Error: secrets.DIGIMIND_PASSWORD is not set"
→ Añade los secrets en Settings > Secrets and variables > Actions

### "Timeout waiting for report"
→ El reporte tardó más de 10 minutos. Aumenta `max_wait_time` en `fetch_selenium.py`

### "Chrome not found"
→ El workflow ya instala Chrome automáticamente, pero si falla, actualiza la action:
```yaml
- uses: browser-actions/setup-chrome@latest
```

### No veo artifacts
→ Verifica que el workflow terminó con éxito (✓ verde)
→ Los artifacts expiran después de 30 días

## Costos

**GRATIS** con GitHub Free:
- 2000 minutos/mes de Actions (Ubuntu)
- Cada ejecución tarda ~5-10 minutos
- Puedes ejecutar ~200-400 veces al mes sin pagar

Si ejecutas 1 vez al día = 30 ejecuciones/mes = ~300 minutos/mes = **$0**

## Monitoreo

GitHub te envía email si un workflow falla 3 veces seguidas.

Para notificaciones instantáneas, usa el workflow con email o añade webhooks de Slack/Discord.

## Logs

Los logs se guardan por 90 días. Puedes verlos en:
**Actions** → Click en cualquier ejecución → Click en cada step para ver detalles

## Próximos pasos

✅ Configurar secrets
✅ Primera ejecución manual
⬜ Esperar a la ejecución automática de mañana
⬜ (Opcional) Configurar S3 o email
⬜ (Opcional) Ajustar horario según necesidad

