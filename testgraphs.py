import matplotlib.pyplot as plt
import numpy as np

datax=np.linspace(0,2,30)
datax = np.split(datax,3)
del datax[1]
datay = [np.sin(datax[0]),np.sin(datax[1])]
print(datax[0],datay)
plt.plot(datax[0], not datay[0],)
plt.show()