from telethon import TelegramClient, events
import asyncio
import pyperclip
import re

# Konfigurasi API
api_id = 21305357
api_hash = 'cfe6cf4f1aff53c42592813935f5bac1'
channel_source = -1002108289721  # ID Channel Sumber (A)
group_destination = -1001684715713  # ID Grup Tujuan (B)

# Inisialisasi sebagai akun pengguna
client = TelegramClient('user_session', api_id, api_hash)

def format_message(message_text):
    mint_match = re.search(r'Mint: ([a-zA-Z0-9]+)', message_text)
    if mint_match:
        mint_address = mint_match.group(1)
        pyperclip.copy(mint_address)  # Salin otomatis ke clipboard
        message_text = message_text.replace(mint_address, f'<a href="https://solscan.io/account/{mint_address}" style="color:blue;">{mint_address}</a>')
    return message_text

@client.on(events.NewMessage(chats=channel_source))
async def forward_message(event):
    try:
        message_text = event.message.message
        print(f"📩 Pesan diterima: {message_text}")  # Menampilkan semua pesan yang masuk

        if "kucoin" in message_text.lower():  # Hanya jika mengandung "KuCoin"
            formatted_text = format_message(message_text)
            print(f"✅ Meneruskan pesan: {formatted_text}")  # Tampilkan pesan yang diteruskan
            await client.send_message(
                entity=group_destination,
                message=formatted_text,
                parse_mode='html'
            )
            await asyncio.sleep(1)  # Hindari flood limit Telegram
        else:
            print("❌ Pesan tidak mengandung 'KuCoin', tidak diteruskan.")
    except Exception as e:
        print(f"⚠️ Error saat meneruskan pesan: {e}")

async def main():
    await client.start()
    user = await client.get_me()
    print(f"🚀 Bot berjalan sebagai: {user.username if user.username else user.phone}")
    print("📡 Menunggu pesan masuk...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot dihentikan secara manual dari terminal.")
