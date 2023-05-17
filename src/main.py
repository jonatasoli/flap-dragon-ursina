from PIL import Image, ImageDraw, ImageFont
from ursina import *

# Cria uma imagem com o símbolo '@'
image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
draw.text((16, 16), '@', fill=(255, 255, 0), font=font)
image.save('player_texture.png')

# Carrega a fonte personalizada
# Text.default_font =tom_font
# Text.default_resolution = 10 * Text.size


class Player(Entity):
    def __init__(self):
        super().__init__(
            model='quad',
            texture='player_texture.png',
            color=color.yellow,
            origin=(4.0, -0.5),
            scale=(1, 1),
        ),
        self.velocity = 0.0
        self.acceleration = 0.2
        self.max_speed = 2.0
        self.can_move = False

    def update(self):
        if self.can_move:
            time.sleep(1)  # Adiciona um atraso de 300 ms (0.3 segundos)
            # Acelera o jogador no eixo x até o valor máximo
            if self.velocity < self.max_speed:
                self.velocity -= self.acceleration

            # Atualiza a posição do jogador no eixo y
            self.y += self.velocity
            self.x += -0.3
            print(self.y)

    def input(self, key):
        if key == 'space':
            self.can_move = True


def playing():
    # Cria uma nova cena
    scene.clear()

    # Adiciona um objeto de fundo azul à cena
    background = Sky(color=color.blue)

    # Adiciona o jogador à cena
    player = Player()
    scene.entities.append(player)
    print("cena")


class PrincipalMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        # Cria o texto "MAIN MENU"
        self.main_menu_text = Text(text='MAIN MENU', y=0.4, x=-0.2, scale=2)

        # Cria o texto "PRESS SPACE TO PLAY"
        self.play_button = Button(
            text='PRESS SPACE TO PLAY',
            y=0.2,
            x=-0.06,
            scale=(0.3, 0.1),
            on_click=self.start_game,
        )

        # Cria o texto "PRESS Q TO QUIT"
        self.quit_button = Button(
            text='PRESS Q TO QUIT',
            y=0.1,
            x=-0.06,
            scale=(0.3, 0.1),
            on_click=self.finalize_exit,
        )

    def start_game(self):
        # Inicia o jogo
        print('Iniciando o jogo!')
        playing()

    def finalize_exit(self):
        # Finaliza o jogo
        app.finalizeExit()

    def input(self, key):
        if key == 'space':
            self.start_game()

        if key == 'q':
            self.finalize_exit()


app = Ursina(title='Flappy Dragon')

main_menu = PrincipalMenu()

def update():
    for entity in scene.entities:
        if isinstance(entity, Player):
            entity.update()

app.run()
