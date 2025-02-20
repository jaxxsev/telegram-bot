from telethon import TelegramClient, events
import asyncio
import pyperclip
import re

# Konfigurasi
api_id = 21305357
api_hash = 'cfe6cf4f1aff53c42592813935f5bac1'
channel_source = -1002108289721  # ID numerik channel A
group_destination = -1001684715713  # ID numerik grup B

# Inisialisasi sebagai akun pengguna
client = TelegramClient('user_session', api_id, api_hash)

def format_message(message_text):
    """Fungsi untuk memformat pesan dan mengganti mint address dengan link"""
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
        print(f"Pesan diterima: {message_text}")  # Debugging

        # Cek apakah ada kata "KuCoin"
        if "kucoin" in message_text.lower():
            # Cari pola supply yang diawali dengan 42,690 atau 42690
            supply_match = re.search(r"Supply:\s*(42,690|42690)[0-9,]*", message_text)

            if supply_match:
                formatted_text = format_message(message_text)
                print(f"Meneruskan pesan: {formatted_text}")

                await client.send_message(
                    entity=group_destination,
                    message=formatted_text,
                    parse_mode='html'
                )

                await asyncio.sleep(1)  # Hindari flood limit Telegram
            else:
                print("Pesan mengandung 'KuCoin' tetapi supply tidak sesuai.")
        else:
            print("Pesan tidak mengandung 'KuCoin'.")

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
