import os
import discord
import openai
import time
import asyncio

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = os.environ.get('DISCORD_CHANNEL_ID')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if DISCORD_TOKEN is None:
    print("DISCORD_TOKEN is not set.")
    exit(1)

if DISCORD_CHANNEL_ID is None:
    print("DISCORD_CHANNEL_ID is not set.")
    exit(1)

if OPENAI_API_KEY is None:
    print("OPENAI_API_KEY is not set.")
    exit(1)


# discordモジュールをつかってチャンネルにに文字列を投稿する
async def post_message(client):
    while True:
        print(client.get_channel(DISCORD_CHANNEL_ID))
        print(client.get_all_channels())
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        for guild in client.guilds:
            for channel in guild.channels:
                print(channel)
        # チャンネルが見つかるまで待つ
        while channel is None:
            await asyncio.sleep(1)
            channel = client.get_channel(DISCORD_CHANNEL_ID)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=2048,
            n=1,
            #stop="\n",
            temperature=0.8,
            frequency_penalty=0,
            messages=[
            {"role": "system", "content": "あなたは知識が豊富な我々の友達です"},
            {"role": "user", "content": "ためになる、面白いことを話してください"}
            ],
            )

        reply = response.choices[0]["message"]["content"].strip()
        await channel.send(reply)
        await asyncio.sleep(1800)

async def main():

    openai.api_key = OPENAI_API_KEY
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f'{client.user} が接続しました.')
        asyncio.create_task(post_message(client=client))

    @client.event
    async def on_message(message):
        print(message.channel.id)
        if message.author == client.user:
            return

        if message.content.startswith('!gptn'):
            prompt = message.content[6:]
        #
        #response = openai.ChatCompletion.create(
        #    engine="gpt-3.5-turbo",
        #    prompt=prompt,
        #    max_tokens=1024,
        #    n=1,
        #    stop="\n",
        #    temperature=0.8,
        #    frequency_penalty=0,
        #    presence_penalty=0
        #)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                max_tokens=2048,
                n=1,
                #stop="\n",
                temperature=0.8,
                frequency_penalty=0,
                messages=[
                    {"role": "system", "content": "あなたは知識が豊富な我々の友達です"},
                    {"role": "user", "content": prompt}
                ],
            )

            reply = response.choices[0]["message"]["content"].strip()
            await message.channel.send(reply)

    await client.start(DISCORD_TOKEN)

asyncio.run(main())