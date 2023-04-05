import discord
import os
import logging
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio
import time
logging.basicConfig(level=logging.DEBUG)
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("The bot is now online")

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:    
        voice = await after.channel.connect()
        source = FFmpegPCMAudio('sed.wav')
        player = voice.play(source)
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
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('sed.wav')
        player = voice.play(source)
    else:
        await ctx.send("You are not connected to a voice channel.")

@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

bot.run("")