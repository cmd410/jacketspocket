from math import sqrt, floor, ceil, trunc, cos, sin, pi

class Vec3:
    def __eq__(self, other):
        if isinstance(other, Vec3):
            return all([self.x == other.x, self.y == other.y, self.z == other.z])
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')
    
    def distance_to(self, other):
        return sqrt(sum([pow(self.x - other.x, 2),
                         pow(self.y - other.y, 2),
                         pow(self.z - other.z, 2)]))

    def as_dict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}

    @staticmethod
    def from_tuple(t):
        return Vec3(t[0], t[1], t[2])

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

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def dot(self, other):
        return sum([self.x * other.x,
                    self.x * other.x,
                    self.x * other.x])

    def unit(self):
        l = self.length
        Vec3(self.x/l, self.y/l, self.z/l)

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f'Vec3({self.x}, {self.y}, {self.z})'

    def __iter__(self):
        def iterator():
            for i in (self.x, self.y, self.z):
                yield i
        return iterator()

    def __getitem__(self, key):
        return getattr(self, key)

    def __add__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')

    def __sub__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        if isinstance(other, int) or isinstance(other, float):
            return Vec3(self.x * other, self.y * other, self.z * other)
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')

    def __truediv__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        if isinstance(other, int) or isinstance(other, float):
            return Vec3(self.x / other, self.y / other, self.z / other)
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')

    def __floordiv__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x // other.x, self.y // other.y, self.z // other.z)
        if isinstance(other, int) or isinstance(other, float):
            return Vec3(self.x // other, self.y // other, self.z // other)
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')
    
    def __pow__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x ** other.x, self.y ** other.y, self.z ** other.z)
        if isinstance(other, int) or isinstance(other, float):
            return Vec3(self.x ** other, self.y ** other, self.z ** other)
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')

    def __iadd__(self, other):
        if isinstance(other, Vec3): 
            self.x, self,y, self,z = (self.x + other.x, 
                                      self.y + other.y, 
                                      self.z + other.z)
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')

    def __isub__(self, other):
        if isinstance(other, Vec3): 
            self.x, self,y, self,z = (self.x - other.x, 
                                      self.y - other.y, 
                                      self.z - other.z)
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')

    def __imul__(self, other):
        if isinstance(other, Vec3): 
            self.x, self,y, self,z = (self.x * other.x, 
                                      self.y * other.y, 
                                      self.z * other.z)
        if isinstance(other, int) or isinstance(other, float): 
            self.x, self,y, self,z = (self.x * other, 
                                      self.y * other, 
                                      self.z * other)                                                    
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')

    def __itruediv__(self, other):
        if isinstance(other, Vec3): 
            self.x, self,y, self,z = (self.x / other.x, 
                                      self.y / other.y, 
                                      self.z / other.z)
        if isinstance(other, int) or isinstance(other, float): 
            self.x, self,y, self,z = (self.x / other, 
                                      self.y / other, 
                                      self.z / other)                                                    
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')

    def __ifloordiv__(self, other):
        if isinstance(other, Vec3): 
            self.x, self,y, self,z = (self.x // other.x, 
                                      self.y // other.y, 
                                      self.z // other.z)
        if isinstance(other, int) or isinstance(other, float): 
            self.x, self,y, self,z = (self.x // other, 
                                      self.y // other, 
                                      self.z // other)                                                    
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')

    def __ipow__(self, other):
        if isinstance(other, Vec3): 
            self.x, self,y, self,z = (self.x ** other.x, 
                                      self.y ** other.y, 
                                      self.z ** other.z)
        if isinstance(other, int) or isinstance(other, float): 
            self.x, self,y, self,z = (self.x ** other, 
                                      self.y ** other, 
                                      self.z ** other)                                                    
        raise NotImplementedError(f'Unsupported type for operation: {type(other)}')

    def __abs__(self):
        return Vec3(abs(self.x), abs(self.y), abs(self.z))

    def __invert__(self):
        return Vec3(~self.x, ~self.y, ~self.z)

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