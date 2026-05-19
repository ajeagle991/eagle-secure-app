import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

# ==================== HARDCODED CREDENTIALS ====================
RENDER_API_KEY = "rnd_W8LBVZ1k7opxzqXMspxdPAuPVzPK"

# ==================== SECURE NODE WHITELIST (500 IDs) ====================
ALLOWED_NODES = [
    "10a23", "11b45", "12c67", "13d89", "14e01", "15f23", "16g45", "17h67", "18j89", "19k01",
    "20m23", "21n45", "22p67", "23q89", "24r01", "25s23", "26t45", "27u67", "28v89", "29w01",
    "30x23", "31y45", "32z67", "33a89", "34b01", "35c23", "36d45", "37e67", "38f89", "39g01",
    "40h23", "41j45", "42k67", "43m89", "44n01", "45p23", "46q45", "47r67", "48s89", "49t01",
    "50u23", "51v45", "52w67", "53x89", "54y01", "55z23", "56a45", "57b67", "58c89", "59d01",
    "60e23", "61f45", "62g67", "63h89", "64j01", "65k23", "66m45", "67n67", "68p89", "69q01",
    "70r23", "71s45", "72t67", "73u89", "74v01", "75w23", "76x45", "77y67", "78z89", "79a01",
    "80b23", "81c45", "82d67", "83e89", "84f01", "85g23", "86h45", "87j67", "88k89", "89m01",
    "90n23", "91p45", "92q67", "93r89", "94s01", "95t23", "96u45", "97v67", "98w89", "99x01",
    "10y11", "11z22", "12a33", "13b44", "14c55", "15d66", "16e77", "17f88", "18g99", "19h00",
    "20j11", "21k22", "22m33", "23n44", "24p55", "25q66", "26r77", "27s88", "28t99", "29u00",
    "30v11", "31w22", "32x33", "33y44", "34z55", "35a66", "36b77", "37c88", "38d99", "39e00",
    "40f11", "41g22", "42h33", "43j44", "44k55", "45m66", "46n77", "47p88", "48q99", "49r00",
    "50s11", "51t22", "52u33", "53v44", "54w55", "55x66", "56y77", "57z88", "58a99", "59b00",
    "60c11", "61d22", "62e33", "63f44", "64g55", "65h66", "66j77", "67k88", "68m99", "69n00",
    "70p11", "71q22", "72r33", "73s44", "74t55", "75u66", "76v77", "77w88", "78x99", "79y00",
    "80z11", "81a22", "82b33", "83c44", "84d55", "85e66", "86f77", "87g88", "88h99", "89j00",
    "90k11", "91m22", "92n33", "93p44", "94q55", "95r66", "96s77", "97t88", "98u99", "99v00",
    "10w12", "11x34", "12y56", "13z78", "14a90", "15b12", "16c34", "17d56", "18e78", "19f90",
    "20g12", "21h34", "22j56", "23k78", "24m90", "25n12", "26p34", "27q56", "28r78", "29s90",
    "30t12", "31u34", "32v56", "33w78", "34x90", "35y12", "36z34", "37a56", "38b78", "39c90",
    "40d12", "41e34", "42f56", "43g78", "44h90", "45j12", "46k34", "47m56", "48n78", "49p90",
    "50q12", "51r34", "52s56", "53t78", "54u90", "55v12", "56w34", "57x56", "58y78", "59z90",
    "60a12", "61b34", "62c56", "63d78", "64e90", "65f12", "66g34", "67h56", "68j78", "69k90",
    "70m12", "71n34", "72p56", "73q78", "74r90", "75s12", "76t34", "77u56", "78v78", "79w90",
    "80x12", "81y34", "82z56", "83a78", "84b90", "85c12", "86d34", "87e56", "88f78", "89g90",
    "90h12", "91j34", "92k56", "93m78", "94n90", "95p12", "96q34", "97r56", "98s78", "99t90",
    "10u43", "11v21", "12w87", "13x65", "14y09", "15z43", "16a21", "17b87", "18c65", "19d09",
    "20e43", "21f21", "22g87", "23h65", "24j09", "25k43", "26m21", "27n87", "28p65", "29q09",
    "30r43", "31s21", "32t87", "33u65", "34v09", "35w43", "36x21", "37y87", "38z65", "39a09",
    "40b43", "41c21", "42d87", "43e65", "44f09", "45g43", "46h21", "47j87", "48k65", "49m09",
    "50n43", "51p21", "52q87", "53r65", "54s09", "55t43", "56u21", "57v87", "58w65", "59x09",
    "60y43", "61z21", "62a87", "63b65", "64c09", "65d43", "66e21", "67f87", "68g65", "69h09",
    "70j43", "71k21", "72m87", "73n65", "74p09", "75q43", "76r21", "77s87", "78t65", "79u09",
    "80v43", "81w21", "82x87", "83y65", "84z09", "85a43", "86b21", "87c87", "88d65", "89e09",
    "90f43", "91g21", "92h87", "93j65", "94k09", "95m43", "96n21", "97p87", "98q65", "99r09",
    "10s55", "11t66", "12u77", "13v88", "14w99", "15x00", "16y11", "17z22", "18a33", "19b44",
    "20c55", "21d66", "22e77", "23f88", "24g99", "25h00", "26j11", "27k22", "28m33", "29n44",
    "30p55", "31q66", "32r77", "33s88", "34t99", "35u00", "36v11", "37w22", "38x33", "39y44",
    "40z55", "41a66", "42b77", "43c88", "44d99", "45e00", "46f11", "47g22", "48h33", "49j44",
    "50k55", "51m66", "52n77", "53p88", "54q99", "55r00", "56s11", "57t22", "58u33", "59v44",
    "60w55", "61x66", "62y77", "63z88", "64a99", "65b00", "66c11", "67d22", "68e33", "69f44",
    "70g55", "71h66", "72j77", "73k88", "74m99", "75n00", "76p11", "77q22", "78r33", "79s44",
    "80t55", "81u66", "82v77", "83w88", "84x99", "85y00", "86z11", "87a22", "88b33", "89c44",
    "90d55", "91e66", "92f77", "93g88", "94h99", "95j00", "96k11", "97m22", "98n33", "99p44",
    "10q50", "11r60", "12s70", "13t80", "14u90", "15v10", "16w20", "17x30", "18y40", "19z50",
    "20a60", "21b70", "22c80", "23d90", "24e10", "25f20", "26g30", "27h40", "28j50", "29k60",
    "30m70", "31n80", "32p90", "33q10", "34r20", "35s30", "36t40", "37u50", "38v60", "39w70",
    "40x80", "41y90", "42z10", "43a20", "44b30", "45c40", "46d50", "47e60", "48f70", "49g80",
    "50h90", "51j10", "52k20", "53m30", "54n40", "55p50", "56q60", "57r70", "58s80", "59t90"
]

# Ephemeral message buffer
message_buffer = {}

# ==================== API KEY VALIDATION ====================
def validate_api_key():
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != RENDER_API_KEY:
        return False
    return True

# ==================== ROUTES ====================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "system": "Eagle Secure App",
        "status": "operational",
        "version": "1.0.0"
    }), 200

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "operational", "system": "Eagle Secure App"}), 200

@app.route("/api/authorize", methods=["POST"])
def authorize_node():
    if not validate_api_key():
        return jsonify({"error": "Invalid API Key"}), 401
    
    data = request.get_json()
    if not data or "node_id" not in data:
        return jsonify({"error": "Missing node_id"}), 400
    
    node_id = data["node_id"]
    if node_id in ALLOWED_NODES:
        return jsonify({"authorized": True, "node_id": node_id}), 200
    else:
        return jsonify({"authorized": False, "error": "Unauthorized Node ID"}), 401

@app.route("/api/send", methods=["POST"])
def send_message():
    if not validate_api_key():
        return jsonify({"error": "Invalid API Key"}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body"}), 400
    
    sender_id = data.get("sender_id")
    target_id = data.get("target_id")
    message = data.get("message")
    attachment = data.get("attachment", None)  # Base64 attachment
    
    if not sender_id or not target_id or not message:
        return jsonify({"error": "Missing required fields"}), 400
    
    if sender_id not in ALLOWED_NODES:
        return jsonify({"error": "Sender Node ID not authorized"}), 401
    
    if target_id not in ALLOWED_NODES:
        return jsonify({"error": "Target Node ID not authorized"}), 401
    
    if target_id not in message_buffer:
        message_buffer[target_id] = []
    
    message_obj = {
        "from": sender_id,
        "to": target_id,
        "content": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if attachment:
        message_obj["attachment"] = attachment
    
    message_buffer[target_id].append(message_obj)
    
    return jsonify({"status": "sent", "to": target_id}), 200

@app.route("/api/receive/<node_id>", methods=["GET"])
def receive_messages(node_id):
    if not validate_api_key():
        return jsonify({"error": "Invalid API Key"}), 401
    
    if node_id not in ALLOWED_NODES:
        return jsonify({"error": "Node ID not authorized"}), 401
    
    messages = message_buffer.get(node_id, [])
    
    # EPHEMERAL: Delete messages immediately after retrieval
    if node_id in message_buffer:
        message_buffer[node_id] = []
    
    return jsonify({"node_id": node_id, "messages": messages}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)