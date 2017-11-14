from appJar import gui
import re
import os
import threading

EMAIL_REG = r"[^@]+@[^2]+\.[^@]+"

NAME = "Name* "
EMAIL = "Email* "
AGE = "Age     "
HEIGHT = "Height "
WEIGHT = "Weight"

test_complete = False


def listen(email):
    com = '''sshpass -p "embracethetech" ssh ian@70.95.198.60 "./r 7011 > ~/sdInnovations/'''+email+'''.csv"'''
    os.system(com)

def close():
    com = '''sshpass -p "embracethetech" ssh ian@70.95.198.60 "kill_port 7011"'''
    os.system(com)



def press(button):
    if button == "Clear":
        app.clearEntry(NAME)
        app.clearEntry(EMAIL)
        app.clearEntry(AGE)
        app.clearEntry(HEIGHT)
        app.clearEntry(WEIGHT)
    elif button == "End Test":
        test_complete = True
        threading.Thread(target=close).start()
        print("TEST ENDED")
    else:
        name = app.getEntry(NAME)
        email = app.getEntry(EMAIL)
        threading.Thread(target=listen(),args=(email)).start()
        print("TEST RUNNING")


if __name__ == "__main__":
    app = gui("Gait Age Test", "800x500")
    app.setBg("purple")
    app.setFont(20)

    app.setTitle("Embrace HealthWear Demo - SD Innovation Showcase")

    app.addLabelEntry(NAME)
    app.addLabelEntry(EMAIL)

    app.addLabelEntry(AGE)
    app.addLabelEntry(HEIGHT)
    app.addLabelEntry(WEIGHT)

    str_msg = "Fields with * required\n"
    str_msg += "Personal information will not be\n"
    str_msg += "shared or sold and is for research\n"
    str_msg += "purposes only."
    app.addLabel(str_msg)
    
    app.addButtons(["Start Test", "End Test", "Clear"], press)

    app.go()




    
