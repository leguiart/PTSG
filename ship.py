try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Frame._hide_status = True
    simplegui.Frame._keep_timers = False
import random
import math
import numpy as np
import operator
from collections import defaultdict
from aux import Auxiliars
from sprite import Sprite
from sprite import SpriteGroup
from physics import Physics
from environment import Environment


# Ship class


class Ship:
    def __init__(self, pars, is_kinetic=False, acc=0, ang_acc=0, fr=0, lives=0, life=0):
        self.image = pars["image"]
        self.image_center = pars["info"].get_center()
        self.image_size = pars["info"].get_size()
        radius = pars["info"].get_radius()
        self.up_key_down = False
        self.left_key_down = False
        self.right_key_down = False
        self.missile_image = pars["missile_image"]
        self.missile_info = pars["missile_info"]
        self.missile_sound = pars["missile_sound"]
        self.ship_thrust_sound = pars["ship_thrust_sound"]
        self.missile_group = set([])
        self.lives = lives
        self.life = life
        self.score = 0
        if is_kinetic:
            self.physics = Physics(
                radius, pars["WIDTH"], pars["HEIGHT"], None, is_kinetic, fr)
            self.physics.set_ang_acc(ang_acc)
            self.physics.set_acc(acc)
        else:
            self.physics = Physics(radius, WIDTH, HEIGHT)
        self.physics.set_pos(pars["pos"])
        self.physics.set_vel(pars["vel"])
        self.physics.set_ang(pars["ang"])
        self.physics.set_ang_vel(pars["ang_vel"])

    def draw(self, canvas):
        if not self.up_key_down:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.physics.get_pos(), self.image_size, self.physics.get_angle())
            self.ship_thrust_sound.rewind()
        else:
            canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0], self.image_center[1]],
             self.image_size, self.physics.get_pos(), self.image_size, self.physics.get_angle())
            self.ship_thrust_sound.play()

    def get_physics_component(self):
        return self.physics

    def turn(self, ang_acc=0):
        self.physics.add_torque(ang_acc)

    def thrust(self, acc=0):
        self.physics.add_force(acc)

    def process_missile_group(self, canvas):
        SpriteGroup.process_sprite_group(canvas, self.missile_group)
        SpriteGroup.process_lifespan_group(canvas, self.missile_group)

    def shoot(self):
        front = self.get_front()
        pos = self.physics.get_pos()
        vel = self.physics.get_vel()
        self.missile_group.add(Sprite([pos[0]+self.physics.get_radius()*front[0], pos[1]+self.physics.get_radius()*front[1]],
        [vel[0] + front[0]*self.physics.get_radius()/5, vel[1] + front[1] *
                                                   self.physics.get_radius()/5],
        0, 0, self.missile_image, self.missile_info, self.physics.WIDTH, self.physics.HEIGHT, self.missile_sound))

    def collide_ship_sprites(self, group, explosion_group, explosion_image, explosion_info, ship=None, ship_group=None):
        group_copy = set([])
        aux_copy = group.copy()
        for sprite in aux_copy:
            if self.physics.collide(sprite) is True:
                group_copy.add(sprite)
                explosion = Sprite(sprite.get_physics_component().get_pos(), [
                                   0, 0], 0, 0, explosion_image, explosion_info, self.physics.WIDTH, self.physics.HEIGHT)
                explosion_group.add(explosion)
                explosion_group.add(Sprite(self.physics.get_pos(), [
                                    0, 0], 0, 0, explosion_image, explosion_info, self.physics.WIDTH, self.physics.HEIGHT))
                if self.life <= 0:
                    self.lives -= 1
                if ship is not None:
                    ship.score += 1

                if ship_group is not None:
                    ship_group.add(self)

        group.difference_update(group_copy)

    def get_front(self):
        return [Auxiliars.angle_to_vector(self.physics.get_angle())[0], Auxiliars.angle_to_vector(self.physics.get_angle())[1]]

    def get_right(self):
        return [Auxiliars.angle_to_vector(self.physics.get_angle()+math.pi/2.0)[0], Auxiliars.angle_to_vector(self.physics.get_angle()+math.pi/2.0)[1]]

    def get_missile_group(self):
        return self.missile_group

    def get_pos(self):
        return self.physics.get_pos()

    def get_acc(self):
        return self.physics.get_acc()

    def get_ang_acc(self):
        return self.physics.get_ang_acc()

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def set_inc_score(self):
        score += 1


class EnemyShip(Ship):
    def __init__(self, pars, player_pos, wih=None, who=None):
        self.pars = pars
        v = random.uniform(0, pars['v_max'])   # velocity      [0, v_max]
        # orientation   [0, 360]
        self.pars["ang"] = random.uniform(0, 360)
        front = Auxiliars.angle_to_vector(self.pars["ang"])
        self.pars["vel"] = [v*front[0], v*front[1]]
        # self.pars["pos"] = [uniform(0, pars['WIDTH']), uniform(0, pars['HEIGHT'])]
        Ship.__init__(self, self.pars, True,
                      self.pars["acc"], self.pars["ang_acc"], self.pars["fr"])
        self.delay = 0
        # self.dv = pars["acc_max"]
        self.d_player = 0   # distance to player
        self.angle_front = 0
        self.angle_right = 0
        self.facing(player_pos)     # orientation to player
        Ship.set_score(self, pars["score"])    # fitness (score)
        self.wih = wih
        self.who = who
        af = lambda x: np.tanh(x)               # activation function
        h1 = af(np.matmul(self.wih, np.mat(
            np.array([1.0, self.angle_front, self.d_player])).transpose()))  # hidden layer
        out = af(np.matmul(self.who, np.mat(
            np.append(np.mat(np.ones(np.size(h1, 1))), h1, axis=0))))        # output layer

    # NEURAL NETWORK

    def think(self, player_pos):
        # SIMPLE MLP
        self.facing(player_pos)
        af = lambda x: np.tanh(x)        # activation function
        h1 = af(np.matmul(self.wih, np.mat(
            np.array([1.0, self.angle_front, self.d_player])).transpose()))  # hidden layer
        out = af(np.matmul(self.who, np.mat(
            np.append(np.mat(np.ones(np.size(h1, 1))), h1, axis=0))))        # output layer
        # UPDATE dv AND dr WITH MLP RESPONSE
        self.nn_dv = float(out[0])   # [-1, 1]  (accelerate=1, don't=-1)
        self.nn_dr = float(out[1])   # [-1, 1]  (left=1, right=-1)

    # UPDATE HEADING

    def update_angle(self):
        # self.r += self.nn_dr * settings['dr_max'] * settings['dt']
        # self.r = self.r % 360
        if self.nn_dr < 0:
            if Ship.get_physics_component(self).get_ang_acc() < 0:
                Ship.turn(self, -self.pars["ang_acc"] * self.nn_dr)
            else:
                Ship.turn(self, self.pars["ang_acc"] * self.nn_dr)
        elif self.nn_dr > 0:
            if Ship.get_physics_component(self).get_ang_acc() > 0:
                Ship.turn(self, self.pars["ang_acc"] * self.nn_dr)
            else:
                Ship.turn(self, -self.pars["ang_acc"] * self.nn_dr)

    # UPDATE VELOCITY

    def update_vel(self):
        if(self.nn_dv > 0):
            Ship.get_physics_component(self).add_force(
                self.pars["acc"] * self.nn_dv)
        # self.v += self.nn_dv * settings['dv_max'] * settings['dt']
        # if self.v < 0: self.v = 0
        # if self.v > settings['v_max']: self.v = settings['v_max']

    # UPDATE POSITION

    def update_pos(self, player_pos):
        self.think(player_pos)
        self.update_angle()
        self.update_vel()
        Ship.get_physics_component(self).update()

    def facing(self, other_pos):
        front = Ship.get_front(self)
        right = Ship.get_right(self)
        self.d_player = Auxiliars.dist(Ship.get_pos(self), other_pos)
        vec = [(other_pos[0] - Ship.get_pos(self)[0])/self.d_player,
                (other_pos[1] - Ship.get_pos(self)[1])/self.d_player]
        phi = math.atan2(vec[1], vec[0])
        # self.angle_front, self.angle_right = (math.acos(front[0]*vec[0] + front[1]*vec[1])*180.0/math.pi, math.acos(right[0]*vec[0] + right[1]*vec[1])*180.0/math.pi)
        front = Ship.get_front(self)
        self.angle_front = (
            (phi - math.atan2(front[1], front[0]))*180.0/math.pi)/360.0
        self.d_player = self.d_player/1000
        if self.angle_front <= self.pars["ang_rang"]/360.0 and self.angle_front >= -self.pars["ang_rang"]/360.0:
            self.delay += 1
            if self.delay >= 5:
                Ship.shoot(self)
                self.delay = 0
                # print(Ship.get_score(self))

    def draw(self, canvas):
        Ship.draw(self, canvas)


class EnemyShips:

    def __init__(self, settings, p):
        self.population = list()
        self.p = p
        self.settings = settings
        self.enemy_group = set()
        self.dead = set()
        self.population = [{"pos": [random.randrange(0, settings['WIDTH']), random.randrange(0, settings['HEIGHT'])], "vel": [0, 0], "ang_vel": float(self.settings["ang_vel_median"]*np.random.randn(1)+self.settings["ang_vel_std_dev"]),
        "ang": float(self.settings["ang_median"]*np.random.randn(1)+self.settings["ang_std_dev"]), "WIDTH": settings["WIDTH"], "HEIGHT": settings["HEIGHT"], "v_max": settings["v_max"], "score": 0, "ang_rang": float(self.settings["ang_rang_median"]*np.random.randn(1)+self.settings["ang_rang_std_dev"]),
        "acc": float(self.settings["acc_median"]*np.random.randn(1)+self.settings["acc_std_dev"]), "ang_acc": float(self.settings["ang_acc_median"]*np.random.randn(1)+self.settings["ang_acc_std_dev"]), "fr": settings["fr"], "lives": settings["lives"], "wih": settings["wih_median"]*np.random.randn(settings["hnodes"], settings["onodes"] + 1) + settings["wih_std_dev"],
        "who": settings["who_median"]*np.random.randn(settings["onodes"], settings["hnodes"] + 1)+settings["who_std_dev"]} for i in range(settings["pop_size"])]

    def spawn_ships(self, player_pos):
        self.enemy_group = set([EnemyShip(Auxiliars.merge_two_dicts(
            org, self.p), player_pos, org["wih"], org["who"]) for org in self.population])

    def update_pos(self, player_pos):
        for enemy in self.enemy_group:
            enemy.update_pos(player_pos)

    # collide player ship with enemies missiles and enemy ships with player's missiles
    def collide_ship_sprites(self, player_ship, missile_group, explosion_group, explosion_image, explosion_info):
        enemy_group_copy = set()
        for enemy in self.enemy_group:
            player_ship.collide_ship_sprites(
                enemy.missile_group, explosion_group, explosion_image, explosion_info, ship=enemy)
            enemy.collide_ship_sprites(player_ship.missile_group, explosion_group, explosion_image,
                                       explosion_info, ship=player_ship, ship_group=enemy_group_copy)
        for enemy in enemy_group_copy:
            self.dead.add(enemy)
        self.enemy_group.difference_update(enemy_group_copy)

    def process_missile_group(self, canvas):
        for enemy in self.enemy_group:
            enemy.process_missile_group(canvas)

    def draw(self, canvas):
        for enemy in self.enemy_group:
            enemy.draw(canvas)

    def evolve(self, organisms_old, gen):
        self.enemy_group = set()
        self.dead = set()
        elitism_num = int(np.floor(self.settings['elitism'] * self.settings['pop_size']))
        new_orgs = self.settings['pop_size'] - elitism_num

        # --- GET STATS FROM CURRENT GENERATION ----------------+
        stats = defaultdict(int)
        for org in organisms_old:
            if org.score > stats['BEST'] or stats['BEST'] == 0:
                stats['BEST'] = org.score
            
            if org.score < stats['WORST'] or stats['WORST'] == 0:
                stats['WORST'] = org.score
            stats['SUM'] += org.score
            stats['COUNT'] += 1
        
        stats['AVG'] = stats['SUM'] / stats['COUNT']
        # --- ELITISM (KEEP BEST PERFORMING ORGANISMS) ---------+
        orgs_sorted = sorted(organisms_old, key=operator.attrgetter('score'), reverse=True)
        self.population = []
        for i in range(0, elitism_num):
            aux_dict = {"wih": orgs_sorted[i].wih, "woh": orgs_sorted[i].who, "pos": [random.randrange(0, self.settings['WIDTH']), \
                random.randrange(0, self.settings['HEIGHT'])]}
            self.population.append(Auxiliars.merge_two_dicts(orgs_sorted[i].pars, aux_dict))

        # --- GENERATE NEW ORGANISMS ---------------------------+
        for w in range(elitism_num - 1, self.settings["pop_size"]):
            aux_dict = dict()
            # SELECTION (TRUNCATION SELECTION)
            canidates = range(0, elitism_num)
            random_index = random.sample(canidates, 2)
            org_1 = orgs_sorted[random_index[0]]
            org_2 = orgs_sorted[random_index[1]]

            # CROSSOVER
            crossover_weight = random.random()
            aux_dict["wih"] = (crossover_weight * org_1.wih) + \
                               ((1 - crossover_weight) * org_2.wih)
            aux_dict["who"] = (crossover_weight * org_1.who) + \
                               ((1 - crossover_weight) * org_2.who)
            aux_dict["pos"] = [random.randrange(
                0, self.settings['WIDTH']), random.randrange(0, self.settings['HEIGHT'])]
            aux_dict["v_max"] = (crossover_weight * org_1.pars["v_max"]) + \
                                 ((1 - crossover_weight) * org_2.pars["v_max"])
            aux_dict["ang_rang"] = (crossover_weight * org_1.pars["ang_rang"]) + \
                                    ((1 - crossover_weight)
                                     * org_2.pars["ang_rang"])
            aux_dict["acc"] = (crossover_weight * org_1.get_acc()) + \
                               ((1 - crossover_weight) * org_2.get_acc())
            aux_dict["ang_acc"] = (crossover_weight * org_1.get_ang_acc()) + \
                                   ((1 - crossover_weight) * org_2.get_ang_acc())
            aux_dict["vel"] = [0, 0]
            aux_dict["ang_vel"] = float(
                self.settings["ang_vel_median"]*np.random.randn(1)+self.settings["ang_vel_std_dev"])
            aux_dict["ang"] = float(
                self.settings["ang_median"]*np.random.randn(1)+self.settings["ang_std_dev"])
            aux_dict["WIDTH"] = self.settings["WIDTH"]
            aux_dict["HEIGHT"] = self.settings["HEIGHT"]
            aux_dict["score"] = 0
            aux_dict["fr"] = self.settings["fr"]
            aux_dict["lives"] = self.settings["lives"]
            # MUTATION
            mutate = random.random()
            if mutate <= self.settings['mutate']:

                # PICK WHICH WEIGHT MATRIX TO MUTATE
                mat_pick = random.randint(0, 1)

                # MUTATE: WIH WEIGHTS
                if mat_pick == 0:
                    index_row = random.randint(0, self.settings['hnodes']-1)
                    aux_dict["wih"][index_row] = aux_dict["wih"][index_row] * \
                        random.uniform(0.9, 1.1)
                    if aux_dict["wih"][index_row].any() > 1: aux_dict["wih"][index_row] = 1
                    if aux_dict["wih"][index_row].any() < - \
                        1: aux_dict["wih"][index_row] = -1

                # MUTATE: WHO WEIGHTS
                if mat_pick == 1:
                    index_row = random.randint(0, self.settings['onodes']-1)
                    index_col = random.randint(0, self.settings['hnodes']-1)
                    aux_dict["who"][index_row][index_col] = aux_dict["who"][index_row][index_col] * \
                        random.uniform(0.9, 1.1)
                    if aux_dict["who"][index_row][index_col] > 1:
                        aux_dict["who"][index_row][index_col] = 1
                    if aux_dict["who"][index_row][index_col] < - 1:
                        aux_dict["who"][index_row][index_col] = -1
            self.population.append(aux_dict)
