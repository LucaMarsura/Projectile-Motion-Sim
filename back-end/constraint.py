def constrain(variable,low,high):
    if bool(variable):
        variable = float(variable)
        if variable > high or variable < low:
            print(f"regard constraints for {variable}, enter a value between {low} and {high}")
            load_trajectory = False