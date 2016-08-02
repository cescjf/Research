import imuQ
from numpy.linalg import norm

db = imuQ.Project.loadDB()
unitSystem = 'SI'

global inputLog
       
def getVar(name):
    # This is a safe method for grabbing scalar values or class structures from the XML database. 
    # Set isVariable to False when pulling a class instead of a single variable.
    # If isVariable is False, in general you will need to manually call the addEntry method to add the class perturbation(s) to the input.dat file.
    modelName = 'MarsEDL'
    value = db.get('multiphysicsModel['+modelName+']::variable['+name+']').float(unitSystem=unitSystem)
    unit = db.get('multiphysicsModel['+modelName+']::variable['+name+']').units(unitSystem=unitSystem)
    addEntry(name, value, unit)
    print('Added variable ' + name + ' to inputs.dat')
    
    return value


#Input log methods -  could potentially have their own file but they integrate seamlessly with the perturbUtils.
def inputLogInit():
    from collections import OrderedDict
    global inputLog
    inputLog = {}
    inputLog['values'] = OrderedDict()
    inputLog['units'] = OrderedDict()
    return None
    
def addEntry(name, value, unit):
    global inputLog
    #Add an entry to the inputLog that gets written at the start of the sim.
    inputLog['values'][name.split(']')[0]] = value
    if unit is None or 'dimensionless' in unit:
        inputLog['units'][name.split(']')[0]] = '-'
    else:
        inputLog['units'][name.split(']')[0]] = unit
    
    return None
    
def writeInputLog():
    
    global inputLog
    spacing = 40
    file = open('./results/inputs.dat','w') # Create summary file to write to
    file.write('#Simulation inputs: '+ str(len(inputLog.keys())) +'\n')
    file.write('Input name'+ ' '*(spacing-10)) #10 is len('Input name')
  
    
    for key in inputLog['values']:
        file.write(key+ ' '*(spacing-len(key)))
    file.write('\n')
    file.write('Value'+ ' '*(spacing-5))
    for key in inputLog['values']:
        file.write(str(inputLog['values'][key]) + ' '*(spacing-len(str(inputLog['values'][key]))))
    file.write('\n')
    file.write('Units'+ ' '*(spacing-5))        
    for key in inputLog['values']:
        file.write(str(inputLog['units'][key]) + ' '*(spacing-len(str(inputLog['units'][key]))))
    file.close()
        
        
    return None