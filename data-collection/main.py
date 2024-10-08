import pandas as pd

from utils import concatenate_save_finaldf

from scrap import scrap_all

def main():

    start = 2006
    end = 2006

    scrap_all(start,end)
    
    concatenate_save_finaldf(start,end)

if __name__ == "__main__":
    main()