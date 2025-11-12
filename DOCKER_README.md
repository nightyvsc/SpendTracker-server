# Guía de Docker para SpendTracker

## Comandos Básicos

### Construir y levantar los contenedores
```bash
docker-compose up --build
```

### Levantar en segundo plano
```bash
docker-compose up -d
```

### Ver logs
```bash
docker-compose logs -f
```

### Detener los contenedores
```bash
docker-compose down
```

### Detener y eliminar volúmenes (incluyendo la base de datos)
```bash
docker-compose down -v
```

### Ejecutar comandos en el contenedor
```bash
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell
```

### Acceder a la base de datos MySQL
```bash
docker-compose exec db mysql -u st_user -p1234 spend_tracker
```

## Acceso

- API: http://localhost:8000
- MySQL: localhost:3306
  - Usuario: st_user
  - Contraseña: 1234
  - Base de datos: spend_tracker

