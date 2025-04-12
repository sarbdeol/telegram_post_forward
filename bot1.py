from telethon import TelegramClient, events
import asyncio, os

# Replace with your own values
api_id = ''
api_hash = ''

# Source chat IDs (groups or channels you want to monitor)
source_chats = [
    -1001543796382,
    -1001870005959,
    -1002305898637,
    -1002018375943,
    -1002110140215
]

# Destination chat ID (your channel)
destination_chat = -1002646228196

client = TelegramClient('forwarder_session', api_id, api_hash)

# Dictionary to hold album messages temporarily
pending_albums = {}

async def process_album(grouped_id):
    # Wait briefly to allow all parts of the album to arrive
    await asyncio.sleep(1)
    events_list = pending_albums.pop(grouped_id, [])
    
    # Sort events by message id to maintain order
    events_list.sort(key=lambda e: e.message.id)
    
    media_files = []
    caption = None
    for event in events_list:
        msg = event.message
        # Download each media file
        try:
            file = await msg.download_media()
            if file:
                media_files.append(file)
            # Use the caption from the first message that has text
            if caption is None and msg.message:
                caption = msg.message
        except Exception as e:
            print(f"Error downloading media from album: {e}")
    
    if media_files:
        try:
            # Send all media as a group (album)
            await client.send_file(destination_chat, media_files, caption=caption if caption else "")
            print(f"Forwarded album (grouped_id: {grouped_id}) with caption: {caption if caption else 'No caption'}")
        except Exception as e:
            print(f"Error forwarding album: {e}")
        finally:
            # Remove temporary files
            for file in media_files:
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"Error removing file {file}: {e}")

@client.on(events.NewMessage(chats=source_chats))
async def handler(event):
    try:
        message = event.message
        text = message.message  # text or caption

        # Check if the message is part of an album
        if message.grouped_id:
            pending_albums.setdefault(message.grouped_id, []).append(event)
            # If this is the first message for this album, schedule processing after a delay
            if len(pending_albums[message.grouped_id]) == 1:
                asyncio.create_task(process_album(message.grouped_id))
            return

        # For messages that are not part of an album:
        # Handle media messages
        if message.media:
            file = await message.download_media()
            await client.send_file(destination_chat, file, caption=text if text else "No caption")
            os.remove(file)
            print(f"Forwarded media with caption: {text if text else 'No caption'}")
        # If text-only message
        elif text:
            await client.send_message(destination_chat, text)
            print(f"Forwarded text: {text}")

    except Exception as e:
        print(f"Error while forwarding message: {e}")

async def main():
    await client.start()
    print("Monitoring... Press Ctrl+C to stop.")
    await client.run_until_disconnected()

asyncio.run(main())
