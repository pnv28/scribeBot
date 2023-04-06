import discord
import logging
from discord.ext import commands
from discord import FFmpegPCMAudio
import pyaudio
import pydub
import discord.opus
import io
import wave

logging.basicConfig(level=logging.DEBUG)
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("The bot is now online")

@bot.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel: 
        voice = await after.channel.connect()
        print(f"Connected to {after.channel}")
        
        audio = pyaudio.PyAudio() 
        
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024) # open audio stream
        
        frames = []
        
        while voice.is_connected():
            data = stream.read(1024)
            print(f"Length of audio data: {len(data)}")
            frames.append(data)
        stream.stop_stream() 
        stream.close() 
        
        audio.terminate() # terminate PyAudio object
        
        waveFile = wave.open("output.wav", "wb") 
        waveFile.setnchannels(1) 
        waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(44100)
        waveFile.writeframes(b"".join(frames))
        waveFile.close() 
        
        await voice.disconnect()
        print(f"Disconnected from {after.channel}")

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