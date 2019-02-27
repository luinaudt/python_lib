#!/usr/bin/python3
from tcam import tcam
import logging

def test_size_limit_insertion():
    mem=tcam(16,8,5,32,2)
    mem.insert(5,3,0,4,0)
    mem.insert(9,3,0,15,1)
    print(mem)
    try:
        mem.insert(5,3,0,4,2)
    except MemoryError:
        print("pass memory control")
        mem.deleteAddr(1)

    try:
        mem.insert(2**16,0,5,256)
    except ValueError:
        print("pass value size control")
        mem.deleteAddr(256)

    try:
        mem.insert(5,2**16,0,4,0)
    except ValueError:
        print("pass mask size control")
        mem.deleteAddr(0)
        
    try:
        mem.insert(5,0,2**8,4,0)
    except ValueError:
        print("pass pri size control")
        mem.deleteAddr(0)

    try:
        mem.insert(5,0,0,2**32,0)
    except ValueError:
        print("pass value size control")
        mem.deleteAddr(0)

    
    

def main():
    logging.basicConfig(level=logging.INFO)
    test_size_limit_insertion()



if __name__ == "__main__":
    main()
