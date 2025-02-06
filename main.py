import discord
from discord.ext import commands
import requests
import random
from PIL import Image, ImageDraw, ImageFont
import io
import openai

# Setup bot with intents
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# OpenAI API Key (Replace with your key)
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# ✅ Auto Slowmode (10s on all channels)
@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int = 10):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Slowmode set to {seconds} seconds.")

# ✅ DM New Members with Avatar & Username
@bot.event
async def on_member_join(member):
    try:
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        response = requests.get(avatar_url)
        avatar = Image.open(io.BytesIO(response.content)).convert("RGBA").resize((100, 100))

        img = Image.new("RGB", (400, 200), (30, 30, 30))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 30)
        draw.text((150, 75), f"Welcome, {member.name}!", (255, 255, 255), font=font)
        img.paste(avatar, (20, 50), avatar)

        img_path = "welcome.png"
        img.save(img_path)

        await member.send(f"Welcome to {member.guild.name}, {member.mention}!", file=discord.File(img_path))
    except Exception as e:
        print(f"Error sending DM: {e}")

# ✅ Fun Games
@bot.command()
async def coinflip(ctx):
    await ctx.send(random.choice(["Heads", "Tails"]))

# ✅ Pokémon Info
@bot.command()
async def pokemon(ctx, name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
    if response.status_code == 200:
        data = response.json()
        types = ', '.join(t['type']['name'] for t in data['types'])
        await ctx.send(f"**{data['name'].title()}** - ID: {data['id']}\nType: {types}")
    else:
        await ctx.send("Pokémon not found!")

# ✅ Anime Quotes
anime_quotes = [
    "Fear is freedom! Control is liberty! - Satsuki Kiryuuin",
    "A lesson without pain is meaningless. - Edward Elric",
]
@bot.command()
async def animequote(ctx):
    await ctx.send(random.choice(anime_quotes))

# ✅ Meme Generator
@bot.command()
async def meme(ctx):
    meme_url = "https://meme-api.com/gimme"
    response = requests.get(meme_url)
    if response.status_code == 200:
        await ctx.send(response.json()["url"])
    else:
        await ctx.send("Couldn't fetch a meme!")

# ✅ AI Image Generation ("Imagine")
@bot.command()
async def imagine(ctx, *, prompt):
    try:
        await ctx.send("Generating your image, please wait...")
        response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
        await ctx.send(f"Here is your image:\n{response['data'][0]['url']}")
    except Exception as e:
        await ctx.send("Sorry, I couldn't generate the image.")
        print(f"Error: {e}")

# ✅ Run Bot
bot.run("MTMzNTk3ODI0Nzk5MjkwNTc4Mg.G87MdH.gcBFh554IkV42xrw3KEaz1x3NAmGRu6nV0fdIA")
