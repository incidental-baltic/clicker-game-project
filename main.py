import tkinter as tk
import random
import Dictionaries as Dc

global rebirth
rebirth=0


#constant needed for realm
realm_base_threshold = 10**7
index_power_increment = 0.5

#time constants for how often a function happens in milliseconds so divide by 1000 to get in seconds
universal_delay = 1000
income_check_delay = 2500
capitalist_duration = 10000
dollar_spawn_interval = 120000

#constants for legacy and research for upgrades
max_upgrade_level = 10
research_mpc_multiplier = 0.1
research_mps_multiplier = 0.1
legacy_mps_multiplier = 0.2
legacy_mpc_multiplier = 0.2

#list of money requirements for the money achievements
money_achievements = [10**6,10**20,10**100]

#base values needed for calculating price of upgrades in the shop
Shop_cost_multiplier = 1.25
mpc_base_cost = 15
mps_base_cost = 100

#boost given during the 'capitalist' buff after clicking on a dollar
capitalist_boost = 7



count=0
global gambcount;gambcount=0
global toggle
toggle = True
widgets = {}

#function to count how long you have been playing for. hours|minutes|seconds format
def time_count():
    Dc.time['seconds']+=1
    if Dc.time['seconds']==60:
        Dc.time['seconds']=0;Dc.time['minutes']+=1
    if Dc.time['minutes']==60:
        Dc.time['hours']+=1;Dc.time['minutes']=0
window = tk.Tk()
window.geometry("1000x1000")

#function to recalculate how much money you should be getting per click or per second. updates every time mpc or mps should change
def recalculate_mpc_mps(n):
    if n == 'mpc':
        Dc.money_per_click['mpc']= ((Dc.money_per_click['mpc_count'] * Dc.money_per_click['mpc_multiplier'])**Dc.realms['mpc_power'])*((1+(research_mpc_multiplier*Dc.research['research_mpc_upgrade']))*(1+(legacy_mpc_multiplier*Dc.legacy['legacy_mps_upgrade'])))
    if n == 'mps':
        Dc.money_per_second['mps']= ((Dc.money_per_second['mps_count'] * Dc.money_per_second['mps_multiplier'])**Dc.realms['mps_power'])*((1+(research_mps_multiplier*Dc.research['research_mps_upgrade']))*(1+(legacy_mps_multiplier*Dc.legacy['legacy_mps_upgrade'])))


def format_money(value):
    if value < 1e6:
        return (str(int(value)))
    return "{:.2e}".format(value)


#function that will alter whether the stats bar is visible or not
def action():
    global toggle
    if(toggle):
        stats_page_dict['frame'].place(x=0,y=0)
        toggle = False
        stats_page_dict['button'].place(x=200,y=490)
        stats_page_dict['label'].update()
    else:
        stats_page_dict['frame'].place(x=-400,y=0)
        toggle = True
        stats_page_dict['button'].place(x=0,y=490)

#function that will deal with buying money per clicks
def buying_mpc():
    c=0
    if Dc.money['money']>= Dc.money_per_click['mpc_cost']:
        Dc.money['money']-=Dc.money_per_click['mpc_cost']
        Dc.money_per_click['mpc_count']+=1
        c=1
    update_money_widget()
    Dc.money_per_click['mpc_cost'] = int(15*(Shop_cost_multiplier**(Dc.money_per_click['mpc_count']-1)))
    if len(str(int(Dc.money_per_click['mpc_cost'])))> 6:
        Shop_dict['mpc_cost'].configure(text=f"you have {Dc.money_per_click['mpc_count']} shop mpc \n this current upgrade will cost {format_money(Dc.money_per_click['mpc_cost'])}")
        Shop_dict['mpc_cost'].update()
    else:    
        Shop_dict['mpc_cost'].configure(text=f"you have {Dc.money_per_click['mpc_count']} shop mpc \n this current upgrade will cost {int(Dc.money_per_click['mpc_cost'])}")
        Shop_dict['mpc_cost'].update()
    recalculate_mpc_mps('mpc')
    c=0
    upgrade_check()

def update_money_widget():
    display = format_money(Dc.money['money'])
    clicker_dict['money'].configure(text=display)
    Shop_dict['shop money'].configure(text=f"you have {display} to spend")
    clicker_dict['money'].update()
    Shop_dict['shop money'].update()

#function that deals with manual money gain
def money_gain(m):
    if Dc.events['capitalist']== False:
        Dc.money['money'] += m
        Dc.money['total_money_made'] += m    
    if Dc.events['capitalist']== True:
        Dc.money['money']+= m * capitalist_boost    
        Dc.money['total_money_made']+= m * capitalist_boost
    if Dc.money['money'] > Dc.money['peak_money']:
        Dc.money['peak_money'] = Dc.money['money']
    update_money_widget()
    stats_page_dict['label'].configure(
        text = f"Statistics:\nhighest money = {format_money(Dc.money['peak_money'])}\ntotal money = {format_money(Dc.money['total_money_made'])}\nmoney per second ={format_money(Dc.money_per_second['mps'])}\nmoney per click = {format_money(Dc.money_per_click['mpc'])}\ntime={Dc.time['hours']}:{Dc.time['minutes']}:{Dc.time['seconds']}\n achievements completed = {Dc.achievements}"
    )
    
    stats_page_dict['label'].update()

#function to loop the automatic money gain
def loop_amoney():
    money_gain(Dc.money_per_second['mps'])

#function to deal with buying money per second
def buying_mps():
    c=0
    if Dc.money['money']>= Dc.money_per_second['mps_cost']:
        Dc.money['money']-=Dc.money_per_second['mps_cost']
        Dc.money_per_second['mps_count']+=1
        c=1
    update_money_widget()
    Dc.money_per_second['mps_cost'] = int(100*(Shop_cost_multiplier**(Dc.money_per_second['mps_count'])))
    if len(str(int(Dc.money_per_second['mps_cost'])))> 6:
        Shop_dict['mps_cost'].configure(text=f"you have {Dc.money_per_second['mps_count']} shop mps \n this current upgrade will cost {format_money(Dc.money_per_second['mps_cost'])}")
        Shop_dict['mps_cost'].update()
    else:    
        Shop_dict['mps_cost'].configure(text=f"you have {Dc.money_per_second['mps_count']} shop mps \n this current upgrade will cost {int(Dc.money_per_second['mps_cost'])}")
        Shop_dict['mps_cost'].update()
    recalculate_mpc_mps('mps')
    c=0
    upgrade_check()
#functions to deal with the dollar boost/ temporary 7x boost in money gain


def stop_capitalist():
    Dc.events['capitalist']=False

def activate_capitalist_boost():
    widgets["DOLLA"].place(x=-300,y=-3000)
    Dc.events['capitalist']=True 
    window.after(capitalist_duration,stop_capitalist)

def spawn_dolla():
    window.after(dollar_spawn_interval,spawn_dolla)
    Dc.events['dolllar_count']+=1
    if Dc.events['dolllar_count']>=2:widgets["DOLLA"].place(x=random.randrange(1,800),y=random.randrange(1,915))

#function to add in income counter
def income_check():
    temp_money_2=Dc.money['money']
    Dc.money['income']=int((temp_money_2-Dc.money['temp_money_1'])/2.5)
    if len(str(int(Dc.money['income']))) > 6:
        clicker_dict['income'].configure(text=f"current average money per second is {format_money(Dc.money['income'])}")
        clicker_dict['income'].update()
    else:
        clicker_dict['income'].configure(text=f"current average money per second is {int(Dc.money['income'])}")
        clicker_dict['income'].update()
    Dc.money['temp_money_1']=temp_money_2
    window.after(income_check_delay,income_check)

def show_widgets(widget_positions):
    for name, pos in widget_positions.items():
        if name in widgets:
            widgets[name].place(x=pos[0], y=pos[1])


#function to spawn all that is needed at the start of the game

def start_game():
    # Hide all main widgets except the menu
    for widget in window.winfo_children():
        widget.place_forget()
    spawn_dolla()
    income_check()  
    universal_update()



    # Show the clicker/game widgets
    show_widgets({
        "menu": (900, 0),
        'click': (395, 100),
        'money': (500 - ((len(str(int(Dc.money['money']))) * 26) // 2), 175),
        'income': (360, 220),
        'research': (0, 0)
    })
    for item in clicker_dict:
        clicker_dict[item].place(x=clicker_dict_positions[item]["x"],y=clicker_dict_positions[item]["y"])



#function to check when a certain achievement has been reached
def achievement():
    global achievements,gambcount
    if Dc.achievement_flags[0]==False and Dc.money['money'] >= money_achievements[0]:
        Dc.achievement_flags[0]=True
        stats_page_dict['1st_ach'].configure(text="congrats on\n becoming a millionaire")
        stats_page_dict['1st_ach'].update()
        achievements+=1
    if Dc.achievement_flags[1]==False and Dc.money['money'] >= money_achievements[1]:
        Dc.achievement_flags[1]=True
        widgets["2nd_ach"].configure(text="20 zeros is quite a lot")
        widgets["2nd_ach"].update()
        achievements+=1
    if Dc.achievement_flags[2]==False and Dc.money['money'] >= money_achievements[2]:
        Dc.achievement_flags[2]=True
        stats_page_dict['3rd_ach'].configure(text="wow 1 whole googol is crazy")
        stats_page_dict['3rd_ach'].update()
        achievements+=1
    if Dc.achievement_flags[3]==False and gambcount >= 30:
        Dc.achievement_flags[3]=True
        stats_page_dict['4th_ach'].configure(text="more likely to: \n win the lotterry")
        stats_page_dict['4th_ach'].update()
        achievements+=1
    if Dc.achievement_flags[4]==False and gambcount <= -20:
        Dc.achievement_flags[4]=True
        stats_page_dict['5th_ach'].configure(text="more likely to:\n get hit by lightning")
        stats_page_dict['5th_ach'].update()
        achievements+=1

#function for giving boosts to manual money gain after buying the respective upgrade
def upgrade(n):
    for group in Dc.upgrade_data:
        if group['type'] == 'mpc' and n <= len(group['costs']):
            idx = n-1
            if Dc.money['money'] >= group['costs'][idx]:
                Dc.money['money'] -= group['costs'][idx]
                Dc.money_per_click['mpc_multiplier'] *= group['multipliers'][idx]
                widgets[group['widgets'][idx]].place_forget()
                Dc.upgrade_flags['click_bought'][idx] = True  
                recalculate_mpc_mps('mpc')

        elif group['type'] == 'mps' and n > 4:
            idx = n-5
            if Dc.money['money'] >= group['costs'][idx]:
                Dc.money['money'] -= group['costs'][idx]
                Dc.money_per_second['mps_multiplier'] *= group['multipliers'][idx]
                widgets[group['widgets'][idx]].place_forget()
                Dc.upgrade_flags['auto_bought'][idx] = True
                recalculate_mpc_mps('mps')
        



#function to spawn upgrades for money gained from clicks
def upgrade_check():
    global menu_var
    for upg in Dc.upgrade_definitions:
        if upg['type'] == 'click':
            current = Dc.money_per_click['mpc_count']
            active = Dc.upgrade_flags['click_active'][upg['index']]
            bought = Dc.upgrade_flags['click_bought'][upg['index']]
        
        else:
            current = Dc.money_per_second['mps_count']
            active = Dc.upgrade_flags['auto_active'][upg['index']]
            bought = Dc.upgrade_flags['auto_bought'][upg['index']]
        
        if current >= upg['count'] and not active and not bought and menu_var.get() == "Shop":
            widgets[upg['widget']].place(x=600, y=300 + 100 * upg['index'])
            if upg['type'] == 'click':
                Dc.upgrade_flags['click_active'][upg['index']] = True
            else:
                Dc.upgrade_flags['auto_active'][upg['index']] = True

        if menu_var.get() != "Shop" and active and not bought:
            if upg['type'] == 'click':
                Dc.upgrade_flags['click_active'][upg['index']] = False
            else:
                Dc.upgrade_flags['auto_active'][upg['index']] = False

#function to change the size of the money bar to fit in the money count or change to a*10^n notation
def monlen():
    if len(str(int(Dc.money['money']))) < 7:
        clicker_dict['money'].configure(width=len(str(int(Dc.money['money'])))*26)
        clicker_dict['money'].update()
    else: 
        clicker_dict['money'].configure(width=160)
        clicker_dict['money'].update()
    if menu_var.get()=="Clicker" :
        if Dc.money['money'] <= 10**6:
            clicker_dict['money'].place_forget()
            clicker_dict['money'].place(x=500-((len(str(int(Dc.money['money'])))*13)),y=175)
        else: 
            clicker_dict['money'].place_forget()
            clicker_dict['money'].place(x=500-78,y=175)

#functions to deal with the realm
def realm_check(): 
    if not Dc.realms['realm1'] and Dc.money['peak_money']>=realm_base_threshold**(Dc.realms['record']+1):
        if menu_var.get() == "Shop":
            widgets['realm1'].place(x=100,y=500)
def realm_change():
    menu_var.set('realm')
    Dc.realms['realm1']=True

#functions to deal with index based increases on money gain
def mpc_index():
    Dc.realms['mpc_power']+=index_power_increment
    Dc.realms['realm1']=False
    Dc.realms['record']+=1
    menu_var.set("Shop")
    recalculate_mpc_mps('mpc')
def mps_index():
    Dc.realms['record']+=1
    Dc.realms['realm1']=False
    Dc.realms['mps_power']+=index_power_increment
    menu_var.set("Shop")
    recalculate_mpc_mps('mps')

#functions that a needed for the legacy system to work.
def legacy_check():
    if Dc.money['total_money_made']>=Dc.legacy['legacy_price']:
        Dc.legacy['legacy_total']+=1
        Dc.legacy['legacies']+=1
    Dc.legacy['legacy_price']=(10**12)*(2**Dc.legacy['legacy_total'])
    clicker_dict['legacy'].configure(text=f"you have {Dc.legacy['legacies']} legacies available")
    clicker_dict['legacy'].update()

def legacy_world():
    menu_var.set('legacy')
    widgets["menu"].place_forget()
    legacy_dict['legacy_count'].configure(text=f"you have {Dc.legacy['legacies']} legacy points available")
    legacy_dict['legacy_count'].update()

def lupers(n):
    if n==1 and Dc.legacy['legacy_mpc_upgrade_price']<=10:
        if Dc.legacy['legacies']>=Dc.legacy['legacy_mpc_upgrade_price']:
            Dc.legacy['legacies']-=Dc.legacy['legacy_mpc_upgrade_price']
            Dc.legacy['legacy_mps_upgrade']+=1
            Dc.legacy['legacy_mpc_upgrade_price']=Dc.legacy['legacy_mps_upgrade']+1
            if Dc.legacy['legacy_mps_upgrade'] <= 10:
                legacy_dict['legacy upg1'].configure(text=f"you have {Dc.legacy['legacy_mps_upgrade']} of this \n this will cost {Dc.legacy['legacy_mpc_upgrade_price']}\n this gives a {1+(Dc.legacy['legacy_mps_upgrade']/5)}x boost to mpc")
                legacy_dict['legacy upg1'].update()
            if Dc.legacy['legacy_mps_upgrade'] == 10:
                legacy_dict['legacy upg1'].configure(text=f"you have the\n max amount of this\n this gives a 3x boost to mpc")
                legacy_dict['legacy upg1'].update()
    if n==2 and Dc.legacy['legacy_mps_upgrade_price']<=10:
        if Dc.legacy['legacies']>=Dc.legacy['legacy_mps_upgrade_price']:
            Dc.legacy['legacies']-=Dc.legacy['legacy_mps_upgrade_price']
            Dc.legacy['legacy_mps_upgrade']+=1
            Dc.legacy['legacy_mps_upgrade_price']=Dc.legacy['legacy_mps_upgrade']+1
            if Dc.legacy['legacy_mps_upgrade'] <= 10:
                legacy_dict['legacy upg2'].configure(text=f"you have {Dc.legacy['legacy_mps_upgrade']} of this \n this will cost {Dc.legacy['legacy_mps_upgrade_price']}\n this gives a {1+(Dc.legacy['legacy_mps_upgrade']/5)}x boost to mpc")
                legacy_dict['legacy upg2'].update()
            if Dc.legacy['legacy_mps_upgrade'] == 10:
                legacy_dict['legacy upg2'].configure(text=f"you have the\n max amount of this\n this gives a 3x boost to mps")
                legacy_dict['legacy upg2'].update()
    legacy_dict['legacy_count'].configure(text=f"you have {Dc.legacy['legacies']} legacy points available")
    legacy_dict['legacy_count'].update()
    recalculate_mpc_mps('mpc')
    recalculate_mpc_mps('mps')    

#functions needed for the research mechanic and its boosts
def research_check():
    if Dc.money['total_money_made']>=Dc.research['research_price']:
        Dc.research['research_total']+=1
        Dc.research['research']+=1
    Dc.research['research_price']=int((10**4)*(1.5**Dc.research['research_total']))
    clicker_dict['research'].configure(text=f"you have {Dc.research['research']} research available")
    clicker_dict['research'].update()

def research_world():
    global rebirth
    if Dc.research['research']> 0:
        menu_var.set('research')
        rebirth+=1
        widgets["menu"].place_forget()
        research_dict['research_count'].configure(text=f"you have {Dc.research['research']} research points available")
        research_dict['research_count'].update()
    else:

        menu_var.set('Clicker')   

def rupers(n):
    if n==1 and Dc.research['research_mpc_upgrade_price']<=10:
        if Dc.research['research']>=Dc.research['research_mpc_upgrade_price']:
            Dc.research['research']-=Dc.research['research_mpc_upgrade_price']
            Dc.research['research_mpc_upgrade']+=1
            Dc.research['research_mpc_upgrade_price']=Dc.research['research_mpc_upgrade']+1
            if Dc.research['research_mpc_upgrade'] <= 10:
                research_dict['research upg1'].configure(text=f"you have {Dc.research['research_mpc_upgrade']} of this \n this will cost {Dc.research['research_mpc_upgrade_price']}\n this gives a {1+(Dc.research['research_mpc_upgrade']/10)}x boost to mpc")
                research_dict['research upg1'].update()
            if Dc.research['research_mpc_upgrade'] == 10:
                research_dict['research upg1'].configure(text=f"you have the\n max amount of this\n this gives a 2x boost to mpc")
                research_dict['research upg1'].update()
    if n==2 and Dc.research['research_mps_upgrade_price']<=10:
        if Dc.research['research']>=Dc.research['research_mps_upgrade_price']:
            Dc.research['research']-=Dc.research['research_mps_upgrade_price']
            Dc.research['research_mps_upgrade']+=1
            Dc.research['research_mps_upgrade_price']=Dc.research['research_mps_upgrade']+1
            if Dc.research['research_mps_upgrade'] <= 10:
                research_dict['research upg2'].configure(text=f"you have {Dc.research['research_mps_upgrade']} of this \n this will cost {Dc.research['research_mps_upgrade_price']}\n this gives a {1+(Dc.research['research_mps_upgrade']/10)}x boost to mpc")
                research_dict['research upg2'].update()
            if Dc.research['research_mps_upgrade'] == 10:
                research_dict['research upg2'].configure(text=f"you have the\n max amount of this\n this gives a 2x boost to mps")
                research_dict['research upg2'].update()
    research_dict['research_count'].configure(text=f"you have {Dc.research['research']} research points available")
    research_dict['research_count'].update()
    recalculate_mpc_mps('mpc')
    recalculate_mpc_mps('mps')

#function to return from other realms
def returning(place):  
    menu_var.set(place)
    widgets["menu"].place(x=900,y=0)

#GAMBLING
def spin_roulette(colour,bet_amount):
    global gambcount
    if bet_amount <= 0 or Dc.money['money'] < bet_amount:
        roulette_dict['gambmount'].configure(text="Invalid bet")
        return
    Dc.money['money']-= bet_amount
    result = random.randint(1,37)
    if Dc.roulette_options[colour]['check'](result):
        Dc.money['money'] += bet_amount * Dc.roulette_options[colour]['payout']
        gambcount+=1
    else:
        gambcount-=1
    update_money_widget()

def rebirthing():
    Dc.money['money']=0
    Dc.money_per_click['mpc'] = 1
    Dc.money_per_click['mpc_count'] = 1
    Dc.money_per_click['mpc_cost'] = 15
    Dc.money_per_click['mpc_multiplier'] = 1
    Dc.money_per_second['mps']= 0
    Dc.money_per_second['mps_cost'] = 100
    Dc.money_per_second['mps_multiplier'] = 1
    Dc.money_per_second['mps_count'] = 0
    Dc.upgrade_flags = {
    'click_active': [False,False,False,False],
    'click_bought': [False,False,False,False],
    'auto_active': [False,False,False,False],
    'auto_bought': [False,False,False,False],
    }
    research_world()




menu_options = ["Clicker", "Shop","Stats_page","the casino"] 
global menu_var
menu_var = tk.StringVar(window)
menu_var.set("Menu")
start_page = tk.PhotoImage(file="Assets/clicker game.png")
dollar = tk.PhotoImage(file="Assets/dollar.png")
click1 = tk.PhotoImage(file="Assets/click1.png")
click2 = tk.PhotoImage(file="Assets/click2.png")
click3 = tk.PhotoImage(file="Assets/click3.png")
click4 = tk.PhotoImage(file="Assets/click4.png")
auto1= tk.PhotoImage(file="Assets/auto1.png")
auto2= tk.PhotoImage(file="Assets/auto2.png")
auto3= tk.PhotoImage(file="Assets/auto3.png")
auto4= tk.PhotoImage(file="Assets/auto4.png")
warp= tk.PhotoImage(file="Assets/warp hole.png")

pixelVirtual = tk.PhotoImage(width=1, height=1)


legacy_dict = {
    'leg_bg' : tk.Label(window,height=1080,width=1920,background="#d88b1e",image=pixelVirtual),
    'legacy upg1': tk.Button(window,image=pixelVirtual,width=175,height=75,font=('Helvetica', 10),foreground="#000000",background="#C49D49",text=f"you have {Dc.legacy['legacy_mps_upgrade']} of this \n this will cost {Dc.legacy['legacy_mpc_upgrade_price']}\n this gives a {1+(Dc.legacy['legacy_mps_upgrade']/5)}x boost to mpc",compound="center",command=lambda:lupers(1)),
    'legacy upg2': tk.Button(window,image=pixelVirtual,width=175,height=75,font=('Helvetica', 10),foreground="#000000",background="#C49D49",text=f"you have {Dc.legacy['legacy_mps_upgrade']} of this \n this will cost {Dc.legacy['legacy_mps_upgrade_price']}\n this gives a {1+(Dc.legacy['legacy_mps_upgrade']/5)}x boost to mps",compound="center",command=lambda:lupers(2)),
    'legacy_count': tk.Label(window,image=pixelVirtual,width=300,height=75,font=('Helvetica', 10),foreground="#000000",background="#C49D49",text=f"you have {Dc.legacy['legacies']} points available to spend.",compound="center"),
    'research return': tk.Button(window,image=pixelVirtual,width=200,height=100,background="#8C8383",foreground="#000000",font=('Helvetica', 8),text="click to return",compound="center",command=lambda:returning("Clicker"))
}   

legacy_dict_positions = {
    'leg_bg' : {"x":0,"y":0},
    'legacy upg1': {"x":300,"y":500},
    'legacy upg2': {"x":600,"y":500},
    'legacy_count': {"x":400,"y":100},
    'research return': {"x":800,"y":0}
}

research_dict = {
    'frame': tk.Frame(window,height=1080,width=1920,background="#1897BD"),    
    'research_count': tk.Label(window,image=pixelVirtual,width=300,height=75,font=('Helvetica', 10),foreground="#000000",background="#90AEF5",text=f"you have {Dc.research['research']} points available to spend.",compound="center"),
    'research upg1': tk.Button(window,image=pixelVirtual,width=175,height=75,font=('Helvetica', 10),foreground="#000000",background="#90AEF5",text=f"you have {Dc.research['research_mpc_upgrade']} of this \n this will cost {Dc.research['research_mpc_upgrade_price']}\n this gives a {1+(Dc.research['research_mpc_upgrade']/10)}x boost to mpc",compound="center",command=lambda:rupers(1)),
    'research upg2': tk.Button(window,image=pixelVirtual,width=175,height=75,font=('Helvetica', 10),foreground="#000000",background="#90AEF5",text=f"you have {Dc.research['research_mps_upgrade']} of this \n this will cost {Dc.research['research_mps_upgrade_price']}\n this gives a {1+(Dc.research['research_mps_upgrade']/10)}x boost to mps",compound="center",command=lambda:rupers(2)),
    'research return': tk.Button(window,image=pixelVirtual,width=200,height=100,background="#8C8383",foreground="#000000",font=('Helvetica', 8),text="click to return",compound="center",command=lambda:returning("Clicker")),

}

research_dict_positions = {
    'frame': {"x": 0,"y": 0},
    'research_count': {"x":400,"y":100},
    'research upg1': {"x":300,"y":500},
    'research upg2': {"x":600,"y":500},
    'research return': {"x":800,"y":0}
}

#    ['legacy'] = tk.Button(window,image=pixelVirtual,width=250,height=50,font=('Helvetica', 10),foreground="#000000",background="#C49D49",text=f"you have {Dc.legacy['legacies']} legacies available",compound="center",command=lambda:legacy_world()),
#    'legacy' : {"x":0,"y":50},

clicker_dict = {
    'click' : tk.Button(window, height=50,width=200,image=pixelVirtual, borderwidth=10, background="#000000", command= lambda : money_gain(Dc.money_per_click['mpc'])),
    'money':tk.Label(window,image=pixelVirtual,height=50,width=len(str(Dc.money['money']))*26,text=Dc.money['money'],font=('Helvetica', 30),foreground="#000000",fg="#000000", background="#FFFFFF", compound='center'),
    'income': tk.Label(window, text= f"current average money per second is {int(Dc.money['income'])}",height=50,width=300,font=('Helvetica', 10),foreground="#000000",fg="#000000", background="#FFFFFF", compound='center',image=pixelVirtual),
    'research': tk.Button(window,image=pixelVirtual,width=250,height=50,font=('Helvetica', 10),foreground="#000000",background="#69789B",text=f"you have {Dc.research['research']} research points available",compound="center",command=lambda:menu_var.set('rebirth confirmation'))
}

clicker_dict_positions = {
    'click': {"x":395,"y": 100},
    'money': {"x":500 - ((len(str(int(Dc.money['money']))) * 26) // 2),"y": 175},
    'income': {"x":360,"y": 220},                
    'research': {"x":0,"y": 0}
}

#clicker_dict_positions['legacy'] = {"x":0,"y":50}

Shop_dict = {
    'upgrades': tk.Label(window,image = pixelVirtual,height=1000,width=400,background="#878383",foreground="#000000"),
    'mps': tk.Button(window, height=50,width=200,image=pixelVirtual, borderwidth=10, background="#000000", command= lambda : buying_mps()),
    'mps_cost': tk.Label(window,image=pixelVirtual,height=50,width=400,text=f"you have {Dc.money_per_second['mps_count']} shop mps \n this current upgrade will cost {int(Dc.money_per_second['mps_cost'])}",font=('Helvetica', 10),foreground="#000000",fg="#000000", background="#FFFFFF", compound='center'),
    'mpc': tk.Button(window, text=Dc.money_per_click['mpc_cost'],image=pixelVirtual,height=50,width=200,borderwidth=10,font=('Helvetica',30),background="#000000", command= lambda :buying_mpc()),
    'mpc_cost':tk.Label(window,image=pixelVirtual,height=50,width=400,text=f"you have {Dc.money_per_click['mpc_count']} shop mpc \n this current upgrade will cost {int(Dc.money_per_click['mpc_cost'])}",font=('Helvetica', 10),foreground="#000000",fg="#000000", background="#FFFFFF", compound='center'),
    'shop money': tk.Label(window,image=pixelVirtual,width=200,height=75,background="#ffffff",foreground="#000000",text=f"you have {int(Dc.money['money'])} to spend",compound="center",font=('Helvetica', 10))
}

shop_dict_positions = {
    'upgrades': {"x":600,"y":0},
    'mps' : {"x":600,"y":175},
    'mps_cost' : {"x":600,"y":125},
    'mpc' : {"x":600,"y":50},
    'mpc_cost' : {"x":600,"y":00},
    'shop money' : {"x":0,"y":0}
}

realm_dict = {
    'mpc_realm': tk.Button(window,image=pixelVirtual,width=200,height=100,font=('Helvetica', 10),foreground="#000000",background="#AE9F9F",text="click to incease click index",compound= "center",command=lambda:mpc_index()),
    'mps_realm': tk.Button(window,image=pixelVirtual,width=200,height=100,font=('Helvetica', 10),foreground="#000000",background="#AE9F9F",text="click to incease time index",compound= "center",command=lambda:mps_index())
}

realm_dict_positions = {
    'mpc_realm': {"x":100,"y":400},
    'mpc_realm': {"x":700,"y":400}
}


widgets['frame'] = tk.Frame(window, height=1000, width=200, background="#000000")
stats_page_dict = {
    'button': tk.Button(window, text="hello", height=20, width=20, image=pixelVirtual, borderwidth=10, background="#000000", command = action),
    'frame': tk.Frame(window, height=1000, width=200, background="#000000"),
    'label':  tk.Label(widgets['frame'], text =f"Statistics:\nhighest money = {Dc.money['peak_money']}\ntotal money generated = {Dc.money['total_money_made']}\nmoney per second = {Dc.money_per_second['mps']}\nmoney per click = {Dc.money_per_click['mpc']}\ntime={Dc.time['hours']}:{Dc.time['minutes']}:{Dc.time['seconds']}\n achievements completed = {Dc.achievements}", foreground="#FFFFFF", background="#000000",font=('Helvetica', 10)),
    '1st_ach': tk.Label(window,image = pixelVirtual,height=100,width=200,background="#ffffff",foreground="#000000",text="achievement not achieved",compound = "center",font=('Helvetica', 10)),
    '2nd_ach':tk.Label(window,image = pixelVirtual,height=100,width=200,background="#ffffff",foreground="#000000",text="achievement not achieved",compound = "center",font=('Helvetica', 10)),
    '3rd_ach': tk.Label(window,image = pixelVirtual,height=100,width=200,background="#ffffff",foreground="#000000",text="achievement not achieved",compound = "center",font=('Helvetica', 10)),
    '4th_ach': tk.Label(window,image = pixelVirtual,height=100,width=200,background="#ffffff",foreground="#000000",text="achievement not achieved",compound = "center",font=('Helvetica', 10)),
    '5th_ach': tk.Label(window,image = pixelVirtual,height=100,width=200,background="#ffffff",foreground="#000000",text="achievement not achieved",compound = "center",font=('Helvetica', 10))
}

stats_page_dict_positions = {
    'button': {"x":0,"y":475},
    'frame': {"x":-400,"y":0},
    'label': {"x":0,"y":0},
    '1st_ach': {"x":200,"y":0},
    '2nd_ach': {"x":400,"y":0},
    '3rd_ach': {"x":600,"y":0},
    '4th_ach': {"x":200,"y":100},
    '5th_ach': {"x":400,"y":100}
}

roulette_dict = {
    'gambling background': tk.Label(window,height=1080,width=1920,background="#467F11",image =pixelVirtual),
    'all in on green': tk.Button(window,image=pixelVirtual,background = "#00ff00",width=200,height=50,command= lambda: spin_roulette('green',Dc.roulette_options['bet_amount'])),
    'all in on red': tk.Button(window,image=pixelVirtual,background = "#ff0000",width=200,height=50,command= lambda: spin_roulette('red',Dc.roulette_options['bet_amount'])),
    'all in on black': tk.Button(window,image=pixelVirtual,background = "#000000",width=200,height=50,command= lambda: spin_roulette('black',Dc.roulette_options['bet_amount'])),
    'return to casino': tk.Button(window,image=pixelVirtual,width=200,height=100,background="#8C8383",foreground="#000000",font=('Helvetica', 10),text="click to return",compound="center",command=lambda:returning("the casino")),
    'gambmon': tk.Text(window,height=1,width=20,background="#ffffff",foreground="#000000",font=('Helvetica', 20)),
    'gambler set': tk.Button(window,image=pixelVirtual,height=100,width=100,background="#ffffff",foreground="#000000",compound="center",font=('Helvetica', 12),text="click to set new betting amount",command=lambda:checkifnumber()),
    'gambmount': tk.Label(window,image=pixelVirtual,height=75,width=225,background="#ffffff",foreground="#000000",font=('Helvetica', 12),compound="center",text=f"you are currently betting {Dc.roulette_options['bet_amount']}")
}


roulette_dict_positions = {
    'gambling background': {"x":0,"y":0},
    'all in on green': {"x":0,"y":100},
    'all in on red' : {"x":0,"y":50},
    'all in on black' : {"x":0,"y":0},
    'return to casino': {"x":800,"y":0},
    'gambmon': {"x":300,"y":100},
    'gambler set': {"x":350,"y":150},
    'gambmount' : {"x":350,"y":250}
}


widgets["menu"] = tk.OptionMenu(window, menu_var ,*menu_options)
widgets["Start_page"] = tk.Label(window,image=start_page)
widgets["start_button"] = tk.Button(window,image=pixelVirtual,height=150,width=700,background="#000000",foreground="#ffffff",text="CLICK TO START",compound="center",font=('Helvetica', 60),command = lambda: start_game())
widgets['click 10'] = tk.Button(window,image=click1,command=lambda: upgrade(1))
widgets['click 25'] = tk.Button(window,image=click2,command=lambda: upgrade(2))
widgets['click 50'] = tk.Button(window,image=click3,command=lambda: upgrade(3))
widgets['click 100'] = tk.Button(window,image=click4,command=lambda: upgrade(4))
widgets['auto 10'] = tk.Button(window,image=auto1,command=lambda: upgrade(5))
widgets['auto 25'] = tk.Button(window,image=auto2,command=lambda: upgrade(6))
widgets['auto 50'] = tk.Button(window,image=auto3,command=lambda: upgrade(7))
widgets['auto 100'] = tk.Button(window,image=auto4,command=lambda: upgrade(8))
widgets["DOLLA"] = tk.Button(window,image=dollar,background="#000000",command=lambda: activate_capitalist_boost())
widgets['realm1'] = tk.Button(window,image=warp,command=lambda:realm_change())
widgets["roulette"] = tk.Button(window,image=pixelVirtual,text="roulette",background="#ffffff",foreground="#000000",borderwidth=10,font=('Helvetica', 30),height=50,width=200, compound='center',command = lambda:start_roulette())
widgets["confirmation"] = tk.Button(window,image=pixelVirtual,text=f"confirm rebirth \n you will recieve {Dc.research['research']} points",background="#ffffff",foreground="#000000",borderwidth=10,font=('Helvetica',20),height=100,width=400,compound='center',command= lambda:rebirthing())

def checkifnumber():
    x=roulette_dict['gambmon'].get("1.0","end")
    if int(x) >1:
        roulette_dict['gambmount'].configure(text=f"you are currently betting {Dc.roulette_options['bet_amount']}")
        roulette_dict['gambmount'].update()
        Dc.roulette_options['bet_amount']=int(x)
    else:
        roulette_dict['gambmount'].configure(text="enter a valid amount")
        roulette_dict['gambmount'].update()

def change_menu(var, index, mode):
    # Hide all widgets first except menu
    for widget in window.winfo_children():
        widget.place_forget()
    widgets["menu"].place(x=900,y=0)
        
    if menu_var.get() == "Shop":
        for item in Shop_dict:
            Shop_dict[item].place(x=shop_dict_positions[item]["x"],y=shop_dict_positions[item]["y"])

    elif menu_var.get() == "Stats_page":

        for item in stats_page_dict:
            stats_page_dict[item].place(x=stats_page_dict_positions[item]["x"],y=stats_page_dict_positions[item]["y"])

    elif menu_var.get() == "Clicker":

        for item in clicker_dict:
            clicker_dict[item].place(x=clicker_dict_positions[item]["x"],y=clicker_dict_positions[item]["y"])

    elif menu_var.get() == "the casino":

        clicker_dict['money'].place(x=0,y=0)
        show_widgets({
            'money': (0, 0),
            "roulette": (0, 50)
        })
        
    elif menu_var.get() == 'realm':

        for item in realm_dict:
            realm_dict[item].place(x=realm_dict_positions[item]["x"],y=realm_dict_positions[item]["y"])

    elif menu_var.get() == 'legacy':

        for item in legacy_dict:
            legacy_dict[item].place(x=legacy_dict_positions[item]["x"],y=legacy_dict_positions[item]["y"])

    elif menu_var.get() == 'research':

        for item in research_dict:
            research_dict[item].place(x=research_dict_positions[item]["x"],y=research_dict_positions[item]["y"])

    elif menu_var.get() == 'roulette':

        clicker_dict['money'].place(x=400,y=0)
        for item in roulette_dict:
            roulette_dict[item].place(x=roulette_dict_positions[item]["x"],y=roulette_dict_positions[item]["y"])

    elif menu_var.get() == 'rebirth confirmation':
        widgets['confirmation'].place(x=300,y=500)


menu_var.trace_add('write', change_menu)

def starting():

    show_widgets({
        "Start_page": (0,0),
        "start_button": (150,700)
    })

def start_roulette():
    menu_var.set('roulette')
    widgets["menu"].place_forget()


def universal_update():
    time_count()
    loop_amoney()
    achievement()
    monlen()
    realm_check()
    if rebirth == 1:
        clicker_dict_positions['legacy'] = {"x":0,"y":50}
        clicker_dict['legacy'] = tk.Button(window,image=pixelVirtual,width=250,height=50,font=('Helvetica', 10),foreground="#000000",background="#C49D49",text=f"you have {Dc.legacy['legacies']} legacies available",compound="center",command=lambda:legacy_world())
    if rebirth > 0:
        legacy_check()
    research_check()
    window.after(universal_delay,universal_update)
if count==0:
    starting()
window.mainloop()    