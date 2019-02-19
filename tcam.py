import sys
class tcam:
    def __init__(self,size=sys.maxsize):
        self.MaxEntries=size
        self.content=[]
        
    def insert(self,key, mask, pri, val, addr=None):
        if len(self.content) < self.MaxEntries:
            self.content.append((key,mask,pri,val,addr))
        else:
            print("memory full")
    
    def search(self,val):
        res=None
        for (mask,key,pri,resO,_) in self.content:
            if (key & mask) == (val & mask) and res[1]<pri:
                res = (resO, pri)
        return res
        
    def delete(self, addr):
        i=0
        for (_,_,_,_,elem) in self.content:
            if addr==elem:
                del self.content[i]
                break
            i=i+1
        
    def delete(self, key, mask):
        i=0
        for (mask, key, _,_) in self.content:
            if mask==mask and key==key:
                del self.content[i]
            else:
                i=i+1

    def print(self):
        print("number of entries ", len(self.content))
        print(self.content)
    
