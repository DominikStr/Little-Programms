import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


""" Defining global variables"""

FACTOR = 1 # standard is 1km, Factor makes the resolution bigger

GRID_DEPTH = 6371  # km
N_DEPTH = 6371 * FACTOR # 

GRID_WIDTH = np.deg2rad(360)    
N_WIDTH = 720 * FACTOR  # 5 km on earth surface

LENGTH = 10




# Getting the PREM modell data and preparing it

PREM = pd.read_csv("PREM500_IDV.csv", header = 1)

#convert to km
PREM['depth[unit="km"]'] = (PREM['radius[unit="m"]']) * 0.001
PREM['Vpv[unit="km/s"]'] = PREM['Vpv[unit="m/s"]']* 0.001

#get rid of the stuff we dont need yet
PREM = PREM.drop(['radius[unit="m"]', 'density[unit="kg/m^3"]', 'Q-kappa[unit=""]',
                  'Q-mu[unit=""]', 'Vph[unit="m/s"]', 'Vph[unit="m/s"]',
                  'eta[unit=""]', 'Vsv[unit="m/s"]', 'Vsh[unit="m/s"]',
                  'Vpv[unit="m/s"]' ], axis = 1)
PREM.drop_duplicates(['depth[unit="km"]'], inplace = True)


#making a linear fitting line

linear_fit = interp1d(PREM['depth[unit="km"]'], PREM['Vpv[unit="km/s"]'], kind = "linear")
#plt.plot(PREM['depth[unit="km"]'], PREM['Vpv[unit="km/s"]'])
#plt.plot(np.linspace(0,6370,6371), linear_fit(np.linspace(0,6370,6371))) #test the fit


# defining a class that represents the earth as a grid

class Grid:
    def __init__(self):
        
        self.r = np.linspace(0, GRID_DEPTH , int((N_DEPTH) +1)) 
        self.theta = np.linspace(0, GRID_WIDTH , int((N_WIDTH) + 1)) 
      
        self.r, self.theta = np.meshgrid(self.r, self.theta)
            
        self.vp = linear_fit(self.r)
            
            
    def plot_grid(self, how):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, polar='True')
        self.ax.grid(False)
        self.ax.spines['polar'].set_visible(False)
        
        if how == "blank":
            self.ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*(6371 - 2883), color='k', linestyle='-')
            self.ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*(6371 - 5154), color='k', linestyle='-')
            self.ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*(6371), color='k', linestyle='-')
            
        else:
            self.pc = self.ax.pcolormesh(self.theta, self.r, self.vp, cmap = "plasma", vmin = min(PREM['Vpv[unit="km/s"]']), 
                                         vmax = max(PREM['Vpv[unit="km/s"]']))
        
            self.fig.colorbar(self.pc)
        
        
        
    def difference_of_two_polar_vektors(self, v1, length, angle):
        """ Angle is measured anticlockwise from the from the r-axis at theta = 0  """
        
        ray_start_theta = v1[0]
        ray_start_r = v1[1]
        
#        print(ray_start_r, ray_start_theta)
        
        ray_end_theta = ray_start_theta + np.arctan2(length* np.sin(angle - ray_start_theta),
                                                   ray_start_r + length * np.cos(angle - ray_start_theta)) 
    
    
        ray_end_r = np.sqrt( ray_start_r**2 + length**2 +
                          2 * ray_start_r * length * np.cos(angle - ray_start_theta))
        
#        print(ray_end_r, ray_end_theta)
        
        d_ray_theta = ray_end_theta - ray_start_theta
        d_ray_r = ray_end_r -ray_start_r
        
#        print(d_ray_r, d_ray_theta)
        
        return [d_ray_theta, d_ray_r], [ray_end_theta, ray_end_r]
    

        
    def get_mean_vp(self, point, angle):
        
        inside = True
        
        all_values_previous = []
        all_values_next = []
        
        Add = np.round(LENGTH * np.cos(angle) )
        #Add = np.ceil(LENGTH * 1/2) 
        
        if Add == 0:
            Add = 1
        
        try:
            for r in np.linspace(point[1], point[1] - Add, int(abs(Add) +1), dtype = int):
                all_values_previous.append(self.vp[int(point[0])][r])
                
            vp_mean_previous = np.mean(all_values_previous)
                
            for r in np.linspace(point[1], point[1] + Add, int(abs(Add) +1), dtype = int):
                all_values_next.append(self.vp[int(point[0])][r])
                
            vp_mean_next = np.mean(all_values_next)
        
        except:
            inside = False
            vp_mean_previous = 0.000001
            vp_mean_next = 0.0000001
            
        
        return vp_mean_previous, vp_mean_next, inside
    
    def get_new_angle(self, prev_vp, new_vp, prev_angle):
        
        reflected = False 
        
        if np.deg2rad(0) <= prev_angle <= np.deg2rad(90):
            if (new_vp/prev_vp)*np.sin(prev_angle) < 1:
                new_angle = np.arcsin( (new_vp/prev_vp)*np.sin(prev_angle) )
            else:
                new_angle = (np.deg2rad(90) - prev_angle) +  np.deg2rad(90)
                
                reflected = True
            
        
        elif np.deg2rad(90) < prev_angle <= np.deg2rad(180):
            
            prev_angle = np.deg2rad(180) - prev_angle
            
            if (new_vp/prev_vp)*np.sin(prev_angle) < 1:
                new_angle = np.arcsin( (new_vp/prev_vp)*np.sin(prev_angle) )
            else:
                new_angle = (np.deg2rad(90) - prev_angle) +  np.deg2rad(90)
                
                reflected = True
                
            
            new_angle = np.deg2rad(180) - new_angle
        
        
        elif np.deg2rad(180) < prev_angle <= np.deg2rad(270):
            
            prev_angle = prev_angle + np.deg2rad(180)
            
            if -1 < (new_vp/prev_vp)*np.sin(prev_angle) < 1:
                new_angle = np.arcsin( (new_vp/prev_vp)*np.sin(prev_angle) )
                
                
            else:
                new_angle = (np.deg2rad(270) - prev_angle) +  np.deg2rad(270)
                reflected = True
                
            
            new_angle = new_angle + np.deg2rad(180)
            
        
        elif np.deg2rad(270) < prev_angle <= np.deg2rad(360):
            
            prev_angle = np.deg2rad(360) - prev_angle
            
            if -1 < (new_vp/prev_vp)*np.sin(prev_angle) < 1:
                new_angle = np.arcsin( (new_vp/prev_vp)*np.sin(prev_angle) )
                
                
            else:
                new_angle = (np.deg2rad(360) - prev_angle) +  np.deg2rad(360)
                reflected = True
                
            
            new_angle = np.deg2rad(360) - prev_angle
               
        
        return new_angle, reflected
        
    def angle_change_while_propagating(self, prev_angle, prev_r, new_r, prev_vp, new_vp):  
        
        new_angle = np.arcsin((prev_r/new_r)* (new_vp/prev_vp) * np.sin(prev_angle))

        return new_angle
    
    
G = Grid()
G.plot_grid("full")

All_Thetas = []
All_R = []


for angle in np.linspace(np.deg2rad(90), np.deg2rad(270), 10005):
    
    R = []
    Theta = []
    
    Depth = 30
    Degree = np.deg2rad(0)
    
    Previous = [0, 6370 - 30] # accounting for degree later on
    
    
    R.append(Previous[1])
    Theta.append(Previous[0])
    
    Prev_Angle = angle
    inside = True
    
    while inside == True:
        
        diff, New = G.difference_of_two_polar_vektors(Previous, LENGTH, Prev_Angle)
        
        vp_previous, vp_next, inside = G.get_mean_vp(New, Prev_Angle)
       
        New_Angle, Reflected = G.get_new_angle( vp_previous, vp_next, Prev_Angle)
        
        
        #prepare for new round
        
        Previous = New
        Prev_Angle = New_Angle

        R.append(Previous[1])
        Theta.append(Previous[0])

    
    for i in range(len(Theta)):
        Theta[i] += Degree 
    
    
    G.ax.plot(Theta, R, color = "k", linewidth = 0.2)
    G.ax.set_theta_zero_location("N")
#    G.ax.set_thetamin(-90)
#    G.ax.set_thetamax(90)
    G.ax.set_rticks([1000,3000,5000])
#    G.ax.set_rmin(5000)

G.fig.show()









