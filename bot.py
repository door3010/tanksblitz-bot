"""Tanks Blitz aimbot entry point.

Usage:
    python bot.py
"""
from tanksbot.aimbot import run_aimbot
from tanksbot.config import AIM

if __name__ == "__main__":
    run_aimbot(AIM)
