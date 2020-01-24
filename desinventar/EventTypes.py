
drr_types =['Fire', 'Other', 'Epidemic', 'Cold Wave', 'Wind storm', 'High Altitude',
 'Landslide', 'Thunderbolt', 'Heavy Rainfall', 'Boat Capsize', 'Flood',
 'Hailstone', 'Snow Storm', 'Animal Incidents', 'Snake Bite', 'Avalanche',
 'Sinkhole', 'Air Crash', 'Hail Storm', 'Forest Fire' ]
des_types = ['Fire', 'Epidemic', 'Cold Wave', 'Accident', 'Thunderstorm', 'Forest Fire',
 'Famine', 'Structural Collapse', 'Strong Wind', 'Flood', 'Landslide',
 'Avalanche' ,'Earthquake', 'Rains', 'Boat Capsize', 'Hailstorm', 'Snow Storm',
 'Explosion', 'Storm', 'Heat Wave']


def drr2des_EventType(drr_incident):
    dict_drr2des = {
        "Thunderbolt": "Thunderstorm",
        "Wind storm": "Strong Wind",
        "Heavy Rainfall":"Rains",
        "Hailstone":"Hailstorm",
        "Hail Storm":"Hailstorm",

        "Fire":"Fire", 
        "Epidemic":"Epidemic", 
        "Cold Wave":"Cold Wave", 
        "Landslide":"Landslide", 
        "Boat Capsize":"Boat Capsize", 
        "Flood":"Flood", 
        "Snow Storm":"Snow Storm",
        "Avalanche":"Avalanche", 
        "Forest Fire":"Forest Fire"

        }
    if drr_incident in dict_drr2des.keys():
        return dict_drr2des[drr_incident]
    return None



matched = []
not_matched = []
for drr_type in drr_types:
    if drr_type in des_types:
        matched.append(drr_type)
        print ("%s Matched \n" % (drr_type))
    else:
        new_des_type = drr2des_EventType(drr_type)
        print (new_des_type)
        if(new_des_type):
            matched.append(drr_type)
            print ("%s Not Matched but converted to %s " % (drr_type, new_des_type))
        else:
            not_matched.append(drr_type)
            print ("%s Not Matched and could not be mapped to DesINVENTAR Database\n" % (drr_type))
print ("Matched")
print (matched)
print ("Not Matched")
print (not_matched)
print ("Remaining To be matched")
print ([x for x in drr_types if x.upper() not in matched])

