import discord
import os
from discord.ext import commands
import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)
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

@bot.command()
async def record(ctx):
    voice_client = ctx.voice_client
    if not voice_client:
        await ctx.send("The bot is not in a VC")
        return
    
    await ctx.send("Recording")
    audio_source = discord.FFmpegPCMAudio("recording.wav")
    if audio_source is None:
        await ctx.send("Failed to create audio source.")
        return
    audio_player = discord.PCMVolumeTransformer(audio_source)
    
    voice_client.play(audio_player)

    while voice_client.is_playing():
        try:
            message = await bot.wait_for('message', timeout = 1.0)
            if message.content.lower() == 'stop' and message.author == ctx.author:
                voice_client.stio()
                await ctx.send("Stopped recording")
        except asyncio.TimeoutError:
            pass

    await ctx.send("Finished recording")
    await ctx.send(file=discord.File("recording.wav"))


bot.run("lol")