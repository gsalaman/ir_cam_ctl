from Tkinter import *
import paho.mqtt.client as mqtt

class Application(Frame):
    def set_client(self, client):
        self.client = client

    def lower_cold_bound(self):
        client.publish("ir_cam_display/set/low_temp", "-")
        print "Lowered cold bound"

    def raise_cold_bound(self):
        client.publish("ir_cam_display/set/low_temp", "+")
        print "Lowered cold bound"

    def lower_hot_bound(self):
        client.publish("ir_cam_display/set/high_temp", "-")
        print "Lowered hot bound"

    def raise_hot_bound(self):
        client.publish("ir_cam_display/set/high_temp", "+")
        print "Raised hot bound"

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(row=3,column=1,columnspan=2)

        self.cold_down = Button(self)
        self.cold_down["text"] = "LowerCold",
        self.cold_down["command"] = self.lower_cold_bound
        self.cold_down.grid(row=2,column=1)

        self.cold_up = Button(self)
        self.cold_up["text"] = "RaiseCold",
        self.cold_up["command"] = self.raise_cold_bound
        self.cold_up.grid(row=1,column=1)

        self.hot_down = Button(self)
        self.hot_down["text"] = "LowerHot",
        self.hot_down["command"] = self.lower_hot_bound
        self.hot_down.grid(row=2,column=2)

        self.hot_up = Button(self)
        self.hot_up["text"] = "RaiseHot",
        self.hot_up["command"] = self.raise_hot_bound
        self.hot_up.grid(row=1,column=2)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

#####################################################

broker_address = "10.0.0.17"
#broker_address = "makerlabPi1"

client = mqtt.Client("ir_ctl_app")
try:
  client.connect(broker_address)
except:
  print "Unable to connect to MQTT broker"
  exit(0)

root = Tk()
root.title("IR Camera Control")
app = Application(master=root)
app.set_client(client)
app.mainloop()
root.destroy()

'''
while True:
  key = getch_noblock()

  if key == 'd':
    client.publish("ir_cam_display/low_temp", "-")
    print "Lowered cold bound"
  elif key == 'f':
    client.publish("ir_cam_display/low_temp", "+")
    print "Raised cold bound"
  elif key == 'j':
    print "Lowered hot bound"
    client.publish("ir_cam_display/high_temp", "-")
  elif key == 'k':
    client.publish("ir_cam_display/high_temp", "+")
    print "Raised hot bound"
  elif key == 'q':
    break;
  elif key == None:
    continue;
  else:  
    print "unknown key: "+key
    print_cmds()
'''
