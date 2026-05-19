def energy(result_ivelocity,result_gravity,result_iheight,true_mass,result_fvelocity,list_velocity,index):
    result_ike = 1/2 * true_mass * result_ivelocity ** 2
    result_ipe = true_mass * result_gravity * result_iheight
    result_ite = result_ike + result_ipe
    result_fte = 1/2 * true_mass * result_fvelocity ** 2
    result_ted = result_fte - result_ite
    result_pke = 1/2 * true_mass * list_velocity[index] **2
    result_ppe = true_mass * result_gravity * result_maxheight
    result_pte = result_pke + result_ppe
    
    print("\nEnergy Analysis:\n")
    print(f"Initial Total Energy: {round(result_ite,2)} Joules") 
    print(f"(Kintetic Energy: {round(result_ike,2)} J/Gravitational Potential Energy: {round(result_ipe,2)} J)")
    print("Total Energy Dissipated: 0 Joules")
    print(f"\nTotal Energy at Peak Height: {round(result_pte,2)} Joules")
    print(f"(Kinetic Energy {round(result_pke,2)} J/Gravitational Potential Energy: {round(result_ppe,2)} J)")
    print(f"Total Energy Dissipated: {round((result_ite - result_pte),2)} Joules")
    print(f"\nFinal Total Energy: {round(result_fte,2)} Joules")
    print(f"(Kinetic Energy {round(result_fte,2)} J/Gravitational Potential Energy: 0 J)")
    print(f"Total Energy Dissipated: {round((result_ite - result_fte),2)} Joules")