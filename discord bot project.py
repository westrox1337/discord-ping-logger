import discord
from discord.ext import tasks, commands
import datetime
import os

#intents ayarlarımız
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

LOG_FILE = "bot_status.log"

def write_log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

@bot.event
async def on_ready():
    write_log(f"Botun aktif! giriş yaptıgı hesap: {bot.user.name} (ID: {bot.user.id})")
    if not log_status.is_running():
        log_status.start()

@tasks.loop(seconds=60)
async def log_status():
    latency = round(bot.latency * 1000, 2)
    guild_count = len(bot.guilds)
    total_members = sum(g.member_count for g in bot.guilds if g.member_count)
    
    status_msg = f"PING: {latency}ms | Sunucu: {guild_count} | Toplam Kullanıcı: {total_members}"
    write_log(status_msg)

@log_status.before_loop
async def before_log():
    await bot.wait_until_ready()

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN", "BURAYA_BOT_TOKENI_YAZIN")
    if TOKEN == "BURAYA_BOT_TOKENI_YAZIN":
        print("[UYARI] Discord tokenınız gecersız.!")
    else:
        bot.run(TOKEN)