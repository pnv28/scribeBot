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

MIN_USERS = 1
p = pyaudio.PyAudio()
frames = []

@bot.event
async def on_voice_state_update(member, before, after):
    # Get the voice channel and voice client
    voice_channel = member.guild.voice_channels[0]
    voice_client = bot.voice_clients[0] if bot.voice_clients else None

    # Check if the bot needs to join the voice channel
    if voice_client is None:
        if voice_channel is not None:
            voice_client = await voice_channel.connect()

    # Check if the bot needs to leave the voice channel
    if voice_client is not None:
        if len(voice_channel.members) == 1 and voice_channel.members[0].id == bot.user.id:
            await voice_client.disconnect()
            voice_client = None

    # Check if the bot needs to start or stop recording
    if voice_client is not None and len(voice_channel.members) >= MIN_USERS:
        if len(frames) == 0:
            # Start recording
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
            print('Recording started')
        # Append the audio data to the frames list
        frames.append(stream.read(1024))
    else:
        if len(frames) > 0:
            # Stop recording and save the audio data to a file
            stream.stop_stream()
            stream.close()
            wf = wave.open('output.wav', 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(frames))
            wf.close()
            frames.clear()
            print('Recording stopped')



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