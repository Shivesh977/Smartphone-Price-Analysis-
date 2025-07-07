import numpy as np
import pandas as pd

df = pd.read_csv('smartphones.csv')

#################################### Data Assessing ##################################

# Quality Issues

# model - some brands are written diiferently like OPPO in model column consistency
# price - has unneccesary '₹' validity
# price - has ',' between numbers validity
# price - phone Namotel has a price of 99 accuracy
# ratings - missing values completeness
# processor - has some incorrect values for some samsung phones(row # -642,647,649,659,667,701,750,759,819,859,883,884,919,927,929,932,1002) validity
# There is ipod on row 756 validity
# memory - incorrect values in rows (441,485,534,553,584,610,613,642,647,649,659,667,701,750,759,819,859,884,919,927,929,932,990,1002) validity
# battery - incorrect values in rows(113,151,309,365,378,441,450,553,584,610,613,630,642,647,649,659,667,701,750,756,759,764,819,855,859,884,915,916,927,929,932,990,1002) validity
# display - sometimes frequency is not available completeness
# display - incorrect values in rows(378,441,450,553,584,610,613,630,642,647,649,659,667,701,750,759,764,819,859,884,915,916,927,929,932,990,1002) validity
# certain phones are foldable and the info is scattered validity
# camera - words like Dual, Triple and Quad are used to represent number of cameras and front and rear cameras are separated by '&'
# camera - problem with rows (100,113,151,157,161,238,273,308,309,323,324,365,367,378,394,441,450,484,506,534,553,571,572,575,584,610,613,615,630,642,647,649,659,667,684,687,705,711,723,728,750,756,759,764,792,819,846,854,855,858,883,884,896,915,916,927,929,932,945,956,990,995,1002,1016 ) validity
# card - sometimes contains info about os and camera validity
# os - sometimes contains info about bluetooth and fm radio validity
# os - issue with rows (324,378) validity
# os - sometimes contains os version name like lollipop consistency
# missing values in camera, card and os completeness
# datatype of price and rating is incorrect validity

# Tidiness Issues

# sim - can be split into 3 cols has_5g, has_NFC, has_IR_Blaster
# ram - can be split into 2 cols RAM and ROM
# processor - can be split into processor name, cores and cpu speed.
# battery - can be split into battery capacity, fast_charging_available
# display - can be split into size, resolution_width, resolution_height and frequency
# camera - can be split into front and rear camera
# card - can be split into supported, extended_upto


########################################## Data cleaning ################################################
# make a copy
df1 = df.copy()

# removing rupees symbol and comma and changing to int
df1['price']=df1['price'].str.replace('₹','').str.replace(',','').astype('int')

# resetting index to match df1 index and csv file index as there is difference of two 
df1=df1.reset_index() # new column will be made with index name
df1['index']=df1['index']+2

# These rows have problems
processor_rows = set((642,647,649,659,667,701,750,759,819,859,883,884,919,927,929,932,1002))
ram_rows = set((441,485,534,553,584,610,613,642,647,649,659,667,701,750,759,819,859,884,919,927,929,932,990,1002))
battery_rows = set((113,151,309,365,378,441,450,553,584,610,613,630,642,647,649,659,667,701,750,756,759,764,819,855,859,884,915,916,927,929,932,990,1002))
display_rows = set((378,441,450,553,584,610,613,630,642,647,649,659,667,701,750,759,764,819,859,884,915,916,927,929,932,990,1002))
camera_rows = set((100,113,151,157,161,238,273,308,309,323,324,365,367,378,394,441,450,484,506,534,553,571,572,575,584,610,613,615,630,642,647,649,659,667,684,687,705,711,723,728,750,756,759,764,792,819,846,854,855,858,883,884,896,915,916,927,929,932,945,956,990,995,1002,1016 ))

# These are the rows having problem we are doing union
df1[df1['index'].isin(processor_rows | ram_rows | battery_rows | display_rows | camera_rows)] # | : means union ...shows all the rows having problem 

df1[df1['index'].isin(processor_rows & ram_rows & battery_rows & display_rows & camera_rows)] # & : all these must have problems 
# above phones are not smartphones these are feature phones or keypad phones so remove those as we are working on smartphones 

df1 = df1[df1['price'] >= 3400] # price above 3400 are all smartphones therefore removing feature phone 

df1.drop([645,857,882,925],inplace=True) # these are the problemst in processor of smartphones so delete it 

df1.drop(582,inplace=True) # removing ram issues phones 

df1.drop([376,754],inplace=True) # removing battery issues phones 

# There is a left shift in iphones as battery data is not available so memory data is shifted in battery col and so on 
#  Therefore we will have to perform right shift 

temp_df = df1[df1['index'].isin(battery_rows)] # problem in battery rows 
x = temp_df.iloc[:,7:].shift(1,axis=1).values # applying shift  x contains shifted data 

df1.loc[temp_df.index,temp_df.columns[7:]] = x # gives these rows values == x  .... making changes in original dataframe 

