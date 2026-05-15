import json
from functions import *
from time_auto import *
def main():
    """Main function to run the Supplement Tracker application.
    """
    time_check()
    welcome_screen("Fizz")
    display_current_stock()
    while True:
        
        try:
            display_menu()
        except KeyboardInterrupt:
            print("\n\nExiting program... Goodbye!")
            break
    
main()