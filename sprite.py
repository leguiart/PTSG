try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Frame._hide_status = True
    simplegui.Frame._keep_timers = False

from aux import Auxiliars
from physics import Physics

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
