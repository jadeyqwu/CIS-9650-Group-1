### predict-price
import pandas as pd

df = pd.read_csv('AllBoroughs2012-2019.csv', usecols = ['BOROUGH','BUILDING CLASS CATEGORY','GROSS SQUARE FEET','YEAR BUILT','SALE PRICE','Sale Year']) #only read in certain row


df = df[(df['YEAR BUILT']!='') & (df['SALE PRICE'].str.isnumeric() == True) & (df['GROSS SQUARE FEET'].str.isnumeric() == True) & (df['BUILDING CLASS CATEGORY'] != "") & (df['YEAR BUILT'] != 0)]



df['SALE PRICE'] = df['SALE PRICE'].astype(float) #convert from object to float
df['GROSS SQUARE FEET'] = df['GROSS SQUARE FEET'].astype(float) 


df = df[(df['SALE PRICE'] >= 70000) & (df['GROSS SQUARE FEET']>= 500) & df['BUILDING CLASS CATEGORY'].str.contains('FAMILY',na=True)] #filter the row


#create new column based on BUILDING CLASS CATEGORY
numofFamily = []

for n in df['BUILDING CLASS CATEGORY']:
    if 'ONE' in n:
         numofFamily.append(1)
    elif 'TWO' in n:
         numofFamily.append(2)       
    elif 'THREE' in n:
         numofFamily.append(3)      
         
df['numofFamily'] = numofFamily #add new series to dataframe


desiredborough=int("2") #User enters the desired borough 1=Manhattan, 2=The Bronx, 3=Brooklyn, 4=Queens, 5=Staten Island)
desirednumofFamily=int("2") #User enters the total units) 1= one family house, 2=two family house, 3=three family house
desiredgrosssquare= int("1209")#User enters the gross square)
desiredyearbuilt= int("2010") #User enters the year built)

#desiredborough=int(input("1=Manhattan, 2=The Bronx, 3=Brooklyn, 4=Queens, 5=Staten Island\nPlease enter your Desired borough:"))
#desirednumofFamily=int(input("\n1=one family house, 2=two family house, 3=three family house\nPlease enter the number of family:"))
#desiredgrosssquare= int(input("Please enters the gross square:"))
#desiredyearbuilt= int(input("Please enters the year built:"))


########
#find closest number 
def findClosest(target,iList):
    diff = 999999
    for i in iList:
        d = abs(i-target)
        if  d < diff:
            diff = d
            result = i
        else:
            continue
    return result

########

#get dataframe of row meet the condituin
res =  df[(df['BOROUGH'] == desiredborough) & (df['numofFamily'] == desirednumofFamily)] #return dataframe

#get dataframe of row meet the condituin
resu = res[(res['GROSS SQUARE FEET'] == findClosest(desiredgrosssquare,res['GROSS SQUARE FEET']))]

print("\n..........Searching................")

#get dataframe of row meet the condituin
result = resu[(resu['YEAR BUILT'] == findClosest(desiredyearbuilt,resu['YEAR BUILT']))]

# caculate avaerge 
avgSQPrice = result['SALE PRICE']/result['GROSS SQUARE FEET']

######## get house ratio based  on 2018 and 2019

housePrice18 = df[(df['Sale Year'] == 2018)]['SALE PRICE'].sum() 
housePrice19 = df[(df['Sale Year'] == 2019)]['SALE PRICE'].sum() 

percentage = (housePrice18)/((housePrice19))

## predict the price 
pprice = desiredgrosssquare * avgSQPrice * (1+percentage)
print("Avgerage Sale price per square Feet: ", avgSQPrice.to_string(index=False), "\nIncrease Percentage: ", percentage)
print("The Estimate Price is ", pprice.to_string(index=False))

# How has the percentage of condos/houses in the boroughs fluctuated over the last 5 years (2015-2019)?

#Question: From 2012 to 2015, which neighborhoods perform better over the other? From 2016 to 2019, which neighborhoods perform better over the other. 
#And is there anything changing from the previous decade? (use dataset II)
#what are the top 3 neighborhoods for 2012 - 2015 and 2016 - 2019?
import pandas as pd
df = pd.read_csv("DOF__Cooperative_Comparable_Rental_Income__Citywide_.csv")

#to filter out blank value
df["Net Operating Income"].fillna(0, inplace = True)
df["Full Market Value"].fillna(0, inplace = True)

#split the dataset into two parts and filter out 0 for NOI and FMV
ff = df[(df["Report Year"] <= 2015)&(df["Report Year"] >= 2012)&(df["Net Operating Income"] >0)&(df["Full Market Value"] > 0)]
gf = df[(df["Report Year"] <= 2019)&(df["Report Year"] >= 2016)&(df["Net Operating Income"] >0)&(df["Full Market Value"] > 0)]

#what are the top 3 neighborhoods for 2012 - 2015?
avgnoi = ff.groupby(["Neighborhood", "Borough Name"])["Net Operating Income"].mean()
afmv = ff.groupby(["Neighborhood", "Borough Name"])["Full Market Value"].mean()
caprate1215 = avgnoi/afmv
print("top 3 neighborhoods for 2012 - 2015")
print(caprate1215.nlargest(3))
nbs = ff["Neighborhood"].unique()

#what are the top 3 neighborhoods for 2016 - 2019?
avnoi = gf.groupby(["Neighborhood", "Borough Name"])["Net Operating Income"].mean()
avfmv = gf.groupby(["Neighborhood", "Borough Name"])["Full Market Value"].mean()
caprate1619 = avnoi/avfmv
print("")
print("top 3 neighborhoods for 2016 - 2019")
print(caprate1619.nlargest(3))

import pandas as pd
df = pd.read_csv("AllBoroughs2012-2019.csv")

import matplotlib.pyplot as plt

df["BOROUGH"]= df["BOROUGH"].replace(1, "Manhattan")
df["BOROUGH"]= df["BOROUGH"].replace(2, "Bronx")
df["BOROUGH"]= df["BOROUGH"].replace(3, "Brooklyn")
df["BOROUGH"]= df["BOROUGH"].replace(4, "Queens")
df["BOROUGH"]= df["BOROUGH"].replace(5, "Staten Island")
    
condos = df[(df["BUILDING CLASS AT PRESENT"] == "A3") | (df["BUILDING CLASS AT PRESENT"] == "A4") | (df["BUILDING CLASS AT PRESENT"] == "A5") | (df["BUILDING CLASS AT PRESENT"] == "A9")
            | (df["BUILDING CLASS AT PRESENT"] == "B1") | (df["BUILDING CLASS AT PRESENT"] == "B2") | (df["BUILDING CLASS AT PRESENT"] == "B3")
            | (df["BUILDING CLASS AT PRESENT"] == "C0") | (df["BUILDING CLASS AT PRESENT"] == "C1") | (df["BUILDING CLASS AT PRESENT"] == "C2") | (df["BUILDING CLASS AT PRESENT"] == "C3")]

houses = df[(df["BUILDING CLASS AT PRESENT"] == "R0") | (df["BUILDING CLASS AT PRESENT"] == "R1") | (df["BUILDING CLASS AT PRESENT"] == "R2") | (df["BUILDING CLASS AT PRESENT"] == "R3") | (df["BUILDING CLASS AT PRESENT"] == "R4") | (df["BUILDING CLASS AT PRESENT"] == "R6") | (df["BUILDING CLASS AT PRESENT"] == "R7") | (df["BUILDING CLASS AT PRESENT"] == "R8") | (df["BUILDING CLASS AT PRESENT"] == "R9")]

# Display the ratio of condos and houses for each borough from 2015 to 2019
num_condos = condos[condos["Sale Year"] >= 2015].groupby(["Sale Year", "BOROUGH"]).count()["ADDRESS"]
num_houses = houses[houses["Sale Year"] >= 2015].groupby(["Sale Year", "BOROUGH"]).count()["ADDRESS"]

ratio = num_condos / num_houses
print("Ratios between condos and houses for NYC's 5 boroughs from 2015 to 2019:")
print(ratio)
ratio.plot.bar(color=['red', 'blue', 'purple', 'green', 'orange'])
plt.title("Ratios between condos and houses for NYC's 5 boroughs (2015 - 2019)")
plt.xlabel("Sale Year, Borough")
plt.ylabel("Ratio")
plt.show()

# Based on the data of the most recent year (2019), provide top 5 neighborhoods supplied most condos/houses for clients interested in condos/houses
print("\nIn 2019, the top 5 neighborhoods supplied most condos are listed below:")
current_condos = condos[condos["Sale Year"] == 2019].groupby(["BOROUGH", "NEIGHBORHOOD"]).count()["ADDRESS"]
print(current_condos.sort_values(ascending = False).head(5))

print("\nIn 2019, the top 5 neighborhoods supplied most houses are listed below:")
current_houses = houses[houses["Sale Year"] == 2019].groupby(["BOROUGH", "NEIGHBORHOOD"]).count()["ADDRESS"]
print(current_houses.sort_values(ascending = False).head(5))

### 0 price
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df = pd.read_csv("AllBoroughs2012-2019.csv",low_memory=False)


# # Data Cleaning
# - Select related columns
# - Drop cells contained '-', feet contained 0 and year before 1900(not valuable for us) 

# In[3]:


price = df.iloc[:,[0,1,2,15,16,19]]
price = price[~(price['SALE PRICE'].str.contains('-') | price['GROSS SQUARE FEET'].str.contains('-'))]
price = price[~((price['GROSS SQUARE FEET'] == 0)|(price['YEAR BUILT'] < 1900))]


# - add one column to caculate unit price and drop invail values

# In[4]:


price['dollar_per_square'] = price['SALE PRICE'].astype(float)/price['GROSS SQUARE FEET'].astype(float)
price['dollar_per_square'].replace(np.inf, np.nan,inplace=True)
price.dropna(inplace = True)
price = price[price['dollar_per_square']<10000]


# # What is percentage of sale-price is 0?

# In[5]:


((price['SALE PRICE'].astype(float) == 0.0000000).sum())/(len(price.index))


# # Which borough has lower percentage of 0 price selling?

# In[6]:


price['NEIGHBORHOOD'] = price['NEIGHBORHOOD'].str.strip()


# In[7]:


nosale1 = price.loc[price['dollar_per_square']==0].groupby('BOROUGH').size()
allsale1 = price.groupby('BOROUGH')['dollar_per_square'].size()
ratio1 = nosale1 / allsale1
ratio1 = ratio1.to_frame(name="ratio").reset_index()
sns.barplot(x = 'BOROUGH',y = 'ratio', data = ratio1);


# # What is top 10 neighborhood that have highest ratio of 0 sale price?

# In[8]:


nosale2 = price.loc[price['dollar_per_square']==0].groupby('NEIGHBORHOOD').size()
allsale2 = price.groupby('NEIGHBORHOOD')['dollar_per_square'].size()
ratio2 = nosale2 / allsale2
ratio2 = ratio2.nlargest(10).to_frame(name="ratio")
ratio2


# # What is top 10 building class category that have highest ratio of 0 sale price?

# In[9]:


nosale3 = price.loc[price['dollar_per_square']==0].groupby('BUILDING CLASS CATEGORY').size()
allsale3 = price.groupby('BUILDING CLASS CATEGORY')['dollar_per_square'].size()
ratio3 = nosale3 / allsale3
ratio3 = ratio3.nlargest(10).to_frame(name="ratio")
ratio3


# # Is there pattern of selling days or months?

# In[10]:


date = df.iloc[:,-1:]
date['SALE DATE'] = pd.to_datetime(df['SALE DATE'], errors='coerce')
date.head()


# In[11]:


date['weekday'] = date['SALE DATE'].dt.dayofweek
date['month'] = date['SALE DATE'].dt.month
date['count'] = 1
date.head()


# In[12]:


date_pivot = date.pivot_table(index='weekday', columns='month', values='count',aggfunc=np.sum)


# In[13]:


sns.heatmap(date_pivot,cmap="YlGnBu",linewidths=.2);


# # What is distruibution of year's selling?

# In[14]:


price['YEAR BUILT'] = price['YEAR BUILT'].astype(int)
year = price.groupby('YEAR BUILT',as_index=False)['dollar_per_square'].mean()
f, ax = plt.subplots(1,2,figsize=(16,30))
sns.countplot(y = 'YEAR BUILT', data = price, orient = 'h',ax=ax[0])
sns.barplot(y = 'YEAR BUILT', x = 'dollar_per_square', data = year, orient = 'h',ax=ax[1]);



####
