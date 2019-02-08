
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Frame._hide_status = True
    simplegui.Frame._keep_timers = False
import math
import random
import numpy as np
from game import Game
from image import ImageInfo
from ship import Ship
from ship import EnemyShip
from ship import EnemyShips
from sprite import Sprite

globals = dict()
p = dict()
missile = dict()
# globals for user interface
globals["WIDTH"] = 1800
globals["HEIGHT"] = 1000
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

p["ship"] = Ship({"pos" : [globals["WIDTH"] / 2, globals["HEIGHT"] / 2],"vel" : [0.5, 0.5], "ang_vel" : 0, "ang" : 0, "image" : p["ship_image"], "info" : p["ship_info"],\
"missile_image" : p["missile_image"], "missile_info" : p["missile_info"], "missile_sound" : p["missile_sound"], "ship_thrust_sound" : p["ship_thrust_sound"], "WIDTH" : globals["WIDTH"], "HEIGHT" : globals["HEIGHT"]}, True, 0.1, 0.0008, 0.009, 10)
#p["ship"].set_values({"ang_acc" : 0.08, "acc" : 0.1})
#p["a_rock"] = Sprite([globals["WIDTH"]+44, globals["HEIGHT"]+44], [random.randrange(-1,2)*random.random(), random.randrange(-1,2)*random.random()], \
# random.random(), 0.10471976, p["asteroid_image"], p["asteroid_info"], globals["WIDTH"], globals["HEIGHT"])

enemy_pars = {"image" : p["ship_image"], "info" : p["ship_info"], "missile_image" : p["missile_image"], "missile_info" : p["missile_info"], \
"missile_sound" : p["missile_sound"], "ship_thrust_sound" : p["ship_thrust_sound"]}
#p["enemy"] = EnemyShip(enemy_pars, p["ship"].get_physics_component().get_pos(),8.0*np.random.randn(5,3), 4.0*np.random.randn(2,6)+2.0)
settings = {"WIDTH" : globals["WIDTH"], "HEIGHT" : globals["HEIGHT"], "ang_vel_median" : 0.01, "ang_vel_std_dev" : 0.1, "ang_median" : 20.0, "ang_std_dev" : 15.0, "v_max" : 5.0, "ang_rang_median" : 30.0, "ang_rang_std_dev" : 15.0, \
"acc_median" : 0.3, "acc_std_dev" : 0.1, "ang_acc_median" : 0.0005, "ang_acc_std_dev" : 0.0001, "fr" : 0.009, "lives" : 3, "wih_median" : 8.0, "wih_std_dev" : 0.0, "who_median" : 2.0, "who_std_dev" : 1.0, "pop_size" : 15, "elitism" : 0.2, "mutate" : 0.3, "hnodes" : 5, "onodes" : 2}

p["settings"] = settings
p["enemy_pars"] = enemy_pars

#p["enemies"] = EnemyShips(settings, enemy_pars)

g = Game(globals, p)
g.start_game(frame)
