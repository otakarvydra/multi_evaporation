   #Imports
   from compound_properties import H20
   from gas_cp_calculation import gas_cp_data
   from gas_cp_calculation import gas_sensible_heat as cP
   from water_boiling_point_calculation import boiling_temp_calc as calc_T
   from water_enthalpy_vap_calculation import heat_vap_calc as calc_latent
   
    #Define the initial conditions of the system 

W_f = 5   #kg/hr
C_f = 5   #wt%
T_f = 25  #deg C

W_S = 10  #kg/hr
T_S = 200 #deg C
P_S = 2.5 #bara

    #Define the pressure of each evaporator

P_all = [1, 0.8, 0.6, 0.4, 0.2] #bara

    #Define empty lists that will then be used to store important parameters 

T_all     = []
W_v_all   = []
C_f_all   = []

    #Engine 

for P in P_all:

    #Evaporator side
    T             = calc_T(P)                                                         #K
    latent_Q      = calc_latent(T - 273.15)                                           #kJ/kg

    #Steam side
    T_cond        = calc_T(P_S)                                                       #K
    latent_Q_steam = calc_latent(T_cond - 273.15)                                      #kJ/kg

    #Energy and material balance
    Q_released      = abs((cP('H20', T_S, T_cond) / 18)) * W_S + W_S * latent_Q_steam  #kJ/hr
    Q_feed_absorbed = W_f * H20[c_p]* (T - T_f)                                       #kJ/hr
    W_v             = (Q_released - Q_feed_absorbed) / latent_Q                       #kg/hr
    W_c             = W_f - W_v                                                       #kg/hr

    #Append important values
    T_all.append(T - 273.15)                                                          #deg C
    W_v_all.append(W_v)                                                               #kg/hr

    #Calculate concentration
    C = 
     
    #Define new variables
    W_f = W_c
    C_f = C
    T_f = T
    W_s = W_v
    T_s = T
    P_s = P


    #Display results