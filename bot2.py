from telethon import TelegramClient, events
import asyncio, os

# Replace with your own values
api_id = ''
api_hash = ''

# Source chat IDs (groups or channels you want to monitor)
source_chats = [-1001469897009,
-1001948053703,
-1001674368694,
-1002163796849,
-1001959740640,
-1002215792814,
-1001539581389,
-1001513663591,
-1001996018221,
-1002004588951,
-1002056246308,
-1001991515151,
-1001849668556,
-1002184961890,
-1002017217723,
-1001801249343,
-1002305942396,
-1002671523354,
-1002356893189,
-1002378175986,
-1002301051033,
-1002023204111,
-1002356183787,
-1002182028642,
-1001687846374,
-1001869129050,
-1001985237330,
-1002438306427,
-1001951471439,
-1001388612979,
-1002210952960,
-1002406970613,
-1002073222957,
-1002110140215,
-1002018375943]
# Destination chat ID (your channel)
destination_chat = -1002647571377


# Create the client and connect
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
