__author__ = "Adrian Torres"
__version__ = "1.1"
__changelog__ = """
				1.1 - Added GUI for adding raids to the raidlist
					- Removed auto-raid functionality, threads cause memory leaks (C++ would perform better...)
					- Better GUI
				1.0 - Threads finally exit properly (memory leaks)
				"""

from Tkinter import *
import ttk
import time as timelib
import TravianRaider
import threading

## Windows ##

root = Tk()
root.title("Travian Raider")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

## Variables ##

isLogged = False
usr = StringVar()
pwd = StringVar()
srv = StringVar()
srv.set("http://tx3.travian.us/")
troops = []
for i in range(1, 11):
    troops.append([PhotoImage(file="img/t"+str(i)+"_R.gif"),
    			   PhotoImage(file="img/t"+str(i)+"_G.gif"),
    			   PhotoImage(file="img/t"+str(i)+"_T.gif")])
troops.append(PhotoImage(file="img/hero.gif"))
swords = PhotoImage(file="img/swords.gif")
truppen = [StringVar() for i in range(11)]
for e in truppen:
	e.set("0")
x = StringVar()
y = StringVar()

## Widgets ##

tribe = ttk.Combobox(mainframe)
tribe.grid(column=2, row=4, sticky=(W, E))
tribe["state"] = "readonly"
tribe["values"] = ("Roman", "Teuton", "Gaul")

## Entries ##

usr_entry = ttk.Entry(mainframe, width=12, textvariable=usr)
usr_entry.grid(column=2, row=1, sticky=(W, E))

pwd_entry = ttk.Entry(mainframe, width=12, textvariable=pwd, show="*")
pwd_entry.grid(column=2, row=2, sticky=(W, E))

srv_entry = ttk.Entry(mainframe, width=12, textvariable=srv)
srv_entry.grid(column=2, row=3, sticky=(W, E))

t1_entry = ttk.Entry(mainframe, width=3, textvariable=truppen[0])
t1_entry.grid(column=3, row=2, sticky=(W, E))

t2_entry = ttk.Entry(mainframe, width=3, textvariable=truppen[1])
t2_entry.grid(column=3, row=4, sticky=(W, E))

t3_entry = ttk.Entry(mainframe, width=3, textvariable=truppen[2])
t3_entry.grid(column=4, row=2, sticky=(W, E))

t4_entry = ttk.Entry(mainframe, width=3, textvariable=truppen[3])
t4_entry.grid(column=4, row=4, sticky=(W, E))

t5_entry = ttk.Entry(mainframe, width=3, textvariable=truppen[4])
t5_entry.grid(column=5, row=2, sticky=(W, E))

t6_entry = ttk.Entry(mainframe, width=3, textvariable=truppen[5])
t6_entry.grid(column=5, row=4, sticky=(W, E))

t7_entry = ttk.Entry(mainframe, width=3, textvariable=truppen[6])
t7_entry.grid(column=6, row=2, sticky=(W, E))

t8_entry = ttk.Entry(mainframe, width=3, textvariable=truppen[7])
t8_entry.grid(column=6, row=4, sticky=(W, E))

t9_entry = ttk.Entry(mainframe, width=3, textvariable=truppen[8])
t9_entry.grid(column=7, row=2, sticky=(W, E))

t10_entry = ttk.Entry(mainframe, width=3, textvariable=truppen[9])
t10_entry.grid(column=7, row=4, sticky=(W, E))

t11_entry = ttk.Entry(mainframe, width=3, textvariable=truppen[10])
t11_entry.grid(column=8, row=2, sticky=(W, E))

x_entry = ttk.Entry(mainframe, width=3, textvariable=x)
x_entry.grid(column=4, row=5, sticky=(W, E))

y_entry = ttk.Entry(mainframe, width=3, textvariable=y)
y_entry.grid(column=6, row=5, sticky=(W, E))

## Labels ##

t1 = ttk.Label(mainframe)
t1.grid(column=3, row=1, sticky=(W, E))

t2 = ttk.Label(mainframe)
t2.grid(column=3, row=3, sticky=(W, E))

t3 = ttk.Label(mainframe)
t3.grid(column=4, row=1, sticky=(W, E))

t4 = ttk.Label(mainframe)
t4.grid(column=4, row=3, sticky=(W, E))

t5 = ttk.Label(mainframe)
t5.grid(column=5, row=1, sticky=(W, E))

t6 = ttk.Label(mainframe)
t6.grid(column=5, row=3, sticky=(W, E))

t7 = ttk.Label(mainframe)
t7.grid(column=6, row=1, sticky=(W, E))

t8 = ttk.Label(mainframe)
t8.grid(column=6, row=3, sticky=(W, E))

t9 = ttk.Label(mainframe)
t9.grid(column=7, row=1, sticky=(W, E))

t10 = ttk.Label(mainframe)
t10.grid(column=7, row=3, sticky=(W, E))

t11 = ttk.Label(mainframe)
t11.grid(column=8, row=1, sticky=(W, E))

troopLabels = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]

ttk.Label(mainframe, text="X:").grid(column=3, row=5, sticky=(W, E))
ttk.Label(mainframe, text="Y:").grid(column=5, row=5, sticky=(W, E))

ttk.Label(mainframe, text="Username: ").grid(column=1, row=1, sticky=(W, E))
ttk.Label(mainframe, text="Password: ").grid(column=1, row=2, sticky=(W, E))
ttk.Label(mainframe, text="Server URL: ").grid(column=1, row=3, sticky=(W, E))

## Functions ##

def combo(*args):
	try:
		t = tribe.current()
	except:
		pass
	if t == 0:
		"""Romans"""
		for i in range(len(troopLabels)):
			troopLabels[i]['image'] = troops[i][0]
	elif t == 2:
		"""Teutons"""
		for i in range(len(troopLabels)):
			troopLabels[i]['image'] = troops[i][1]
	else:
		"""Gauls"""
		for i in range(len(troopLabels)):
			troopLabels[i]['image'] = troops[i][2]
	t11['image'] = troops[-1]

def login(*args):
	global isLogged
	try:
		USR = usr.get()
		PWD = pwd.get()
		SRV = srv.get()
		isLogged = TravianRaider.login(USR, PWD, SRV)
	except:
		pass

def raid():
	if isLogged:
		TravianRaider.raidGoldless()
	else:
		pass

def addToRaidlist(*args):
	values = [int(i.get()) for i in truppen]
	q = ([4, (int(x.get()), int(y.get()))] + values)
	with open("raidlist.txt", "a") as f:
		f.write(repr(q)+"\n")
			

## Other ##

raiding_thread = threading.Thread(target=raid)
raidIt = lambda *args: raiding_thread.start()

## Buttons ##

ttk.Button(mainframe, text="Log in", command=login).grid(column=2, row=5, sticky=(W, E))
ttk.Button(mainframe, text="Add to raidlist", command=addToRaidlist).grid(column=3, row=6, columnspan=3, sticky=(W, E))
ttk.Button(mainframe, text="Raid!", image=swords, compound="left", command=raidIt).grid(column=6, row=6, columnspan=3, sticky=(W, E))

## Execution ##

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

usr_entry.focus()
tribe.bind("<<ComboboxSelected>>", combo)

root.mainloop()
