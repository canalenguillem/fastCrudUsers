#!/bin/bash

# Crear estructura de directorios
mkdir -p app/{models,crud,schemas,routers}
touch app/{__init__.py,main.py,database.py}
touch app/models/{__init__.py,user.py}
touch app/crud/{__init__.py,user.py}
touch app/schemas/{__init__.py,user.py}
touch app/routers/{__init__.py,user.py}
touch requirements.txt

echo "Estructura del proyecto creada exitosamente."