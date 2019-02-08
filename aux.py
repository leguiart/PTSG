import math

class Auxiliars:
    """
    This class contains helper functions for mathematical convenience
        ...
        Methods
        -------
        static angle_to_vector(ang) 
            return vector value of an angle with respect to the origin
        static dist(p,q)
            return euclidean distance between two points
    """
    @staticmethod
    def angle_to_vector(ang):
        """
        Parameters
        ----------
        ang : float
            angle 
        """
        return [math.cos(ang), math.sin(ang)]

    @staticmethod
    def dist(p,q):
        return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

    @staticmethod
    def merge_two_dicts(x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z