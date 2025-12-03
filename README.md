# Proyecto BeagleBone - Monitor MQTT con Flask

![BeagleBone Black](Informe/figuras/f88b6ddd233f3e7a0354031500455b1d3873dd94.png)

## 📋 Descripción

Proyecto desarrollado para la asignatura **Sistemas Embebidos** del Máster Universitario de Informática Industrial y Robótica de la Universidad de La Laguna.

Sistema de monitorización en tiempo real implementado en BeagleBone Black que integra:
- **Broker MQTT** (Mosquitto)
- **Cliente MQTT** (Paho-MQTT)
- **Servidor Web** (Flask)
- **Interfaz web responsive** con actualización automática

La BeagleBone actúa simultáneamente como broker y cliente MQTT, permitiendo la visualización de datos de sensores a través de una interfaz web accesible desde cualquier dispositivo en la red local.

## 🎯 Objetivos

- Configurar BeagleBone Black como broker MQTT utilizando Mosquitto
- Implementar un cliente MQTT que se suscriba a múltiples tópicos
- Desarrollar una interfaz web con Flask para visualización de datos en tiempo real
- Integrar comunicación asíncrona mediante threading
- Validar el sistema completo con herramientas como MQTT Explorer

## 🛠️ Tecnologías Utilizadas

- **Hardware**: BeagleBone Black
- **Sistema Operativo**: Debian (Linux)
- **Lenguaje**: Python 3
- **Frameworks y Librerías**:
  - Flask (servidor web)
  - Paho-MQTT (cliente MQTT)
  - Threading (ejecución concurrente)
- **Broker MQTT**: Mosquitto
- **Frontend**: HTML5, CSS3, JavaScript

## 📁 Estructura del Proyecto

```
BeagleBone/
├── Interfaz.py                 # Aplicación principal Flask + MQTT
├── launch.txt                  # Script de lanzamiento
├── Informe/                    # Documentación LaTeX
│   ├── Beaglebone_vinaperezAlvaro.tex
│   └── figuras/               # Imágenes del informe
└── README.md                   # Este archivo
```

## 🚀 Instalación y Configuración

### 1. Configurar el Broker MQTT (Mosquitto)

```bash
# Actualizar paquetes
sudo apt-get update

# Instalar Mosquitto broker y cliente
sudo apt-get install mosquitto mosquitto-clients

# Habilitar servicio para inicio automático
sudo systemctl enable mosquitto

# Iniciar el servicio
sudo systemctl start mosquitto

# Verificar estado
sudo systemctl status mosquitto
```

### 2. Configurar Mosquitto

Editar el archivo de configuración:

```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

Añadir estas líneas:

```
listener 1883
allow_anonymous true
```

Reiniciar el servicio:

```bash
sudo systemctl restart mosquitto
```

### 3. Instalar Dependencias Python

```bash
# Instalar Flask
pip3 install flask

# Instalar Paho-MQTT
pip3 install paho-mqtt
```

### 4. Clonar el Repositorio

```bash
git clone https://github.com/AlvaroVP96/BeagleBone.git
cd BeagleBone
```

## ▶️ Ejecución

### Método 1: Usando el script de lanzamiento

```bash
bash launch.txt
```

### Método 2: Ejecución directa

```bash
python3 -m flask --app Interfaz run --host=0.0.0.0
```

### Método 3: Ejecutar el script Python

```bash
python3 Interfaz.py
```

El servidor estará disponible en: `http://<IP_BEAGLEBONE>:5000`

## 📊 Tópicos MQTT Configurados

El sistema se suscribe automáticamente a los siguientes tópicos:

| Tópico | Descripción |
|--------|-------------|
| `Sensores/temperatura` | Datos de temperatura |
| `Sensores/humedad` | Datos de humedad |
| `Sensores/Puertas/Puerta1` | Estado puerta exterior |
| `Sensores/Puertas/Puerta2` | Estado puerta interior |

## 🧪 Pruebas del Sistema

### Prueba 1: Comunicación local

Terminal 1 (Suscriptor):
```bash
mosquitto_sub -h localhost -t test/topic
```

Terminal 2 (Publicador):
```bash
mosquitto_pub -h localhost -t test/topic -m "Hola desde BeagleBone"
```

### Prueba 2: Publicar en tópicos del sistema

```bash
# Publicar temperatura
mosquitto_pub -h localhost -t Sensores/temperatura -m "25.5"

# Publicar humedad
mosquitto_pub -h localhost -t Sensores/humedad -m "60"

# Publicar estado de puerta
mosquitto_pub -h localhost -t Sensores/Puertas/Puerta1 -m "Abierta"
```

### Prueba 3: Usar MQTT Explorer

1. Descargar MQTT Explorer desde [mqtt-explorer.com](http://mqtt-explorer.com/)
2. Configurar conexión con la IP de la BeagleBone
3. Puerto: 1883
4. Conectar y publicar mensajes en los tópicos configurados

## 🌐 Interfaz Web

La interfaz web incluye:

- **Header**: Título del sistema y estado de conexión
- **Dashboard**: Grid responsive con 4 tarjetas de sensores
- **Tarjetas de sensores**:
  - 🌡️ Sensor Temperatura
  - 💧 Sensor Humedad
  - 🚪 Puerta Exterior
  - 🚪 Puerta Interior
- **Actualización automática**: Cada 2 segundos
- **Diseño responsive**: Adaptable a móviles y tablets

### Características visuales:
- Gradiente de fondo (púrpura/azul)
- Efecto hover en tarjetas
- Badges de tópicos
- Tipografía monoespaciada para datos

## 🔧 Configuración Personalizada

### Cambiar el broker MQTT

Editar en `Interfaz.py`:

```python
MQTT_BROKER = "localhost"  # Cambiar por IP del broker
MQTT_PORT = 1883
```

### Añadir nuevos tópicos

1. Definir el tópico:
```python
MQTT_TOPIC_NUEVO = "Sensores/nuevo_sensor"
```

2. Añadir variable global:
```python
ultimo_mensaje_nuevo = "Esperando actualización..."
```

3. Suscribirse en `on_connect`:
```python
client.subscribe(MQTT_TOPIC_NUEVO)
```

4. Manejar mensajes en `on_message`:
```python
elif msg.topic == MQTT_TOPIC_NUEVO:
    ultimo_mensaje_nuevo = msg.payload.decode()
```

5. Añadir tarjeta en `HTML_TEMPLATE` y pasar variable en `index()`

## 📝 Arquitectura del Sistema

```
┌─────────────────────────────────────────┐
│         BeagleBone Black                │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Mosquitto  │◄───┤ Cliente MQTT │  │
│  │    Broker    │    │  (Paho-MQTT) │  │
│  └──────┬───────┘    └──────┬───────┘  │
│         │                   │          │
│         │              ┌────▼────┐     │
│         │              │  Flask  │     │
│         │              │ Server  │     │
│         │              └────┬────┘     │
└─────────┼───────────────────┼──────────┘
          │                   │
          │                   │ HTTP
          │                   ▼
    ┌─────▼─────┐      ┌─────────────┐
    │   MQTT    │      │  Navegador  │
    │  Explorer │      │    Web      │
    └───────────┘      └─────────────┘
```

## 🔄 Flujo de Datos

1. **Publicación**: Un cliente publica un mensaje en un tópico MQTT
2. **Broker**: Mosquitto recibe y distribuye el mensaje a los suscriptores
3. **Cliente**: El cliente MQTT en `Interfaz.py` recibe el mensaje vía callback
4. **Almacenamiento**: El callback actualiza las variables globales
5. **Visualización**: Flask renderiza el HTML con los valores actuales
6. **Actualización**: JavaScript recarga la página cada 2 segundos

## 📚 Documentación Adicional

Para más detalles técnicos, consultar:
- [Informe completo en LaTeX](Informe/Beaglebone_vinaperezAlvaro.tex)
- Incluye diagramas, capturas de pantalla y explicación detallada del código

## 👨‍💻 Autor

**Álvaro Viña Pérez**
- Máster Universitario de Informática Industrial y Robótica
- Universidad de La Laguna
- GitHub: [@AlvaroVP96](https://github.com/AlvaroVP96)

## 📄 Licencia

Este proyecto está desarrollado con fines académicos para la asignatura de Sistemas Embebidos.

