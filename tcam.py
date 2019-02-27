import sys
import math
import warnings
class tcam:
    """ a basic tcam class
    
    """
    def __init__(self,entryWidth, priWidth=8, addrWidth=int(math.log2(sys.maxsize)), valueWidth=32, size=sys.maxsize):
        """
        entryWidth : width in bits of the entry
        priWidth : Width of the priority in bits
        addrWidth : width of addresses in bits
        valueWidth : width of the associated value in bit
        size : max number of entries
        entryWidth : size of an entry in bits
        
        """
        if math.log2(size) > addrWidth :
            warnings.warn("addr width can't represents the size of table")
        self.MaxEntries=size
        self.PriorityWidth=priWidth
        self.AddrWidth=addrWidth
        self.ValueWidth=valueWidth
        self.EntryWidth=entryWidth
        self.Content=[]
        
    def insert(self,key, mask, pri, val, addr=None):
        """insert information
        key : key to look
        mask : mask of the entry
        pri : priority
        val : result
        addr : position inside the TCAM : optional
        """
        line=(key,mask,pri,val,addr)

        if len(self.Content) >= self.MaxEntries:
            raise MemoryError("memory full content {} not inserted".format(line))
        if key != 0 and math.log2(key) > self.EntryWidth:
            raise ValueError("inserted key {} too large".format(key))
        if mask != 0 and math.log2(mask) > self.EntryWidth:
            raise ValueError("inserted mask {} too large".format(mask))
        if pri!= 0 and math.log2(pri) > self.PriorityWidth:
            raise ValueError("inserted priority key {} too large".format(pri))
        if val != 0 and math.log2(val) > self.ValueWidth:
            raise ValueError("inserted value {} too large".format(val))
        
        self.Content.append(line)
        print("content {} inserted".format(line))

    
    def search(self,val):
        """
        return the value associtated to val with the highest priority
        if two match have the same priority take the first one found
        TODO: better algorithm for search
        """
        res=(0,-1)
        for (key,mask,pri,resO,_) in self.Content:
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
        for (_,_,_,_,elem) in self.Content:
            if addr==elem:
                del self.Content[i]
                break
            i=i+1
        
    def delete(self, key, mask):
        """
        delete the entry corresponding key, mask
        """
        i=0
        for (mask, key, _,_) in self.Content:
            if mask==mask and key==key:
                del self.Content[i]
            else:
                i=i+1

    def print(self):
        """
        simple print of the memory content
        TODO: look at a way for a better format
        """
        find_all = lambda c,s: [x for x in range(c.find(s), len(c)) if c[x] == s]
        printFormat='{{0:0{0}b}}'.format(self.EntryWidth)
        print("number of entries ", len(self.Content))
        for (key,mask,pri,res,_) in self.Content:
            #print("key  : {}".format(printFormat.format(key)))
            #print("mask : {}".format(printFormat.format(mask)))
            l=list(printFormat.format(key))
            for i in find_all(printFormat.format(mask),'1'):
                l[i]='*'
            print("key : {}".format("".join(l)))
            print("priority : {0}, result : {1}".format(pri,res))
