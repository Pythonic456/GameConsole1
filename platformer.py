import console, platformer_maps


map = 0
width = 50
height = 50
delay = 50

console = console.console(width, height)

character = {'x': 1, 'y': 1, 'direction': 'up', 'momentum': 0}
width -= 1
height -= 1

map = platformer_maps.maps[map]
map_lst = []
for i in range(height+1):
    for b in range(width+1):
        c = map.split('\n')[i][b]
        #if c == ' ':
        #    #tmp.append((b,i,0))
        if c == '#':
            map_lst.append((b,i,1))

def process():
    global character, console, width, height
    old_character = character.copy()
    if character['momentum'] > 0:
        if character['direction'] == 'up':
            character['y'] -= 1
        elif character['direction'] == 'down':
            character['y'] += 1
        elif character['direction'] == 'right':
            character['x'] += 1
        elif character['direction'] == 'left':
            character['x'] -= 1
        character['momentum'] -= 1
    else:
        character['direction'] = 'down'

    tmp = (character['x'],character['y'],1)
    if tmp in map_lst:
        if character['direction'] == 'up':
            character['y'] += 1
        elif character['direction'] == 'down':
            character['y'] -= 1
        elif character['direction'] == 'right':
            character['x'] += 1
        elif character['direction'] == 'left':
            character['x'] -= 1
    elif character['direction'] != 'up':
        pass#character['y'] += 1
    
    if character['x'] > width:
        character['x'] = width
    if character['y'] > height:
        character['y'] = height
    if character['x'] < 0:
        character['x'] = 0
    if character['y'] < 0:
        character['y'] = 0
    ## Map
    for led in map_lst:
        console.set_led(led[0],led[1],led[2])

    console.set_led(old_character['x'], old_character['y'], 0)
    console.set_led(character['x'], character['y'], 1)

    console.after(delay, process)

def move_up(ev):
    global character
    character['momentum'] = 4
    character['direction'] = 'up'
def move_down(ev):
    global character
    character['momentum'] = 4
    character['direction'] = 'down'
def move_right(ev):
    global character
    character['momentum'] = 4
    character['direction'] = 'right'
def move_left(ev):
    global character
    character['momentum'] = 4
    character['direction'] = 'left'

console.assign_button(0, move_up, '<Up>')
console.assign_button(1, move_down, '<Down>')
console.assign_button(2, move_left, '<Left>')
console.assign_button(3, move_right, '<Right>')

console.after(delay, process)
console.start_loop()