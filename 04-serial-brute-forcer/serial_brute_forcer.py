import time


#open the serial connection
#wake up the shell
send_command("")
time.sleep(2)

# Perhaps first I should do a whoami command to see if I am already root. If I am not already root, then I need to start my brute force

send_command("whoami")

# if not root or some kind of administrator then proceed to brute force
response = send_command("whoami")
if b"root" not in response:
    # proceed to brute force


then 
# Load the credential list

credentials = [
    ("admin", "admin"),
    ("admin", "password"),
    ("guest", "password"),
    ("user", ""),
    ("root", "toor"),
    ("root", "password"),
    ("administrator", "password")
]

''' Try each combination of username and password in the credential list
This is an example of why using default IoT passwords is dangerous.
In my case, after interrupting the bootloader of the TP-Link router, I was immediately dropped into a shell, logged as as root.
'''

for username, password in credentials:
    print(f"Trying ->{username},{password}")#attempt to log in with this username and password
    # TODO: replace with real success detection
    #if it worked:
        # print(f"{username}/ {password} worked!")
    #break
    

else:
    print("no valid credentials found")