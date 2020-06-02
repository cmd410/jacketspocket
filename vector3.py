from math import *
from itertools import product

class Vec3:
    def distance_to(self, other):
        return sqrt(sum([pow(self.x - other.x, 2),
                         pow(self.y - other.y, 2),
                         pow(self.z - other.z, 2)]))

    def as_dict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}

    def as_tuple(self):
        return (self.x, self.y, self.z)

    @staticmethod
    def from_tuple(t):
        return Vec3(t[0], t[1], t[2])

    @staticmethod
    def from_dict(d):
        return Vec3(d['x'], d['y'], d['z'])

    @staticmethod
    def from_yaw(yaw: float):
        z = cos(yaw)
        x = -sin(yaw)
        return Vec3(x, 0, z)

    @property
    def length(self):
        return sqrt(sum([pow(self.x, 2),
                         pow(self.y, 2),
                         pow(self.z, 2)]))

    def increment_neigbours(self):
        for i in product([0, 1, -1], repeat=3):
            vec = Vec3.from_tuple(i) + self
            if vec == self:
                continue
            yield vec

    def dot(self, other):
        return sum([self.x * other.x,
                    self.x * other.x,
                    self.x * other.x])

    def cross(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.y * other.z - self.z * other.y,
                        self.z * other.x - self.x * other.z,
                        self.x * other.y - self.y * other.x)
        return NotImplemented

    def unit(self):
        l = self.length
        Vec3(self.x/l, self.y/l, self.z/l)

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        if isinstance(other, Vec3):
            return all([self.x == other.x, self.y == other.y, self.z == other.z])
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __str__(self):
        return f'Vec3({self.x}, {self.y}, {self.z})'

    def __iter__(self):
        def iterator():
            for i in (self.x, self.y, self.z):
                yield i
        return iterator()

    def __getitem__(self, key):
        if isinstance(key, int): return (self.x, self.y, self.z)[key]
        return getattr(self, key)

    def __add__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        if isinstance(other, int) or isinstance(other, float):
            return Vec3(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        if isinstance(other, int) or isinstance(other, float):
            return Vec3(self.x / other, self.y / other, self.z / other)
        return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x // other.x, self.y // other.y, self.z // other.z)
        if isinstance(other, int) or isinstance(other, float):
            return Vec3(self.x // other, self.y // other, self.z // other)
        return NotImplemented
    
    def __pow__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x ** other.x, self.y ** other.y, self.z ** other.z)
        if isinstance(other, int) or isinstance(other, float):
            return Vec3(self.x ** other, self.y ** other, self.z ** other)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, Vec3):
            return other + self
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, Vec3):
            return other - self
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        if isinstance(other, int) or isinstance(other, float):
            return Vec3(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, Vec3):
            return other / self
        if isinstance(other, int) or isinstance(other, float):
            return Vec3(other / self.x, other / self.y, other / self.z)
        return NotImplemented

    def __rfloordiv__(self, other):
        if isinstance(other, Vec3):
            return other // self
        if isinstance(other, int) or isinstance(other, float):
            return Vec3(other // self.x, other // self.y, other // self.z)
        return NotImplemented
    
    def __rpow__(self, other):
        if isinstance(other, Vec3):
            return other ** self
        if isinstance(other, int) or isinstance(other, float):
            return Vec3(other ** self.x, other ** self.y, other ** self.z)
        return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Vec3): 
            self.x, self,y, self,z = (self.x + other.x, 
                                      self.y + other.y, 
                                      self.z + other.z)
        return NotImplemented

    def __isub__(self, other):
        if isinstance(other, Vec3): 
            self.x, self,y, self,z = (self.x - other.x, 
                                      self.y - other.y, 
                                      self.z - other.z)
        return NotImplemented

    def __imul__(self, other):
        if isinstance(other, Vec3): 
            self.x, self,y, self,z = (self.x * other.x, 
                                      self.y * other.y, 
                                      self.z * other.z)
        if isinstance(other, int) or isinstance(other, float): 
            self.x, self,y, self,z = (self.x * other, 
                                      self.y * other, 
                                      self.z * other)                                                    
        return NotImplemented

    def __itruediv__(self, other):
        if isinstance(other, Vec3): 
            self.x, self,y, self,z = (self.x / other.x, 
                                      self.y / other.y, 
                                      self.z / other.z)
        if isinstance(other, int) or isinstance(other, float): 
            self.x, self,y, self,z = (self.x / other, 
                                      self.y / other, 
                                      self.z / other)                                                    
        return NotImplemented

    def __ifloordiv__(self, other):
        if isinstance(other, Vec3): 
            self.x, self,y, self,z = (self.x // other.x, 
                                      self.y // other.y, 
                                      self.z // other.z)
        if isinstance(other, int) or isinstance(other, float): 
            self.x, self,y, self,z = (self.x // other, 
                                      self.y // other, 
                                      self.z // other)                                                    
        return NotImplemented

    def __ipow__(self, other):
        if isinstance(other, Vec3): 
            self.x, self,y, self,z = (self.x ** other.x, 
                                      self.y ** other.y, 
                                      self.z ** other.z)
        if isinstance(other, int) or isinstance(other, float): 
            self.x, self,y, self,z = (self.x ** other, 
                                      self.y ** other, 
                                      self.z ** other)                                                    
        return NotImplemented

    def __abs__(self):
        return Vec3(abs(self.x), abs(self.y), abs(self.z))

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __round__(self, *args):
        return Vec3(round(self.x, *args),round(self.y, *args),round(self.z, *args))
    
    def __trunc__(self):
        return Vec3(trunc(self.x), trunc(self.y), trunc(self.z))

    def __floor__(self):
        return Vec3(floor(self.x), floor(self.y), floor(self.z))
    
    def __ceil__(self):
        return Vec3(ceil(self.x), ceil(self.y), ceil(self.z))
