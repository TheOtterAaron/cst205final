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
  def __init__(this, number, description):
    this.number = number
    this.description = description
    this.callback = 0
  
  # Methods
  def getNumber(this):
    return this.number
    
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
    for i in range(0, len(this.actions)):
      if this.actions[i].getNumber() == number:
        this.actions[i].callback()
        return
    printNow("I don't understand, please make sure you are using a number!")

  #def printActions(this):
  #  for i in range(0, len(this.actions)):
  #    number = this.actions[i].getNumber()
  #    description = this.actions[i].getDescription()
  #    printNow("%s. %s"  % (number,description))  
  def buildActions(this):
    built = ""
    for i in range(0, len(this.actions)):
      number = this.actions[i].getNumber()
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
    this.currentRoom.printDesc()
    
  def getCurrentRoom(this):
    return this.currentRoom

  def getInventory(this):
    return this.inventory
    
  def damage(this, amount):
    this.health -= amount
    if(this.health <= 0):
      printNow("Oh dear you are dead!")
      #Do death condition
  def removeSanity(this, sanity):
    this.sanity -= sanity
    if(this.sanity <= 0):
      printNow("I'm sorry but it seems that you have lost your mind")
      #Do sanity condition
  
######
def testCallBack():
  printNow("test callback")

TURNS = 7

#When doing an action, remove a turn
#Should we handle this in the main game loop?

test = room("test")
test.setDescription("test room")
test_action = action(1, "test action")
test_action.setCallback(testCallBack)
second_test_action = action(2, "second action")
second_test_action.setCallback(testCallBack)
test.addAction(test_action)
test.addAction(second_test_action)
#test.printActions()
#test.takeAction(1)

while true:
  playerInput = requestString(test.buildActions())

#player = player()
#player.damage(20)
#player.removeSanity(20)
