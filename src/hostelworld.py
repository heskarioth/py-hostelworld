import pandas as pd
import numpy as np
from hostelworld_utils import json_parser,parse_review_apiurl,parse_review_get_request
import requests 


class Hostelworld:
    
    def __init__(self):
        
        self.last_city = pd.DataFrame()
        self.last_country = pd.DataFrame()
        self.search_history = []
        self.search_history_values = []
        self.list_places_ids = pd.read_csv('places_id_hostel_world.csv',index_col='id')
        
    def get__hostel_by_city_name(self,city_name):
        real_ids = []
        potential_id = list(set(self.list_places_ids[self.list_places_ids.name.str.lower().str.replace(' ','')==city_name.lower().replace(' ','')].index.to_list()))
        
        for idx in potential_id:
            url = 'https://api.m.hostelworld.com/2.2/cities/{}/properties'.format(idx)
            r = requests.get(url)
            data = r.json()
            if len(data['properties'])>0:
                real_ids.append(idx)
        
        if len(real_ids)>1:
            country_name = list_places_ids[self.list_places_ids.index.isin(real_ids)]['country'].values.tolist()
            country_name = ', '.join(country_name)
            print('There\'s more than one city called {}. These are in {}. Please specify also country name and use get__hostel_by_city_name_multiple_locations to get response from the preferred location.\nIf you want to show all places corresponding to chosen city, regardless of Country, then use (city_name, None) as params for the function.'.format(city_name,country_name))
            self.search_history.append(' get__hostel_by_city_name()## Searched for {} . Found multiple results across different countries. Search again using __get__hostel_by_city_name_multiple_locations'.format(city_name))
        
        elif len(real_ids)==1:
            url = 'https://api.m.hostelworld.com/2.2/cities/{}/properties/?currency=GBP&application=web&user-id=8f74a954-453f-4197-ab17-d46f753b0854&num-nights=1&guests=1&per-page=1000&show-rooms=1&property-num-images=30'.format(real_ids[0])
            r = requests.get(url)
            data = r.json()
            print(' {} hostels found in {}.'.format(len(data['properties']),city_name))
            self.last_city = json_parser(data)
            self.search_history_values.append(self.last_city)
            self.search_history.append(' get__hostel_by_city_name()## Searched for {} . Number results: {}'.format(city_name,self.last_city.shape[0]))
            return self.last_city
        
        elif len(real_ids)==0:
            print('No hostels were found for "{}".'.format(city_name))
            self.search_history.append(' get__hostel_by_city_name()## Searched for {} . No results found'.format(city_name))

    def get_hostel_by_country_name(self,country_name):
        #tmp_l1 = 
        real_ids = list(set(self.list_places_ids[self.list_places_ids.country.str.lower().str.replace(' ','')==country_name.lower().replace(' ','')].index.to_list()))
        if len(real_ids)==0:
            print('Sorry, we have not found any results for {}.'.format(country_name))
        complete_df = pd.DataFrame()
        print_message = False
        for idx in real_ids:
            url = 'https://api.m.hostelworld.com/2.2/cities/{}/properties'.format(idx)
            r = requests.get(url)
            data = r.json()
            complete_df = pd.concat([complete_df,json_parser(data)])
            print_message = True
        complete_df = complete_df.fillna(0)
        if print_message:
            print('{} hostels found in {}.'.format(complete_df.shape[0],country_name))
        self.last_country=complete_df
        self.search_history_values.append(self.last_country)
        self.search_history.append('get_hostel_by_country_name()## Searched for {} . Number results: {}'.format(country_name,complete_df.shape[0]))
        return complete_df

    
    def get__hostel_by_city_name_multiple_locations(self,city_name,country_name=None):
        if country_name!=None:
            real_ids = self.list_places_ids[(self.list_places_ids.country.str.lower().str.replace(' ','')==country_name.lower().replace(' ','')) & (self.list_places_ids.name.str.lower().str.replace(' ','')==city_name.lower()).replace(' ','')].index.to_list()
        else:
            real_ids = self.list_places_ids[(self.list_places_ids.name.str.lower().replace(' ','')==city_name.lower()).replace(' ','')].index.to_list()
        country_name = 'all available countries' if country_name==None else country_name
        if len(real_ids)==0:
            #print('Sorry, we have not found any results for {} - {}.'.format(city_name,country_name))
            self.search_history.append('get_hostel_by_country_name()## Sorry, we have not found any results for {} - {}.'.format(city_name,country_name))
            return 'Sorry, we have not found any results for a city called {} in {}.'.format(city_name,country_name)
        else:    
            complete_df = pd.DataFrame()
            for idx in real_ids:
                url = 'https://api.m.hostelworld.com/2.2/cities/{}/properties'.format(idx)
                r = requests.get(url)
                data = r.json()
                complete_df = pd.concat([complete_df,json_parser(data)])
            complete_df = complete_df.fillna(0)
            self.last_city = complete_df
            self.search_history_values.append(self.last_city)
            
            self.search_history.append('get__hostel_by_city_name_multiple_locations()## Searched for {} in {} . Number results: {}'.format(city_name,country_name,complete_df.shape[0]))        
            return complete_df

    
    def get_hostel_review_by_hostel_id(self,hostel_id):
        
        """
        There are two different endpoint calls we can use to get hostel reviews. Each response object will have different attributes
        compared to the other one. Here we capture them both, we combine them and return a single dataframe with all the info per 
        review.
        We call first extraction api url
        We call second request get request
        """
    
        def get_review_data_from_endpoint(url,base_url,api_url=True):
            df_reviews = pd.DataFrame()
            headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
            r = requests.get(url,headers=headers)
            data = r.json()
            try:
                n_pages = data['pagination']['numberOfPages']
                if n_pages>0:
                    if api_url==True:
                        df_reviews = parse_review_apiurl(data)
                    else:
                        df_reviews = parse_review_get_request(data)
                    for page in range(1,n_pages):
                        next_href = data['pagination']['next']
                        if next_href is None:
                            break
                        r = requests.get(base_url+next_href,headers=headers)
                        data = r.json()
                        if api_url==True:
                            df_reviews = pd.concat([df_reviews,parse_review_apiurl(data)])
                        else:
                            df_reviews = pd.concat([df_reviews,parse_review_get_request(data)])
            except IndexError:
                print('No reviews available for hostel ID: {}'.format(hostel_id))
            return df_reviews

        url = 'https://api.m.hostelworld.com/2.2/properties/{}/reviews/?sort=newest&allLanguages=true&page=1&monthCount=36&application=web'.format(hostel_id)
        base_url = 'https://api.m.hostelworld.com/2.2/'
        df_reviews_apiurl = get_review_data_from_endpoint(url,base_url,api_url=True)

        url="https://www.hostelworld.com/properties/{}/reviews?sort=newest&allLanguages=False&page=1&monthCount=36".format(hostel_id)
        base_url = 'https://www.hostelworld.com/'
        df_reviews_get_reviews = get_review_data_from_endpoint(url,base_url,api_url=False)

        df_reviews = df_reviews_get_reviews.merge(df_reviews_apiurl,left_on=['review_id'],right_on=['review_id'])
        self.search_history.append('get_hostel_review_by_hostel_id()## Searched for Hostel ID:{}. Number reviews: {}'.format(hostel_id,df_reviews.shape[0]))        
        self.search_history_values.append(df_reviews)
        
        return df_reviews
    
    
    
    
    
    
    def _describe_last_city(self):
        try:
            return self.last_city.describe()
        except ValueError as e:
            print('It doesn\'t loook like you\'ve searched for a City yet.\nCall one of the other methods to search for a city and then you can use this method :)')
    
    def __describe_last_country():
        pass
    
    
    
    
    
if __name__ == "__main__":
    hw = Hostelworld()
