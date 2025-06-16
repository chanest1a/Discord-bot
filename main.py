import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.voice_states = True
intents.members = True

def read_tokens():
    if not os.path.exists('tokens.txt'):
        print("tokens.txt dosyası eksik!")
        return []
    with open('tokens.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]

async def join_voice_channel(bot, guild_id, channel_id):
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            print(f"Sunucu ID'si {guild_id} bulunamadı.")
            return None
        channel = guild.get_channel(int(channel_id))
        if not channel or not isinstance(channel, discord.VoiceChannel):
            print(f"Ses kanalı ID'si geçersiz: {channel_id}")
            return None
        voice_client = await channel.connect()
        print(f"{bot.user.name} {channel.name} kanalına bağlandı!")
        return voice_client
    except Exception as e:
        print(f"Ses kanalına bağlanma hatası: {e}")
        return None

async def send_message(bot, channel_id, message):
    try:
        channel = bot.get_channel(int(channel_id))
        if not channel or not isinstance(channel, discord.TextChannel):
            print(f"Metin kanalı ID'si geçersiz: {channel_id}")
            return
        await channel.send(message)
        print(f"{bot.user.name}, {channel.name} kanalına mesaj gönderdi: {message}")
    except Exception as e:
        print(f"Mesaj gönderme hatası: {e}")

async def ban_member(bot, guild_id, user_id):
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            print(f"Sunucu ID'si {guild_id} bulunamadı.")
            return
        member = guild.get_member(int(user_id))
        if not member:
            print(f"Kullanıcı ID'si {user_id} bulunamadı.")
            return
        await guild.ban(member, reason="Bot tarafından banlandı")
        print(f"{bot.user.name}, {member.name} kullanıcısını banladı.")
    except Exception as e:
        print(f"Banlama hatası: {e}")

async def mute_member(bot, guild_id, user_id):
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            print(f"Sunucu ID'si {guild_id} bulunamadı.")
            return
        member = guild.get_member(int(user_id))
        if not member:
            print(f"Kullanıcı ID'si {user_id} bulunamadı.")
            return
        await member.edit(mute=True)
        print(f"{bot.user.name}, {member.name} kullanıcısını susturdu.")
    except Exception as e:
        print(f"Susturma hatası: {e}")

async def kick_member(bot, guild_id, user_id):
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            print(f"Sunucu ID'si {guild_id} bulunamadı.")
            return
        member = guild.get_member(int(user_id))
        if not member:
            print(f"Kullanıcı ID'si {user_id} bulunamadı.")
            return
        await guild.kick(member, reason="Bot tarafından atıldı")
        print(f"{bot.user.name}, {member.name} kullanıcısını attı.")
    except Exception as e:
        print(f"Atma hatası: {e}")

async def send_dm(bot, user_id, message):
    try:
        user = await bot.fetch_user(int(user_id))
        if not user:
            print(f"Kullanıcı ID'si {user_id} bulunamadı.")
            return
        await user.send(message)
        print(f"{bot.user.name}, {user.name} kullanıcısına DM gönderdi: {message}")
    except Exception as e:
        print(f"DM gönderme hatası: {e}")

async def start_bot(token, operation, guild_id=None, channel_id=None, user_id=None, message=None):
    bot = commands.Bot(command_prefix='!', intents=intents)
    voice_client = None

    @bot.event
    async def on_ready():
        nonlocal voice_client
        print(f"{bot.user.name} giriş yaptı!")
        if operation == 'join_voice':
            voice_client = await join_voice_channel(bot, guild_id, channel_id)
        elif operation == 'send_message':
            await send_message(bot, channel_id, message)
        elif operation == 'ban_member':
            await ban_member(bot, guild_id, user_id)
        elif operation == 'mute_member':
            await mute_member(bot, guild_id, user_id)
        elif operation == 'kick_member':
            await kick_member(bot, guild_id, user_id)
        elif operation == 'send_dm':
            await send_dm(bot, user_id, message)

    try:
        await bot.start(token)
    except Exception as e:
        print(f"Bot başlatma hatası: {e}")
        if voice_client:
            await voice_client.disconnect()
        raise

async def main():
    tokens = read_tokens()
    if not tokens:
        print("Hiçbir bot token'ı bulunamadı. tokens.txt dosyasını kontrol edin.")
        return

    bot_tasks = []
    bots = []

    print("\n=== Discord Bot Yönetim ===\n")
    while True:
        print("1. Ses kanalına bağlan")
        print("2. Metin kanalına mesaj gönder")
        print("3. Kullanıcıyı banla")
        print("4. Kullanıcıyı sustur")
        print("5. Kullanıcıyı at")
        print("6. Kullanıcıya DM gönder")
        print("7. Çıkış")
        choice = input("Seçiminizi yapın (1-7): ")

        if choice == '1':
            guild_id = input("Sunucu ID'sini girin: ")
            channel_id = input("Ses kanalı ID'sini girin: ")
            for token in tokens:
                print(f"\nBot başlatılıyor: {token[:10]}...")
                task = asyncio.create_task(start_bot(token, 'join_voice', guild_id, channel_id))
                bot_tasks.append(task)
            print("\nBotlar ses kanalına bağlandı. Çıkmak için 7'yi seçin.")
            await asyncio.Event().wait()

        elif choice == '2':
            channel_id = input("Metin kanalı ID'sini girin: ")
            message = input("Gönderilecek mesajı girin: ")
            for token in tokens:
                print(f"\nBot başlatılıyor: {token[:10]}...")
                await start_bot(token, 'send_message', channel_id=channel_id, message=message)
            print("\nMesajlar gönderildi.")

        elif choice == '3':
            guild_id = input("Sunucu ID'sini girin: ")
            user_id = input("Banlanacak kullanıcının ID'sini girin: ")
            for token in tokens:
                print(f"\nBot başlatılıyor: {token[:10]}...")
                await start_bot(token, 'ban_member', guild_id, user_id=user_id)
            print("\nBanlama işlemi tamamlandı.")

        elif choice == '4':
            guild_id = input("Sunucu ID'sini girin: ")
            user_id = input("Susturulacak kullanıcının ID'sini girin: ")
            for token in tokens:
                print(f"\nBot başlatılıyor: {token[:10]}...")
                await start_bot(token, 'mute_member', guild_id, user_id=user_id)
            print("\nSusturma işlemi tamamlandı.")

        elif choice == '5':
            guild_id = input("Sunucu ID'sini girin: ")
            user_id = input("Atılacak kullanıcının ID'sini girin: ")
            for token in tokens:
                print(f"\nBot başlatılıyor: {token[:10]}...")
                await start_bot(token, 'kick_member', guild_id, user_id=user_id)
            print("\nAtma işlemi tamamlandı.")

        elif choice == '6':
            user_id = input("DM gönderilecek kullanıcının ID'sini girin: ")
            message = input("Gönderilecek DM mesajını girin: ")
            for token in tokens:
                print(f"\nBot başlatılıyor: {token[:10]}...")
                await start_bot(token, 'send_dm', user_id=user_id, message=message)
            print("\nDM'ler gönderildi.")

        elif choice == '7':
            print("Program kapatılıyor...")
            for task in bot_tasks:
                task.cancel()
            for bot in bots:
                if bot.is_ready():
                    await bot.close()
            break
        else:
            print("Geçersiz seçim! 1-7 arasında bir sayı girin.")

    if bot_tasks:
        await asyncio.gather(*bot_tasks, return_exceptions=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram durduruldu.")