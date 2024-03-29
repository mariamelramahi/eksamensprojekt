import discord
import io
from io import BytesIO
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import Storage


async def meme(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    user_meme = Storage.memedict[user]
    meme = Image.open(io.BytesIO(user_meme.image_data))
    Storage.memedict[user].image_data = io.BytesIO(user_meme.image_data)
    meme = meme.resize((250, 150))

    text_font = ImageFont.truetype('impact/impact.ttf', 25)
    textup_text = user_meme.textup
    textdown_text = user_meme.textdown
    image_editable = ImageDraw.Draw(meme)

    _, _, w1, _ = image_editable.textbbox((0, 0), textup_text, font=text_font)
    _, _, w2, _ = image_editable.textbbox((0, 0), textdown_text, font=text_font)

    image_editable.text(((250 - w1) / 2, 5), textup_text, (250, 250, 250), font=text_font)
    image_editable.text(((250 - w2) / 2, 115), textdown_text, (250, 250, 250), font=text_font)

    image_binary = io.BytesIO()
    meme.save(image_binary, format='PNG')
    image_binary.seek(0)

    # hvis brugeren ikke allerede er en del af dictionarien laver den en key med brugerens id
    if user not in Storage.memeStorage:
        Storage.memeStorage[user] = []

    Storage.memeStorage[user].append(image_binary)
    Storage.memedict[user].image = Image.open("meme.png")
    Storage.memedict[user].i = 0

    # Sender memen
    await ctx.channel.send(file=discord.File(image_binary, filename='meme.png'))

# Sender alle de memes brugeren har lavet
async def send_user_memes(ctx, user: discord.member = None):
    if user is None:
        user = ctx.author
    
    # Tjekker hvis brugeren har lavet en meme
    if user not in Storage.memeStorage:
        await ctx.channel.send("You have no memes")
        return
    
    # Sender brugerens memes
    for meme in Storage.memeStorage[user]:
        image_bytes = io.BytesIO()
        with Image.open(meme) as img:
            img.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            await ctx.channel.send(file=discord.File(fp=image_bytes, filename='meme.png'))

