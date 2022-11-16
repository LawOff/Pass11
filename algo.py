import js2py

def resCharaSetOff(password):
    resCharaSet = {
        'lowercase': False,
        'uppercase': False,
        'numbers': False,
        'special': False
    }
    for i in password:
        if i.islower():
            resCharaSet['lowercase'] = True
        elif i.isupper():
            resCharaSet['uppercase'] = True
        elif i.isdigit():
            resCharaSet['numbers'] = True
        else:
            resCharaSet['special'] = True
    return resCharaSet

def AlgoCheck(password,tempfile):
    strength = ["Very Weark", "Weak", "Good", "Strong", "Very Strong"]
    result= tempfile.checkThisPassword(password)

    resStrength = {"strength": strength[result[1]]}
    resNStrength = {"nstrength": result[1]}
    resTime = {"time": result[0]}
    resLength = {"length": len(password)}
    resCharaSet = resCharaSetOff(password)
    
    resColor = {"color": "#767676"}
    
    if resStrength["strength"] == "Very Weak":
        resColor = {"color": "#767676"}
    elif resStrength["strength"] == "Weak":
        resColor = {"color": "#FF8C00"}
    elif resStrength["strength"] == "Good":
        resColor = {"color": "#FFB900"}
    elif resStrength["strength"] == "Strong":
        resColor = {"color": "#00CC6A"}
    else:
        resColor = {"color": "#10893E"}

    return {**resColor, **resNStrength, **resStrength, **resTime, **resLength, **resCharaSet}
