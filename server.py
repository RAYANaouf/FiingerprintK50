from flask import Flask, request
import requests

app = Flask(__name__)

# URL brute du JSON sur GitHub
GITHUB_RAW_URL = "https://raw.githubusercontent.com/RAYANaouf/FiingerprintK50/main/users.json"

def get_users():
    """
    Récupère le dictionnaire ID → Nom depuis GitHub.
    """
    try:
        r = requests.get(GITHUB_RAW_URL)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("❌ Erreur en récupérant users.json :", e)
        return {}

@app.route('/iclock/cdata', methods=['POST'])
def receive_data():
    data = request.data.decode(errors="ignore").strip()
    if not data:
        return "OK"

    table = request.args.get("table")

    if table == "ATTLOG":
        # Exemple : '1\t2026-02-07 07:35:52\t0\t1\t0\t0\t0\t0\t0\t0\t'
        fields = data.split('\t')
        if len(fields) >= 2:
            user_id = fields[0]
            timestamp = fields[1]
            users = get_users()  # récupère toujours la dernière version du JSON
            name = users.get(user_id, f"Utilisateur {user_id}")
            print(f"✅ Bienvenue {name} ! Heure : {timestamp}")
        else:
            print(f"Impossible de parser les données ATTLOG: {data}")

    return "OK"

@app.route('/iclock/getrequest', methods=['GET'])
def get_request():
    sn = request.args.get("SN")
    info = request.args.get("INFO")
    print(f"📤 COMMAND REQUEST from {sn}, INFO: {info}")

    # Demander au K50 d’envoyer tous les utilisateurs si besoin
    command = "DATA QUERY USERINFO\n"
    return command

@app.route('/')
def home():
    return "Serveur K50 actif"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)