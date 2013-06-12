import sys
import time

class Room(object):      
  def __init__(self, description=None, exits=None, commands=None, internal_contents=None, contents=None, hidden_contents=None, hidden_exits=None):
      
    self.description = description
    self.exits = exits or { }
    self.hidden_exits = hidden_exits or { }
    self.internal_contents = internal_contents or { }
    self.contents = contents or { }
    self.commands = commands or { }
    self.hidden_contents = hidden_contents or { }

    self.commands['look'] = PrintRoom
    self.commands['l'] = PrintRoom
    #self.commands['exa'] = Exa
    self.commands['search'] = Search
    self.commands['tester'] = RoomTester
    
def Search(room, location=None):
  isithere=0
  foundit=0
  if location==None:
    sys.stdout.write('Search what?\n')
    return room
  else:
    for x in room.internal_contents.values():
      for item in x:
        if location==item.name:
          isithere=1
          sys.stdout.write('You start to search the %s.\n' %item.name)
          for y in room.hidden_contents.values():
            for itemm in y:
              if itemm.location == location:
                time.sleep(3)
                sys.stdout.write('You find ' + itemm.description.lower() + '!\n')
                foundit=1
                room.contents[itemm.name] = [itemm]
                del room.hidden_contents[itemm.name]
                break  
    if isithere==0:
      sys.stdout.write('You find no %s to search.\n' %location)
      foundit=1
    if foundit==0:
      time.sleep(3)
      sys.stdout.write('Your search yields nothing.\n')    
    return room

def PrintRoom(room):
  obvious_exits = []
  for x in room.exits:
    if len(obvious_exits)==0:
      obvious_exits.append(x)
    elif len(obvious_exits)>0:
      obvious_exits.append(', ' + x)
  contents_descriptions = []
  for x in room.contents.values():
    for item in x:
      if len(contents_descriptions)==0:
        contents_descriptions.append(item.description)
      elif len(contents_descriptions)>0:
        contents_descriptions.append(', ' + item.description.lower())
  sys.stdout.write(room.description)
  if len(contents_descriptions)>0:
    sys.stdout.write('\n'+''.join(contents_descriptions)+ '.')
  sys.stdout.write('\nThe only obvious exits are: '+''.join(obvious_exits)+'.\n')
  return room 

def TryToGo(room, direction):
  if direction in room.exits:
    sys.stdout.write('You leave %s.\n' %direction)
    PrintRoom(room.exits[direction])
    return room.exits[direction]
  else:
    sys.stdout.write('There is no obvious exit %s.\n' %direction)
    return room
   
class Item(object):
  def __init__(self, name=None, description=None, long_description=None):
    self.name = name
    self.description = description  
    self.long_description = long_description  

class HiddenItem(object):
  def __init__(self, name=None, description=None, long_description=None, location=None):
    self.name = name
    self.description = description
    self.long_description = long_description
    self.location = location 
    
class Person(object):
  def __init__(self, name=None, inventory=None, commands=None, room=None):
  
    self.name = name
    self.inventory = inventory or { }
    self.commands = commands or { }
    self.room = room

  
    self.commands['i']=Inventory
    self.commands['exa']=Exa
    self.commands['get'] = Get
    self.commands['drop'] = Drop
    #self.commands['tester'] = Tester
    self.commands['climb'] = Climb

def RoomTester(room):
  for x in room.contents.values():
    print x
    
  return(room)
  
def Exa(person, thing=None):
  
  if thing is None:
    sys.stdout.write('Examine what?\n')
    return person
  isithere=0
  for x in person.room.internal_contents.values():
    for item in x:
      if thing == item.name:
        isithere=1
        sys.stdout.write(item.long_description + '\n')
  for x in person.room.contents.values():
    for item in x:
      if thing == item.name:
        isithere=1
        sys.stdout.write(item.long_description + '\n')
  for x in person.inventory.values():
    for item in x:
      if thing == item.name:
        isithere=1
        sys.stdout.write(item.long_description + '\n')
        return person       
  if isithere==0:
    sys.stdout.write('You find no %s.\n' %thing)
  return person
    
def Inventory(person):
  possessions = []
  for x in person.inventory.values():
    for item in x:
      if len(possessions)==0:
        possessions.append(item.description.lower())
      elif len(possessions)>0:
        possessions.append(', ' + item.description.lower())
  if len(possessions)==0:
    sys.stdout.write('You don\'t have anything.\n')
  else:
    sys.stdout.write('You are carrying ' + ''.join(possessions) + '.\n')
  return person  
  
def Get(person, thing=None):
  if thing is None:
    sys.stdout.write('Get what?\n')
  for x in person.room.contents.values():
    for item in x:
      if thing == item.name:
        sys.stdout.write('You get %s. \n' %item.description.lower() )
        person.inventory[item.name] = [item]
        del person.room.contents[thing]
        return person
        break
  sys.stdout.write('You find no %s to get.\n' %thing)
  return person
  
def Drop(person, thing=None):  
  if thing is None:
    sys.stdout.write('Drop what?\n')
  for x in person.inventory.values():
    for item in x:
      if thing == item.name:
        sys.stdout.write('You drop %s.\n' %item.description.lower())
        person.room.contents[item.name] = [item]
        del person.inventory[thing]
        return person
        break
  sys.stdout.write('You have no %s to drop.\n' %thing)
  return person

def Climb(user, direction=None):
  if direction is None:
    sys.stdout.write('Climb what? \n')
  elif direction in user.room.hidden_exits:
    sys.stdout.write('You climb %s.\n' %direction)
    PrintRoom(user.room.hidden_exits[direction])
    user.room = user.room.hidden_exits[direction]
    return user
  else:
    sys.stdout.write('You can\'t climb %s.\n' %direction)
  return user
       
    
   
  
