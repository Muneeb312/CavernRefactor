from random import choice, randint, random
from pgzero.builtins import Actor, keyboard
from src.common import *

class CollideActor(Actor):
    def __init__(self, game_instance, pos, anchor=ANCHOR_CENTRE):
        super().__init__("blank", pos, anchor)
        self.game = game_instance

    def move(self, dx, dy, speed):
        new_x, new_y = int(self.x), int(self.y)
        for i in range(speed):
            new_x, new_y = new_x + dx, new_y + dy
            if new_x < 70 or new_x > 730:
                return True
            
            # Check collisions with grid
            if ((dy > 0 and new_y % GRID_BLOCK_SIZE == 0 or
                 dx > 0 and new_x % GRID_BLOCK_SIZE == 0 or
                 dx < 0 and new_x % GRID_BLOCK_SIZE == GRID_BLOCK_SIZE-1)
                and self.game.block(new_x, new_y)):
                    return True
            self.pos = new_x, new_y
        return False

class Orb(CollideActor):
    MAX_TIMER = 250
    def __init__(self, game_instance, pos, dir_x):
        super().__init__(game_instance, pos)
        self.direction_x = dir_x
        self.floating = False
        self.trapped_enemy_type = None
        self.timer = -1
        self.blown_frames = 6

    def hit_test(self, bolt):
        if self.collidepoint(bolt.pos):
            self.timer = Orb.MAX_TIMER - 1
            return True
        return False

    def update(self):
        self.timer += 1
        if self.floating:
            self.move(0, -1, randint(1, 2))
        else:
            if self.move(self.direction_x, 0, 4):
                self.floating = True
        
        if self.timer == self.blown_frames:
            self.floating = True
        elif self.timer >= Orb.MAX_TIMER or self.y <= -40:
            self.game.pops.append(Pop(self.game, self.pos, 1))
            if self.trapped_enemy_type is not None:
                self.game.fruits.append(Fruit(self.game, self.pos, self.trapped_enemy_type))
            self.game.play_sound("pop", 4)

        # Animation
        if self.timer < 9:
            self.image = "orb" + str(self.timer // 3)
        else:
            if self.trapped_enemy_type is not None:
                self.image = "trap" + str(self.trapped_enemy_type) + str((self.timer // 4) % 8)
            else:
                self.image = "orb" + str(3 + (((self.timer - 9) // 8) % 4))

class Bolt(CollideActor):
    SPEED = 7
    def __init__(self, game_instance, pos, dir_x):
        super().__init__(game_instance, pos)
        self.direction_x = dir_x
        self.active = True

    def update(self):
        if self.move(self.direction_x, 0, Bolt.SPEED):
            self.active = False
        else:
            for obj in self.game.orbs + [self.game.player]:
                if obj and obj.hit_test(self):
                    self.active = False
                    break
        direction_idx = "1" if self.direction_x > 0 else "0"
        anim_frame = str((self.game.timer // 4) % 2)
        self.image = "bolt" + direction_idx + anim_frame

class Pop(Actor):
    def __init__(self, game_instance, pos, type):
        super().__init__("blank", pos)
        self.game = game_instance
        self.type = type
        self.timer = -1

    def update(self):
        self.timer += 1
        self.image = "pop" + str(self.type) + str(self.timer // 2)

class GravityActor(CollideActor):
    MAX_FALL_SPEED = 10
    def __init__(self, game_instance, pos):
        super().__init__(game_instance, pos, ANCHOR_CENTRE_BOTTOM)
        self.vel_y = 0
        self.landed = False

    def update(self, detect=True):
        self.vel_y = min(self.vel_y + 1, GravityActor.MAX_FALL_SPEED)
        if detect:
            if self.move(0, sign(self.vel_y), abs(self.vel_y)):
                self.vel_y = 0
                self.landed = True
            if self.top >= HEIGHT:
                self.y = 1
        else:
            self.y += self.vel_y

class Fruit(GravityActor):
    APPLE = 0
    RASPBERRY = 1
    LEMON = 2
    EXTRA_HEALTH = 3
    EXTRA_LIFE = 4

    def __init__(self, game_instance, pos, trapped_enemy_type=0):
        super().__init__(game_instance, pos)
        if trapped_enemy_type == Robot.TYPE_NORMAL:
            self.type = choice([Fruit.APPLE, Fruit.RASPBERRY, Fruit.LEMON])
        else:
            types = 10 * [Fruit.APPLE, Fruit.RASPBERRY, Fruit.LEMON] + 9 * [Fruit.EXTRA_HEALTH] + [Fruit.EXTRA_LIFE]
            self.type = choice(types)
        self.time_to_live = 500

    def update(self):
        super().update()
        if self.game.player and self.game.player.collidepoint(self.center):
            if self.type == Fruit.EXTRA_HEALTH:
                self.game.player.health = min(3, self.game.player.health + 1)
                self.game.play_sound("bonus")
            elif self.type == Fruit.EXTRA_LIFE:
                self.game.player.lives += 1
                self.game.play_sound("bonus")
            else:
                self.game.player.score += (self.type + 1) * 100
                self.game.play_sound("score")
            self.time_to_live = 0
        else:
            self.time_to_live -= 1
        
        if self.time_to_live <= 0:
            self.game.pops.append(Pop(self.game, (self.x, self.y - 27), 0))
        
        anim_frame = str([0, 1, 2, 1][(self.game.timer // 6) % 4])
        self.image = "fruit" + str(self.type) + anim_frame

class Player(GravityActor):
    def __init__(self, game_instance):
        super().__init__(game_instance, (0, 0))
        self.lives = 2
        self.score = 0
        self.health = 3
        self.reset()

    def reset(self):
        self.pos = (WIDTH / 2, 100)
        self.vel_y = 0
        self.direction_x = 1
        self.fire_timer = 0
        self.hurt_timer = 100
        self.health = 3
        self.blowing_orb = None

    def hit_test(self, other):
        if self.collidepoint(other.pos) and self.hurt_timer < 0:
            self.hurt_timer = 200
            self.health -= 1
            self.vel_y = -12
            self.landed = False
            self.direction_x = other.direction_x
            if self.health > 0:
                self.game.play_sound("ouch", 4)
            else:
                self.game.play_sound("die")
            return True
        return False

    def update(self, input_state):
        super().update(self.health > 0)
        self.fire_timer -= 1
        self.hurt_timer -= 1

        if self.landed:
            self.hurt_timer = min(self.hurt_timer, 100)

        if self.hurt_timer > 100:
            # Hurt logic
            if self.health > 0:
                self.move(self.direction_x, 0, 4)
            else:
                if self.top >= HEIGHT * 1.5:
                    self.lives -= 1
                    self.reset()
        else:
            # Movement logic
            dx = 0
            if input_state.left: dx = -1
            elif input_state.right: dx = 1

            if dx != 0:
                self.direction_x = dx
                if self.fire_timer < 10:
                    self.move(dx, 0, 4)

            if input_state.fire_pressed and self.fire_timer <= 0 and len(self.game.orbs) < 5:
                x = min(730, max(70, self.x + self.direction_x * 38))
                y = self.y - 35
                self.blowing_orb = Orb(self.game, (x, y), self.direction_x)
                self.game.orbs.append(self.blowing_orb)
                self.game.play_sound("blow", 4)
                self.fire_timer = 20

            if input_state.jump_pressed and self.vel_y == 0 and self.landed:
                self.vel_y = -16
                self.landed = False
                self.game.play_sound("jump")

        # Held fire logic
        if input_state.fire_held:
            if self.blowing_orb:
                self.blowing_orb.blown_frames += 4
                if self.blowing_orb.blown_frames >= 120:
                    self.blowing_orb = None
        else:
            self.blowing_orb = None

        # Animation
        self.image = "blank"
        if self.hurt_timer <= 0 or self.hurt_timer % 2 == 1:
            dir_index = "1" if self.direction_x > 0 else "0"
            if self.hurt_timer > 100:
                if self.health > 0: self.image = "recoil" + dir_index
                else: self.image = "fall" + str((self.game.timer // 4) % 2)
            elif self.fire_timer > 0: self.image = "blow" + dir_index
            elif dx == 0: self.image = "still"
            else: self.image = "run" + dir_index + str((self.game.timer // 8) % 4)

class Robot(GravityActor):
    TYPE_NORMAL = 0
    TYPE_AGGRESSIVE = 1

    def __init__(self, game_instance, pos, type):
        super().__init__(game_instance, pos)
        self.type = type
        self.speed = randint(1, 3)
        self.direction_x = 1
        self.alive = True
        self.change_dir_timer = 0
        self.fire_timer = 100

    def update(self):
        super().update()
        self.change_dir_timer -= 1
        self.fire_timer += 1

        if self.move(self.direction_x, 0, self.speed):
            self.change_dir_timer = 0

        if self.change_dir_timer <= 0:
            directions = [-1, 1]
            if self.game.player:
                directions.append(sign(self.game.player.x - self.x))
            self.direction_x = choice(directions)
            self.change_dir_timer = randint(100, 250)

        if self.type == Robot.TYPE_AGGRESSIVE and self.fire_timer >= 24:
            for orb in self.game.orbs:
                if orb.y >= self.top and orb.y < self.bottom and abs(orb.x - self.x) < 200:
                    self.direction_x = sign(orb.x - self.x)
                    self.fire_timer = 0
                    break

        if self.fire_timer >= 12:
            fire_prob = self.game.fire_probability()
            if self.game.player and self.top < self.game.player.bottom and self.bottom > self.game.player.top:
                fire_prob *= 10
            if random() < fire_prob:
                self.fire_timer = 0
                self.game.play_sound("laser", 4)
        elif self.fire_timer == 8:
            self.game.bolts.append(Bolt(self.game, (self.x + self.direction_x * 20, self.y - 38), self.direction_x))

        for orb in self.game.orbs:
            if orb.trapped_enemy_type is None and self.collidepoint(orb.center):
                self.alive = False
                orb.floating = True
                orb.trapped_enemy_type = self.type
                self.game.play_sound("trap", 4)
                break

        direction_idx = "1" if self.direction_x > 0 else "0"
        image = "robot" + str(self.type) + direction_idx
        if self.fire_timer < 12:
            image += str(5 + (self.fire_timer // 4))
        else:
            image += str(1 + ((self.game.timer // 4) % 4))
        self.image = image