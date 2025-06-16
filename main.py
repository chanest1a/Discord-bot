import discord
from discord.ext import commands
import asyncio
import os
import random
import datetime
from datetime import timezone

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.voice_states = True
intents.members = True
intents.reactions = True

class CloseTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket'ı Kapat", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_button(self, interaction: discord.Interaction):
        print(f"Buton tıklandı: Kanal: {interaction.channel.name}, Kullanıcı: {interaction.user.name}, Sunucu: {interaction.guild.name}")
        if not interaction.channel.name.startswith("ticket-"):
            print("Hata: Bu buton ticket kanalında değil.")
            await interaction.response.send_message("Bu buton yalnızca ticket kanallarında kullanılabilir!", ephemeral=True)
            return
        try:
            # Botun izinlerini kontrol et
            if not interaction.channel.permissions_for(interaction.guild.me).manage_channels:
                print("Hata: Botun kanalı silme izni yok.")
                await interaction.response.send_message("Botun bu kanalı silme izni yok. Lütfen botun 'Kanalları Yönet' iznini kontrol edin.", ephemeral=True)
                return
            await interaction.response.send_message("Ticket kapatılıyor...", ephemeral=True)
            await interaction.channel.delete()
            print(f"{interaction.client.user.name}, {interaction.channel.name} ticket kanalını kapattı.")
        except discord.errors.Forbidden:
            print("Hata: Botun kanalı silme izni yok (Forbidden).")
            await interaction.followup.send("Ticket kapatılırken bir hata oluştu: Botun kanalı silme izni yok.", ephemeral=True)
        except discord.errors.HTTPException as e:
            print(f"HTTP hatası: {e}")
            await interaction.followup.send(f"Ticket kapatılırken bir hata oluştu: {e}", ephemeral=True)
        except Exception as e:
            print(f"Genel hata: {e}")
            await interaction.followup.send(f"Ticket kapatılırken bir hata oluştu: {e}", ephemeral=True)

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

async def start_giveaway(bot, channel_id, duration, prize, winner_count):
    try:
        channel = bot.get_channel(int(channel_id))
        if not channel or not isinstance(channel, discord.TextChannel):
            print(f"Metin kanalı ID'si geçersiz: {channel_id}")
            return
        try:
            duration = int(duration)
            if duration <= 0:
                print("Geçersiz süre: Süre pozitif bir sayı olmalı.")
                await channel.send("Çekiliş başlatılamadı: Süre pozitif bir sayı olmalı.")
                return
        except ValueError:
            print("Geçersiz süre: Sayısal bir değer girin.")
            await channel.send("Çekiliş başlatılamadı: Geçerli bir süre (dakika) girin.")
            return
        try:
            winner_count = int(winner_count)
            if winner_count <= 0:
                print("Geçersiz kazanan sayısı: Pozitif bir sayı olmalı.")
                await channel.send("Çekiliş başlatılamadı: Kazanan sayısı pozitif olmalı.")
                return
        except ValueError:
            print("Geçersiz kazanan sayısı: Sayısal bir değer girin.")
            await channel.send("Çekiliş başlatılamadı: Geçerli bir kazanan sayısı girin.")
            return

        end_time = datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=duration)
        embed = discord.Embed(
            title="🎉 Çekiliş! 🎉",
            description=f"**Ödül**: {prize}\n**Kazanan Sayısı**: {winner_count}\n**Bitiş Zamanı**: <t:{int(end_time.timestamp())}:R>\nKatılmak için 🎉 emojisine tıklayın!",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(timezone.utc)
        )
        embed.set_footer(text=f"Çekiliş {bot.user.name} tarafından düzenleniyor.")
        message = await channel.send(embed=embed)
        await message.add_reaction("🎉")
        print(f"{bot.user.name}, {channel.name} kanalında çekiliş headlattı: {prize}, {winner_count} kazanan, {duration} dakika")

        await asyncio.sleep(duration * 60)
        message = await channel.fetch_message(message.id)
        reaction = next((r for r in message.reactions if str(r.emoji) == "🎉"), None)
        if not reaction:
            await channel.send("Çekilişe kimse katılmadı! Çekiliş iptal edildi.")
            print(f"Çekilişe katılım olmadı: {prize}")
            return

        users = [user async for user in reaction.users() if not user.bot]
        if not users:
            await channel.send("Çekilişe kimse katılmadı! Çekiliş iptal edildi.")
            print(f"Çekilişe katılım olmadı: {prize}")
            return

        winners = random.sample(users, min(winner_count, len(users)))
        winner_mentions = ", ".join(winner.mention for winner in winners)
        await channel.send(f"Tebrikler {winner_mentions}! **{prize}** ödülünü kazandınız!")
        for winner in winners:
            try:
                await winner.send(f"Tebrikler! {channel.guild.name} sunucusundaki **{prize}** çekilişini kazandın!")
                print(f"{winner.name} kullanıcısına kazanan DM'si gönderildi.")
            except Exception as e:
                print(f"{winner.name} kullanıcısına DM gönderilemedi: {e}")
        print(f"Çekiliş sona erdi, kazananlar: {[w.name for w in winners]}, ödül: {prize}")
    except Exception as e:
        print(f"Çekiliş hatası: {e}")
        try:
            await channel.send("Çekiliş sırasında bir hata oluştu. Lütfen tekrar deneyin.")
        except:
            pass

async def setup_ticket_system(bot, guild_id, channel_id, category_id=None):
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            print(f"Sunucu ID'si {guild_id} bulunamadı.")
            return
        channel = guild.get_channel(int(channel_id))
        if not channel or not isinstance(channel, discord.TextChannel):
            print(f"Metin kanalı ID'si geçersiz: {channel_id}")
            return
        category = guild.get_channel(int(category_id)) if category_id else None
        if category_id and (not category or not isinstance(category, discord.CategoryChannel)):
            print(f"Kategori ID'si geçersiz: {category_id}")
            return

        embed = discord.Embed(
            title="📩 Destek Talebi Oluştur",
            description="Bir destek talebi oluşturmak için 📩 emojisine tıklayın!",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Destek {bot.user.name} tarafından yönetiliyor.")
        message = await channel.send(embed=embed)
        await message.add_reaction("📩")
        print(f"{bot.user.name}, {channel.name} kanalında ticket sistemi kurdu.")
    except Exception as e:
        print(f"Ticket sistemi kurulum hatası: {e}")

async def create_ticket(bot, guild, user, category=None):
    try:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }
        for role in guild.roles:
            if role.permissions.manage_channels or role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)

        channel_name = f"ticket-{user.name}-{user.discriminator}"
        ticket_channel = await guild.create_text_channel(
            channel_name,
            category=category,
            overwrites=overwrites
        )
        embed = discord.Embed(
            title="Destek Talebi",
            description=f"{user.mention}, talebiniz oluşturuldu. Lütfen sorununuzu detaylı bir şekilde açıklayın.\nTicket'ı kapatmak için aşağıdaki butona tıklayın.",
            color=discord.Color.green()
        )
        view = CloseTicketButton()
        await ticket_channel.send(embed=embed, view=view)
        print(f"{bot.user.name}, {user.name} için ticket kanalı oluşturdu: {ticket_channel.name}")
        return ticket_channel
    except Exception as e:
        print(f"Ticket oluşturma hatası: {e}")
        return None

async def start_bot(token, operation, guild_id=None, channel_id=None, user_id=None, message=None, duration=None, prize=None, winner_count=None, category_id=None):
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
        elif operation == 'start_giveaway':
            await start_giveaway(bot, channel_id, duration, prize, winner_count)
        elif operation == 'setup_ticket':
            await setup_ticket_system(bot, guild_id, channel_id, category_id)

    @bot.event
    async def on_reaction_add(reaction, user):
        if user.bot or str(reaction.emoji) != "📩":
            return
        message = reaction.message
        if not message.embeds or "Destek Talebi Oluştur" not in message.embeds[0].title:
            return
        guild = message.guild
        category = message.channel.category
        ticket_channel = await create_ticket(bot, guild, user, category)
        if ticket_channel:
            await reaction.remove(user)

    @bot.event
    async def on_interaction(interaction):
        print(f"Etkileşim alındı: Tür: {interaction.type}, Custom ID: {interaction.data.get('custom_id') if interaction.data else 'Yok'}, Kanal: {interaction.channel.name if interaction.channel else 'Yok'}, Kullanıcı: {interaction.user.name}")
        if interaction.type == discord.InteractionType.component and interaction.data.get('custom_id') == 'close_ticket':
            await CloseTicketButton().close_button(interaction)
        else:
            print(f"İşlenmeyen etkileşim: Custom ID: {interaction.data.get('custom_id') if interaction.data else 'Yok'}")

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
        print("7. Çekiliş başlat")
        print("8. Ticket sistemi kur")
        print("9. Çıkış")
        choice = input("Seçiminizi yapın (1-9): ")

        if choice == '1':
            guild_id = input("Sunucu ID'sini girin: ")
            channel_id = input("Ses kanalı ID'sini girin: ")
            for token in tokens:
                print(f"\nBot başlatılıyor: {token[:10]}...")
                task = asyncio.create_task(start_bot(token, 'join_voice', guild_id, channel_id))
                bot_tasks.append(task)
            print("\nBotlar ses kanalına bağlandı. Çıkmak için 9'u seçin.")
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
            channel_id = input("Çekilişin yapılacağı metin kanalı ID'sini girin: ")
            duration = input("Çekiliş süresi (dakika cinsinden): ")
            prize = input("Çekiliş ödülü: ")
            winner_count = input("Kazanan sayısı (varsayılan 1): ") or "1"
            for token in tokens:
                print(f"\nBot başlatılıyor: {token[:10]}...")
                task = asyncio.create_task(start_bot(token, 'start_giveaway', channel_id=channel_id, duration=duration, prize=prize, winner_count=winner_count))
                bot_tasks.append(task)
            print("\nÇekiliş başlatıldı. Çıkmak için 9'u seçin.")
            await asyncio.Event().wait()

        elif choice == '8':
            guild_id = input("Sunucu ID'sini girin: ")
            channel_id = input("Ticket sisteminin kurulacağı metin kanalı ID'sini girin: ")
            category_id = input("Ticket kanallarının oluşturulacağı kategori ID'sini girin (isteğe bağlı, boş bırakabilirsiniz): ") or None
            for token in tokens:
                print(f"\nBot başlatılıyor: {token[:10]}...")
                task = asyncio.create_task(start_bot(token, 'setup_ticket', guild_id, channel_id, category_id=category_id))
                bot_tasks.append(task)
            print("\nTicket sistemi kuruldu. Çıkmak için 9'u seçin.")
            await asyncio.Event().wait()

        elif choice == '9':
            print("Program kapatılıyor...")
            for task in bot_tasks:
                task.cancel()
            for bot in bots:
                if bot.is_ready():
                    await bot.close()
            break
        else:
            print("Geçersiz seçim! 1-9 arasında bir sayı girin.")

    if bot_tasks:
        await asyncio.gather(*bot_tasks, return_exceptions=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram durduruldu.")