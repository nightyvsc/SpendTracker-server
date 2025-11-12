#!/bin/bash

set -e

echo "Esperando a que MySQL esté listo..."
python << END
import sys
import time
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

max_attempts = 30
attempt = 0

while attempt < max_attempts:
    try:
        connection.ensure_connection()
        print("MySQL está listo!")
        sys.exit(0)
    except Exception as e:
        attempt += 1
        if attempt >= max_attempts:
            print(f"Error: No se pudo conectar a MySQL después de {max_attempts} intentos")
            sys.exit(1)
        print(f"Intento {attempt}/{max_attempts}: MySQL no está listo aún. Esperando...")
        time.sleep(2)
END

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Iniciando servidor..."
exec "$@"

