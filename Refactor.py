
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    simplegui.Frame._hide_status = True
    simplegui.Frame._keep_timers = False

import math
import random
import numpy as np

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

class Auxiliars:
    # helper functions to handle transformations
    @staticmethod
    def angle_to_vector(ang):
        return [math.cos(ang), math.sin(ang)]

    @staticmethod
    def dist(p,q):
        return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, angle_vel, image, info, missile_image, missile_info, missile_sound, ship_thrust_sound, WIDTH, HEIGHT, is_kinetic = False, acc = 0, ang_acc = 0, fr = 0, lives = 0, life = 0):
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        radius = info.get_radius()
        self.up_key_down = False
        self.left_key_down = False
        self.right_key_down = False
        self.missile_image = missile_image
        self.missile_info = missile_info
        self.missile_sound = missile_sound
        self.ship_thrust_sound = ship_thrust_sound
        self.missile_group = set([])
        self.lives = lives
        self.life = life
        self.score = 0
        if is_kinetic:             
            self.physics = Physics(radius, WIDTH, HEIGHT, None, is_kinetic, fr)
            self.physics.set_ang_acc(ang_acc)
            self.physics.set_acc(acc)
        else:
            self.physics = Physics(radius, WIDTH, HEIGHT)
        self.physics.set_pos(pos)
        self.physics.set_vel(vel)
        self.physics.set_ang(angle)
        self.physics.set_ang_vel(angle_vel)

        
    def draw(self,canvas):
        if not self.up_key_down:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.physics.get_pos(), self.image_size, self.physics.get_angle())
            self.ship_thrust_sound.rewind()
        else:
            canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0], self.image_center[1]] ,\
             self.image_size , self.physics.get_pos(), self.image_size, self.physics.get_angle())
            self.ship_thrust_sound.play()

    def get_physics_component(self):
        return self.physics 

    def turn(self, ang_acc = 0):
        self.physics.add_torque(ang_acc) 

    def thrust(self, acc = 0):
        self.physics.add_force(acc)

    def process_missile_group(self, canvas):
        SpriteGroup.process_sprite_group(canvas, self.missile_group)
        SpriteGroup.process_lifespan_group(canvas, self.missile_group)

    def shoot(self):
        front = self.get_front()
        pos = self.physics.get_pos()
        vel = self.physics.get_vel()
        self.missile_group.add(Sprite([pos[0]+self.physics.get_radius()*front[0], pos[1]+self.physics.get_radius()*front[1]],
        [vel[0] + front[0]*self.physics.get_radius()/5, vel[1] + front[1]*self.physics.get_radius()/5],
        0, 0, self.missile_image, self.missile_info, self.physics.WIDTH, self.physics.HEIGHT,self.missile_sound))

    def collide_ship_sprites(self, group, explosion_group, explosion_image, explosion_info):
        group_copy= set([])
        aux_copy = group.copy()
        for sprite in aux_copy:
            if self.physics.collide(sprite) is True:
                group_copy.add(sprite)
                explosion = Sprite(sprite.get_physics_component().get_pos(), [0,0], 0, 0, explosion_image, explosion_info, self.physics.WIDTH, self.physics.HEIGHT)
                explosion_group.add(explosion)
                explosion_group.add(Sprite(self.physics.get_pos(), [0,0], 0, 0, explosion_image, explosion_info, self.physics.WIDTH, self.physics.HEIGHT))
                if self.life <= 0:
                    self.lives-=1
        group.difference_update(group_copy)

    def get_front(self):
        return [Auxiliars.angle_to_vector(self.physics.get_angle())[0], Auxiliars.angle_to_vector(self.physics.get_angle())[1]]
    
    def get_right(self):
        return [Auxiliars.angle_to_vector(self.physics.get_angle()+math.pi/2.0)[0], Auxiliars.angle_to_vector(self.physics.get_angle()+math.pi/2.0)[1]]

    def get_missile_group():
        return self.missile_group

# Sprite class
class Sprite:

    def __init__(self, pos, vel, angle, angle_vel, image, info, WIDTH, HEIGHT, sound = None, is_kinetic = False, acc = 0, ang_acc = 0, fr = 0):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = angle
        self.angle_vel = angle_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        #self.age = 0
        if sound:
            sound.rewind()
            sound.play()
        if is_kinetic:
            if self.lifespan == None: 
                self.physics = Physics(radius, WIDTH, HEIGHT, None, is_kinetic, fr)
            else:
                self.physics = Physics(radius, WIDTH, HEIGHT, self.lifespan, is_kinetic, fr)
            self.physics.set_ang_acc(ang_acc)
            self.physics.set_acc(acc)            
        else:
            if self.lifespan == None:
                self.physics = Physics(radius, WIDTH, HEIGHT)
            else:
                self.physics = Physics(radius, WIDTH, HEIGHT, self.lifespan)
        self.physics.set_pos(pos)
        self.physics.set_vel(vel)
        self.physics.set_ang(angle)
        self.physics.set_ang_vel(angle_vel)
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + (self.physics.age*self.image_size[0]), self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.physics.get_pos(), self.image_size, self.physics.get_angle())
    
    def get_physics_component(self):
        return self.physics


class SpriteGroup(Sprite):

    @staticmethod
    def process_sprite_group(canvas, group):
        group_copy = group.copy()
        for sprite in group_copy:
            sprite.draw(canvas)
            sprite.get_physics_component().update()

    @staticmethod
    def process_lifespan_group(canvas, group):
        SpriteGroup.process_sprite_group(canvas, group)
        group_copy = set([])
        for sprite in group:
            if sprite.get_physics_component().update() is False:
                group_copy.add(sprite)            
        group.difference_update(group_copy)
        
    @staticmethod
    def collide_sprite_sprite(group1, group2, explosion_group, explosion_image, explosion_info, shipObject = None):
        group1_copy= set([])
        group2_copy= set([])
        aux_copy1 = group1.copy() #Same for this
        aux_copy2 = group2.copy() #And for this
        for element1 in aux_copy1:
            for element2 in aux_copy2:
                if element1.physics.collide(element2) is True:
                    group1_copy.add(element1)
                    group2_copy.add(element2)
                    if shipObject is not None:
                        shipObject.score+=1
                    explosion= Sprite(element1.get_physics_component().get_pos(), [0,0], 0, 0, explosion_image, explosion_info, element1.physics.WIDTH, element2.physics.HEIGHT)
                    explosion_group.add(explosion)
        group1.difference_update(group1_copy)
        group2.difference_update(group2_copy)


class Physics:

    def __init__(self, radius, WIDTH, HEIGHT, lifespan = None, is_kinetic = False, fr = 0):
        self.explosion_group = set()
        self.kinematic_dict = dict()
        self.radius = radius
        self.kinematic_dict["pos"] = [0, 0] 
        self.kinematic_dict["ang"] = 0
        self.kinematic_dict["vel"] = [0, 0]
        self.kinematic_dict["ang_vel"] = 0
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.lifespan = lifespan
        self.age = 0
        self.is_kinetic = is_kinetic
        if self.is_kinetic:
            self.kinetic_dict = dict()
            self.kinetic_dict["acc"] = 0
            self.kinetic_dict["ang_acc"] = 0
            try:
                self.kinetic_dict["fr"] = fr
            except:
                print("Chosen kinetic, but no friction given")
            
    def collide(self, other):
        if Auxiliars.dist(self.kinematic_dict["pos"], other.get_physics_component().get_pos()) <= self.radius + other.get_physics_component().get_radius():
            return True
        else:
            return False

    #Using euler's solver
    def update(self):
        for i in range(2):
            if i==0:
                if self.kinematic_dict["pos"][i]>self.WIDTH:
                    self.kinematic_dict["pos"][i]=self.kinematic_dict["pos"][i]%self.WIDTH
                elif self.kinematic_dict["pos"][i]<0:
                    self.kinematic_dict["pos"][i]=self.kinematic_dict["pos"][i]%self.WIDTH + self.WIDTH
            elif i==1:
                if self.kinematic_dict["pos"][i]>self.HEIGHT:
                    self.kinematic_dict["pos"][i]=self.kinematic_dict["pos"][i]%self.HEIGHT
                elif self.kinematic_dict["pos"][i]<0:
                    self.kinematic_dict["pos"][i]=self.kinematic_dict["pos"][i]%self.HEIGHT + self.HEIGHT
            self.kinematic_dict["pos"][i]+= self.kinematic_dict["vel"][i]
        self.kinematic_dict["ang"] += self.kinematic_dict["ang_vel"]
        if self.lifespan is not None:
            self.age += 1
            if self.age>= self.lifespan:
                return False
            else:
                return True
        if self.is_kinetic:
            for i in range(2):
                self.kinematic_dict["vel"][i]= self.kinematic_dict["vel"][i]*(1-self.kinetic_dict["fr"])
            self.kinematic_dict["ang_vel"] = self.kinematic_dict["ang_vel"]*(1-self.kinetic_dict["fr"])
        
    def add_force(self, acc = 0):
        if acc != 0:
            self.kinetic_dict["acc"] = acc
        front = self.get_front()
        self.update()
        for i in range(2):
            self.kinematic_dict["vel"][i] += front[i]*self.kinetic_dict["acc"]

    def add_torque(self, ang_acc = 0):
        if ang_acc != 0:
            self.kinetic_dict["ang_acc"] = ang_acc
        self.update()
        self.kinematic_dict["ang_vel"] += self.kinetic_dict["ang_acc"]

    def get_radius(self):
        return self.radius
    
    def get_pos(self):
        return self.kinematic_dict["pos"]
    
    def get_angle(self):
        return self.kinematic_dict["ang"]

    def get_vel(self):
        return self.kinematic_dict["vel"]

    def get_friction(self):
        return self.kinetic_dict["fr"]
    
    def get_ang_acc(self):
        return self.kinetic_dict["ang_acc"]

    def get_acc(self):
        return self.kinetic_dict["acc"]

    def set_acc(self, acc):
        self.kinetic_dict["acc"] = acc
    
    def set_ang(self, ang):
        self.kinematic_dict["ang"] = ang

    def set_ang_acc(self, ang_acc):
        self.kinetic_dict["ang_acc"] = ang_acc
    
    def set_pos(self, pos):
        self.kinematic_dict["pos"] = pos 

    def set_vel(self, vel):
        self.kinematic_dict["vel"] = vel

    def set_ang_vel(self, ang_vel):
        self.kinematic_dict["ang_vel"] = ang_vel

    def get_front(self):
        return [Auxiliars.angle_to_vector(self.kinematic_dict["ang"])[0], Auxiliars.angle_to_vector(self.kinematic_dict["ang"])[1]]
    
    def get_right(self):
        return [Auxiliars.angle_to_vector(self.kinematic_dict["ang"]+math.pi/2.0)[0], Auxiliars.angle_to_vector(self.kinematic_dict["ang"]+math.pi/2.0)[1]]


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
        if self.globals_dict["started"]:
            self.pars["soundtrack"].play()        
            
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
        SpriteGroup.process_sprite_group(canvas, self.rock_group)
        self.pars["ship"].collide_ship_sprites(self.rock_group, self.explosion_group, self.pars["explosion_image"], self.pars["explosion_info"])
        SpriteGroup.collide_sprite_sprite(self.rock_group, self.pars["ship"].missile_group, self.explosion_group, self.pars["explosion_image"], self.pars["explosion_info"], self.pars["ship"])
        SpriteGroup.process_sprite_group(canvas, self.rock_group)
        SpriteGroup.process_sprite_group(canvas, self.explosion_group)
        self.pars["ship"].process_missile_group(canvas)
        
        canvas.draw_text("Lives", (40, 40), 18, "White", "sans-serif")
        canvas.draw_text(str(self.pars["ship"].lives), (40, 64), 18, "White", "sans-serif")
        
        canvas.draw_text("Score", (self.globals_dict["WIDTH"] - 80, 40), 18, "White", "sans-serif")
        canvas.draw_text(str(self.pars["ship"].score), (self.globals_dict["WIDTH"] - 80, 64), 18, "White", "sans-serif")
        
        if self.pars["ship"].lives<0:
            self.globals_dict["started"] = False
            self.pars["ship"].lives = self.lives
            self.pars["ship"].score = 0  
            self.rock_group = set([])
            #self.enemy_ships.spawn = True
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

    def start_game(self, frame):
        # register handlers
        frame.set_draw_handler(self.draw)
        frame.set_keydown_handler(self.keydown_hand)
        frame.set_keyup_handler(self.keyup_hand)
        frame.set_mouseclick_handler(self.click)
        timer = simplegui.create_timer(1000.0, self.rock_spawner)
        # get things rolling
        timer.start()
        frame.start()

globals = dict()
p = dict()
missile = dict()
# globals for user interface
globals["WIDTH"] = 800
globals["HEIGHT"] = 600
globals["lives"] = 3
globals["time"] = 0.5
globals["sc_dif"] = 1.0
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
p["debris_info"] = ImageInfo([320, 240], [640, 480])
p["debris_image"] = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
p["nebula_info"] = ImageInfo([400, 300], [800, 600])
p["nebula_image"] = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
p["splash_info"] = ImageInfo([200, 150], [400, 300])
p["splash_image"] = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
p["ship_info"] = ImageInfo([45, 45], [90, 90], 35)
p["ship_image"] = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
p["missile_info"] = ImageInfo([5,5], [10, 10], 3, 50)
p["missile_image"] = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
p["asteroid_info"] = ImageInfo([45, 45], [90, 90], 40)
p["asteroid_image"] = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
p["explosion_info"] = ImageInfo([64, 64], [128, 128], 17, 24, True)
p["explosion_image"] = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
p["soundtrack"] = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
p["missile_sound"] = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
p["missile_sound"].set_volume(0.5)
p["ship_thrust_sound"] = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
p["explosion_sound"] = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# initialize frame
frame = simplegui.create_frame("Asteroids", globals["WIDTH"], globals["HEIGHT"])

p["ship"] = Ship([globals["WIDTH"] / 2, globals["HEIGHT"] / 2], [0, 0], 0, 0, p["ship_image"], p["ship_info"],\
p["missile_image"], p["missile_info"], p["missile_sound"], p["ship_thrust_sound"], globals["WIDTH"], globals["HEIGHT"],True, 0.1, 0.0008, 0.009, 3)
#p["ship"].set_values({"ang_acc" : 0.08, "acc" : 0.1})
#p["a_rock"] = Sprite([globals["WIDTH"]+44, globals["HEIGHT"]+44], [random.randrange(-1,2)*random.random(), random.randrange(-1,2)*random.random()], \
# random.random(), 0.10471976, p["asteroid_image"], p["asteroid_info"], globals["WIDTH"], globals["HEIGHT"])

g = Game(globals, p)
g.start_game(frame)