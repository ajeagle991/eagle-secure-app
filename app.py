from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import threading
from collections import defaultdict

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Volatile memory: store messages per receiver as list of dicts
message_store = defaultdict(list)  # key: receiver_id, value: list of fragments

# Automatic 10-second cleaner thread
def clean_expired_messages():
    while True:
        time.sleep(10)
        for receiver in list(message_store.keys()):
            if message_store[receiver]:
                # clear all fragments for that user after 10 secs
                message_store[receiver] = []
        print("[CLEANER] Purged all message fragments (10-sec TTL)")

cleaner_thread = threading.Thread(target=clean_expired_messages, daemon=True)
cleaner_thread.start()

@app.route('/api/send', methods=['POST'])
def send_message():
    data = request.get_json()
    sender = data.get('sender')
    receiver = data.get('receiver')
    text = data.get('text')
    
    if not sender or not receiver or not text:
        return jsonify({"error": "Missing fields"}), 400
    
    # Create fragment (complete message as one fragment for simplicity - but hex style)
    fragment = f"[FRAG][FROM:{sender}] {text} - timestamp:{int(time.time())}"
    
    # Store for receiver
    message_store[receiver].append({
        "fragment": fragment,
        "timestamp": time.time()
    })
    print(f"[SEND] {sender} -> {receiver} | msg: {text}")
    return jsonify({"status": "sent", "fragment": fragment}), 200

@app.route('/api/receive/<receiver_id>', methods=['GET'])
def receive_messages(receiver_id):
    if receiver_id not in message_store or not message_store[receiver_id]:
        return jsonify({"status": "empty"}), 200
    
    # Get the most recent fragment and remove it (military-grade one-time fetch)
    fragments_list = message_store[receiver_id]
    if fragments_list:
        latest = fragments_list.pop(0)   # FIFO
        return jsonify({"fragment": latest["fragment"]}), 200
    
    return jsonify({"status": "empty"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)