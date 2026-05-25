class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
        

v1 = Vector(5, 12)
v2 = Vector(2, 24)

v3 = v1 + v2
print(v3)