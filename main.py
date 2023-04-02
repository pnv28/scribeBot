import discord
from discord.ext import commands
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("The bot is now online")

@bot.command()
async def lol(ctx):
    id = ctx.message.author.id;
    await ctx.send(f"I am laughing at you <@{id}>")

bot.run("MTA5MjEwNDYwODg3MDA0MzcwOA.GuTTHT.feI5_ZwmwjW0lhQRFUgKra-f751e5LZ3BQR4-g")