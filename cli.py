import argparse
from utils import MyPool, scrape, convertToExcel, printCategories
from conf import DEFAULT, DUMP
from sites import SITE_NAMES
import os
import shutil

DEFAULT = "Furniture"
parser = argparse.ArgumentParser()
parser.add_argument('-f','--func', help='Specify a function to use. This value can be one of following: scrape, view', required=True)
parser.add_argument('-s','--sites', nargs='+', help='Websites to scrape. Values include Harvey Norman, Freedom, Target, Tsb Living, Treasure Box', required=False)
parser.add_argument('-k','--keywords', nargs='+', help='Categories or keywords to scrape listings for.', required=False)
parser.add_argument('-o','--outfile', help='Name for the output Excel file.', required=False)
args = parser.parse_args()

print(args.keywords)
sites = args.sites if args.sites is not None else list(SITE_NAMES.keys())
keywords = args.keywords if args.keywords is not None else [DEFAULT]

if args.func == "scrape":
    try:
        os.makedirs(DUMP, exist_ok = True)
    except:
        pass

    mapping = [(s, keywords) for s in sites]
    pool = MyPool(processes = len(mapping))
    data = pool.starmap(scrape, mapping)
    pool.close()
    res = [d for dat in data for d in dat]
    # res = []
    # for siteName in sites:
    #     res += scrape(siteName, keywords)

    if args.outfile:
        convertToExcel(res, output_filename = args.outfile)
    else:
        convertToExcel(res)

    # clean dump directory after job done
    try:
        shutil.rmtree(DUMP, ignore_errors = True)
    except Exception as e:
        print("Could not remove dump. Exception: ", e)

elif args.func == "view":

    for each in sites:
        print(f"########## Categories for {each}:################ \n")
        printCategories(each)
    print("################################################")
