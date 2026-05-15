from datetime import datetime, date, timedelta
from load_dump_json import *
from helper_functions import *
import math



#* =================================================================================
#* function - Auto deduct current quantity based on how many day's passed since last
#* logged in
#* =================================================================================
def auto_deduct(days_passed):
    """Automatically deducts supplement quantities based on days passed.

    Args:
        days_passed (int): The number of days to deduct consumption for.
    """
    a_d_data = load_from_json('data.json')

    print("\n")
    print("===================================")
    print("=== Auto-Deducting ================")


    for data in a_d_data:
        current_key = a_d_data[data]
        dosage = a_d_data[data]["Dosage"]
        to_be_deducted = dosage*days_passed
        new_current_quantity =current_key["Current Quantity"] - to_be_deducted
        if new_current_quantity < 0:
            new_current_quantity = 0
        current_key["Current Quantity"] = new_current_quantity
        print(f"{data}'s current quantity deducted by {to_be_deducted}")


    print("===================================")
    print("===================================")
    print("\n")

    try:
        dump_to_json('data.json',a_d_data)
        print(f"Successfully updated new Current Quantity value\n\n")  
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")



#* =================================================================================
#* function - calculate when to restock supplement
#* =================================================================================
def when_to_restock(consumption_days,avg_delivery_time=4):
    """Calculates the estimated date to restock supplements.

    Args:
        consumption_days (int): The number of days current stock will last.
        avg_delivery_time (int, optional): Average days for delivery. Defaults to 4.

    Returns:
        str: A message indicating when to restock.
    """
    today = date.today()
    
    days_to_restock = consumption_days - avg_delivery_time

    if days_to_restock < 0:
        days_to_restock = 0
        to_restock_date_strf = "TODAY"
    else:
        to_restock_date = today + timedelta(days=days_to_restock)
        to_restock_date_strf = to_restock_date.strftime("%Y-%m-%d")

    
    
    return f"You should restock in {days_to_restock} day(s), at {to_restock_date_strf}, based on {avg_delivery_time} days average delivery time + 1 buffer day."



#* =================================================================================
#* function - overwrite date in user_info.json to earlier date
#* =================================================================================
def overwrite_date():
    """Overwrites the last login date in user_info.json based on user input.
    """

    datedata = load_from_json('user_info.json')

    print("!!! Overwriting Last Login Date !!!")
    print("Format MUST be YYYY-MM-DD (e.g. 2024-05-15)")
    print("Insert exactly XXC to cancel.\n")

    while True:
        new_date = input("Insert new Last Login date: ")
        
        if validate_XXC(new_date):
            return

        try:
            #validate format
            datetime.strptime(new_date, "%Y-%m-%d")
            datedata["Last Login"] = new_date
            dump_to_json('user_info.json',datedata)
            print(f"Successfully overwrite date to {new_date}.\n\n")  
            break
        except ValueError:
            print("Invalid date format! Use YYYY-MM-DD only and make sure it's a real date!!\n")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {e}")
            break





#* =================================================================================
#* function - check and compare time from last login to current local time
#* =================================================================================
def time_check():
    """Checks the time since last login and triggers auto-deduction if needed.
    """
    user_data = load_from_json('user_info.json')

    #This is local time
    #?so if local time get changed , how do u know actual now time
    # without using extra library, I think best way is to let user confirm whether to use the
    # new date.. if delta is negative

    # it checks today's date
    # then check last logged in 
    # if last logged in, is previous day(s)
    # calculate differences and auto deduct

    # if last logged in, is ahead of today
    # tell user to fix their time

    today = date.today()
    today_strf = today.strftime("%Y-%m-%d")

    
    last_login_strf = user_data["Last Login"]
    last_login_time_obj = datetime.strptime(last_login_strf,"%Y-%m-%d").date()


    delta = (last_login_time_obj - today).days
    #* so if u deduct date from date , timedelta is created
    #* using .days to get day .seconds to get second value etc....
    #* dont like it but have to refer documentation


    if user_data["Is First Time"] == True:
        user_data["Is First Time"] = False
        user_data["Last Login"] = today_strf


    #* So if last_log > today, it means we're behind
    elif last_login_time_obj > today: 
        print(f"You're behind by {delta} day(s) since the last time you logged in.")
        print(f"Please fix your clock or if today {today_strf} is the correct date,")
        print("fix it by going to menu (8)")


    elif last_login_time_obj < today:
        print(f"It's been {-delta} days since you logged in, updating your supplement consumption")
        auto_deduct(-delta)
        user_data["Last Login"] = today_strf


    else:
        print("Welcome back")
        
        
    try:
        dump_to_json('user_info.json',user_data)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
