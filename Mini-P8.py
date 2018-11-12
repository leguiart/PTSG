
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    simplegui.Frame._hide_status = True
    simplegui.Frame._keep_timers = False

import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
flag= False
started = False
sc_dif=1.0

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

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.key_up= False
        self.fr=.009
        self.missile_group = set([])
        
    def draw(self,canvas):
        if self.key_up is False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0], self.image_center[1]] , self.image_size , self.pos, self.image_size, self.angle)
    
    def update(self):
        for i in range(2):
            if i==0:
                if self.pos[i]>WIDTH:
                    self.pos[i]=self.pos[i]%WIDTH
                elif self.pos[i]<0:
                    self.pos[i]=self.pos[i]%WIDTH + WIDTH
            elif i==1:
                if self.pos[i]>HEIGHT:
                    self.pos[i]=self.pos[i]%HEIGHT
                elif self.pos[i]<0:
                    self.pos[i]=self.pos[i]%HEIGHT + HEIGHT
            self.pos[i]+= self.vel[i]
        self.angle += self.angle_vel
       
        if self.key_up:
            vel= angle_to_vector(self.angle)
            for i in range(2):
                self.vel[i]=self.vel[i]+vel[i]*.1

        for i in range(2):
            self.vel[i]= (self.vel[i]/1.0)*(1-self.fr)
        
    def key(self, ang_acc, key_up= False):
        if key_up is True:
            self.angle_vel=0
        self.angle_vel += ang_acc
        
        
    def thrust(self, key_up= False):
        self.key_up= key_up
        if self.key_up is True:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()

    def process_missile_group(self, canvas):
        SpriteGroup.process_sprite_group(canvas, self.missile_group)
        missiles_copy= set([])
        for missile in self.missile_group:
            if missile.update() is False:
                missiles_copy.add(missile)            
        self.missile_group.difference_update(missiles_copy)


    def shoot(self):
        self.missile_group.add(Sprite([self.pos[0]+self.radius*math.cos(self.angle), self.pos[1]+self.radius*math.sin(self.angle)],\
        [self.vel[0] + (angle_to_vector(self.angle)[0])*7 , self.vel[1]+(angle_to_vector(self.angle)[1])*7], 0, 0, missile_image,\
        missile_info, missile_sound))

    def get_radius(self):
        return self.radius
    
    def get_pos(self):
        return self.pos
    
    def get_missile_group():
        return self.missile_group

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + (self.age*self.image_size[0]), self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        for i in range(2):
            if i==0:
                if self.pos[i]>WIDTH:
                    self.pos[i]=self.pos[i]%WIDTH
                elif self.pos[i]<0:
                    self.pos[i]=self.pos[i]%WIDTH + WIDTH
            elif i==1:
                if self.pos[i]>HEIGHT:
                    self.pos[i]=self.pos[i]%HEIGHT
                elif self.pos[i]<0:
                    self.pos[i]=self.pos[i]%HEIGHT + HEIGHT
            self.pos[i]+= self.vel[i]
        self.angle += self.angle_vel
        self.age += 1
        if self.age>= self.lifespan:
            return False
        else:
            return True
            
    def get_radius(self):
        return self.radius
    
    def get_pos(self):
        return self.pos
        
    def collide(self, other_object):
        if dist(other_object.get_pos(), self.get_pos()) <= other_object.get_radius()+self.get_radius():
            return True
        else:
            return False

class SpriteGroup(Sprite):
    @staticmethod
    def process_sprite_group(canvas, group):
        group_copy = group.copy()
        for sprite in group_copy:
            sprite.draw(canvas)
            sprite.update()


# sets
rock_group = set([])
explosion_group = set()
           
def draw(canvas):
    global time, started, lives, rock_group, score, sc_dif
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    if started:
        soundtrack.play()        
        a_rock.draw(canvas)

    # update ship and sprites
    my_ship.update()
    SpriteGroup.process_sprite_group(canvas, rock_group)
    collide_ship_asteroid(rock_group, my_ship)
    collide_proyectile_asteroid(rock_group, my_ship.missile_group)
    SpriteGroup.process_sprite_group(canvas, explosion_group)
    
    canvas.draw_text("Lives", (40, 40), 18, "White", "sans-serif")
    canvas.draw_text(str(lives), (40, 64), 18, "White", "sans-serif")
    
    canvas.draw_text("Score", (WIDTH - 80, 40), 18, "White", "sans-serif")
    canvas.draw_text(str(score), (WIDTH - 80, 64), 18, "White", "sans-serif")
    
    if lives<=0:
        started = False
        lives = 3
        score = 0
        rock_group=set([])
        sc_dif=1.0

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        soundtrack.rewind()

#GOOD
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, sc_dif, explosion_group
    x=0
    for s in rock_group:
        x+=1
    rock_pos=[random.randrange(0, WIDTH-44),random.randrange(0,HEIGHT-44)]
    if score>0:
        if score%5==0:
            explosion_group=set()
            sc_dif+=.2
    rock_vel=[random.randrange(-1,3) * random.random() * sc_dif, random.randrange(-1,3) * random.random() * sc_dif]
    if started and x<12:
        if dist(rock_pos, my_ship.get_pos())> (ship_info.get_radius() + asteroid_info.get_radius())*1.2:
            a_rock = Sprite(rock_pos ,rock_vel, random.random(), 0.10471976, asteroid_image, asteroid_info)
            rock_group.add(a_rock)

def collide_ship_asteroid(group, other_object):
    global lives
    group_copy= set([])
    aux_copy = group.copy()
    for sprite in aux_copy:
        if sprite.collide(other_object) is True:
            group_copy.add(sprite)
            explosion= Sprite(sprite.get_pos(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
            lives-=1
    group.difference_update(group_copy)

def collide_proyectile_asteroid(group1, group2):
    global score
    group1_copy= set([])
    group2_copy= set([])
    aux_copy1 = group1.copy() #Same for this
    aux_copy2 = group2.copy() #And for this
    for element1 in aux_copy1:
        for element2 in aux_copy2:
            if element2.collide(element1) is True:
                group1_copy.add(element1)
                group2_copy.add(element2)
                score+=1
                explosion= Sprite(element1.get_pos(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
                explosion_group.add(explosion)
    group1.difference_update(group1_copy)
    group2.difference_update(group2_copy)
       
def keydown_hand(key):
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust(True)
    if key == simplegui.KEY_MAP['left']:
        acc = -0.08
        my_ship.key(acc)
    elif key == simplegui.KEY_MAP['right']:
        acc = 0.08
        my_ship.key(acc)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def keyup_hand(key): 
    if key== simplegui.KEY_MAP['up']:        
        my_ship.thrust()
    elif simplegui.KEY_MAP.get("left") == key:
        my_ship.key(0.0, True)
    elif simplegui.KEY_MAP.get("right") == key:
        my_ship.key(0.0, True)

# mouseclick handlers that reset UI and conditions whether splash image is drawn        
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH+44,HEIGHT+44], [random.randrange(-1,2)*random.random(), random.randrange(-1,2)*random.random()], random.random(), 0.10471976, asteroid_image, asteroid_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_hand)
frame.set_keyup_handler(keyup_hand)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()