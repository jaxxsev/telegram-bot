from telethon import TelegramClient, events
import asyncio
import re

# Konfigurasi
api_id = 21305357
api_hash = 'cfe6cf4f1aff53c42592813935f5bac1'
channel_source = -1001758611100  # ID numerik channel sumber yang baru
group_destination = -1002383914499  # ID numerik grup tujuan

# Inisialisasi sebagai akun pengguna
client = TelegramClient('user_session', api_id, api_hash)

@client.on(events.NewMessage(chats=channel_source))
async def forward_message(event):
    try:
        message_text = event.message.message
        print(f"Pesan diterima: {message_text}")  # Debugging

        # Cek apakah pesan mengandung "SONIC" atau "$sonic" (tidak case sensitive)
        if re.search(r"\bSONIC\b|\$sonic", message_text, re.IGNORECASE):
            print(f"Meneruskan pesan tanpa perubahan:\n{message_text}")
            
            await client.send_message(
                entity=group_destination,
                message=message_text  # Mengirim pesan tanpa perubahan
            )
            
            await asyncio.sleep(1)  # Hindari flood limit Telegram
        else:
            print("Pesan tidak mengandung 'SONIC' atau '$sonic'.")
    
    except Exception as e:
        print(f"⚠️ Error saat meneruskan pesan: {e}")

async def main():
    await client.start()
    user = await client.get_me()
    print(f"Bot berjalan sebagai: {user.username if user.username else user.phone}")
    print("Menunggu pesan...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot dihentikan secara manual dari terminal.")
