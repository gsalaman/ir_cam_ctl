from Tkinter import *
import paho.mqtt.client as mqtt

################################################
#  Our application class definition
################################################
class Application(Frame):
    def set_client(self, client):
        self.client = client

    def refresh_cold_bound(self, cold_bound):
        self.cold_bound.set(cold_bound) 
        print " window cold bound:"+cold_bound

    def refresh_hot_bound(self, hot_bound):
        self.hot_bound.set(hot_bound)
        print "window hot bound:"+hot_bound

    def lower_cold_bound(self):
        client.publish("ir_cam_display/set/low_temp", "-")
        print "Lowered cold bound"
        client.publish("ir_cam_display/query/low_temp","")

    def raise_cold_bound(self):
        client.publish("ir_cam_display/set/low_temp", "+")
        print "Lowered cold bound"
        client.publish("ir_cam_display/query/low_temp","")

    def lower_hot_bound(self):
        client.publish("ir_cam_display/set/high_temp", "-")
        print "Lowered hot bound"
        client.publish("ir_cam_display/query/high_temp","")

    def raise_hot_bound(self):
        client.publish("ir_cam_display/set/high_temp", "+")
        print "Raised hot bound"
        client.publish("ir_cam_display/query/high_temp","")

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(row=3,column=1,columnspan=3)

        self.cold_label_text = Label(self, text="Cold Bound:")
        self.cold_label_text.grid(row=2,column=1)
        self.cold_label = Label(self,textvariable=self.cold_bound)
        self.cold_label.grid(row=2,column=2)

        self.hot_label_text = Label(self, text="Hot Bound:")
        self.hot_label_text.grid(row=1,column=1)
        self.hot_label = Label(self,textvariable=self.hot_bound)
        self.hot_label.grid(row=1,column=2)

        self.cold_down = Button(self)
        self.cold_down["text"] = "LowerCold",
        self.cold_down["command"] = self.lower_cold_bound
        self.cold_down.grid(row=2,column=3)

        self.cold_up = Button(self)
        self.cold_up["text"] = "RaiseCold",
        self.cold_up["command"] = self.raise_cold_bound
        self.cold_up.grid(row=2,column=4)

        self.hot_down = Button(self)
        self.hot_down["text"] = "LowerHot",
        self.hot_down["command"] = self.lower_hot_bound
        self.hot_down.grid(row=1,column=3)

        self.hot_up = Button(self)
        self.hot_up["text"] = "RaiseHot",
        self.hot_up["command"] = self.raise_hot_bound
        self.hot_up.grid(row=1,column=4)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.cold_bound = StringVar()
        self.cold_bound.set("?")
        self.hot_bound = StringVar() 
        self.hot_bound.set("?")
        self.pack()
        self.createWidgets()

#####################################################
# Message callback for MQTT
#####################################################
def on_message(client, userdata, message):
  global app

  #print "CALLBACK"

  if message.topic == "ir_cam_display/value/low_temp":
    app.refresh_cold_bound(message.payload)
  elif message.topic == "ir_cam_display/value/high_temp":
    app.refresh_hot_bound(message.payload)
  else:
    print "Unhandled message topic: ",message.topic

#####################################################
# Main code 
#####################################################

root = Tk()
root.title("IR Camera Control")
app = Application(master=root)

broker_address = "10.0.0.17"
#broker_address = "makerlabPi1"

client = mqtt.Client("ir_ctl_app")
client.on_message = on_message
try:
  client.connect(broker_address)
except:
  print "Unable to connect to MQTT broker"
  exit(0)
client.loop_start()
client.subscribe("ir_cam_display/value/#")

client.publish("ir_cam_display/query/low_temp","")
client.publish("ir_cam_display/query/high_temp","")

app.set_client(client)

app.mainloop()
root.destroy()

