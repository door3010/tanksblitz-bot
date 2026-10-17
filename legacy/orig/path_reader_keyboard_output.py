import pydirectinput
import time
DIRECTION_ORDER = ['UP', 'RIGHT', 'DOWN', 'LEFT']
def get_turn_sequence(current_dir, target_dir):
    curr_idx = DIRECTION_ORDER.index(current_dir)
    targ_idx = DIRECTION_ORDER.index(target_dir)
    diff = (targ_idx - curr_idx) % 4
    if diff == 0: return []
    if diff == 1: return ['d']
    if diff == 2: return ['d', 'd']
    return ['a']
def get_target_direction(dy, dx):
    if dx > 0: return 'RIGHT'
    if dx < 0: return 'LEFT'
    if dy > 0: return 'DOWN'
    if dy < 0: return 'UP'
    return None
def execute_path(path, initial_direction='UP', step_delay=1.25, dry_run=False):
    if len(path) < 2:
        print("Path too short.")
        return
    pos = path[0]
    facing = initial_direction
    commands = []
    for i in range(1, len(path)):
        nxt = path[i]
        dy = nxt[0] - pos[0]
        dx = nxt[1] - pos[1]
        if dx == 0 and dy == 0:
            continue
        if dx != 0 and dy != 0:
            segments = [('x', dx), ('y', dy)]
        elif dx != 0:
            segments = [('x', dx)]
        else:
            segments = [('y', dy)]
        for axis, delta in segments:
            if delta == 0:
                continue
            target = get_target_direction(dy if axis == 'y' else 0,dx if axis == 'x' else 0)
            distance = abs(delta)
            for turn in get_turn_sequence(facing, target):
                commands.append(turn)
            facing = target
            commands.extend(['w'] * distance)
        pos = nxt
    # commands=replace_w(commands)
    if dry_run:
        return commands
    for key in commands:
        pydirectinput.keyDown(key)
        if key=="w":
            time.sleep(0.5)
        else:
            time.sleep(step_delay)
        pydirectinput.keyUp(key)
    return facing, commands
# def replace_w(commands):
#     command_string=""
#     new_commands=[]
#     for i in commands:
#         command_string=command_string+i
#     command_string=command_string.replace("www", "w")
#     command_string=command_string.replace("www", "w")
#     command_string=command_string.replace("ww", "w")
#     for i in command_string:
#         new_commands.append(i)
#     return new_commands