import discord
import aiohttp
from discord.ext import commands
from dotenv import load_dotenv
import os
from datetime import datetime
import requests
from replit_keep_alive import keep_alive

# Fetch the bot token and API keys from environment variables or use default values
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
CAT_API_KEY = os.getenv('CAT_API_KEY')
DOG_API_KEY = os.getenv('DOG_API_KEY')

intents = discord.Intents().all()

bot = commands.Bot(command_prefix=".", intents=intents)

# Function to log user commands to a TXT file with timestamps
async def log_user_command(ctx):
    user = ctx.author
    command = ctx.command
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open("user_commands.txt", "a") as log_file:
        log_file.write(f"{timestamp} | {user} used command '{command}'\n")

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def cat(ctx):
    try:
        # Log the user command with timestamp
        await log_user_command(ctx)

        async with aiohttp.ClientSession() as session:
            headers = {"x-api-key": CAT_API_KEY}

            # Fetch the cat image from The Cat API
            async with session.get("https://api.thecatapi.com/v1/images/search", headers=headers) as response:
                if response.status != 200:
                    await ctx.send("Sorry, something went wrong while fetching the cat image.")
                    return
                data = await response.json()
                cat_image_url = data[0]["url"]

        embed = discord.Embed(title="Kitty Cat 🐈", description="Cats :star_struck:", color=discord.Colour.purple())
        embed.set_image(url=cat_image_url)
        embed.set_footer(text="")

        # Send the embed
        message = await ctx.send(embed=embed)

        # Delete the command message and the response after a delay (e.g., 10 seconds)
        await ctx.message.delete(delay=0)
        await message.delete(delay=300)
    except Exception as e:
        await ctx.send("Sorry, something went wrong while fetching the cat image. Meow!")

@bot.command()
async def dog(ctx):
    try:
        # Log the user command with timestamp
        await log_user_command(ctx)

        async with aiohttp.ClientSession() as session:
            headers = {"x-api-key": DOG_API_KEY}

            # Fetch the dog image from a Dog API
            async with session.get("https://api.thedogapi.com/v1/images/search", headers=headers) as response:
                if response.status != 200:
                    await ctx.send("Sorry, something went wrong while fetching the dog image.")
                    return
                data = await response.json()
                dog_image_url = data[0]["url"]

        embed = discord.Embed(title="Cute Dog 🐕", description="Dogs :heart_eyes:", color=discord.Colour.orange())
        embed.set_image(url=dog_image_url)
        embed.set_footer(text="")

        # Send the embed
        message = await ctx.send(embed=embed)

        # Delete the command message and the response after a delay (e.g., 10 seconds)
        await ctx.message.delete(delay=0)
        await message.delete(delay=300)
    except Exception as e:
        await ctx.send("Sorry, something went wrong while fetching the dog image. Woof!")

@bot.command()
async def ping(ctx):
    # Log the user command with timestamp
    await log_user_command(ctx)

    # Send the ping message
    await ctx.send(f"Pong! {round(bot.latency * 1000)} ms")
    
@bot.command()
async def joke(ctx):
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    if response.status_code == 200:
        joke_data = response.json()
        setup = joke_data['setup']
        punchline = joke_data['punchline']
        await ctx.send(f'**Joke:** {setup}\n**Punchline:** {punchline}')
    else:
        await ctx.send('Sorry, I couldn\'t fetch a joke at the moment.')
        



@bot.command()
async def raccoon(ctx):
    try:
        # Log the user command with timestamp
        await log_user_command(ctx)

        async with aiohttp.ClientSession() as session:
            # Fetch a random raccoon image from the provided API
            async with session.get("https://some-random-api.com/img/raccoon/") as response:
                if response.status != 200:
                    await ctx.send("Sorry, something went wrong while fetching the raccoon image.")
                    return

                data = await response.json()
                raccoon_image_url = data["link"]

        embed = discord.Embed(title="Adorable Raccoon 🦝", color=discord.Colour.orange())
        embed.set_image(url=raccoon_image_url)
        embed.set_footer(text="")

        # Send the embed
        message = await ctx.send(embed=embed)

        # Delete the command message and the response after 2 minutes
        await ctx.message.delete(delay=0)
        await message.delete(delay=300)

    except Exception as e:
        error_message = f"An error occurred while fetching the raccoon image:\n{e}"
        await ctx.send("Sorry, something went wrong while fetching the raccoon image. 🦨")
        print(error_message)

@bot.command()
async def hug(ctx, member: discord.Member):
    # Send a hug message
    await ctx.send(f"{ctx.author.mention} hugged {member.mention} :hugging:")

    # Fetch a random "hug" image from the API
    response = requests.get('https://some-random-api.com/animu/hug/')
    if response.status_code == 200:
        data = response.json()
        if 'link' in data:
            image_url = data['link']
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't fetch a hug image at the moment. :(")
    else:
        await ctx.send("Couldn't fetch a hug image at the moment. :(")

keep_alive()
bot.run(TOKEN)
