# Guía de Despliegue en Render

## Estado Actual

| Recurso | URL |
|---------|-----|
| **App en Render** | https://agenciacode-studio.onrender.com |
| **Dashboard Render** | https://dashboard.render.com/web/srv-d8s9ih7avr4c73fg0u6g |

## Credenciales de Prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| `admin` | `admin123` | admin |
| `usuario1` | `user123` | user |

---

## Cómo se desplegó (resumen técnico)

1. **Web Service** creado via Render API con:
   - Runtime: Python
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn "app:create_app()"`
   - Plan: Free
   - AutoDeploy: activado (cada push a `main` dispara deploy)

2. **Base de datos**: SQLite (embebida). El seed se ejecuta automáticamente al iniciar via `create_app()` en `app/__init__.py`.

3. **Variables de entorno** configuradas:
   - `DATABASE_URL=sqlite:///agenciacode.db`
   - `FLASK_ENV=production`
   - `SECRET_KEY=render-deploy-agenciacode-2026-secure-key`
   - `MAIL_*` (SMTP Gmail)

---

## Nota sobre PostgreSQL

Se intentó usar PostgreSQL pero `psycopg2-binary` no soporta Python 3.14 (que Render usa por defecto). La app usa SQLite que:
- Se crea automáticamente al iniciar
- Hace seed con datos de prueba (`admin`/`admin123`)
- **Los datos se pierden al redeployar** (Render Free no persiste disco)

### Para datos persistentes, se necesita:
- DB externa (Railway, Supabase, Neon, etc.)
- O Render con Python 3.12 (si se puede especificar)

---

## Re-deploy manual

```bash
git push origin main
```

AutoDeploy está activado. Cada push a `main` dispara un deploy automático en Render.

---

## Verificar estado del deploy

```bash
# Via API (requiere API key de Render)
curl -s "https://api.render.com/v1/services/srv-d8s9ih7avr4c73fg0u6g/deploys?limit=1" \
  -H "Authorization: Bearer TU_API_KEY" | python3 -m json.tool
```

---

## Archivos Clave para Deploy

| Archivo | Función |
|---------|---------|
| `Procfile` | Define el start command para Render |
| `requirements.txt` | Dependencias Python |
| `app/__init__.py` | Factory que crea la app + DB + seed |
| `app/database/seed.py` | Datos iniciales (admin, clientes, proyectos) |
| `.env` | **NO** subir a Git (está en .gitignore) |

---

## Solución de Problemas

| Problema | Solución |
|----------|----------|
| App no inicia | Verificar start command: `gunicorn "app:create_app()"` |
| Login falla | Verificar que el seed ejecuta (logs de Render) |
| App se duerme (15 min) | Render Free duerme la app tras 15 min de inactividad |
| Datos se pierden | SQLite no persiste en Render Free. Usar DB externa para persistencia |
