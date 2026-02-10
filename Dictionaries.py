#prices of each upgrade for mpc or mps when a certain mpc or mps count is reach
mpc_upgrade_costs = [250,10**4,10**7,2.5*(10**7)]
mpc_upgrade_multipliers = [2,20,50,100]
mps_upgrade_costs = [8000,10**6,10**8,2.5*(10**10)]
mps_upgrade_multipliers = [25,25,50,100]


roulette_options = {
    'green': {'payout': 37, 'check': lambda x: x==37},
    'red': {'payout': 2, 'check': lambda x: x%2 == 0},
    'black': {'payout': 2, 'check': lambda x: x!=37 and(x+1)%2 ==0},
    'bet_amount':10
}

#global variables for upgrades, click/auto upgrade check to see if the the widget for the upgrade beem used yet (has the upgrade been bought yet)
# "click/upgrade_flags['auto_bought'][check" is used to check whether the upgrade option as appeared on the screen yet 
upgrade_flags = {
    'click_active': [False,False,False,False],
    'click_bought': [False,False,False,False],
    'auto_active': [False,False,False,False],
    'auto_bought': [False,False,False,False],
}
upgrade_definitions = [
    {'type': 'click', 'count': 10, 'widget': 'click 10', 'active': upgrade_flags['click_bought'][0], 'index' : 0},
    {'type': 'click', 'count': 25, 'widget': 'click 25', 'active': upgrade_flags['click_bought'][1], 'index' : 1 },
    {'type': 'click', 'count': 50, 'widget': 'click 50', 'active': upgrade_flags['click_bought'][2], 'index' : 2 },
    {'type': 'click', 'count': 100, 'widget': 'click 100', 'active': upgrade_flags['click_bought'][3], 'index': 3 },
    {'type': "auto", 'count': 10, 'widget': 'auto 10', 'check': upgrade_flags['auto_active'][0], 'active': upgrade_flags['auto_bought'][0], 'index' :  0 },
    {'type': "auto", 'count': 25, 'widget': 'auto 25', 'check': upgrade_flags['auto_active'][1], 'active': upgrade_flags['auto_bought'][1], 'index' : 1 },
    {'type': "auto", 'count': 50, 'widget': 'auto 50', 'check': upgrade_flags['auto_active'][2], 'active': upgrade_flags['auto_bought'][2], 'index' : 2 },
    {'type': "auto", 'count': 100, 'widget': 'auto 100', 'check': upgrade_flags['auto_active'][3], 'active': upgrade_flags['auto_bought'][3], 'index' : 3 }
    ]
upgrade_data= [
    {'type': 'mpc','costs': mpc_upgrade_costs, 'multipliers': mpc_upgrade_multipliers, 'widgets': ['click 10','click 25','click 50', 'click 100'], 'checks': [upgrade_flags['click_active'][0],upgrade_flags['click_active'][1],upgrade_flags['click_active'][2],upgrade_flags['click_active'][3]]},
    {'type': 'mps','costs': mps_upgrade_costs, 'multipliers': mps_upgrade_multipliers, 'widgets': ['auto 10','auto 25','auto 50', 'auto 100'], 'checks': [upgrade_flags['auto_active'][0],upgrade_flags['auto_active'][1],upgrade_flags['auto_active'][2],upgrade_flags['auto_active'][3]]}
    ]



#variables for whether achievements have been reached
achievements=0
achievement_flags=[False,False,False,False,False]

realms = {
    'realm1':False,
    'record':0,
    'mps_power': 1,
    'mpc_power': 1
}

research = {
    'research_total': 0,
    'research_price': (10**4),
    'research': 1,
    'research_mpc_upgrade':0,
    'research_mps_upgrade':0,
    'research_mpc_upgrade_price':1,
    'research_mps_upgrade_price':1
}

ascension  = {
    'ascension_total' : 0,
    'ascension_price' : (10**12),
    'ascensions' : 1,
    'ascension_mps_upgrade': 0,
    'ascension_mpc_upgrade_price': 1,
    'ascension_mps_upgrade': 0,
    'ascension_mps_upgrade_price' : 1
}

money = {
    'money': 0,
    'temp_money_1': 0,
    'income': 0,
    'peak_money': 0,
    'total_money_made':0
}


events = {
    'dolllar_count': 0,
    'capitalist': False
}

time = {
    'hours': 0,
    'minutes': 0,
    'seconds' : 0
}

money_per_second = {
    'mps_count': 0,
    'mps': 0,
    'mps_cost': 100,
    'mps_multiplier': 1
}

money_per_click = {
    'mpc': 1,
    'mpc_count':1,
    'mpc_cost':15,
    'mpc_multiplier':1,

}