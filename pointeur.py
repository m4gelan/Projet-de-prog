import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import EllipseSelector
where_is_the_planet = []
def remember_where_is_the_planet(x,y):
    where_is_the_planet.append(x)
    where_is_the_planet.append(y)
    return where_is_the_planet
def draw_planet(x,y,r):
    suns = []
    list_of_planetes = remember_where_is_the_planet(x,y)
    print(list_of_planetes)
    i=0
    figure, axes = plt.subplots()
    while(i< len(list_of_planetes)):
        if i<2:
            plt.gcf().gca().add_artist(plt.Circle((list_of_planetes[i],list_of_planetes[i+1]), r*2, color ='red'))
        
        if i>=2:
            plt.gcf().gca().add_artist(plt.Circle((list_of_planetes[i],list_of_planetes[i+1]), r*r, color ='green'))

    i+=2
    plt.xlim([-4, 4])
    plt.ylim([-4, 4])
    plt.yticks(np.arange(-4, 4, 0.5))
    plt.xticks(np.arange(-4, 4, 0.5))
    axes.set_aspect(1)
    plt.show()
def onselect(eclick, erelease):
    "eclick and erelease are matplotlib events at press and release."
    print('startposition: (%f, %f)' % (eclick.xdata, eclick.ydata))
    print('endposition  : (%f, %f)' % (erelease.xdata, erelease.ydata))
    print('used button  : ', eclick.button)
    plt.plot(eclick.xdata, erelease.ydata, marker = 'o', color ='green')
    r = 0.01*np.round(np.sqrt((eclick.xdata-erelease.xdata)*(eclick.xdata-erelease.xdata)+(eclick.ydata-erelease.ydata)*(eclick.ydata-erelease.ydata)),2)*100
    xO = np.round((eclick.xdata+erelease.xdata)/2, 2)
    yO = np.round((eclick.ydata+erelease.ydata)/2,2)
    #print(xO-r1,xO1+r1)
    print(r)
    draw_planet(xO, yO,r)

def toggle_selector(event):
    print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.ES.active:
        print('EllipseSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.ES.active:
        print('EllipseSelector activated.')
        toggle_selector.ES.set_active(True)

x = np.arange(100.) / 99

fig, ax = plt.subplots()
#ax.plot(x, y)
plt.axis([-2,2,-2,2])
toggle_selector.ES = EllipseSelector(ax, onselect, drawtype='line')
fig.canvas.mpl_connect('key_press_event', toggle_selector)
plt.show()
