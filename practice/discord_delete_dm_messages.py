"""
delete_dm_messages.py

This script is used to **automatically delete your own messages** from a private (DM) conversation with a specific user on Discord.

⚠️ Requirements:
- Your Discord user token (from browser or app)
- Your own Discord user ID
- The target user's Discord ID (the person you chatted with)

📌 Warning:
- Use this script at your own risk. Automating message deletion may go against Discord's Terms of Service.
- This script only deletes messages that you sent, not the other person's messages.
"""

import requests
import time

# === CONFIGURATION ===
TOKEN = "YOUR_DISCORD_TOKEN"           # Your Discord token (starts with "mfa." or "eyJ...")
USER_ID = "YOUR_USER_ID"               # Your own Discord user ID (as a string)
TARGET_USER_ID = "TARGET_USER_ID"      # The user ID of the person you messaged (as a string)

# === HEADERS FOR AUTHENTICATION ===
headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

# === STEP 1: Find the Direct Message (DM) channel with the target user ===
response = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers)
if response.status_code != 200:
    print(f"Failed to fetch DM channels. Status: {response.status_code}")
    exit()

channels = response.json()
dm_channel_id = None

for channel in channels:
    if "recipients" in channel:
        for recipient in channel["recipients"]:
            if recipient["id"] == TARGET_USER_ID:
                dm_channel_id = channel["id"]
                break
    if dm_channel_id:
        break

if not dm_channel_id:
    print("Failed to retrieve DM channel ID with the specified user.")
    exit()

# === STEP 2: Loop through messages in the DM and delete those sent by you ===
deleted_count = 0
last_message_id = None

while True:
    # Fetch up to 100 messages per request
    url = f"https://discord.com/api/v9/channels/{dm_channel_id}/messages?limit=100"
    if last_message_id:
        url += f"&before={last_message_id}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch messages. Status: {response.status_code}")
        break

    messages = response.json()
    if not messages:
        print("No more messages to process.")
        break

    # Filter only messages sent by you
    user_messages = [msg for msg in messages if msg["author"]["id"] == USER_ID]
    if not user_messages:
        print("No more of your messages found in this batch.")
        break

    for msg in user_messages:
        while True:
            delete_response = requests.delete(
                f"https://discord.com/api/v9/channels/{dm_channel_id}/messages/{msg['id']}",
                headers=headers
            )

            if delete_response.status_code == 204:
                deleted_count += 1
                print(f"Deleted message {msg['id']}")
                time.sleep(1.5)  # Respect rate limits
                break
            elif delete_response.status_code == 429:
                retry_after = delete_response.json().get("retry_after", 1)
                print(f"Rate limited! Waiting {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                print(f"Failed to delete message {msg['id']}, status: {delete_response.status_code}")
                break

    # Prepare to fetch older messages in the next loop
    last_message_id = messages[-1]["id"]

print(f"\n✅ Total deleted messages: {deleted_count}")

✅ What to do before running:

    Replace these placeholders:

        "YOUR_DISCORD_TOKEN" – your account token.

        "YOUR_USER_ID" – your Discord ID.

        "TARGET_USER_ID" – the person’s Discord ID you're chatting with.