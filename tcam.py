import sys
import math
import warnings
import logging

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
        if key > 2**self.EntryWidth-1 or key < 0:
            raise ValueError("inserted key {} too large".format(key))
        if mask > 2**self.EntryWidth-1 or mask < 0:
            raise ValueError("inserted mask {} too large".format(mask))
        if pri > 2**self.PriorityWidth-1 or pri < 0:
            raise ValueError("inserted priority key {} too large".format(pri))
        if val > 2**self.ValueWidth-1 or val < 0:
            raise ValueError("inserted value {} too large".format(val))
        
        self.Content.append(line)
        logging.info("content {} inserted".format(line))

    
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
        
    def deleteAddr(self, addr):
        """
        delete the entry at addr
        """
        i=0
        notFind=True
        for (_,_,_,_,elem) in self.Content:
            if addr==elem:
                del self.Content[i]
                notFind=False
                break
            i=i+1
        if notFind:
            raise ValueError("Address {} is not present".format(addr))
        
    def deleteKM(self, key, mask):
        """
        delete the entry corresponding key, mask
        """
        i=0
        notFind=True
        for (keyC,maskC,_,_,_) in self.Content:
            if mask==maskC and key==keyC:
                del self.Content[i]
                notFind=False
            else:
                i=i+1

        if notFind:
            raise ValueError("pair (key,mask): ({}, {}) not found".format(key,mask))
        
    def __str__(self):
        ret=[]
        find_all = lambda c,s: [x for x in range(c.find(s), len(c)) if c[x] == s]
        printFormat='{{0:0{0}b}}'.format(self.EntryWidth)
        ret.append("number of entries {}".format(len(self.Content)))
        for (key,mask,pri,res,_) in self.Content:
            l=list(printFormat.format(key))
            for i in find_all(printFormat.format(mask),'1'):
                l[i]='*'
            ret.append("key : {}".format("".join(l)))
            ret.append("priority : {0}, result : {1}".format(pri,res))
        return "\n".join(ret)
    def __len__(self):
        """return number of entries
        """
        return len(self.Content)
