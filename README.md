# 💰 SpendTracker – Backend

> Gestor de gastos personales. API REST con JWT, CRUD de finanzas y reportes (resumen, categorías, tendencias).

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.x-red.svg)](https://www.django-rest-framework.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.x-orange.svg)](https://www.mysql.com/)

---

## 📋 Índice

- [Arquitectura](#-arquitectura)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación-rápida)
- [Base de datos](#-base-de-datos-mysql)
- [Ejecución](#-ejecución)
- [Autenticación JWT](#-autenticación-jwt)
- [API Endpoints](#-api-endpoints)
  - [Finances](#finances)
  - [Reports](#reports)
- [Pruebas](#-pruebas)
- [Postman](#-postman-tips)
- [Flujo Git](#-flujo-git)

---

## 🏗️ Arquitectura

```
SpendTracker-server/
├─ apps/
│  ├─ accounts/   # Auth + perfil
│  ├─ finances/   # Categorías, Gastos, Metas, Dashboard
│  └─ reports/    # Resumen, Categorías, Tendencias (analytics)
├─ config/        # settings/urls/wsgi
├─ manage.py
└─ requirements.txt
```

### Módulos principales:

- **accounts**: Login JWT, registro, perfil, cambio de contraseña
- **finances**: `Category`, `Expense`, `SavingsGoal` y utilidades de periodo/balance
- **reports**: Endpoints analíticos (sin modelos propios; usan `finances`)

---

## 📦 Requisitos

- Python **3.12**
- MySQL **8.x**
- Git
- Postman (opcional)

---

## 🚀 Instalación rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/nightyvsc/SpendTracker-server.git
cd SpendTracker-server
```

### 2. Crear entorno virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> ⚠️ **Nota**: Asegúrate de que `.gitignore` incluya `.venv/`, `__pycache__/`, etc.

---

## 🗄️ Base de datos (MySQL)

### Configuración por defecto

En `config/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "spend_tracker",
        "USER": "st_user",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

### Crear base de datos y usuario

```sql
CREATE DATABASE IF NOT EXISTS spend_tracker
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'st_user'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON spend_tracker.* TO 'st_user'@'localhost';
FLUSH PRIVILEGES;
```

### Migraciones y superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Para tests (opcional)

Django crea automáticamente `test_spend_tracker`. Si es necesario:

```sql
GRANT ALL PRIVILEGES ON `test_spend_tracker`.* TO 'st_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## ▶️ Ejecución

```bash
python manage.py runserver
```

Servidor disponible en: **http://127.0.0.1:8000**

---

## 🔐 Autenticación (JWT)

### Rutas disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/auth/login/` | Obtener tokens (access + refresh) |
| `POST` | `/api/auth/refresh/` | Renovar access token |
| `POST` | `/api/auth/signup/` | Registro de usuario |
| `GET` | `/api/auth/profile/` | Perfil del usuario |
| `POST` | `/api/auth/change-password/` | Cambiar contraseña |

### 🔑 Login

**Request:**
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "usuario",
  "password": "clave"
}
```

**Response:**
```json
{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}
```

### Usar en requests protegidos

Agregar header:
```
Authorization: Bearer <JWT_ACCESS_TOKEN>
```

### 🔄 Refresh token

**Request:**
```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "JWT_REFRESH_TOKEN"
}
```

---

## 📡 API Endpoints

### Finances

**Base URL:** `/api/`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/categories/` | Lista categorías del usuario |
| `POST` | `/categories/` | Crea categoría (`name`, `icon?`, `color?`) |
| `DELETE` | `/categories/<id>/delete/` | Elimina categoría (gastos quedan sin categoría) |
| `GET` | `/expenses/` | Lista gastos (ordenados por fecha desc) |
| `POST` | `/expenses/` | Crea gasto (`date`, `category?`, `amount`, `description?`) |
| `GET` | `/expenses/<id>/` | Detalle de un gasto |
| `PUT/PATCH` | `/expenses/<id>/` | Edita gasto |
| `DELETE` | `/expenses/<id>/` | Elimina gasto |
| `GET` | `/savings/` | Lista metas de ahorro |
| `POST` | `/savings/` | Crea meta de ahorro |
| `GET/PUT/DELETE` | `/savings/<id>/` | Operaciones sobre meta específica |
| `GET` | `/dashboard/summary/` | Resumen simple del periodo actual |

> 🔒 **Todos los endpoints requieren autenticación JWT**

---

### Reports

**Base URL:** `/api/reports/`

#### 1️⃣ Summary (Resumen)

Obtiene totales diarios y mensuales.

```http
GET /api/reports/summary/?start=YYYY-MM-DD&end=YYYY-MM-DD&daily_limit=7&monthly_limit=6
```

**Parámetros:**
- `start` *(opcional)*: Fecha de inicio
- `end` *(opcional)*: Fecha de fin
- `daily_limit` *(opcional)*: Límite de días a mostrar (default: 7)
- `monthly_limit` *(opcional)*: Límite de meses a mostrar (default: 6)

**Response:**
```json
{
  "filters": {
    "start": "2025-10-01",
    "end": "2025-10-31",
    "daily_limit": 7,
    "monthly_limit": 6
  },
  "total": 640.0,
  "daily": [
    {"date": "2025-10-31", "total": 150.0},
    {"date": "2025-10-20", "total": 80.0},
    {"date": "2025-10-15", "total": 250.0}
  ],
  "monthly": [
    {"month": "2025-10", "total": 640.0}
  ]
}
```

---

#### 2️⃣ By Category (Por categoría)

Gastos agrupados por categoría.

```http
GET /api/reports/by-category/?start=YYYY-MM-DD&end=YYYY-MM-DD&include_uncategorized=true&top_n=5
```

**Parámetros:**
- `start`, `end` *(opcional)*: Rango de fechas
- `include_uncategorized` *(opcional)*: Incluir gastos sin categoría (default: true)
- `top_n` *(opcional)*: Top N categorías (default: todas)

**Response:**
```json
{
  "filters": {
    "start": "2025-10-01",
    "end": "2025-10-31",
    "include_uncategorized": false,
    "top_n": 5
  },
  "total_spending": 640.0,
  "by_category": [
    {
      "category": "Comida",
      "total": 640.0,
      "pct": 100.0
    }
  ]
}
```

---

#### 3️⃣ Trend (Tendencias)

Serie temporal de gastos.

```http
GET /api/reports/trend/?start=YYYY-MM-DD&end=YYYY-MM-DD&granularity=month
```

**Parámetros:**
- `start`, `end` *(opcional)*: Rango de fechas
- `granularity` *(opcional)*: `day`, `week` o `month` (default: month)

**Response:**
```json
{
  "filters": {
    "start": "2025-09-01",
    "end": "2025-11-30",
    "granularity": "month"
  },
  "series": [
    {"period": "2025-09", "total": 90.0},
    {"period": "2025-10", "total": 640.0},
    {"period": "2025-11", "total": 40.0}
  ]
}
```

---

### ⚠️ Validaciones

- `start` debe ser menor o igual a `end` → Error 400 si no cumple
- `granularity` debe ser `day`, `week` o `month` → Error 400 si no cumple

---

## 🧪 Pruebas

### Ejecutar todos los tests

```bash
python manage.py test -v 2
```

### Solo tests de reports

```bash
python manage.py test apps.reports.tests -v 2
```

### Modo rápido (reutiliza BD)

```bash
python manage.py test apps.reports.tests --keepdb --parallel -v 2
```

### Cobertura de código (opcional)

```bash
pip install coverage
coverage run manage.py test apps.reports.tests
coverage report -m
coverage html  # Abre htmlcov/index.html
```

---

## 📮 Postman (Tips)

### Configurar Environment

| Variable | Valor inicial |
|----------|---------------|
| `base_url` | `http://127.0.0.1:8000` |
| `token` | *(vacío)* |
| `refresh_token` | *(vacío)* |

### Tests para Login

En la pestaña **Tests** del request de login:

```javascript
pm.environment.set("token", pm.response.json().access);
pm.environment.set("refresh_token", pm.response.json().refresh);
```

### Usar token en requests protegidos

```
Authorization: Bearer {{token}}
```

### Tests para Refresh

```javascript
pm.environment.set("token", pm.response.json().access);
```

---

## 🌿 Flujo Git

- **Rama base**: `develop`
- **Features**: `feature/<nombre>` (ej: `feature/reports-sebas`)
- **Pull Request** → `develop` (con reviewers y checks)

### Después del merge

```bash
git fetch origin
git switch develop
git pull origin develop
```

---

## 👥 Contribuidores

- [@nightyvsc](https://github.com/nightyvsc)
- [@santibeltrann](https://github.com/santibeltrann)
- [@sebasbasto](https://github.com/sebasbasto)
- [@PerezsA-ux](https://github.com/PerezsA-ux)

---

## 📄 Licencia

Este proyecto es parte de un trabajo académico de Desarrollo de Software.

---

⭐ **¡Si te gustó el proyecto, deja una estrella!**
