class ImageInfo:
    """
    This class holds all the information related to the images of sprites
        ...
        Attributes
        ----------
        center : int list [2]
            This holds the center coordinates of the image for the sprite
        size : int list [2]
            This holds the size [Width, Height] of the image for the sprite
        radius : int (optional)
            Holds the radius of the sphere collider that will be associated with the sprite
        lifespan : int (optional)
            Holds the lifespan of the sprite, which indicates that upon construction it will exist on the 
            game scene for a certain amount of time
        animated : bool (optional)
            Holds whether the image will be a secuence of images for animation

        Methods
        -------
            get_center()
                Get the center attribute
            get_size()
                Get the size attribute
            get_radius()
                Get the radius attribute
            get_lifespan()
                Get the lifespan attribute
            get_animated()
                Get whetther the sprite will be animated or not

    """
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        """
        Parameters
        ----------
        center : int list [2]
            This holds the center coordinates of the image for the sprite
        size : int list [2]
            This holds the size [Width, Height] of the image for the sprite
        radius : int (optional)
            Holds the radius of the sphere collider that will be associated with the sprite
        lifespan : int (optional)
            Holds the lifespan of the sprite, which indicates that upon construction it will exist on the 
            game scene for a certain amount of time
        animated : bool (optional)
            Holds whether the image will be a secuence of images for animation
        """
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan: #If object is instantiated with lifespan attribute set pointer to instance's lifespan attribute to received attribute
            self.lifespan = lifespan 
        else: #Otherwise set it to infinite
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        """
        Get the center attribute
        """
        return self.center

    def get_size(self):
        """
        Get the size attribute
        """
        return self.size

    def get_radius(self):
        """
        Get the radius attribute
        """
        return self.radius

    def get_lifespan(self):
        """
        Get the lifespan attribute
        """
        return self.lifespan

    def get_animated(self):
        """
        Get the animated attribute
        """
        return self.animated
