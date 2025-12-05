import paho.mqtt.client as mqtt
import json
import time
import random

# Configuration
BROKER = "localhost"
PORT = 1883
TOPIC_BASE = "hopital/service_A/patient_"

def get_vital_signs(patient_id):
    """Génère des données médicales simulées"""
    fievre = random.randint(0, 20) == 0
    
    # Génération de la tension (Systolique / Diastolique)
    sys = random.randint(110, 140)
    dia = random.randint(70, 90)
    tension_str = f"{sys}/{dia}"

    data = {
        "id": patient_id,
        "bpm": random.randint(110, 140) if fievre else random.randint(60, 90),
        "temp": round(random.uniform(38.5, 40.0), 1) if fievre else round(random.uniform(36.5, 37.5), 1),
        "spo2": random.randint(94, 100),
        "tension": tension_str,   # <--- C'EST ICI QUE CA MANQUAIT
        "timestamp": int(time.time())
    }
    return data

def main():
    client = mqtt.Client()
    
    print("Connexion au Broker Mosquitto...")
    try:
        client.connect(BROKER, PORT, 60)
        client.loop_start()
        print("✅ Connecté !")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return

    patients = ["001", "002", "003"]

    try:
        while True:
            for p in patients:
                donnees = get_vital_signs(p)
                topic = TOPIC_BASE + p
                payload = json.dumps(donnees)
                
                client.publish(topic, payload)
                print(f"📤 {topic} -> BPM:{donnees['bpm']} | Tension:{donnees['tension']}")
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("Arrêt de la simulation.")
        client.loop_stop()

if __name__ == "__main__":
    main()