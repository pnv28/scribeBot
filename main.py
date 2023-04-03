import discord
from discord.ext import commands
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("The bot is now online")

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:    
        await after.channel.connect()
    if before.channel is not None and after.channel is None:
        voice_client = member.guild.voice_client
        if voice_client is not None and len(voice_client.channel.members) == 1:
            await voice_client.disconnect()

@bot.command()
async def lol(ctx):
    id = ctx.message.author.id;
    await ctx.send(f"I am laughing at you <@{id}>")

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        return
    if(voice_client.is_connected):
        await voice_client.disconnect()

bot.run("MTA5MjEwNDYwODg3MDA0MzcwOA.GuTTHT.feI5_ZwmwjW0lhQRFUgKra-f751e5LZ3BQR4-g")