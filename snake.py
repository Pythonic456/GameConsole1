import console, random, led_numbers

width = 50
height = 50
console = console.console(led_height=height, led_width=width, buttons=5)

width -= 1
height -= 1


## Snake
delay = 50

tail = []
head = {'x':random.randint(0,width), 'y':random.randint(0,height)}
food = {}
score = 0
direction = 'up'
length = 5
all_leds = -1
def process():
    global food, tail, head, length, direction, width, height, all_leds, score
    tail.append({'x':head['x'],'y':head['y']})
    if direction == 'up':
        head['y'] -= 1
    elif direction == 'down':
        head['y'] += 1
    elif direction == 'right':
        head['x'] += 1
    elif direction == 'left':
        head['x'] -= 1

    if head['y'] < 0:
        head['y'] = height
    if head['y'] > height:
        head['y'] = 0
    if head['x'] < 0:
        head['x'] = width
    if head['x'] > width:
        head['x'] = 0

    if len(tail) > length:
        del tail[0]
    #print(tail)
    #print(head)
    if food == head:
        food = {}
        length += 1
        score += 1
    if food == {}:
        if random.randint(0,16) == 0:
            food = head
            while (food in tail) or food == head:
                food = {'x':random.randint(0,width), 'y':random.randint(0,height)}
    console.set_all_leds(0)
    console.set_led(head['x'],head['y'],1)
    if food != {}:
        console.set_led(food['x'],food['y'],1)
    for part in tail:
        console.set_led(part['x'],part['y'],1)
    if head in tail:
        if all_leds == -1: all_leds = 0
    if all_leds != -1:
        all_leds = not all_leds
        console.set_all_leds(0)
        leds_num = led_numbers.draw_numbers(score)
        for led in leds_num:
            console.set_led(led['x'],led['y'],led['state'])
        #console.set_all_leds(int(all_leds))
    if all_leds == -1:
        console.after(delay, process)

def direction_up(ev=None):
    global direction
    direction = 'up'
def direction_down(ev=None):
    global direction
    direction = 'down'
def direction_right(ev=None):
    global direction
    direction = 'right'
def direction_left(ev=None):
    global direction
    direction = 'left'

def increase_length(ev=None):
    global length
    length += 1

console.assign_button(0, direction_up, '<Up>')
console.assign_button(1, direction_down, '<Down>')
console.assign_button(2, direction_right, '<Right>')
console.assign_button(3, direction_left, '<Left>')
console.assign_button(4, increase_length, '<Return>')

## end

console.after(delay, process)
console.start_loop()