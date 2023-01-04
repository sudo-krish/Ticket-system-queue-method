# This is a queue data structure which allows you to add values and remove them 
# based on FIFO (First In First Out) order

from queue import Empty


class ticketSystem:
    def __init__(self, w, n):
            """
            initialization
            """
            self.n = n
            self.w = w
            self.queues = [[None for i in range(n)]for j in range(w)]
            self.starts = [0 for i in range(w)]
            self.ends =   [0 for i in range(w)]
            self.size =   [0 for i in range(w)]
            self.open =   [False for i in range(w)]
            self.open[0] = True

    def outputFile (self,id,value,method):
        f = open('outputPS4.txt', 'a+')
        f.writelines(str(method)+str(id)+' >> '+str(value)+'\n')
    
    def isOpen (self, windowId):
        """ 
        This function returns True if the box office window is open and False if it is yet to be
        opened (closed). This function is called when the following tag “isOpen” is encountered in the inputPS4.txt file. 
        """
        
        self.outputFile(windowId,ticketSystem.open[windowId-1],'isOpen:')
        return ticketSystem.open[windowId -1]

    def getWindow (self, windowId): 
        """
        This function returns the queue (number of people waiting) in front of the window.
        (Will return empty queue if window is closed). This function is called when the following tag “getWindow” is
        encountered in the inputPS4.txt file.
        """
        personList = []
        if ticketSystem.size[windowId-1] > 0:
            for i in range(self.n):
              if self.queues[windowId-1][i] != None:
                personList += str(self.queues[windowId-1][i])
        self.outputFile(windowId,personList,'getWindow:')
        return personList
    def updateOpenStatus (self): 
        for i in range(self.w):
            if ticketSystem.size[i] > 0 :
                ticketSystem.open[i] = True
            else:
                ticketSystem.open[i] = False
    def addPerson (self, personId): 
        """This function is called to add a new person to one of the open window queues. It
        returns windowId of the window where the person should go to and - 1 if all the queues are full. This function is
        called when the following tag “addPerson” is encountered in the inputPS4.txt file.
        """
        flag =0
        flag_1 = 0

        for i in range(self.w):
#                 print(ticketSystem.open[i])
                 if ticketSystem.size[i] < self.n  and flag == 0  :
                        print("window " + str(i+1) + "  is available")

                        self.outputFile(personId,i+1,'addPerson:')
                        #print( ticketSystem.size[i])
                        ticketSystem.enqueue(i, personId)
                        #print( ticketSystem.size[i]) 
                        break
                       
                 else:
                        print("window " + str(i+1) + " is full")
        ticketSystem.updateOpenStatus()


    def giveTicket (self): 
        """This function is called to issue a ticket at every open box office window with a queue of
        at least one person. The function is called when the following tag “giveTicket” is encountered in the
        inputPS4.txt file.
        """
        flag =0
        for i in range(self.w):
            if ticketSystem.size[i] > 0:
                ticketSystem.dequeue(i)
                flag += 1
        ticketSystem.updateOpenStatus()
        
        self.outputFile(':',flag,'giveTicket')
        return flag
    def dequeue(self,windowId):
        """
        Remove and return the first element of the queue (FIFO)
        Raise Empty exception if the queue is empty
        """

        if ticketSystem.size[windowId] == 0:
            raise Empty('Queue is empty')
        else:
            starts = ticketSystem.starts[windowId]
            answer = ticketSystem.queues[windowId][starts]
            ticketSystem.queues[windowId][starts] = None # help garbage collection
 

            ticketSystem.starts[windowId] = (ticketSystem.starts[windowId] + 1) % ticketSystem.size[windowId]
            ticketSystem.size[windowId] -= 1

        return answer   
        
    def enqueue(self,windowId, personId):
        """
        Add an element to the back of the queue
        """
        if ticketSystem.size[windowId] < ticketSystem.n:
            avail = (ticketSystem.starts[windowId] + ticketSystem.size[windowId]) % ticketSystem.n           # find the available position to insert the element
            ticketSystem.queues[windowId][avail]=personId                          # insert the new element in the available position
            ticketSystem.size[windowId] += 1
            ticketSystem.ends[windowId] += 1
            flag =1
        else:
            print("Queue "+str(windowId)+" is full")

    def first(self):
        """
        Return (but do not remove) the element at the front of the queue.
        Raise Empty exception if the queue is empty
        """
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._data[self._front]
            
f = open('outputPS4.txt', 'a')
f.truncate(0)
with open('inputPS4.txt') as f:
    for line in f :
       # print(line)
        x = line.split(":")
        print(x[0])
        if x[0]=="ticketSystem":
            
            ticketSystem = ticketSystem(int(x[1]),int(x[2]))
        elif x[0] == "addPerson" :

            ticketSystem.addPerson(int(x[1]))
        elif x[0] == "getWindow":

            ticketSystem.getWindow(int(x[1]))
        elif x[0] == "isOpen":

            ticketSystem.isOpen(int(x[1]))
        elif x[0] == "giveTicket":

             ticketSystem.giveTicket()