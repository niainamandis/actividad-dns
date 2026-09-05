# Actividad DNS: Construir un Resolver - CC4303

Resolver DNS iterativo en Python mediante sockets UDP que navega la jerarquía de servidores para encontrar IPs, incluye un modo debug para trazar las consultas y maneja un sistema de caché en memoria.

## Requisitos

Python 3. Se utiliza la librería estándar `socket` y la librería externa `dnslib`.

Se recomienda utilizar un entorno virtual para instalar la dependencia aislada del sistema:

```bash
# Crear el entorno virtual
python3 -m venv .venv

# Activar el entorno virtual (Linux/macOS)
source .venv/bin/activate

# Instalar la librería requerida
pip install dnslib

```

## Ejecución

Antes de correr el resolver, ajusta la variable `IP_VM` dentro de `resolver.py` según tu propia IP o máquina virtual.

```bash
python3 resolver.py

```

El servidor quedará escuchando en el puerto UDP 8000. Para probarlo:

```bash
dig -p8000 @IP_VM www.uchile.cl

```
