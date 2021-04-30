
import numpy as np
from hostelworld_utils import json_parser

class Hostelworld:
    
    def __init__(self):
        
        self.last_city = pd.DataFrame()
        self.last_country = pd.DataFrame()
        self.search_history = []
        self.search_history_values = []
        self.list_places_ids = pd.read_csv('places_id_hostel_world.csv',index_col='id')
        
    def get__hostel_by_city_name(self,city_name):
        potential_id = [] #list_places_ids may contain multiple places called london with no listings. We get all the potentials, then we only keep the good ones
        real_ids = []
        tmp_l1 = self.list_places_ids[self.list_places_ids.name.str.lower().str.replace(' ','')==city_name.lower().replace(' ','')].index.to_list()
        #tmp_l2 = list_places_ids[self.list_places_ids.name.str.lower().replace(' ','')==city_name.lower().replace(' ','')].index.to_list()
        potential_id = list(set(tmp_l1))
        
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
            self.search_history.append(' get__hostel_by_city_name()## Searched for {} . Number results: {}'.format(city_name,complete_df.shape[0]))
            return self.last_city
        
        elif len(real_ids)==0:
            print('No hostels were found for "{}".'.format(city_name))
            self.search_history.append(' get__hostel_by_city_name()## Searched for {} . No results found'.format(city_name))

    def get_hostel_by_country_name(self,country_name):
        tmp_l1 = self.list_places_ids[self.list_places_ids.country.str.lower().str.replace(' ','')==country_name.lower().replace(' ','')].index.to_list()
        real_ids = list(set(tmp_l1))
        if len(real_ids)==0:
            print('Sorry, we have not found any results for {}.'.format(country_name))
        complete_df = pd.DataFrame()
        for idx in real_ids[15:]:
            url = 'https://api.m.hostelworld.com/2.2/cities/{}/properties'.format(idx)
            r = requests.get(url)
            data = r.json()
            complete_df = pd.concat([complete_df,json_parser(data)])
        complete_df = complete_df.fillna(0)
        self.last_country=complete_df
        self.search_history_values.append(self.last_country)
        self.search_history.append('get_hostel_by_country_name()## Searched for {} . Number results: {}'.format(country_name,complete_df.shape[0]))
        return complete_df

    def _describe_last_city(self):
        try:
            return self.last_city.describe()
        except ValueError as e:
            print('It doesn\'t loook like you\'ve searched for a City yet.\nCall one of the other methods to search for a city and then you can use this method :)')
    
    def __describe_last_country():
        pass
    
if __name__ == "__main__":
    hw = Hostelworld()
    print(hw.get__hostel_by_city_name('Acireale').shape)
    print(hw.search_history)
