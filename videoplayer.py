import console, os
from PIL import Image

print('Usage: Provide "video.mp4" file in current directory (must be less than 15-20 seconds long,\n\
and less than 10 MB in size)')

console = console.console(led_width=100, led_height=100)


os.system('ffmpeg -hide_banner -loglevel error -i video.mp4 -vf scale=100:100 output.mp4')
os.system('rm -r /tmp/videoplayer_frames/;mkdir /tmp/videoplayer_frames/')
os.system('ffmpeg -hide_banner -loglevel error -i output.mp4 /tmp/videoplayer_frames/frame%04d.jpg;rm output.mp4')

fr_paths = os.listdir('/tmp/videoplayer_frames/')
fr_paths.sort()
frame_paths = []
fr_paths.reverse()
for path in fr_paths:
    frame_paths.append('/tmp/videoplayer_frames/'+path)
print('Loading frames...',end='')
frames = {}
for frame_path in frame_paths:
    frames[frame_path] = Image.open(frame_path)
print('Done')

playing = False
ms_per_frame = 50

def process(force=0):
    global frame_paths, delay, console, playing
    if (playing and force) or (playing or force):
        frame = frame_paths.pop()
        img = Image.open(frame)
        x = y = 0
        for pix in list(img.getdata()):
            if sum(pix) > 500:
                console.set_led(x, y, 1)
            else:
                console.set_led(x, y, 0)
            x += 1
            if x == 100:
                x = 0
                y += 1
    console.after(ms_per_frame, process)
process(force=1)

print('Button 2: Play')
print('Button 3: Pause')
def button_0(ev=None):
    pass#process(force=1)
def button_1(ev=None):
    global playing
    playing = True
def button_2(ev=None):
    global playing
    playing = False

console.assign_button(0, button_0)
console.assign_button(1, button_1)
console.assign_button(2, button_2)
console.start_loop()