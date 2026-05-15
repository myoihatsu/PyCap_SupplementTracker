
#* =================================================================================
#* Small functions
#* =================================================================================
def validate_XXC(user_input):
    """Checks if the user input is "XXC" to cancel the operation.

    Args:
        user_input (str): The input from the user.

    Returns:
        bool: True if input is "XXC", False otherwise.
    """
    if user_input == "XXC":
        print("\n\n== Previous Operation Cancelled. ==\n\n")
        return True
    return False

def get_n_validate_numerical_input(msg="Enter option number: ",range=0):
    """Gets and validates a numerical input from the user.

    Args:
        msg (str): The prompt message for the user.
        range (int): The maximum allowed value (inclusive). 0 means no range check.

    Returns:
        str: The validated numerical input or special commands "XXC"/"XSM".
    """
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
    """Gets a menu selection from the user and validates it.

    Args:
        menu_range (int): The number of options in the menu.

    Returns:
        int: The selected menu ID, or None if cancelled.
    """
    
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
    """Generates a mapping of IDs to supplement names for easier selection.

    Args:
        supplement_dict (dict): The dictionary containing supplement data.

    Returns:
        dict: A dictionary mapping integer IDs to supplement names.
    """
    id_to_name = {}
    count = 1

    for data in supplement_dict:
        id_to_name[count] = data
        count +=1

    return id_to_name
