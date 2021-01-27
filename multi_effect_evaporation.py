#Imports
from thermo_functions import water_boiltemp
from thermo_functions import water_vapheat
from thermo_functions import gas_sensheat
from material_properties import Water
   
#Define the initial conditions of the system 
W_f     = 10    #kg/hr
C_f     = 5     #wt%
T_f     = 25    #deg C

W_s_ini = 6.25  #kg/hr
T_s     = 200   #deg C
P_s     = 2.5   #bara

#Define the pressure of each evaporator, this at the same time defines the number of evaporators
P_all = [1, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]  #bara

#Define empty lists that will then be used to store important parameters 
T_all     = []
W_v_all   = []
C_f_all   = []

#Engine set up
W_s     = W_s_ini            #kg/hr
W_salt  = W_f * (C_f / 100)  #kg/hr

#Engine
for P in P_all:

    #Solve the input stream 
    W_f_water = W_f - W_salt                                                                      #kg/hr

    #Evaporator side
    T               = water_boiltemp(P)                                                           #K
    latent_Q        = water_vapheat(T - 273.15)                                                   #kJ/kg

    #Steam side
    T_cond          = water_boiltemp(P_s)                                                         #K
    latent_Q_steam  = water_vapheat(T_cond - 273.15)                                              #kJ/kg

    #Energy and material balance
    Q_released      = abs((gas_sensheat('H20', T_s, T_cond) / 18)) * W_s + W_s * latent_Q_steam   #kJ/hr
    Q_feed_absorbed = W_f * Water.c_v * (T - T_f)                                                 #kJ/hr
    W_v             = (Q_released - Q_feed_absorbed) / latent_Q                                   #kg/hr
    W_c_water       = W_f_water - W_v                                                             #kg/hr

    #Sanity Check
    if W_v <= 0:
        print('No evaporation or negative evaporation at evaporator no. {value}'.format(value =(P_all.index(P) + 1)))
        exit()
    
    if W_v >= W_f_water:
        print('Complete evaporation or over evaporation at evaporator no. {value}'.format(value=(P_all.index(P) +1)))
        exit()
    
    #Calculate concentration                                                                      #%
    C = 100 * W_salt / (W_salt + W_c_water)

    #Append important values
    T_all.append(T - 273.15)                                                                      #deg C
    W_v_all.append(W_v)
    C_f_all.append(C)                                                                             #kg/hr
     
    #Define new variables
    W_f = W_c_water + W_salt
    T_f = T
    W_s = W_v
    T_s = T
    P_s = P

#Final Variable calculation   
steam_econ = sum(W_v_all) / W_s_ini

#Data Output
print('The condensate flowrate is {value} kg/hr'.format(value = W_f))
print('The final concentration is {value} %.'.format(value = C))
print('The steam economy is {value} kg vapour/kg fresh steam'.format(value = steam_econ))
