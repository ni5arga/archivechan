import discord

def archive_discord_channel(token, channel_id, output_file):
    intents = discord.Intents.default()
    intents.messages = True
    client = discord.Client(intents=intents)
    messages = []
    @client.event
    async def on_ready():
        channel = client.get_channel(channel_id)
        async for message in channel.history(limit=None):
            messages.append({
                'author': str(message.author),
                'content': message.content,
                'timestamp': str(message.created_at)
            })
        with open(output_file, 'w') as f:
            json.dump(messages, f)
        await client.close()
    client.run(token)
