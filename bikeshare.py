#Version 1.1 : Developed by Maverics on 17th May 2018
#Editted on 21st May 2018

#Importing Libraries
import pandas as pd
import datetime as dt
import numpy as np
import time as t

def main():
    again='yes'
    while again=='yes':
        print("Hello! Let's explore some US bikeshare data!")
        city = input("Would to like to see data for Chicago, New York, Washington : \n")
        city=city.lower()
        filtertype=input("would you like to filer by 'month' , 'day' of week , 'both' or not at all  Type 'none' for no filter : \n")
    
        month=0
        day=0
        
        if filtertype=='month':
            month=input("which Month: January February March April May or June : \n")
            month=month.lower()        
        elif filtertype=='day':
            day=input("which Day: Please give as integer (e.g. 1=Sunday) :\n")
        elif filtertype=='both':
            month=input("which Month: January February March April May or June : \n")
            month=month.lower()
            day=input("which Day: Please give as integer (e.g. 1= Monday) : \n")
            
        df=filter_data_frame(city,month,day)
        time_stats(df,filtertype)
        station_stats(df)
        user_stats(df)
        trip_duration_stats(df)
        dataview=input("\n Want to view few of Data : 'yes or no' \n")
        dataview=dataview.lower()
        while dataview=='yes':
            print(df.sample(5))
            dataview=input("\n Want to view few of Data : 'yes or no' \n")
        again=input("\n Do you want to again \n")
        again=again.lower()
	
def filter_data_frame(city,month,day):
    citydata={'chicago':'chicago.csv', 'new york':'new_york_city.csv', 'washington':'washington.csv'}
    df=pd.read_csv(citydata[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']=df['Start Time'].dt.month
    df['day']= df['Start Time'].dt.weekday
    df['dayee']= df['Start Time'].dt.weekday_name
    if month!='all' and month!=0:
        months={'january':1,'february':2,'march':3,'april':4,'may':5,'june':6}
        mon=months[month]
        df=df[df['month']==mon]
    if day!='all' and day!=0:
        df=df[df['day']==(int(day)-1)]
    return df

def time_stats(df,filtertype):
    """Displays statistics on the most frequent times of travel."""
    print('-'*40)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = t.time()
    print("Calculating the first statistics")
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['hour']=df['Start Time'].dt.hour
    phour= df['hour'].mode()[0]
    pcount=df['hour'].value_counts().max()
    print(("Most Popular Hour: {}, Count: {}, Filter: {} ").format(phour,pcount,filtertype))
    print("\nThis took %s seconds." % (t.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = t.time()
    pstartst=df['Start Station'].mode()[0]
    pendst=df['End Station'].mode()[0]
    df_gp=df.groupby(['Start Station','End Station']).size().reset_index(name='counts').sort_values(by='counts',ascending=False).head(1)[['Start Station','End Station']]
    df_gp["period"] = df_gp["Start Station"]+ "  to  "+ df_gp["End Station"]
    pcombo=df_gp['period'].iloc[0]
    print(("Most Popular Start Station: {},\n End Station : {},\n Start-End Combo: {} ").format(pstartst,pendst,pcombo))
    print("\nThis took %s seconds." % (t.time() - start_time))
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = t.time()
    print("User types Info : ")
    print(df['User Type'].value_counts().reset_index(name='counts').to_string(index=False,header=None))
    print("\nGender types Info : ")
    print(df['Gender'].value_counts().reset_index(name='counts').to_string(index=False,header=None))
    earliest=df['Birth Year'].min()
    mostrecent=df['Birth Year'].max()
    mmostcommon=df['Birth Year'].mode()
    print(("\nEarliest Year: {} \nMost Recent Year : {} \nMost Common Year : {}").format(int(earliest),int(mostrecent),int(mmostcommon)))
    print("\nThis took %s seconds." % (t.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = t.time()
    total_tsum=df['Trip Duration'].sum()
    print("\nTotal travel time : {}".format(total_tsum))
    mean_ttime=df['Trip Duration'].mean()
    print("\nMean travel time : {}".format(mean_ttime))
    print("\nThis took %s seconds." % (t.time() - start_time))
    print('-'*40)

main()
