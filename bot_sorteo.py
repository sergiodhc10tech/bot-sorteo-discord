import discord
from discord.ext import commands
import os


DISCORD_TOKEN==${{shared.DICORD_TOKEN}}
TOKEN = os.getenv(DISCORD_TOKEN)  
ARCHIVO = "participantes.txt"
sorteo_abierto = True

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- FUNCIONES DE CONTROL ----------
def es_admin(ctx):
    return ctx.author.guild_permissions.administrator

# ---------- BOT LISTO ----------
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# ---------- PARTICIPAR ----------
@bot.command()
async def participar(ctx):
    global sorteo_abierto

    if not sorteo_abierto:
        await ctx.send("⛔ El sorteo está cerrado.")
        return

    usuario = ctx.author.display_name  # <-- usa el apodo actual del servidor

    if not os.path.exists(ARCHIVO):
        open(ARCHIVO, "w").close()

    with open(ARCHIVO, "r", encoding="utf-8") as f:
        participantes = f.read().splitlines()

    if usuario in participantes:
        await ctx.send(f"❌ {usuario}, ya estás participando.")
    else:
        with open(ARCHIVO, "a", encoding="utf-8") as f:
            f.write(usuario + "\n")
        await ctx.send(f"✅ {usuario}, participación registrada.")

# ---------- LISTA ----------
@bot.command()
async def lista(ctx):
    if not os.path.exists(ARCHIVO):
        await ctx.send("📭 No hay participantes aún.")
        return

    with open(ARCHIVO, "r", encoding="utf-8") as f:
        participantes = f.read().strip()

    if participantes == "":
        await ctx.send("📭 La lista está vacía.")
    else:
        await ctx.send("🎯 **Participantes:**\n" + participantes)

# ---------- CERRAR ----------
@bot.command()
async def cerrar(ctx):
    global sorteo_abierto

    if not es_admin(ctx):
        await ctx.send("🚫 Solo un ADMIN puede cerrar el sorteo.")
        return

    sorteo_abierto = False
    await ctx.send("🔒 El sorteo ha sido **CERRADO**.")

# ---------- ABRIR ----------
@bot.command()
async def abrir(ctx):
    global sorteo_abierto

    if not es_admin(ctx):
        await ctx.send("🚫 Solo un ADMIN puede abrir el sorteo.")
        return

    sorteo_abierto = True
    await ctx.send("🔓 El sorteo ha sido **ABIERTO**.")

# ---------- RESET ----------
@bot.command()
async def reset(ctx):
    global sorteo_abierto

    if not es_admin(ctx):
        await ctx.send("🚫 Solo un ADMIN puede resetear la lista.")
        return

    if os.path.exists(ARCHIVO):
        os.remove(ARCHIVO)

    sorteo_abierto = True
    await ctx.send("🧹 Lista borrada. Nuevo sorteo iniciado.")

bot.run(TOKEN)

