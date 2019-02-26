#!/usr/bin/python3
from tcam import tcam

def main():
    mem=tcam()
    mem.insert(5,1,0,4,256)
    mem.print()
    print(mem.search(5))
    print(mem.search(4))
    print(mem.search(8))
    
if __name__ == "__main__":
    main()