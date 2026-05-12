
#* =================================================================================
#* Small functions
#* =================================================================================
def validate_XXC(user_input):
    if user_input == "XXC":
        print("\n\n== Previous Operation Cancelled. ==\n\n")
        return True
    return False

def get_n_validate_numerical_input(msg="Enter option number: ",range=0):
    if range == 0:
        while True:
            user_input = input(f"{msg}")
            print("\n")
            if user_input == "XXC":
                return "XXC"
            elif user_input == "XSM":
                return "XSM"
            elif not user_input.isnumeric():
                print("Non-Negative 'numerical' value only!\n")
                continue
            else:
                return user_input
    else:
        while True:
            user_input = input(f"{msg}")
            print("\n")
            if user_input == "XXC":
                return "XXC"
            elif user_input == "XSM":
                return "XSM"
            elif not user_input.isnumeric():
                print("Non-Negative 'numerical' value only!\n")
                continue
            elif int(user_input) > range or int(user_input) == 0:
                print(f"Value must be from 1 to {range} only!\n") 
            else:
                return user_input



#* =================================================================================
#* function get user input
#* =================================================================================
def get_id_or_menu_input(menu_range):
    
    while True:
        get_menu_id=None

        try:
            get_menu_id = get_n_validate_numerical_input("Enter option number: ", menu_range)
            if validate_XXC(get_menu_id):
                return 
            get_menu_id = int(get_menu_id)
            return get_menu_id
        except ValueError as e:
            print(f"{e}, Insert number only!\n")
            continue



#* =================================================================================
#* function 
#* =================================================================================
#generate id to make supplement selection easier across multiple functons
#
def generate_id(supplement_dict):
    id_to_name = {}
    count = 1

    for data in supplement_dict:
        id_to_name[count] = data
        count +=1

    return id_to_name
