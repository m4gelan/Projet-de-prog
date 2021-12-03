import numpy as np
from numpy import sin, cos, pi, sqrt
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Slider, Button, RadioButtons, EllipseSelector
import os
from netCDF4 import Dataset as netcdf_dataset
from cartopy import config
import cartopy.crs as ccrs
import sys
import fromCtoPy

rayon = 30
print('nouveau dictionnaire', fromCtoPy.simulation(rayon, 2,3))
print('le rayon init', fromCtoPy.rayon_init )

where_is_the_planet = []
sun = 0
ani = 0
e = 0.047
p = 1
z = 0
ani2 = 0
frames = 20       # Number of frames
eof_num=0
fname = os.path.join(config["repo_data_dir"],
                     'netcdf', 'HadISST1_SST_update.nc'
                     )
dataset = netcdf_dataset(fname)
sst = dataset.variables['sst'][0, :, :]
lats = dataset.variables['lat'][:]
lons = dataset.variables['lon'][:]
levels = np.linspace(-60,60,21)

def rho(p,e):
    t = np.arange(0,2*pi, (2*pi)/1000)
    return p/(1+e*cos(t))
nombre_de_planete = 1
def elipse(a,b):
    l = []
    t=np.arange(0, 2*np.pi, 2*np.pi/100)
    l.append(a*np.cos(t))
    l.append(b*np.sin(t))
    return l
def animate_the_planet(list_of_planetes):
    axis_color = 'lightgoldenrodyellow'
    t = np.arange(0.0, 2*pi, (2*pi)/1000)
    global e
    global p
    p_int= list_of_planetes[0]
    e_int = list_of_planetes[1]
    Unity = np.linspace(0,p_int/(1+e_int) + list_of_planetes[2][0],2000)
    [UAI] = ax.plot(Unity, np.zeros(2000), linewidth = 1, color = 'black', linestyle = '--', alpha = 1, label = '1 UAI')
    x1 = rho(p_int,e_int)*cos(t) + list_of_planetes[2][0]
    y1 = rho(p_int,e_int)*sin(t) + list_of_planetes[2][1]
    line, = plt.plot(x1,y1,linewidth = 1, color = 'white', linestyle = '--', alpha = 0.9, label = 'initial elipse of your earth')
    p_ax  = fig.add_axes([0.25, 0.10, 0.65, 0.03])
    p = Slider(p_ax, 'rayon', 0, p_int*5, valinit=p_int)
    e_ax = fig.add_axes([0.25,0.05,0.65,0.03])
    e = Slider(e_ax,'excentricité',0,1,e_int)
    def sliders_on_changed(val):
        line.set_xdata(rho(p.val,e.val)*cos(t)+ list_of_planetes[2][0])
        line.set_ydata(rho(p.val,e.val)*sin(t)+ list_of_planetes[2][1])
        fig.canvas.draw_idle()
    p.on_changed(sliders_on_changed)
    e.on_changed(sliders_on_changed)
    global reset_button
    # Add a button for resetting the parameters
    reset_button_ax = fig.add_axes([0.05, 0.08, 0.1, 0.04])
    reset_button = Button(reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')
    def reset_button_on_clicked(mouse_event):
        p.reset()
        e.reset()
    reset_button.on_clicked(reset_button_on_clicked)
    global animate_button
    animate_button_ax = fig.add_axes([0.05, 0.15,0.1,0.04])
    animate_button = Button(animate_button_ax, 'animate', color = 'olivedrab',hovercolor = '0.975')
    def lets_groove(mouse_event):
        t = np.arange(0.0, 2*pi, (2*pi)/1000)
        #redDot, = ax.plot([(p.val/(1+e.val*cos(0)))*cos(0)], [(p.val/(1+e.val*cos(0)))*sin(0)],'o', color = 'teal')
        redDot, = ax.plot([-200000000], [-200000000],'o', color = 'teal', ms = 7, label = 'earth')
        def animate(i):
            x = rho(p.val,e.val)*cos(t) + list_of_planetes[2][0]
            y = rho(p.val,e.val)*sin(t)+ list_of_planetes[2][1]
            redDot.set_data(x[int(i)],y[int(i)])
            x1 = rho(p.val,e.val)*cos(t) + list_of_planetes[2][0]
            y1 = rho(p.val,e.val)*sin(t) + list_of_planetes[2][1]
            line, = ax.plot(x1,y1,linewidth = 1, color = 'red', linestyle = '--', alpha = 0.9, label = 'trajectory of your earth')
            return redDot, line,
        global ani
        # create animation using the animate() function
        ani = animation.FuncAnimation(fig, animate, frames=np.arange(0.0,len(t),2.5), \
                                              interval=0.01, blit=True, repeat=True)
        ax.legend(loc = 'upper right', fontsize = 'x-small')
        cplt = ax2.contourf(lons, lats, sst, transform=ccrs.PlateCarree(), levels=levels, cmap='RdBu_r')
        #cb = plt.colorbar(ax2.contourf(lons, lats, sst, transform=ccrs.PlateCarree(), levels=levels, cmap='RdBu_r'),fraction=0.02)
        frames = 20
        def init():
            return animate2(0)
        def animate2(frame):
            ax2.cla()
            global sst
            global lons
            global lats
            print(sst)
            levels = np.linspace(-60,60,21)
            cplt = []
            sst = sst + 25*np.sin(0.2*frame)
            cplt = ax2.contourf(lons, lats, sst, transform=ccrs.PlateCarree(), levels=levels, cmap='RdBu_r')
            ax2.coastlines()
            ax2.set_global()
            #cb.set_label(label='I don t know', fontsize=12)
            sst = sst - 25*np.sin(0.2*frame)
            return [cplt]
        #
        global ani2
        ani2 = animation.FuncAnimation(fig2, animate2, frames=200, interval=10, init_func=init, repeat=True)

    animate_button.on_clicked(lets_groove)
    fig.subplots_adjust( bottom=0.25)
    #ax.set_aspect(aspect = 'equal', adjustable = 'datalim')
def remember_where_is_the_planet(x,y,r):
    where_is_the_planet.append(x)
    where_is_the_planet.append(y)
    where_is_the_planet.append(r)
    return where_is_the_planet

def return_rho_and_e(x,y,x2,y2):
    X = max(x,x2)
    x = min(x,x2)
    Y = max(x,x2)
    y = min(y,y2)
    center = [(X+x)/2,(Y+y)/2]
    demi_grand_axe = X - center[0]
    demi_petit_axe = Y - center[1]
    demi_grand_axe = max(demi_grand_axe,demi_petit_axe)
    demi_petit_axe = min(demi_grand_axe,demi_petit_axe)
    print(demi_grand_axe)
    print(demi_petit_axe)
    P = (demi_petit_axe**2)/demi_petit_axe
    e = sqrt(demi_grand_axe**2-demi_petit_axe**2)/demi_grand_axe
    return [P,e,center]

def draw_planet(x,y,x2,y2):
    l = return_rho_and_e(x,y,x2,y2)
    list_of_planetes = remember_where_is_the_planet(l[0],l[1],l[2])
    global ax
    animate_the_planet(list_of_planetes)

def le_click_parfait(eclick, erelease):
    "eclick and erelease are matplotlib events at press and release."
    #print('startposition: (%f, %f)' % (eclick.xdata, eclick.ydata))
    #print('endposition  : (%f, %f)' % (erelease.xdata, erelease.ydata))
    #print('used button  : ', eclick.button)

    #r = 0.005*np.round(np.sqrt((eclick.xdata-erelease.xdata)*(eclick.xdata-erelease.xdata)+(eclick.ydata-erelease.ydata)*(eclick.ydata-erelease.ydata)),2)*100
    xO = np.round((eclick.xdata), 5)
    yO = np.round((eclick.ydata),5)
    x1 = np.round((erelease.xdata), 5)
    y1 = np.round((erelease.ydata),5)
    #plt.plot(xO, yO, marker = 'o', color ='green')
    draw_planet(xO, yO,x1,y1)


def toggle_selector(event):
    #print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.ES.active:
        print('EllipseSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.ES.active:
        print('EllipseSelector activated.')
        toggle_selector.ES.set_active(True)
fig2 = plt.figure(2, figsize = [6,6])
ax2 = plt.axes(projection=ccrs.Robinson(central_longitude=270))
cplt = ax2.contourf(lons, lats, sst, transform=ccrs.PlateCarree(), levels=levels, cmap='RdBu_r')
x = np.arange(100.) / 99
fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.set_facecolor('darkblue')
#ax.plot(x, y)
plt.axis([-1000,1000,-1000,1000])

background =np.random.rand(2000,2000)
stars_x = []
stars_y = []
for i in range(0,len(background)):
    for j in range(0,len(background[i])):
        if background[i][j]>0.9997:
            if (j<900) or (j<1100 and i<900) or (j>1100 and i>1100) or (j>1100) or (j<1100 and i>1100):
                stars_x.append(i-1000)
                stars_y.append(j-1000)
plt.plot([stars_x],[stars_y], 'o', color = 'yellow', ms = 0.5, alpha = 0.7)
sun = plt.Circle((0,0),100, color = 'firebrick', alpha = 1, fill = True)
ax.add_artist(sun)
toggle_selector.ES = EllipseSelector(ax, le_click_parfait, drawtype='line')
fig.canvas.mpl_connect('key_press_event', toggle_selector)
plt.grid(color = 'white', linewidth = 0.2)
plt.show()
