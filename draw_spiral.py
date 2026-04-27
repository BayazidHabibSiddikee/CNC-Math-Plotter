import numpy as np
from CNC_simulation import CNC

cnc = CNC(title="CNC Spiral", width=800, height=800,
          x_range=(-30, 30), y_range=(-30, 30),
          draw_delay=0.01)  # Fast for many segments

# Generate spiral
t = np.linspace(0, 8*np.pi, 800)
points = [(t[i]*np.cos(t[i]), t[i]*np.sin(t[i])) for i in range(len(t))]

# Draw it (watch the red dot move!)
for i in range(len(points) - 1):
    cnc.segment(points[i], points[i+1], color='blue', width=2)

cnc.show()