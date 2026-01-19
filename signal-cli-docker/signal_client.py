#!/usr/bin/env python3
"""
Simple WebSocket client that connects to a URL and logs received messages.
Handles redirects automatically during the WebSocket handshake.
"""
import asyncio
import logging
import sys
from argparse import ArgumentParser

import websockets


# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


async def connect_and_listen(url: str):
    """Connect to WebSocket URL and log all received messages."""
    try:
        logger.info(f"Connecting to {url}")
        
        # websockets library automatically follows redirects (301, 302, 307, 308)
        async with websockets.connect(url) as websocket:
            logger.info(f"Connected to {websocket.remote_address}")
            
            # Listen for messages indefinitely
            async for message in websocket:
                logger.info(f"Received: {message}")
                
    except websockets.exceptions.WebSocketException as e:
        logger.error(f"WebSocket error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


def main():
    parser = ArgumentParser(description="Simple WebSocket client")
    parser.add_argument("url", help="WebSocket URL to connect to (ws:// or wss://)")
    args = parser.parse_args()
    
    # Run the async function
    asyncio.run(connect_and_listen(args.url))


if __name__ == "__main__":
    main()

