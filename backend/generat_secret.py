from cryptography.fernet import Fernet
import os

# Generar una clave secreta
secret_key = Fernet.generate_key().decode()

# Especificar el archivo .env
env_file = ".env"

# Añadir o actualizar la clave secreta en el archivo .env
if os.path.exists(env_file):
    with open(env_file, 'a') as f:
        f.write(f'SECRET_KEY={secret_key}\n')
else:
    with open(env_file, 'w') as f:
        f.write(f'SECRET_KEY={secret_key}\n')

print(f"Clave secreta generada y guardada en {env_file}: {secret_key}")
