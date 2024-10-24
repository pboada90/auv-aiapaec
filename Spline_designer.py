import numpy as np
import ezdxf

a = 300
b = 900
c = 200
d = 180

l = a+b+c
n = 2.5

theta = 50
theta = theta * np.pi / 180

x = np.linspace(0, l, 100)
body = np.zeros((len(x), 3))
values =[]
for count, element in enumerate(x):
    if element <= a:
        value = 0.5*d*(1-((element-a)/a)*((element-a)/a))**(1/n)
    if (element <= (a+b)) & (element > a):
        value = d*0.5
    if (element <= l) & (element > (a+b)):
        value = 0.5*d - (3*d/(2*c*c)-np.tan(theta)/c)*(element-a-b)*(element-a-b) + (
            d/(c*c*c)-np.tan(theta)/(c*c))*(element-a-b)*(element-a-b)*(element-a-b)
    body[count] = np.array([x[count], value, 0])

doc=ezdxf.new('R2010')
msp=doc.modelspace()
msp.add_spline(body)
# save the DXF document
doc.saveas("spline50_degrees_c_200.dxf")
