import math

class Shape:
    total_number = 0

    def __init__(self):
        self.__area = None
        Shape.total_number += 1

    def calc_area(self):
        raise NotImplementedError("子类必须重写 calc_area 方法")

    def _set_area(self, area_value):
        self.__area = area_value

    def get_area(self):
        if self.__area is None:
            self._calc_area()
        return self.__area
    @staticmethod
    def get_total_number(cls):
        return (f"已经有{Shape.total_number}个数据")

class Circle(Shape):
    def __init__(self,radius):
        super().__init__()
        Circle.__radius = radius

    def _calc_area(self):
        area = math.pi*(Circle.__radius**2)
        self._set_area(area)

class Rectangle(Shape):
    def __init__(self,width,height):
        super().__init__()
        Rectangle.__width = width
        Rectangle.__height = height

    def _calc_area(self):
        area = Rectangle.__width * Rectangle.__height
        self._set_area(area)

circle1 = Circle(1)
print(f"Circle1 的面积为 {circle1.get_area():.2f}")
