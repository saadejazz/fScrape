# Furniture Scraper  

## Getting Started  
If you are using conda, make a virtual environment using:  
```bash
conda create -n scrape python=3.7
```

To install requirements, first activate the environment: 
```
conda activate scrape
python -m pip install argparse xlsxwriter bs4 pillow 
```

Then clone this repository:   
```
sudo apt install git
git clone https://wwww.github.com/saadejazz/fScrape
cd fScrape
```

## Command Line Interface  

```
usage: cli.py [-h] -f FUNC [-s SITES [SITES ...]] [-k KEYWORDS [KEYWORDS ...]]
              [-o OUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  -f FUNC, --func FUNC  Specify a function to use. This value can be one of
                        following: scrape, view
  -s SITES [SITES ...], --sites SITES [SITES ...]
                        Websites to scrape. Values include Harvey Norman,
                        Freedom, Target, Tsb Living, Treasure Box
  -k KEYWORDS [KEYWORDS ...], --keywords KEYWORDS [KEYWORDS ...]
                        Categories or keywords to scrape listings for.
  -o OUTFILE, --outfile OUTFILE
                        Name for the output Excel file.
```

### Site Names  
The following site names should be strictly adhered to:  

* Freedom  
* Harvey Norman  
* Target  
* Treasure Box  
* Tsb Living  

### Example Usage  

```
python cli.py -f scrape -s "Harvey Norman" -k "Furniture" -o "HN_furniture.xlsx"
```

In the above example, arguments followed by -s are site names that must be from the above-mentioned site names, arguments followed by -k are the categories to scrape, and the argument followed by -o is the filename of the ouput.  

There can be more than one argument for sites (-s) and keywords (-k). For this, use:  

```
python cli.py -f scrape -s "Target" "Freedom" "Treasure Box" -k "Furniture: Sofas" "Furniture: Beds" -o "Sofas_and_Beds.xlsx"
```

Furthermore, you can view a list of categories for each site using:  
```
python cli.py -f view -s "Harvey Norman" "Tsb Living"
```
This will result in the following output:  
```
########## Categories for Harvey Norman:################ 

Furniture
Furniture: Bedding Furniture
Furniture: Kids Bedroom
Furniture: Bedding and Bed Linen
Furniture: Home Decor
Furniture: Lounge
Furniture: Home Office
Furniture: Dining
Furniture: More
Furniture: Outdoor

########## Categories for Tsb Living:################ 

Furniture
Furniture: Living Room
Furniture: Bed Room
Furniture: Dining Room
Furniture: Kitchen Tools
Furniture: Bathroom / Laundry
Furniture: Office / Home

Pet Care
Pet Care: Dog Supplies
Pet Care: Aquarium Filters
Pet Care: Farm Supplies
Pet Care: Cat Supplies
Pet Care: Bird Supplies
Pet Care: Hutch & Coops

Fitness & Travel
Fitness & Travel: Home Gym
Fitness & Travel: Camping
Fitness & Travel: Bike Accessories
Fitness & Travel: Boat Accessories
Fitness & Travel: Travel
Fitness & Travel: Kayaking
Fitness & Travel: Gun Safe & Accessories

Electronics & Tools
Electronics & Tools: Industrial tools
Electronics & Tools: Heaters & fans
Electronics & Tools: Auto Accessories
Electronics & Tools: Projectors screens
Electronics & Tools: Pumps
Electronics & Tools: Tools Storage
Electronics & Tools: Barn Door
Electronics & Tools: Air Brush & Compressors

Baby & Kids
Baby & Kids: Kids furniture
Baby & Kids: Toys
Baby & Kids: Nursery furniture

Outdoors and Lawns
Outdoors and Lawns: Outdoors
Outdoors and Lawns: Gazebo & Shade
Outdoors and Lawns: Outdoor storage
Outdoors and Lawns: Garden Accessories
Outdoors and Lawns: Pool Products
Outdoors and Lawns: Gate & Garage Accessories

Home & Living
Home & Living: Bedding
Home & Living: Living Room Accessories
Home & Living: Kitchen
Home & Living: Bathroom
Home & Living: Sauna
Home & Living: Musical instruments
Home & Living: Health and Beauty

Appliances
Appliances: Kitchen and Cooking
Appliances: Laundry
Appliances: Refrigerator
Appliances: Small Appliance
Appliances: Ice makers
Appliances: Air fryer
Appliances: Bar fridge
Appliances: Chest freezer

################################################
```

If you do not provide a site (-s) argument it is assumed that all sites are in question. Also, for a keyword that is not a category for a site, it performs a search and provides the resulting data.   

Finally, the output file is stored in "results/" directory.  
 