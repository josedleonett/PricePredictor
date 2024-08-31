# function to print a message in the console that receives a message and have a method to print message type, if is a warning, error, info, etc with a color
def print_console(message_type, message):
    if message_type == "warning":
        print(f"\033[93m{message}\033[0m")
    elif message_type == "success":
        print(f"\033[92m{message}\033[0m")
    elif message_type == "error":
        print(f"\033[91m{message}\033[0m")
    elif message_type == "info":
        print(f"\033[94m{message}\033[0m")
    else:
        print(message)