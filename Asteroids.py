
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Frame._hide_status = True
    simplegui.Frame._keep_timers = False
import math
import random
from game import Game
from image import ImageInfo
from ship import Ship
from sprite import Sprite

globals = dict()
p = dict()
shipP = dict()
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
shipP["missile_info"] = ImageInfo([5,5], [10, 10], 3, 50)
shipP["missile_image"] = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
p["asteroid_info"] = ImageInfo([45, 45], [90, 90], 40)
p["asteroid_image"] = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
p["explosion_info"] = ImageInfo([64, 64], [128, 128], 17, 24, True)
p["explosion_image"] = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
p["soundtrack"] = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
shipP["missile_sound"] = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
shipP["missile_sound"].set_volume(.5)
shipP["ship_thrust_sound"] = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
p["explosion_sound"] = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# initialize frame
frame = simplegui.create_frame("Asteroids", globals["WIDTH"], globals["HEIGHT"])


p["my_ship"] = Ship([globals["WIDTH"] / 2, globals["HEIGHT"] / 2], [0, 0], p["ship_image"], p["ship_info"], globals["WIDTH"], globals["HEIGHT"], shipP)
p["my_ship"].set_values({"ang_acc" : 0.08, "acc" : 0.1})
#p["a_rock"] = Sprite([globals["WIDTH"]+44, globals["HEIGHT"]+44], [random.randrange(-1,2)*random.random(), random.randrange(-1,2)*random.random()], \
# random.random(), 0.10471976, p["asteroid_image"], p["asteroid_info"], globals["WIDTH"], globals["HEIGHT"])
p["enemy"] = Ship([globals["WIDTH"] / 2, globals["HEIGHT"] / 2], [0, 0], p["ship_image"], p["ship_info"], globals["WIDTH"], globals["HEIGHT"], shipP)
p["enemy_len"] = 5
#p["ranges"] = {"angle" : 6.0, "ang_acc" : 0.02, "acc" : 0.05, "ang_rang" : 30.0, "min_dist" : 120.0, "V" : 2000.0, "T" : 0.99}
#The next values would correspond to a manually set population of 4 individuals with an established fenotype
p["enemy_list"] = [{"angle" : 6.0, "ang_acc" : 0.05, "acc" : 0.08, "ang_rang" : 26.0, "min_dist" : 120.0, "V" : 2000.0, "T" : 0.99},
                    {"angle" : 6.0, "ang_acc" : 0.02, "acc" : 0.04, "ang_rang" : 26.0, "min_dist" : 120.0, "V" : 2000.0, "T" : 0.6},
                    {"angle" : 6.0, "ang_acc" : 0.01, "acc" : 0.06, "ang_rang" : 26.0, "min_dist" : 120.0, "V" : 2000.0, "T" : 0.6},
                    {"angle" : 6.0, "ang_acc" : 0.06, "acc" : 0.02, "ang_rang" : 26.0, "min_dist" : 120.0, "V" : 2000.0, "T" : 0.7}
                    ]
g = Game(globals, p)
g.get_rolling(frame)