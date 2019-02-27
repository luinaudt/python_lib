import sys
class tcam:
    """ a basic tcam class
    
    """
    def __init__(self,entryWidth, size=sys.maxsize):
        """
        size : max number of entries
        TODO : add the possibility to constraints entry width
        """
        self.MaxEntries=size
        self.EntryWidth=entryWidth
        self.content=[]
        
    def insert(self,key, mask, pri, val, addr=None):
        """insert information
        key : key to look
        mask : mask of the entry
        pri : priority
        val : result
        addr : position inside the TCAM : optional
        """
        if len(self.content) < self.MaxEntries:
            self.content.append((key,mask,pri,val,addr))
        else:
            print("memory full")
    
    def search(self,val):
        """
        return the value associtated to val with the highest priority
        if two match have the same priority take the first one found
        TODO: better algorithm for search
        """
        res=(0,-1)
        for (key,mask,pri,resO,_) in self.content:
            if (key & ~mask) == (val & ~mask) and  res[1]<pri:
                res = (resO, pri)
        if res==(0,-1):
            return None
        else:
            return res[0]
        
    def delete(self, addr):
        """
        delete the entry at addr
        """
        i=0
        for (_,_,_,_,elem) in self.content:
            if addr==elem:
                del self.content[i]
                break
            i=i+1
        
    def delete(self, key, mask):
        """
        delete the entry corresponding key, mask
        """
        i=0
        for (mask, key, _,_) in self.content:
            if mask==mask and key==key:
                del self.content[i]
            else:
                i=i+1

    def print(self):
        """
        simple print of the memory content
        TODO: look at a way for a better format
        """
        find_all = lambda c,s: [x for x in range(c.find(s), len(c)) if c[x] == s]
        printFormat='{{0:0{0}b}}'.format(self.EntryWidth)
        print("number of entries ", len(self.content))
        for (key,mask,pri,res,_) in self.content:
            #print("key  : {}".format(printFormat.format(key)))
            #print("mask : {}".format(printFormat.format(mask)))
            l=list(printFormat.format(key))
            for i in find_all(printFormat.format(mask),'1'):
                l[i]='*'
            print("key : {}".format("".join(l)))
            print("priority : {0}, result : {1}".format(pri,res))
