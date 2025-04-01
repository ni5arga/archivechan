from telethon.sync import TelegramClient

def archive_telegram_channel(api_id, api_hash, channel_name, output_file):
    with TelegramClient('session', api_id, api_hash) as client:
        messages = []
        for message in client.iter_messages(channel_name, limit=None):
            messages.append({
                'date': str(message.date),
                'text': message.text,
                'media': bool(message.media)
            })
        with open(output_file, 'w') as f:
            json.dump(messages, f)
