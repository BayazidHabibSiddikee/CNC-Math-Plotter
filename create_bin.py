import struct

def export_to_binary(x, y, filename="cnc_path.bin"):
    """Export as binary file for C to read directly"""
    x_list = x.tolist()
    y_list = y.tolist()
    
    with open(filename, 'wb') as f:
        # Write number of points (4 bytes, unsigned int)
        f.write(struct.pack('I', len(x_list)))
        
        # Write x, y pairs (8 bytes each point: 2 floats)
        for xi, yi in zip(x_list, y_list):
            f.write(struct.pack('ff', xi, yi))
    
    print(f"Binary file exported to {filename}")
    print(f"File size: {len(x_list) * 8 + 4} bytes")




#Creating 2d spiral path
import numpy as np
i = input("Insert time interval from 0 to 8*pi eg(800): ")
t = np.linspace(0,10*np.pi, int(i))
x = t * np.cos(t)
y = t * np.sin(t)
points_2d = [(int(x[i]),float(y[i])) for i in range(len(t))]

export_to_binary(x,y)

import matplotlib.pyplot as plt
plt.plot(*points_2d)
plt.show()