from random import shuffle, randint
from pgzero.builtins import sounds, screen
from src.common import *
from src.entities.actors import Player, Robot, Fruit, Bolt, Pop, Orb

class Game:
    def __init__(self, app, player=None):
        self.app = app
        self.player = player
        if self.player:
            self.player.game = self

        self.level_colour = -1
        self.level = -1
        self.grid = []
        self.fruits = []
        self.bolts = []
        self.enemies = []
        self.pops = []
        self.orbs = []
        self.pending_enemies = []
        self.timer = 0
        self.next_level()

    def block(self, x, y):
        grid_x = (x - LEVEL_X_OFFSET) // GRID_BLOCK_SIZE
        grid_y = y // GRID_BLOCK_SIZE
        if 0 < grid_y < NUM_ROWS:
            row = self.grid[grid_y]
            return 0 <= grid_x < NUM_COLUMNS and len(row) > 0 and row[grid_x] != " "
        return False

    def fire_probability(self):
        return 0.001 + (0.0001 * min(100, self.level))

    def max_enemies(self):
        return min((self.level + 6) // 2, 8)

    def next_level(self):
        self.level_colour = (self.level_colour + 1) % 4
        self.level += 1
        self.grid = LEVELS[self.level % len(LEVELS)]
        self.grid = self.grid + [self.grid[0]]
        self.timer = -1

        if self.player:
            self.player.reset()

        self.fruits = []
        self.bolts = []
        self.enemies = []
        self.pops = []
        self.orbs = []

        num_enemies = 10 + self.level
        num_strong_enemies = 1 + int(self.level / 1.5)
        num_weak_enemies = num_enemies - num_strong_enemies

        self.pending_enemies = num_strong_enemies * [Robot.TYPE_AGGRESSIVE] + num_weak_enemies * [Robot.TYPE_NORMAL]
        shuffle(self.pending_enemies)
        self.play_sound("level", 1)

    def get_robot_spawn_x(self):
        r = randint(0, NUM_COLUMNS-1)
        for i in range(NUM_COLUMNS):
            grid_x = (r+i) % NUM_COLUMNS
            if self.grid[0][grid_x] == ' ':
                return GRID_BLOCK_SIZE * grid_x + LEVEL_X_OFFSET + 12
        return WIDTH/2

    def update(self, input_state=None):
        self.timer += 1
        
        if self.player and input_state:
            self.player.update(input_state)

        for obj in self.fruits + self.bolts + self.enemies + self.pops + self.orbs:
            if obj: obj.update()

        self.fruits = [f for f in self.fruits if f.time_to_live > 0]
        self.bolts = [b for b in self.bolts if b.active]
        self.enemies = [e for e in self.enemies if e.alive]
        self.pops = [p for p in self.pops if p.timer < 12]
        self.orbs = [o for o in self.orbs if o.timer < 250 and o.y > -40]

        if self.timer % 100 == 0 and len(self.pending_enemies + self.enemies) > 0:
            self.fruits.append(Fruit(self, (randint(70, 730), randint(75, 400))))

        if self.timer % 81 == 0 and len(self.pending_enemies) > 0 and len(self.enemies) < self.max_enemies():
            robot_type = self.pending_enemies.pop()
            pos = (self.get_robot_spawn_x(), -30)
            self.enemies.append(Robot(self, pos, robot_type))

        if len(self.pending_enemies + self.fruits + self.enemies + self.pops) == 0:
            if len([orb for orb in self.orbs if orb.trapped_enemy_type is not None]) == 0:
                self.next_level()

    def draw(self):
        screen.blit("bg%d" % self.level_colour, (0, 0))
        block_sprite = "block" + str(self.level % 4)
        for row_y in range(NUM_ROWS):
            row = self.grid[row_y]
            if len(row) > 0:
                x = LEVEL_X_OFFSET
                for b in row:
                    if b != ' ': screen.blit(block_sprite, (x, row_y * GRID_BLOCK_SIZE))
                    x += GRID_BLOCK_SIZE
        
        all_objs = self.fruits + self.bolts + self.enemies + self.pops + self.orbs
        if self.player: all_objs.append(self.player)
        for obj in all_objs:
            if obj: obj.draw()

    def draw_status(self):
        if not self.player: return
        s = str(self.player.score)
        draw_text(s, 451, WIDTH - 2 - (CHAR_WIDTH[0] * len(s)))
        draw_text("LEVEL " + str(self.level + 1), 451)

        lives_health = ["life"] * min(2, self.player.lives)
        if self.player.lives > 2: lives_health.append("plus")
        if self.player.lives >= 0: lives_health += ["health"] * self.player.health

        x = 0
        for image in lives_health:
            screen.blit(image, (x, 450))
            x += IMAGE_WIDTH[image]

    def play_sound(self, name, count=1):
        if self.player:
            try:
                sound = getattr(sounds, name + str(randint(0, count - 1)))
                sound.play()
            except Exception:
                pass