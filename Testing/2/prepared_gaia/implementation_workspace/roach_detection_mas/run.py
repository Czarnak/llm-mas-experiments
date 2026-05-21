import asyncio
import sys
import os

# Add src to path so we can import our agents
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import run_system

if __name__ == "__main__":
    asyncio.run(run_system())