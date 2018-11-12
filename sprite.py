try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Frame._hide_status = True
    simplegui.Frame._keep_timers = False

from aux import Auxiliars

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, WIDTH, HEIGHT, sound = None):
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
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
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
        if Auxiliars.dist(other_object.get_pos(), self.get_pos()) <= other_object.get_radius()+self.get_radius():
            return True
        else:
            return False

class SpriteGroup:
    @staticmethod
    def process_sprite_group(canvas, group):
        group_copy = group.copy()
        for sprite in group_copy:
            sprite.draw(canvas)
            sprite.update()
            
    @staticmethod
    def process_lifespan_group(canvas, group):
        if(len(group))>0:
            aux_copy = group.copy()
            group_copy = set([]) 
            for sprite in aux_copy:
                if sprite.update() is False:
                    group_copy.add(sprite)            
            group.difference_update(group_copy)
            aux_copy = group.copy()
            for sprite in aux_copy:
                sprite.draw(canvas)
                sprite.update()
    
    @staticmethod
    def process_groups_of_group(canvas, group):
        group_copy = group.copy() #Make a copy of the group to process in order to avoid set change execution error during the iteration
        for sprite in group_copy:
            SpriteGroup.process_lifespan_group(canvas, sprite.missile_group)

    @staticmethod
    def collide1(group, other_object, explosion_group, globals_dict, par):
        group_copy= set([])
        aux_copy = group.copy() #Same for this
        for sprite in aux_copy:
            if sprite.collide(other_object) is True:
                group_copy.add(sprite)
                explosion= Sprite(sprite.get_pos(), [0,0], 0, 0, par["explosion_image"], par["explosion_info"], \
                 globals_dict["WIDTH"], globals_dict["HEIGHT"] ,par["explosion_sound"])
                explosion_group.add(explosion)
                globals_dict["lives"]-=1
        group.difference_update(group_copy)

    @staticmethod
    def collide2(group1, group2, explosion_group, globals_dict, par):
        group1_copy= set([])
        group2_copy= set([])
        aux_copy1 = group1.copy() #Same for this
        aux_copy2 = group2.copy() #And for this
        for element1 in aux_copy1:
            for element2 in aux_copy2:
                if element2.collide(element1) is True:
                    group1_copy.add(element1)
                    group2_copy.add(element2)
                    globals_dict["score"]+=1
                    explosion= Sprite(element1.get_pos(), [0,0], 0, 0, par["explosion_image"], par["explosion_info"], \
                     globals_dict["WIDTH"], globals_dict["HEIGHT"], par["explosion_sound"])
                    explosion_group.add(explosion)
        group1.difference_update(group1_copy)
        group2.difference_update(group2_copy)

    @staticmethod
    def collide3(group1, group2, explosion_group, globals_dict, par):
        group1_copy= set([])
        group2_copy= set([])
        aux_copy1 = group1.enemy_group.copy() #Same as the things up there
        aux_copy2 = group2.copy() #Same here
        for element1 in aux_copy1:
            for element2 in aux_copy2:
                if element2.collide(element1) is True:
                    group1_copy.add(element1)
                    group2_copy.add(element2)
                    globals_dict["score"]+=1
                    explosion= Sprite(element1.get_pos(), [0,0], 0, 0, par["explosion_image"], par["explosion_info"], \
                     globals_dict["WIDTH"], globals_dict["HEIGHT"], par["explosion_sound"])
                    explosion_group.add(explosion)
                    if globals_dict["score"]>0 and globals_dict["score"]%5==0:
                        group1.spawn = True
        group1.enemy_group.difference_update(group1_copy)
        group2.difference_update(group2_copy)

    @staticmethod
    def collide4(group, player, explosion_group, globals_dict, par):
        for element in group:
            SpriteGroup.collide1(element.missile_group, player, explosion_group, globals_dict, par)