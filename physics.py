
from aux import Auxiliars

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

    def get_ang_vel(self):
        return self.kinematic_dict["ang_vel"]

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
