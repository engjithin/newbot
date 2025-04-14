import os

os.makedirs("data", exist_ok=True)

# utils.py

import json
import os

STORAGE_PATH = "data/storage.json"

# Create directories if they don't exist
os.makedirs("data", exist_ok=True)

SNIPING_WALLETS_FILE = "data/sniping_wallets.json"
SIM_WALLETS_FILE = "data/simulation_wallets.json"
SETTINGS_FILE = "data/settings.json"

# === Utility for File Handling ===
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# === Sniping Wallets ===
def add_wallet(address, storage_path="data/storage.json"):
    if not os.path.exists(storage_path):
        data = {"wallets": []}
    else:
        with open(storage_path, "r") as f:
            data = json.load(f)
    
    if address in data["wallets"]:
        return False

    data["wallets"].append(address)
    with open(storage_path, "w") as f:
        json.dump(data, f, indent=4)
    return True

def remove_wallet(address):
    # Code to remove a wallet from your storage
    pass

def list_wallets():
    try:
        with open("data/storage.json", "r") as f:
            data = json.load(f)
        return data.get("wallets", [])
    except Exception as e:
        print(f"[list_wallets Error]: {e}")
        return []

def clear_wallet_logs(wallet_address):
    # Placeholder for deleting wallet-specific logs
    pass

def delete_wallet_and_logs(address, storage_path="data/storage.json"):
    address = address.strip().lower()  # Normalize input
    if not os.path.exists(storage_path):
        return False

    with open(storage_path, "r") as f:
        data = json.load(f)

    wallets = data.get("wallets", [])
    normalized_wallets = [w.lower().strip() for w in wallets]  # Normalize stored list

    if address not in normalized_wallets:
        return False

    # Remove from wallet list
    data["wallets"] = [w for w in wallets if w.lower().strip() != address]

    # Save updated data
    with open(storage_path, "w") as f:
        json.dump(data, f, indent=4)

    # Optionally delete logs
    log_path = f"data/logs/{address}.log"
    if os.path.exists(log_path):
        os.remove(log_path)

    return True

# === Base Wallet and Swap Settings ===
def set_base_wallet(private_key):
    data = load_json(SETTINGS_FILE)
    data['base_wallet'] = private_key
    save_json(SETTINGS_FILE, data)

def set_slippage(slippage):
    data = load_json(SETTINGS_FILE)
    data['slippage'] = slippage
    save_json(SETTINGS_FILE, data)

def set_amount(amount):
    data = load_json(SETTINGS_FILE)
    data['swap_amount'] = amount
    save_json(SETTINGS_FILE, data)

def get_swap_logs():
    return []  # Implement log retrieval if needed

def get_simulation_logs():
    return []  # Implement simulation log retrieval if needed

# === Simulation Wallets ===
def load_sim_wallets():
    return load_json(SIM_WALLETS_FILE)

def save_sim_wallets(wallets):
    save_json(SIM_WALLETS_FILE, wallets)

def add_sim_wallet(address):
    with open(STORAGE_PATH, "r") as f:
        data = json.load(f)
    sim_wallets = data.get("simulation_wallets", [])

    if address in sim_wallets:
        print(f"Wallet {address} is already in the simulation wallets.")
        return False
    
    sim_wallets.append(address)
    data["simulation_wallets"] = sim_wallets
    with open(STORAGE_PATH, "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"Wallet {address} added to simulation wallets.")
    return True

def list_sim_wallets():
    with open(STORAGE_PATH, "r") as f:
        data = json.load(f)
    return data.get("simulation_wallets", [])

def delete_sim_wallet_and_logs(address):
    with open(STORAGE_PATH, "r") as f:
        data = json.load(f)
    
    sim_wallets = data.get("simulation_wallets", [])
    
    print(f"Attempting to delete wallet address: {address}")
    print(f"Current simulation wallets: {sim_wallets}")
    
    if address not in sim_wallets:
        print(f"Address {address} not found in simulation wallets.")
        return False
    
    sim_wallets.remove(address)
    data["simulation_wallets"] = sim_wallets
    
    with open(STORAGE_PATH, "w") as f:
        json.dump(data, f, indent=4)
    
    log_path = f"data/logs/sim_{address}.json"
    if os.path.exists(log_path):
        os.remove(log_path)
    
    print(f"Wallet address {address} deleted successfully.")
    return True

def set_sim_slippage(slippage):
    data = load_json(SETTINGS_FILE)
    data['sim_slippage'] = slippage
    save_json(SETTINGS_FILE, data)

# === Helius Webhook Sync ===
def sync_wallets_with_helius():
    from bot import HELIUS_API_KEY, HELIUS_WEBHOOK_URL
    import requests

    wallets = list_wallets()
    if not wallets:
        print("No wallets to sync.")
        return

    url = f"https://api.helius.xyz/v0/webhooks?api-key={HELIUS_API_KEY}"
    payload = {
        "webhookURL": HELIUS_WEBHOOK_URL,
        "wallets": wallets,
        "transactionTypes": ["TRANSFER", "SWAP", "TOKEN_MINT", "CREATE_POOL"],
        "webhookType": "enhanced"
    }
    response = requests.post(url, json=payload)
    print("Helius sync response:", response.json())

# === Placeholder for Actions ===
def init_wallet_connection():
    pass

def execute_swap(wallet, token):
    return True  # Stub

def schedule_auto_sell(wallet, token, delay):
    pass

def check_webhook_health():
    return True

def log_swap_result():
    pass
