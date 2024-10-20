import numpy as np
import ezdxf

a = 300
b = 800
c = 300
d = 200

l = a+b+c
n = 2.5

alpha = 30
alpha = alpha * np.pi / 180

x = np.linspace(0, l, 100)
body = np.zeros((len(x), 3))
values =[]
for count, element in enumerate(x):
    if element <= a:
        value = 0.5*d*(1-((element-a)/a)*((element-a)/a))**(1/n)
    if (element <= (a+b)) & (element > a):
        value = d*0.5
    if (element <= l) & (element > (a+b)):
        value = 0.5*d - (3*d/(2*c*c)-np.tan(alpha)/c)*(element-a-b)*(element-a-b) + (
            d/(c*c*c)-np.tan(alpha)/(c*c))*(element-a-b)*(element-a-b)*(element-a-b)
        #print(value)
    body[count] = np.array([x[count], value, 0])


doc=ezdxf.new('R2010')
msp=doc.modelspace()
msp.add_spline(body)
# save the DXF document
doc.saveas("spline30_degrees.dxf")
