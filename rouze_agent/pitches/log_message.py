import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.style_mimic import log_convo

if __name__ == "__main__":
    # usage: python pitches/log_message.py "Acme Beauty" "client" "Their reply text..."
    if len(sys.argv) < 4:
        print('usage: python pitches/log_message.py "<Client Name>" client|me "message text"')
        sys.exit(1)
    client, role, text = sys.argv[1], sys.argv[2], sys.argv[3]
    log_convo(client, role, text)
    print("[log] saved.")
