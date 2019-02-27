#!/usr/bin/python3
from tcam import tcam
import logging

def test_size_limit_insertion():
    mem=tcam(16,8,5,32,2)
    mem.insert(5,3,0,4,0)
    mem.insert(9,3,0,15,1)
    try:
        mem.insert(5,3,0,4,2)
    except MemoryError:
        logging.info("pass memory control")
        mem.deleteAddr(1)

    try:
        mem.insert(2**16,0,5,256)
    except ValueError:
        logging.info("pass value size control")

    try:
        mem.insert(5,2**16,0,4,0)
    except ValueError:
        logging.info("pass mask size control")
        
    try:
        mem.insert(5,0,2**8,4,0)
    except ValueError:
        logging.info("pass pri size control")

    try:
        mem.insert(5,0,0,2**32,0)
    except ValueError:
        logging.info("pass value size control")
    del mem

def test_result_lookup():
    mem=tcam(16,4,8,32,256)
    logging.info("actual memory length {}".format(len(mem)))
    mem.insert(5,int("0111",2),0,4,0)
    mem.insert(5,0,1,256,1)
    logging.info("actual memory length {}".format(len(mem)))
    print(mem.search(5))
    print(mem.search(1))
    print(mem.search(25))

def test_delete_element():
    mem=tcam(16,4,8,32,256)
    mem.insert(5,int("0111",2),0,4,54)
    mem.insert(5,0,1,256,1)    
    try:
        mem.deleteAddr(254)
    except ValueError:
        logging.info("pass deleteAddr error")

    try:
        mem.deleteKM(6,5)
    except ValueError:
        logging.info("pass deleteKM error")

    mem.deleteKM(5,0)
    if len(mem) == 1:
        logging.info("pass deleteKM")
    mem.deleteAddr(54)
    if len(mem) == 0:
        logging.info("pass deleteAddr")
                
def main():
    test_size_limit_insertion()
    logging.getLogger().setLevel(logging.INFO)
    test_delete_element()
    test_result_lookup()



if __name__ == "__main__":
    main()
