from flask import Flask
import paho.mqtt.client as mqtt
import threading

app = Flask(__name__)

# Variable global para almacenar el último mensaje recibido
ultimo_mensaje = "Esperando mensaje..."

# Configuración MQTT
MQTT_BROKER = "localhost"  # Cambia esto por la IP de tu broker MQTT
MQTT_PORT = 1883
MQTT_TOPIC = "test"  # Cambia esto por tu topic

# Callback cuando se conecta al broker MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker MQTT con código: {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"Suscrito al topic: {MQTT_TOPIC}")

# Callback cuando se recibe un mensaje
def on_message(client, userdata, msg):
    global ultimo_mensaje
    ultimo_mensaje = msg.payload.decode()
    print(f"Mensaje recibido en {msg.topic}: {ultimo_mensaje}")

# Inicializar cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Conectar al broker en un hilo separado
def start_mqtt():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

# Iniciar MQTT en segundo plano
mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
mqtt_thread.start()

@app.route("/")
def hola_mundo():
    return f"""
    <html>
        <head>
            <title>MQTT Monitor</title>
            <meta http-equiv="refresh" content="2">
        </head>
        <body>
            <h1>Monitor MQTT</h1>
            <h2>Último mensaje recibido:</h2>
            <p style="font-size: 24px; color: blue;">{ultimo_mensaje}</p>
            <p style="font-size: 14px; color: gray;">Topic: {MQTT_TOPIC}</p>
        </body>
    </html>
    """
