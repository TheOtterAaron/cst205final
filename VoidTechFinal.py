import pickle

TURNS = 7
NAME = requestString("Can you please tell me your name?")

class frame:
  def __init__(this):
    timeOfDay = 7
    initialFrame = "" #TODO
    mainFrame = pickle.deepcopy(initialFrame) #TODO
    #Initial frame will be the frame to be painted
    #Will paint the frame with everything minus the stats
    #Stats to be painted later
    #Frame to be painted to is the mainFrame
    #MainFrame will always deepcopy the initial frame to copy over the data
    #Possibly cache "new" frames for different times of day for speed effeciency, however loadtime will be rough
  
  def getMainFrame(this, frame): #Returns a deepcopy of initial frame
    return pickle.deepcopy(initialFrame)
    
  def paintStats(this, frame): #Should be called whenever sanity or health gets updated
    print("Repainting stats!")
    
    #Paint stats TODO
    return frame
  
  def timeOfDay(this, frame):
    print("Painting the time of day!")
    if(timeOfDay == 7):
      print("TODO")
      #Paint a certain color over a subsection of the frame
    
    this.timeOfDay = this.timeOfDay - 1 #When a day passes
    return frame
    
  #When changes are done repaint in main game loop

class inventory:

  # Members
  def __init__(this):
    this.contents = list()
  
  # Methods
  def addItem(this, item):
    this.contents.append(item)
        
  def removeItem(this, item):
    this.contents.remove(item)
    
  def hasItem(this, item):
    for i in range(0, len(this.contents)):
      if this.contents[i] == item:
        return true
    return false
    
  def printItems(this):
    printNow("Inventory:")
    for i in range(0, len(this.contents)):
      printNow("   " + this.contents[i])
      
# === ACTION ===
class action:
  
  # Members
  def __init__(this, description):
    this.description = description
    this.callback = 0
  
  # Methods
  def getDescription(this):
    return this.description
  
  def setCallback(this, callback):
    this.callback = callback
      
# === ROOM ===
class room:

  # Members
  def __init__(this, name):
    this.name = name
    this.description = ""
    this.inventory = inventory()
    this.actions = list()
  
  # Methods
  def setDescription(this, description):
    this.description = description
    
  def printDescription(this):
    printNow("======= " + this.name + " =======")
    printNow(this.description)
    
  def getInventory(this):
    return this.inventory
    
  def addAction(this, action):
    this.actions.append(action)
  
  def removeAction(this, action):
    this.actions.remove(action)  
  
  def takeAction(this, number):
    number = number - 1
    for i in range(0, len(this.actions)):
      if i == number:
        this.actions[i].callback()
        return 1
    showInformation("I don't understand, please make sure you are using a valid number!")
    return 0
  #def printActions(this):
  #  for i in range(0, len(this.actions)):
  #    number = this.actions[i].getNumber()
  #    description = this.actions[i].getDescription()
  #    printNow("%s. %s"  % (number,description))  
  def buildActions(this):
    built = ""
    for i in range(0, len(this.actions)):
      number = i + 1
      description = this.actions[i].getDescription()
      built += "%s. %s \n" %(number, description)
    return built
# === PLAYER ===
class player:
  
  # Members
  def __init__(this):
    this.currentRoom = 0
    this.inventory = inventory()
    this.health = 20
    this.sanity = 20
  
  # Methods
  def setCurrentRoom(this, newRoom):
    this.currentRoom = newRoom
    this.currentRoom.printDescription()
    
  def getCurrentRoom(this):
    return this.currentRoom

  def getInventory(this):
    return this.inventory
    
  def damage(this, amount):
    this.health -= amount
    if(this.health <= 0):
      printNow("Oh dear you are dead!")
      TURNS = 0
      #Do death condition
  def removeSanity(this, sanity):
    this.sanity -= sanity
    if(this.sanity <= 0):
      printNow("I'm sorry but it seems that you have lost your mind")
      TURNS = 0
      #Do sanity condition
  
######
def testCallBack():
  printNow("test callback")

#When doing an action, remove a turn
#Should we handle this in the main game loop?

player = player()
test = room("test")
test.setDescription("test room")
test_action = action("test action")
test_action.setCallback(testCallBack)
second_test_action = action("second action")
second_test_action.setCallback(testCallBack)
test.addAction(test_action)
test.addAction(second_test_action)
player.setCurrentRoom(test)
#test.printActions()
test.takeAction(1)

while true:
  if(TURNS == 0):
    showInformation("I am sorry but you have lost the game, better luck next time!")
    break
  playerInput = requestString(test.buildActions())
  if playerInput.upper() == "HELP":
    print("TODO")
  else:
    val = player.getCurrentRoom().takeAction(int(playerInput))
    if(val == 1):
      TURNS -= 1
    else:
      continue
#player.damage(20)
#player.removeSanity(20)
