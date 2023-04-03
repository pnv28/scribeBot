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
    if ctx.author.voice is None:
        await ctx.send("You need to join a voice channel first.")
        return

    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    audio_source = discord.FFmpegPCMAudio("recording.wav")
    voice_client.play(audio_source)

    await ctx.send("Recording started.")

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client is not None:
        await voice_client.disconnect()
        await ctx.send("Recording stopped.")
    else:
        await ctx.send("I'm not in a voice channel.")


bot.run("")