from telethon import TelegramClient, events
import asyncio
import re

# Konfigurasi
api_id = 21305357
api_hash = 'cfe6cf4f1aff53c42592813935f5bac1'
channel_source = -1002108289721  # Channel sumber
group_destination = -1002383914499  # Grup tujuan

# Inisialisasi client
client = TelegramClient('user_session', api_id, api_hash)

@client.on(events.NewMessage(chats=channel_source))
async def forward_message(event):
    try:
        message_text = event.message.message
        print(f"Pesan diterima: {message_text}")

        # Cek apakah mengandung "KUCOIN" (tidak peduli huruf besar kecil)
        if re.search(r"kucoin", message_text, re.IGNORECASE):
            print(f"Meneruskan pesan:\n{message_text}")
            await client.send_message(
                entity=group_destination,
                message=message_text
            )
            await asyncio.sleep(1)
        else:
            print("Pesan tidak mengandung 'kucoin'.")

    except Exception as e:
        print(f"⚠️ Error saat memproses pesan: {e}")

async def main():
    await client.start()
    user = await client.get_me()
    print(f"Bot aktif sebagai: {user.username if user.username else user.phone}")
    print("Menunggu pesan dari channel...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot dihentikan secara manual.")
