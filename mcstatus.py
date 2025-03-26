import requests
from mcstatus import JavaServer

# Minecraft Server Details
SERVER_IP = "pms.castiamc.com"  # Replace with your server's IP or domain
PORT = 25565  # Default Java Edition port

# Discord Webhook Details
WEBHOOK_URL = "https://discord.com/api/webhooks/1354430851089170654/aqJcNDNJy2ictB8sC5Assh_VHPUKVsMtRNwjdVO07C8nUb_WVdwKNXrVZ7KfyAh7cEtk"
MESSAGE_ID = "1354431489546125454"

def get_minecraft_status():
    try:
        server = JavaServer.lookup(f"{SERVER_IP}:{PORT}")
        status = server.status()

        # Get Player List
        player_names = ", ".join([player.name for player in status.players.sample]) if status.players.sample else "No players online"

        return (
            f"🟢 **Server Online**\n"
            f"**Players:** {status.players.online}/{status.players.max}\n"
            f"**Version:** {status.version.name}\n"
            f"**Ping:** {status.latency}ms\n"
            f"**Online Players:** {player_names}"
        )
    except Exception as e:
        print(f"Error fetching server status: {e}")
        return "🔴 **Server Offline**"

def update_webhook_message(content):
    payload = {"content": content}
    headers = {"Content-Type": "application/json"}

    response = requests.patch(f"{WEBHOOK_URL}/messages/{MESSAGE_ID}", json=payload, headers=headers)

    if response.status_code == 200:
        print("✅ Webhook message updated successfully.")
    else:
        print(f"❌ Failed to update webhook message: {response.status_code}, Response: {response.text}")

# Run once per execution (GitHub Actions will handle scheduling)
status_message = get_minecraft_status()
update_webhook_message(status_message)
