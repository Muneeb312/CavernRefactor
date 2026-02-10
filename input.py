space_down = False

def space_pressed():
    global space_down
    if keyboard.space:
        if space_down:
            return False
        space_down = True
        return True
    space_down = False
    return False
