try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Frame._hide_status = True
    simplegui.Frame._keep_timers = False
import random
import math
import numpy as np
from aux import Auxiliars
from sprite import Sprite
from sprite import SpriteGroup
from environment import Environment

# Ship class es sublase de sprite
class Ship(Sprite):
    def __init__(self, pos, vel, image, info, WIDTH, HEIGHT, pars):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        #Poner values en subclase EnemyShip
        self.values = dict()
        self.values["angle"] = 0
        self.angle_vel = 0
        self.values["ang_acc"] = 0
        self.values["acc"] = 0
        self.values["ang_rang"] = None
        self.values["min_dist"] = None
        self.image = image
        self.ship_info = info
        self.image_center = self.ship_info.get_center()
        self.image_size = self.ship_info.get_size()
        self.radius = self.ship_info.get_radius()
        self.key_up= False
        #Poner friccion como atributo en una clase de fisica
        self.fr=.009
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.pars = pars
        self.missile_group = set([])
        #Poner vectores frontales y laterales como atributos de superclase sprite
        self.front = self.get_front()
        self.right = self.get_right()
        self.angle_front = None
        self.angle_right = None

        
    def draw(self,canvas):
        if self.key_up is False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.values["angle"])
        else:
            canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0], self.image_center[1]] , self.image_size , self.pos, self.image_size, self.values["angle"])
    
    def set_values(self, values):
        self.values.update(values)

    def update(self):
        for i in range(2):
            if i==0:
                if self.pos[i]>self.WIDTH:
                    self.pos[i]=self.pos[i]%self.WIDTH
                elif self.pos[i]<0:
                    self.pos[i]=self.pos[i]%self.WIDTH + self.WIDTH
            elif i==1:
                if self.pos[i]>self.HEIGHT:
                    self.pos[i]=self.pos[i]%self.HEIGHT
                elif self.pos[i]<0:
                    self.pos[i]=self.pos[i]%self.HEIGHT + self.HEIGHT
            self.pos[i]+= self.vel[i]
        self.values["angle"] += self.angle_vel
       
        self.front = self.get_front()
        self.right = self.get_right()
        if self.key_up:
            for i in range(2):
                self.vel[i]=self.vel[i]+self.front[i]*self.values["acc"]

        for i in range(2):
            self.vel[i]= (self.vel[i])*(1-self.fr)
        
    def key(self,ang_acc = 0.0, key_up= False):
        if key_up:
            self.angle_vel=0
        else:
            self.angle_vel += ang_acc
        
        
    def thrust(self, key_up= False):
        self.key_up= key_up
        if self.key_up is True:
            self.pars["ship_thrust_sound"].play()
        else:
            self.pars["ship_thrust_sound"].rewind()
    
    def shoot(self):
        self.missile_group.add(Sprite([self.pos[0]+self.radius*Auxiliars.angle_to_vector(self.values["angle"])[0],\
         self.pos[1]+self.radius*Auxiliars.angle_to_vector(self.values["angle"])[1]], \
         [self.vel[0]+(Auxiliars.angle_to_vector(self.values["angle"])[0])*7 , self.vel[1]+(Auxiliars.angle_to_vector(self.values["angle"])[1])*7], \
          0, 0, self.pars["missile_image"], self.pars["missile_info"], self.WIDTH, self.HEIGHT, self.pars["missile_sound"]))

    def process_lifespan_group(self, canvas):
        SpriteGroup.process_lifespan_group(canvas, self.missile_group)
    
    def get_radius(self):
        return self.radius
    
    def get_pos(self):
        return self.pos
    
    def get_front(self):
        return [Auxiliars.angle_to_vector(self.values["angle"])[0], Auxiliars.angle_to_vector(self.values["angle"])[1]]
    
    def get_right(self):
        return [Auxiliars.angle_to_vector(self.values["angle"]+math.pi/2.0)[0], Auxiliars.angle_to_vector(self.values["angle"]+math.pi/2.0)[1]]


class EnemyShips(Ship, SpriteGroup):
    def __init__(self, ship, ranges_dict = None, population = 1, group_values = None):
        self.enemy_group = set([])
        self.ship = ship
        self.population = population
        self.spawn = True
        self.ranges_dict = ranges_dict 
        self.group_values = group_values   
        if self.ranges_dict is not None:
            self.set_rand_values(self.ranges_dict)
        else:
            self.population = len(self.group_values)
        self.spawn_ships()
        self.set_group_values()

    def spawn_ships(self):
        self.enemy_group = set([])
        for i in range(self.population):
            pos = [random.randrange(0, self.ship.WIDTH-44),random.randrange(0, self.ship.HEIGHT-44)]
            a_ship = Ship(pos, [0, 0], self.ship.image, self.ship.ship_info, self.ship.WIDTH, self.ship.HEIGHT, self.ship.pars)
            self.enemy_group.add(a_ship)
    
    def update(self):
        enemy_copy = self.enemy_group.copy()
        for element in enemy_copy:
            element.update()
        self.enemy_group = enemy_copy.copy()

    def set_rand_values(self, ranges_dict):
        self.group_values = [{key : np.random.uniform(0,ranges_dict[key])  for key in ranges_dict} for i in range(self.population)]
        print(self.group_values)

    def set_group_values(self):
        enemy_copy = self.enemy_group.copy()
        i = 0
        for element in enemy_copy:
            element.set_values(self.group_values[i])
            i += 1
        self.enemy_group = enemy_copy.copy()

    def facing(self, enemy, other):
        front = enemy.front
        right = enemy.right
        vec = [(other.pos[0] - enemy.pos[0])/Auxiliars.dist(enemy.pos, other.pos), (other.pos[1] - enemy.pos[1])/Auxiliars.dist(enemy.pos, other.pos)]
        enemy.angle_front, enemy.angle_right = (math.acos(front[0]*vec[0] + front[1]*vec[1])*180.0/math.pi, math.acos(right[0]*vec[0] + right[1]*vec[1])*180.0/math.pi)
        if enemy.angle_front <= enemy.values["ang_rang"]:
            return True
            
    #do differential control
    def enemy_ai(self, player):
        """
        #error de posicion: posicion deseada - posicion actual
        error_x = goal_x - robot_x
        error_y = goal_y - robot_y
        #angulo deseado: angulo del vector de error
        goal_a = np.arctan2(error_y,error_x)
        #error del angulo: angulo deseado - angulo actual
        error_a = goal_a - robot_a
        #nos aseguramos que la rotacion del robot sea la minima hasta el angulo deseado
        if error_a < - M_PI:
            error_a+=2*M_PI
        else if error_a > M_PI:
            error_a-=2*M_PI
        #si la distancia hasta el punto meta es mayor o igual que 0.1 mts calculamos la funcion de velocidad lineal y angular (gaussiana y sigmoide respectivamente)
        if np.sqrt(error_x*error_x + error_y*error_y)>=0.1:
            v_x = Kv * exp(-error_a*error_a/0.5)
            w = Ka * (2/(1 + exp(-error_a/0.5))-1)
        """
        enemy_copy = self.enemy_group.copy()
        for enemy in enemy_copy:
            if self.facing(enemy, player) and Auxiliars.dist(enemy.pos, player.pos) > enemy.values["min_dist"]:
                enemy.thrust(True)

                print("thrust")
            elif self.facing(enemy, player) and Auxiliars.dist(enemy.pos, player.pos) < enemy.values["min_dist"]:
                enemy.thrust()
                enemy.shoot()
                print("not thrust")
            #if self.facing(enemy, player) and np.random.random_sample()<math.exp(-(enemy.values["V"])/enemy.values["T"]):
            #    enemy.key(0.0, True)
            elif not self.facing(enemy, player) and 0.0 <= enemy.angle_right < 90.0:
                enemy.key(enemy.values["ang_acc"])
            elif not self.facing(enemy, player) and 90.0 <= enemy.angle_right <= 180.0:
                enemy.key(-enemy.values["ang_acc"])
            elif self.facing(enemy, player) and Auxiliars.dist(enemy.pos, player.pos) <= enemy.values["min_dist"]:
                enemy.shoot()
                print("Shoot")
        self.enemy_group = enemy_copy.copy()