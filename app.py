from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import ssl

app = Flask(__name__)

data = {
    "temperature": " ",
    "humidity": " ",
    "heating_status": " "
}

#funzione richiamata ogni volta che arriva un messaggio mqtt.
def on_message(client, userdata, msg):
    global data
    print(f"Ricevuto: {msg.topic} -> {msg.payload.decode()}")
    if msg.topic == "home/temperature":
        data["temperature"] = msg.payload.decode()
    elif msg.topic == "home/humidity":
        data["humidity"] = msg.payload.decode()
    elif msg.topic == "home/heating":
        data["heating_status"] = msg.payload.decode()

#configura client mqtt
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.username_pw_set("usermatteogiannini", "Matteo1234")
mqtt_client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
mqtt_client.connect("1a7bb209364644989f843ad0d1a15f38.s1.eu.hivemq.cloud", 8883)
mqtt_client.subscribe("home/#")
mqtt_client.loop_start()

#rotta per la homepage
@app.route('/')
def home():
    return render_template("index.html")

#restituisce i dati in formato json
@app.route('/data')
def get_data():
    return jsonify(data)

#avvia il server Flask
if __name__ == '__main__':
    app.run(debug=True)
