# Guía: Ejecutar Frontend y Backend con Docker

## Opción 1: Usar docker-compose.yml del Frontend (RECOMENDADO)

El frontend ya tiene un `docker-compose.yml` completo que incluye:
- MySQL (base de datos)
- Backend Django
- Frontend React

### Pasos:

1. Ve al directorio del frontend:
```bash
cd /home/estudiante/SpendTracker-client
```

2. Levanta todos los servicios:
```bash
docker-compose up --build
```

3. Accede a:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - MySQL: localhost:3306

### Ventajas:
- Todo en un solo comando
- Todos los servicios en la misma red Docker
- Configuración ya lista
- El frontend ya está configurado para apuntar al backend

---

## Opción 2: Ejecutar Backend y Frontend por Separado

Si quieres desarrollar independientemente cada parte:

### Backend (desde SpendTracker-server):
```bash
cd /home/estudiante/SpendTracker-server
docker-compose up --build
```

### Frontend (desde SpendTracker-client):
```bash
cd /home/estudiante/SpendTracker-client
docker-compose up --build
```

**IMPORTANTE**: Si usas esta opción, asegúrate de que:
1. Solo uno de los dos docker-compose.yml tenga MySQL (para evitar conflictos de puerto)
2. Ambos usen la misma red Docker (`spendtracker-network`)
3. El frontend apunte al backend correcto (localhost:8000 desde el navegador)

---

## Opción 3: Crear un docker-compose.yml Maestro (AVANZADO)

Puedes crear un `docker-compose.yml` en el directorio padre que orqueste todo:

```yaml
version: '3.8'

services:
  db:
    # ... configuración MySQL

  backend:
    build:
      context: ./SpendTracker-server
      dockerfile: Dockerfile
    # ... configuración backend

  frontend:
    build:
      context: ./SpendTracker-client
      dockerfile: Dockerfile
    # ... configuración frontend
```

---

## Recomendación

**Usa la Opción 1** (docker-compose.yml del frontend) porque:
- Ya está configurado y funcionando
- Incluye todos los servicios necesarios
- El frontend ya está configurado para comunicarse con el backend
- Es más simple de gestionar

Si necesitas desarrollar solo el backend o solo el frontend, usa la **Opción 2** pero ten cuidado con los conflictos de puertos.

---

## Comandos útiles

### Ver logs de todos los servicios:
```bash
docker-compose logs -f
```

### Ver logs de un servicio específico:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Detener todos los servicios:
```bash
docker-compose down
```

### Detener y eliminar volúmenes (incluyendo la base de datos):
```bash
docker-compose down -v
```

### Reconstruir solo un servicio:
```bash
docker-compose up --build backend
docker-compose up --build frontend
```

### Ejecutar comandos en los contenedores:
```bash
# Backend
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py shell

# Frontend
docker-compose exec frontend sh

# Base de datos
docker-compose exec db mysql -u st_user -p1234 spend_tracker
```

