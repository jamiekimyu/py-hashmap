# *************************************
#  Fixed-size Hash Map Implementation
#  Author: Mike Wu
#  Description: Uses __hash__
#  hashing with linear probing. 
# *************************************

class HashMap(object):
  def __init__(self, size):
    self.count = 0
    # This is a fixed size!!!
    self.size = size
    self.keys = [None]*size
    self.items = [None]*size

  # Rely on python for the hash. 
  def hashme(self, key):
    return key.__hash__() % self.size

  def rehashme(self, oldhash):
    return (oldhash + 1) % self.size
  
  def set(self, key, value):
    hashvalue = self.hashme(key)
    returnvalue = False
    # No conflict? Just add it.
    if self.keys[hashvalue] is None: 
      self.keys[hashvalue] = key
      self.items[hashvalue] = value
      self.count += 1
      returnvalue = True
    else: # There is a conflict.
      if self.keys[hashvalue] == key:
        self.items[hashvalue] = value # Handle replacement.
        returnvalue = True
      else:
        tryagain = self.rehashme(hashvalue)
        # Loop until you find an empty slot. (Make sure you don't loop)
        while (not self.keys[tryagain] is None) and (tryagain != hashvalue):
          tryagain = self.rehashme(tryagain)
        # Double check if we found an empty spot.
        if self.keys[tryagain] is None: 
          self.keys[tryagain] = key
          self.items[tryagain] = value
          self.count += 1
          returnvalue = True
        else: # B/c this is fixed length, if we can't get open spot, fail.
          returnvalue = False
    return returnvalue

  def get(self, key):
    # This is important to prevent looping.
    initialvalue = self.hashme(key)
    hashvalue = initialvalue
    myitem = None # Default if not found.
    exitloop = False
    # Same thing: Loop through and probe.
    while (not self.keys[hashvalue] is None) and (not exitloop):
      if self.keys[hashvalue] == key:
        myitem = self.items[hashvalue]
        exitloop = True # Indicate we found key.
      else: # tryagain
        hashvalue = self.rehashme(hashvalue)
        if hashvalue == initialvalue: 
          exitloop = True # Inidicate we found loop.
          # This will output None
    return myitem

  def delete(self, key):
    # This is important to prevent looping.
    initialvalue = self.hashme(key)
    hashvalue = initialvalue
    returnValue = None # Default if not found.
    exitloop = False
    while (not self.keys[hashvalue] is None) and (not exitloop):
      if self.keys[hashvalue] == key:
        # return value associated with deleted value.
        returnValue = self.items[hashvalue]
        # Set the values to null (thereby deleting it).
        self.keys[hashvalue] = None
        self.items[hashvalue] = None
        # Record the deletion.
        self.count -= 1
        exitloop = True # Indicate we found key.
      else: # tryagain
        hashvalue = self.rehashme(hashvalue)
        if hashvalue == initialvalue: 
          exitloop = True # Inidicate we found loop.
          # This will output None
    return returnValue

  def load(self):
    if (self.count + self.size == 0): 
      return 0
    return self.count / float(self.size)

  # Python has default __getitem__ and __setitem__ functions.
  def __getitem__(self, key):
    return self.get(key)

  def __setitem__(self, key, value):
    return self.set(key, value)

  def __repr__(self):
    return "<HashMap, style:linear-probing, size:%d>" % self.size 


