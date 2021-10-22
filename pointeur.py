import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import EllipseSelector

def onselect(eclick, erelease):
    "eclick and erelease are matplotlib events at press and release."
    print('startposition: (%f, %f)' % (eclick.xdata, eclick.ydata))
    print('endposition  : (%f, %f)' % (erelease.xdata, erelease.ydata))
    print('used button  : ', eclick.button)
    plt.plot(eclick.xdata, erelease.ydata, marker = 'o', color ='green')
    r = np.round(np.sqrt((eclick.xdata-erelease.xdata)*(eclick.xdata-erelease.xdata)+(eclick.ydata-erelease.ydata)*(eclick.ydata-erelease.ydata)),2)*100
    xO = np.round((eclick.xdata+erelease.xdata)/2, 2)*100
    yO = np.round((eclick.ydata+erelease.ydata)/2,2)*100
    xO1 = xO.astype(int)
    yO1 = yO.astype(int)
    r1 = r.astype(int)
    print(xO1-r1,xO1+r1)
    #plt.plot(xO, yO, marker = 'o', color ='red')
    for x in range((xO1-r1),(xO1+r1),10):
        for y in range(yO1-r1,yO1+r1,10):
            dr = x*x + y*y
            if (dr>0 and dr<r*r):
                plt.plot(x/1000, y/1000, marker = 'o', color ='red')

def toggle_selector(event):
    print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.ES.active:
        print('EllipseSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.ES.active:
        print('EllipseSelector activated.')
        toggle_selector.ES.set_active(True)

x = np.arange(100.) / 99
y = np.sin(x)
fig, ax = plt.subplots()
ax.plot(x, y)
plt.axis([-2,2,-2,2])
i=0
while i<8:
    print(i)
    x = onselect
    print(x)
    toggle_selector.ES = EllipseSelector(ax, onselect, drawtype='line')
    fig.canvas.mpl_connect('key_press_event', toggle_selector)
    i+=1
    plt.show()
