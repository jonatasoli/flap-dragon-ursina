from random import randint

from ursina import *


class Pipe(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.model = 'quad'
        self.scale = (1, 7)
        self.color = color.green
        self.x = x
        self.y = y
        self.collider = 'box'
        self.score_tag = True


def died():
    Text(
        text='You dieded! Reload the game!',
        origin=(0, 0),
        scale=3,
        color=color.red,
    )


# Main code
app = Ursina()

bird = Entity(
    collider='box',
    model='quad',
    # texture='player_texture.png',
    color=color.yellow,
    # scale = (1.3,0.8),
    # y = 1.5,
    origin=(4.0, -0.5),
    scale=(1, 1),
)
# Some variables
offset = 0
run = True
n_frame = 0
num = 5
x = 6
score = 0
run_game = False
bg = Sky(color=color.blue)

pipes_bottom = [None] * num
pipes_bottom[0] = Pipe(x, -4)

pipes_top = [None] * num
pipes_top[0] = Pipe(x, -4 + 9)

for m in range(1, num):

    x += 4
    y = -7 + randint(0, 50) / 10
    pipes_bottom[m] = Pipe(x, y)
    pipes_top[m] = Pipe(x, y + 9)

text = Text(
    text=f'Score: {score}',
    position=(-0.65, 0.4),
    origin=(0, 0),
    scale=2,
    color=color.yellow,
    background=True,
)


def input(key):
    global run_game

    if key == 'space' and not run_game:
        run_game = True
    elif key == 'space' and run_game:
        bird.y += 0.25

    if key == 'q':
        app.finalizeExit()


def update():
    global offset, run_game, n_frame, score, text

    if run_game:

        # Rolling background
        offset += time.dt * 0.3
        setattr(bg, 'texture_offset', (offset, 0))
        bird.y -= time.dt * 0.5

        for m in range(num):
            pipes_top[m].x -= time.dt * 1.8
            pipes_bottom[m].x -= time.dt * 1.8

            if pipes_top[m].x < -8:
                pipes_top[m].x += 4 * num
                pipes_bottom[m].x += 4 * num
                pipes_top[m].score_tag = True

            if pipes_top[m].x < bird.x and pipes_top[m].score_tag:
                score += 1
                text.y = 1
                text = Text(
                    text=f'Score: {score}',
                    position=(-0.65, 0.4),
                    origin=(0, 0),
                    scale=2,
                    color=color.green,
                    background=True,
                )
                pipes_top[m].score_tag = False

        # Collision
        hit_info = bird.intersects()
        if hit_info.hit:
            run_game = False
            invoke(Func(bird.shake, duration=2))
            invoke(Func(bird.fade_out, duration=3))
            invoke(died, delay=3)


app.run()
