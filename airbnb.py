


##How to approach the project

*Importing the data
*Cleaning the price column
*Calculating average price
*Comparing costs to the private rental market
*Cleaning the room_type column
*What timeframe are we working with?
*Joining the DataFrames
*Analyzing listing prices by NYC borough
*Price range by borough
*Storing the final result


# Step 1 : Importing the data
import pandas as pd
import numpy as np
import datetime as dt
pri = pd.read_csv('/content/price.csv')
xl = pd.ExcelFile('/content/xls.xlsx')
room_types = xl.parse(0)
revi = pd.read_csv('/content/review.tsv', sep = '\t')

# Step 2. Cleaning the price column

pri['price'] = pri['price'].str.replace(' dollars', '')
pri['price'] = pd.to_numeric(pri['price'])
#pri['price'] = pri['price'].apply(str)

# Step 3. Calculating average price

free_listings = pri['price'] == 0
pri = pri.loc[~free_listings]
avi_price = round(pri['price'].mean(),2)

# Step 4. Comparing costs to the private rental market

pri['price_per_month'] = pri['price'] * 365/12
average_price_per_month = round(pri['price_per_month'].mean(),2)
difference = round(average_price_per_month - 3100 , 2)

# Step 5. Cleaning the room_type column

room_types['room_type'] = room_types['room_type'].str.lower()
room_types['room_type'] = room_types['room_type'].astype('category')
room_frequencies = room_types['room_type'].value_counts()

# Step 6. What timeframe are we working with?

# revi['last_review'] = revi['last_review'].astype('datetime')
revi['last_review'] = pd.to_datetime(revi['last_review'])
first_reviewed = revi['last_review'].dt.date.min()
last_reviewed = revi['last_review'].dt.date.max()

# Step 7. Joining the DataFrames

rooms_and_prices = pri.merge(room_types, how = 'outer', on = 'listing_id')
airbnb_merged = rooms_and_prices.merge(revi, how = 'outer', on = 'listing_id')
airbnb_merged.dropna (inplace = True)
airbnb_merged.duplicated().sum()

# Step 8. Analyzing listing prices by NYC borough

# airbnb_merged['borough'] = airbnb_merged['nbhood_full'].str.split(',').str[1]
airbnb_merged['borough'] = airbnb_merged['nbhood_full'].str.partition(',')[0]
boroughs = airbnb_merged.groupby('borough')['price'].agg(['sum', 'mean', 'median', 'count'])
boroughs = boroughs.round(2).sort_values('mean', ascending=False)

# Step 9. Price range by borough

label_names = ["Budget", "Average", "Expensive", "Extravagant"]
ranges = [0,69,175,350, np.inf]
airbnb_merged['price_range'] = pd.cut(airbnb_merged['price'], bins = ranges, labels = label_names )
prices_by_borough = airbnb_merged.groupby(['borough', 'price_range'])['price_range'].count()

# Step 10. Storing the final result

solution = {'avg_price':avi_price,
            'average_price_per_month': average_price_per_month,  
            'difference':difference,          
            'room_frequencies':room_frequencies, 
            'first_reviewed': first_reviewed,
            'last_reviewed': last_reviewed,
            'prices_by_borough':prices_by_borough}
print(solution)
