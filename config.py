"""Backward-compatible shim for legacy scripts.

New code should import from the package directly:
    from tanksbot.config import AIM, MINIMAP, DEBUG_AIM
"""
from tanksbot.config import AIM, DEBUG_AIM, MINIMAP

# Original names used by the pre-refactor scripts.
AimTank = AIM
Minimap = MINIMAP
