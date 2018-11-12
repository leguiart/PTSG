try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Frame._hide_status = True
    simplegui.Frame._keep_timers = False
import random
import math
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
        #self.missile_group = set([])
        self.enemy_ships = EnemyShips(self.pars["enemy"], None, 1, self.pars["enemy_list"])
        self.explosion_group = set()
        self.globals_dict["score"] = 0
        self.lives = globals_dict["lives"]
        self.sc_dif = globals_dict["sc_dif"]
        self.globals_dict["started"] = False
        self.spawn = True

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
        self.pars["my_ship"].draw(canvas)

        if self.globals_dict["started"] and self.globals_dict["score"] == 0:
            self.pars["soundtrack"].play()        
            #self.pars["a_rock"].draw(canvas)


        if self.enemy_ships.spawn and self.globals_dict["started"]:
            self.enemy_ships.spawn = False
        elif self.globals_dict["started"]:
            SpriteGroup.process_sprite_group(canvas, self.rock_group)
            SpriteGroup.process_sprite_group(canvas, self.explosion_group)
            SpriteGroup.process_sprite_group(canvas, self.enemy_ships.enemy_group)
            SpriteGroup.process_groups_of_group(canvas, self.enemy_ships.enemy_group)
            SpriteGroup.process_lifespan_group(canvas, self.pars["my_ship"].missile_group)

        # update ship and sprites
        self.pars["my_ship"].update()
        self.enemy_ships.update()
        SpriteGroup.collide1(self.rock_group, self.pars["my_ship"], self.explosion_group,self.globals_dict, self.pars)
        SpriteGroup.collide2(self.rock_group, self.pars["my_ship"].missile_group, self.explosion_group,self.globals_dict, self.pars)
        SpriteGroup.collide3(self.enemy_ships, self.pars["my_ship"].missile_group, self.explosion_group, self.globals_dict, self.pars)
        SpriteGroup.collide4(self.enemy_ships.enemy_group, self.pars["my_ship"], self.explosion_group, self.globals_dict, self.pars)
        self.enemy_ships.enemy_ai(self.pars["my_ship"])
        
        canvas.draw_text("Lives", (40, 40), 18, "White", "sans-serif")
        canvas.draw_text(str(self.globals_dict["lives"]), (40, 64), 18, "White", "sans-serif")
        
        canvas.draw_text("Score", (self.globals_dict["WIDTH"] - 80, 40), 18, "White", "sans-serif")
        canvas.draw_text(str(self.globals_dict["score"]), (self.globals_dict["WIDTH"] - 80, 64), 18, "White", "sans-serif")
        
        if self.globals_dict["lives"]<=0:
            self.globals_dict["started"] = False
            self.globals_dict["lives"] = self.lives
            self.globals_dict["score"] = 0
            self.rock_group = set([])
            self.enemy_ships.spawn = True
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
        if self.globals_dict["score"]>0 and self.globals_dict["score"]%5==0:
            self.explosion_group=set()
            self.globals_dict["sc_dif"]+=.2
        rock_vel=[random.randrange(-1,3) * random.random() * self.globals_dict["sc_dif"], random.randrange(-1,3) * random.random() * self.globals_dict["sc_dif"]]
        if self.globals_dict["started"] and x<12 and Auxiliars.dist(rock_pos, self.pars["my_ship"].get_pos())> (self.pars["ship_info"].get_radius() + self.pars["asteroid_info"].get_radius())*1.2:
            a_rock = Sprite(rock_pos ,rock_vel, random.random(), 0.10471976, self.pars["asteroid_image"], \
                self.pars["asteroid_info"], self.globals_dict["WIDTH"], self.globals_dict["HEIGHT"])
            self.rock_group.add(a_rock)

    def keydown_hand(self, key):
        if key == simplegui.KEY_MAP['up']:
            self.pars["my_ship"].thrust(True)
        if key == simplegui.KEY_MAP['left']:
            self.pars["my_ship"].key(-self.pars["my_ship"].values["ang_acc"])
        elif key == simplegui.KEY_MAP['right']:
            self.pars["my_ship"].key(self.pars["my_ship"].values["ang_acc"])
        elif key == simplegui.KEY_MAP['space']:
            self.pars["my_ship"].shoot()

    def keyup_hand(self, key): 
        if key== simplegui.KEY_MAP['up']:      
            self.pars["my_ship"].thrust()
        elif simplegui.KEY_MAP.get("left") == key:
            self.pars["my_ship"].key(0.0,True)
        elif simplegui.KEY_MAP.get("right") == key:
            self.pars["my_ship"].key(0.0,True)

    # mouseclick handlers that reset UI and conditions whether splash image is drawn        
    def click(self, pos):
        center = [self.globals_dict["WIDTH"] / 2, self.globals_dict["HEIGHT"] / 2]
        size = self.pars["splash_info"].get_size()
        inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
        inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
        if (not self.globals_dict["started"]) and inwidth and inheight:
            self.globals_dict["started"] = True
    
    def get_rolling(self, frame):
        # register handlers
        frame.set_draw_handler(self.draw)
        frame.set_keydown_handler(self.keydown_hand)
        frame.set_keyup_handler(self.keyup_hand)
        frame.set_mouseclick_handler(self.click)
        #timer = simplegui.create_timer(1000.0, self.rock_spawner)
        # get things rolling
        #timer.start()
        frame.start()