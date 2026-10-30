# /// script
# dependencies = [
#     "pygame-ce",
# ]
# ///
import asyncio
from src.Game import Game
import pygame
import sys
async def main():
    run = Game()
    await run.run_game()

asyncio.run(main())
