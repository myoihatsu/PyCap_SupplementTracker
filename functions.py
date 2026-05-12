from helper_functions import *
from load_dump_json import *
from time_auto import *
import json, math


#* =================================================================================
#* function - calculate consumption days left 
#* =================================================================================
def total_consumption_days(current_quantity,dosage):
    if current_quantity == 0:
        return 0
    try:
        return math.floor(current_quantity/dosage)
    except ZeroDivisionError:
        raise ZeroDivisionError("Dosage can't be zero")



#* =================================================================================
#* function - display current stock 
#* =================================================================================
def display_current_stock():

    try:
        stock_data  = load_from_json('data.json')
        if not stock_data:
            print("No stock data available.\n")
            return    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")

    if not stock_data:
        print("No stock data available.\n")
        return
    num = 1
    print("========== Current Stock ==========\n")

    for supp_identifier in stock_data:
        current_supp = stock_data[supp_identifier]

        if current_supp["Type"] in ["Tablet","Capsule","Pill","Sachet","Packet"]:
            quantity_type = "pcs"
        else:
            quantity_type = "ml"
        
        t_c_days = total_consumption_days(current_supp["Current Quantity"],current_supp["Dosage"])

        restock_str = when_to_restock(t_c_days)
        print(num)
        print(f"Supp Name: {supp_identifier}")
        print(f"Current Amount: {current_supp["Current Quantity"]} {quantity_type}")
        print(f"Daiy Dosage: {current_supp["Dosage"]}")
        print(f"Will last for: {t_c_days} days")
        print(f"== ATTENTION: {restock_str}")
        print(f"Remarks: {current_supp["Remarks"]}")
        print("===================================\n")
        num += 1    
    return



#* =================================================================================
#* function - get supplement info to be passed to add_supplement()
#* =================================================================================
def get_supplement_info():
    print("=== Beginning adding new supplement.")
    print("Insert new supplement info. At anypoint, insert exactly XXC to cancel.\n")

    sname,stype,sremarks = "","",""
    sintl_qty,sdosage = 0.0,0.0
    scurrent_qty = 0.0


    sname = str(input("Insert supplement name: "))
    if validate_XXC(sname):
        return
    

    print("\n")
    print("Select supplement type (number only):\n1. Pill/Capsule/Tablet\n2. Liquid(ml)\n3. Sachet/Packet")
    type_selection = get_id_or_menu_input(3)
    if type_selection is None:
        return
    match type_selection:
        case 1:
            stype = "Pill/Capsule/Tablet"
        case 2:
            stype = "Liquid(ml)"
        case 3:
            stype = "Sachet/Packet" 
    

    sremarks = str(input("Insert remarks: "))
    if validate_XXC(sremarks):
        return
    
    print("\n")
    try:
        sintl_qty = (get_n_validate_numerical_input("Insert initial quantity:"))
        if validate_XXC(sintl_qty):
            return
        sintl_qty = float(sintl_qty)
    except ValueError:
        raise ValueError("Value must be numerical only!")
    try:
        sdosage = get_n_validate_numerical_input("Insert dosage (daily): ")
        if validate_XXC(sdosage):
            return
        sdosage = float(sdosage)
    except ValueError:
        raise ValueError("Value must be numerical only!")
    try:
        scurrent_qty = get_n_validate_numerical_input("Insert current quantity (type XSM if same as intial quantity): ")
        if scurrent_qty == "XSM":
            scurrent_qty = sintl_qty
        if validate_XXC(scurrent_qty):
            return
        scurrent_qty = float(scurrent_qty)
    except ValueError:
        raise ValueError("Value must be numerical only!")
    return sname,stype,sintl_qty,sdosage,scurrent_qty,sremarks



#* =================================================================================
#* function - add new Supplements
#* =================================================================================
def add_new_supplement():

    input_result = get_supplement_info()
    if input_result is None:
        return
    
    name,type,intl_qty,dosage,current_qty,remarks = input_result
    
    x_data = load_from_json('data.json')

    if name in x_data:
        print(f"Process aborted, {name} already exist!\n\n")
        return
     
    x_data[name] = {
        "Type": type,
        "Initial Quantity": intl_qty,
        "Current Quantity": current_qty,
        "Dosage": dosage,
        "Remarks": remarks
        }

    ##updating it
    try:
        dump_to_json('data.json',x_data)
        print(f"{name} successfully updated")
        return
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")



#* =================================================================================
#* function - edit existing supplements attribute
#* =================================================================================
def edit_existing_supplement():
    
    dl = load_from_json('data.json')
    display_id = generate_id(dl)

    print("\n")
    print("!!!! Make sure to double check !!!!")
    print("=== Editing =======================\n")

    if dl == {}:
        print("There's not a single supplement to edit, how about adding one.")
        return
    else:
        print("Which of this supplement is to be edited?")
        for id in display_id:
            print(f"{id} : {display_id[id]}")
        selected_id = get_id_or_menu_input(len(display_id))
        if selected_id is None:  # 👈 Add check
            return

    selected_key = display_id[selected_id]
    to_be_edit = dl[selected_key]
    print("!!! Enter XXC at any point to cancel\n")    
    print("Which of these attribute need to be edited?")
    print("1.Type\n2.Initial Quantity\n3.Current Quantity\n4.Dosage\n5.Remarks\n")

    edit_menu_id = get_id_or_menu_input(5)
    att = ""
    if edit_menu_id is None:  # 👈 Add check
        return
    match edit_menu_id:

        case 1:
            att = "Type"
            print(f"Before edit value: {to_be_edit["Type"]}\n")
            print("Select supplement type (number only):\n1. Pill/Capsule/Tablet\n2. Liquid(ml)\n3. Sachet/Packet")
            type_selection = get_id_or_menu_input(3) #XXCed
            if type_selection is None:  # 👈 Add check
                return
            match type_selection:
                case 1:
                    stype = "Pill/Capsule/Tablet"
                case 2:
                    stype = "Liquid(ml)"
                case 3:
                    stype = "Sachet/Packet"
            to_be_edit["Type"] = stype

        case 2:
            att = "Initial quantity"
            print(f"Before edit value: {to_be_edit["Initial Quantity"]}\n")
            try:
                sintl_qty = get_n_validate_numerical_input("Insert initial quantity: ")
                if validate_XXC(sintl_qty):
                    return
                sintl_qty = float(sintl_qty)
            except ValueError:
                raise ValueError("Value must be numerical only!")
            to_be_edit["Initial Quantity"] = sintl_qty

        case 3:
            att = "Current quantity"
            print(f"Before edit value: {to_be_edit["Current Quantity"]}\n")
            try:
                scurrent_qty = get_n_validate_numerical_input("Insert current quantity: ")
                if validate_XXC(scurrent_qty):
                    return
                scurrent_qty = float(scurrent_qty)
            except ValueError:
                raise ValueError("Value must be numerical only!")
            to_be_edit["Current Quantity"] = scurrent_qty

        case 4:
            att = "Dosage"
            print(f"Before edit value: {to_be_edit["Dosage"]}\n")
            try:
                sdosage = get_n_validate_numerical_input("Insert dosage (daily): ")
                if validate_XXC(sdosage):
                    return
                sdosage = float(sdosage)
            except ValueError:
                raise ValueError("Value must be numerical only!")
            to_be_edit["Dosage"] = sdosage
        
        case 5:
            att = "Remarks"
            print(f"Before edit value: {to_be_edit["Remarks"]}\n")
            sremarks = input("Insert remarks: ")
            if validate_XXC(sremarks):
                return
            to_be_edit["Remarks"] = sremarks

    try:
        dump_to_json('data.json',dl)
        print(f"{selected_key}'s {att}successfully updated\n\n")
        
        #temporary, will move to a menu function
        return

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")


     
#* =================================================================================
#* function - correcting_current_qty() for when user missed to consume supplement
#* =================================================================================
def correcting_current_qty():
    
    #connect
    z_data = load_from_json('data.json')
    
    display_id = generate_id(z_data) #dict

    print("\n\n")
    print("=== Going back in time ============")
    print("Which of this supplement(s) you forgot to consume?")
    
    for id in display_id:
        print(f"{id} : {display_id[id]}")
    selected_id = get_id_or_menu_input(len(display_id))
    
    print("How many day(s) you forgot to consume?")
    while True:
        try:
            days_missed = int(input("Enter day(s) missed: "))
            if days_missed == 0:
                print("YOU DIDNT MISSED ANYTHING! Are you sure you're not on drug or drunk?")
                continue
            elif days_missed < 0:
                print("Days missed cannot be negative!")
                continue
            break
        except ValueError as e:
            print(f"{e}, Insert number only!")
            continue

    #//no error checking for supplement name for now,
    #//gonna change to id for identifier later =
    current_key = display_id[selected_id]
    to_be_edit = z_data[current_key]
       
    daily_dosage = to_be_edit["Dosage"]
    missed_dosage = daily_dosage*days_missed

    to_be_edit["Current Quantity"] += missed_dosage

    dump_to_json('data.json',z_data)
    
    print(f"Succesfully added {missed_dosage} (pcs/ml/sachet/packets) to {current_key}\n\n")
    return



#* =================================================================================
#* function - greet and welcome user
# todo: time parameter will be updated later when I integrate time module aka if this time this, then this
#* =================================================================================
def welcome_screen(username,time="Morning"):
    print("=== Welcome =======================")
    print(f"Good {time}, {username}.")
    print("Make sure to be responsible and consistent with your supplement consumption.")
    print("===================================\n\n")



#* =================================================================================
#* function - display a list of menu 
#* =================================================================================
def display_menu():
    print("=== MENU ==========================")
    print("Operational Menu, insert number only:")
    print("1. Add supplement\n2. Edit existing supplement\n3. Delete supplement\n4. Forgot to take supplements (We do a bit of time travelling)\n5. Re-display List\n6. Exit-- Good Bye\n7. Credits\n8. Overwrite date(only if you're prompted to do so and you want to do so)")
    match get_id_or_menu_input(8):
        case 1:
            add_new_supplement()
        case 2:
            edit_existing_supplement()
        case 3:
            delete_supp() #D
        case 4:
            correcting_current_qty() #D
        case 5:
            display_current_stock() #D
        case 6:
            exit() #D
        case 7:
            print("Code entirely by: Fizz(me!), as my first ever non-guided capstone project.")
            print("\n\n")
        case 8:
            overwrite_date()



#* =================================================================================
#* function - delete certain supplement
#* =================================================================================
def delete_supp():
    dl= load_from_json('data.json')
    display_id = generate_id(dl)
    print("=== Delete supplement? ============")
    if dl == {}:
        print("There's nothing to delete")
        return
    else:
        print("Which of this supplement is to be deleted?")
        for id in display_id:
            print(f"{id} : {display_id[id]}")
        selected_id = get_id_or_menu_input(len(display_id))

        print("Are you sure?\n1. Absolutely, Yes\n2. Actually, No.")
        conf = get_id_or_menu_input(2)
        if conf == 1:
            del dl[display_id[selected_id]]
            dump_to_json('data.json',dl)
            print(f"Sucessfully deleted {display_id[selected_id]}")
        else:
            return