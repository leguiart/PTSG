try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Frame._hide_status = True
    simplegui.Frame._keep_timers = False
import random
import math
import operator
from aux import Auxiliars
from sprite import Sprite
from sprite import SpriteGroup
from ship import Ship
from ship import EnemyShips


class Game:

    def __init__(self, globals_dict, pars):
        self.globals_dict = globals_dict
        self.pars = pars
        # sets
        self.rock_group = set([])
        self.explosion_group = set()
        self.lives = pars["ship"].lives
        self.sc_dif = globals_dict["sc_dif"]
        self.globals_dict["started"] = False
        self.spawn = True
        self.turn = False
        self.enemies = EnemyShips(pars["settings"], pars["enemy_pars"])
        self.previous_started = False
        self.generation = -1


    def draw(self, canvas):
        # animate background
        self.globals_dict["time"] += 1
        wtime = (self.globals_dict["time"] / 4) % self.globals_dict["WIDTH"]
        center = self.pars["debris_info"].get_center()
        size = self.pars["debris_info"].get_size()
        canvas.draw_image(self.pars["nebula_image"], self.pars["nebula_info"].get_center(), self.pars["nebula_info"].get_size(),\
        [self.globals_dict["WIDTH"] / 2, self.globals_dict["HEIGHT"] / 2], [self.globals_dict["WIDTH"], self.globals_dict["HEIGHT"]])
        canvas.draw_image(self.pars["debris_image"], center, size, (wtime - self.globals_dict["WIDTH"] / 2, self.globals_dict["HEIGHT"] / 2), \
        (self.globals_dict["WIDTH"], self.globals_dict["HEIGHT"]))
        canvas.draw_image(self.pars["debris_image"], center, size, (wtime + self.globals_dict["WIDTH"] / 2, self.globals_dict["HEIGHT"] / 2), \
         (self.globals_dict["WIDTH"], self.globals_dict["HEIGHT"]))

        # draw ship and sprites
        self.pars["ship"].draw(canvas)
        self.enemies.draw(canvas)
        if self.globals_dict["started"]:
            self.pars["soundtrack"].play()
            if self.previous_started:
                self.generation+=1 
                self.enemies.spawn_ships(self.pars["ship"].get_pos())
                self.previous_started = False
            elif self.generation > -1 and len(self.enemies.enemy_group) == 0:
                self.enemies.evolve(self.enemies.dead, self.generation)
                self.previous_started = True
           
        # update ship and sprites
        if self.pars["ship"].up_key_down:
            self.pars["ship"].thrust(self.pars["ship"].physics.get_acc())
        
        if self.pars["ship"].left_key_down:
            if self.pars["ship"].physics.get_ang_acc() < 0:
                self.pars["ship"].turn(self.pars["ship"].physics.get_ang_acc())
            else:
                self.pars["ship"].turn(-self.pars["ship"].physics.get_ang_acc())            
        elif self.pars["ship"].right_key_down:
            if self.pars["ship"].physics.get_ang_acc() > 0:
                self.pars["ship"].turn(self.pars["ship"].physics.get_ang_acc())
            else:
                self.pars["ship"].turn(-self.pars["ship"].physics.get_ang_acc())
        
        self.pars["ship"].get_physics_component().update()
        #SpriteGroup.process_sprite_group(canvas, self.rock_group)
        #self.pars["ship"].collide_ship_sprites(self.rock_group, self.explosion_group, self.pars["explosion_image"], self.pars["explosion_info"])
        self.enemies.update_pos(self.pars["ship"].get_pos())
        self.enemies.collide_ship_sprites(self.pars["ship"], self.pars["ship"].missile_group, self.explosion_group, self.pars["explosion_image"], self.pars["explosion_info"])
        #SpriteGroup.collide_sprite_sprite(self.rock_group, self.pars["ship"].missile_group, self.explosion_group, self.pars["explosion_image"], self.pars["explosion_info"], self.pars["ship"])
        #SpriteGroup.process_sprite_group(canvas, self.rock_group)
        SpriteGroup.process_sprite_group(canvas, self.explosion_group)
        self.pars["ship"].process_missile_group(canvas)
        self.enemies.process_missile_group(canvas)
        
        canvas.draw_text("Lives", (40, 40), 18, "White", "sans-serif")
        canvas.draw_text(str(self.pars["ship"].lives), (40, 64), 18, "White", "sans-serif")
        
        canvas.draw_text("Score", (self.globals_dict["WIDTH"] - 80, 40), 18, "White", "sans-serif")
        canvas.draw_text(str(self.pars["ship"].score), (self.globals_dict["WIDTH"] - 80, 64), 18, "White", "sans-serif")
        
        canvas.draw_text("Generation", (self.globals_dict["WIDTH"] - 100, 936), 18, "White", "sans-serif")
        canvas.draw_text(str(self.generation), (self.globals_dict["WIDTH"] - 80, 960), 18, "White", "sans-serif")

        if self.pars["ship"].lives<=0:
            self.globals_dict["started"] = False
            self.pars["ship"].lives = self.lives
            self.pars["ship"].score = 0  
            self.rock_group = set([])
            if self.enemies.dead is not None:
                self.enemies.evolve(list(self.enemies.enemy_group.union(self.enemies.dead)), self.generation)
            else:
                self.enemies.evolve(list(self.enemies.enemy_group), self.generation)
            self.generation+=1
            self.globals_dict["sc_dif"] = self.sc_dif  

        # draw splash screen if not started
        if not self.globals_dict["started"]:        
            canvas.draw_image(self.pars["splash_image"], self.pars["splash_info"].get_center(), 
                            self.pars["splash_info"].get_size(), [self.globals_dict["WIDTH"] / 2, self.globals_dict["HEIGHT"] / 2], 
                            self.pars["splash_info"].get_size())
            self.pars["soundtrack"].rewind()


    # timer handler that spawns a rock    
    def rock_spawner(self):
        x=0
        for s in self.rock_group:
            x+=1
        rock_pos=[random.randrange(0, self.globals_dict["WIDTH"]-44),random.randrange(0, self.globals_dict["HEIGHT"]-44)]
        if self.pars["ship"].score>0 and self.pars["ship"].score%5==0:
            self.explosion_group=set()
            self.globals_dict["sc_dif"]+=.2
        rock_vel=[random.randrange(-1,3) * random.random() * self.globals_dict["sc_dif"], random.randrange(-1,3) * random.random() * self.globals_dict["sc_dif"]]
        if self.globals_dict["started"] and x<12 and Auxiliars.dist(rock_pos, self.pars["ship"].get_physics_component().get_pos())> (self.pars["ship_info"].get_radius() + self.pars["asteroid_info"].get_radius())*1.2:
            a_rock = Sprite(rock_pos, rock_vel, random.random(), 0.10471976, self.pars["asteroid_image"], \
                self.pars["asteroid_info"], self.globals_dict["WIDTH"], self.globals_dict["HEIGHT"])
            self.rock_group.add(a_rock)


    def keydown_hand(self, key):
        if key == simplegui.KEY_MAP['up']:
            self.pars["ship"].up_key_down = True
        if key == simplegui.KEY_MAP['left']:
            self.pars["ship"].left_key_down = True
        elif key == simplegui.KEY_MAP['right']:
            self.pars["ship"].right_key_down = True
        elif key == simplegui.KEY_MAP['space']:
            self.pars["ship"].shoot()

    def keyup_hand(self, key): 
        if key== simplegui.KEY_MAP['up']:      
            self.pars["ship"].up_key_down = False
        elif simplegui.KEY_MAP.get("left") == key:
            self.pars["ship"].left_key_down = False
        elif simplegui.KEY_MAP.get("right") == key:
            self.pars["ship"].right_key_down = False

    # mouseclick handlers that reset UI and conditions whether splash image is drawn        
    def click(self, pos):
        center = [self.globals_dict["WIDTH"] / 2, self.globals_dict["HEIGHT"] / 2]
        size = self.pars["splash_info"].get_size()
        inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
        inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
        if (not self.globals_dict["started"]) and inwidth and inheight:
            self.globals_dict["started"] = True
            self.previous_started = True

    def start_game(self, frame):
        # register handlers
        frame.set_draw_handler(self.draw)
        frame.set_keydown_handler(self.keydown_hand)
        frame.set_keyup_handler(self.keyup_hand)
        frame.set_mouseclick_handler(self.click)
        #timer = simplegui.create_timer(1000.0, self.rock_spawner)
        # get things rolling
        #timer.start()
        frame.start()
