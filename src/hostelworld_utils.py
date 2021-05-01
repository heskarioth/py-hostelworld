
import pandas as pd
import numpy as np

def check_json_value(json_response,key_response):
    """ Helper function to check if json_response has expected value"""
    dict_parsed = {}
    try:
        dict_parsed[key_response] = json_response[key_response]
    except KeyError as k:
        dict_parsed[key_response] = 0
    return dict_parsed[key_response]


def json_parser(data):
    body_len = data['pagination']['totalNumberOfItems']
    body = data['properties']
    complete_df = pd.DataFrame()
    for idx in range(body_len):
        #pp.pprint(body[idx].keys())
        tmp_dict = {
         'id' :body[idx]['id']
         , 'name':body[idx]['name']
            ,'CityName':data['location']['city']['name']
         ,'Country':data['location']['city']['country']
         ,'Region':data['location']['region']['name'] if data['location']['region'] is not None else data['location']['region']
         , 'isPromoted':body[idx]['isPromoted']
         , 'hbid':body[idx]['hbid']

         , 'starRating':body[idx]['starRating']
         , 'overallRating_overall': body[idx]['overallRating']['overall'] if body[idx]['overallRating'] is not None else np.nan
         , 'overallRating_NumberOfRatings':body[idx]['overallRating']['numberOfRatings'] if body[idx]['overallRating'] is not None else np.nan
         , 'ratingBreakdown_ratingsCount':body[idx]['ratingBreakdown']['ratingsCount'] if body[idx]['overallRating'] is not None else np.nan
         , 'ratingBreakdown_security':body[idx]['ratingBreakdown']['security']
         , 'ratingBreakdown_location':body[idx]['ratingBreakdown']['location']
         , 'ratingBreakdown_staff':body[idx]['ratingBreakdown']['staff']
         , 'ratingBreakdown_fun':body[idx]['ratingBreakdown']['fun']
         , 'ratingBreakdown_clean':body[idx]['ratingBreakdown']['clean']
         , 'ratingBreakdown_facilities':body[idx]['ratingBreakdown']['facilities']
         , 'ratingBreakdown_value':body[idx]['ratingBreakdown']['value']
         , 'ratingBreakdown_average':body[idx]['ratingBreakdown']['average']
         , 'latitude':body[idx]['latitude']
         , 'longitude':body[idx]['longitude']
         , 'isFeatured':body[idx]['isFeatured']
         , 'type':body[idx]['type']
         , 'address1':body[idx]['address1']
         , 'address2':body[idx]['address2']
         , 'freeCancellationAvailable':body[idx]['freeCancellationAvailable']
         , 'freeCancellationAvailableUntil':body[idx]['freeCancellationAvailableUntil']
         , 'district':body[idx]['district']['name'] if body[idx]['district'] is not None else body[idx]['district']
         , 'lowestPricePerNight':body[idx]['lowestPricePerNight']['value']
         , 'lowestPrivatePricePerNight': body[idx]['lowestPrivatePricePerNight']['value'] if isinstance(body[idx]['lowestPrivatePricePerNight'],dict) else body[idx]['lowestPrivatePricePerNight']
         , 'lowestDormPricePerNight':body[idx]['lowestDormPricePerNight']['value'] if isinstance(body[idx]['lowestDormPricePerNight'],dict) else body[idx]['lowestDormPricePerNight']
         , 'lowestAveragePricePerNight':body[idx]['lowestAveragePricePerNight'] if isinstance(body[idx]['lowestAveragePricePerNight'],dict) else body[idx]['lowestAveragePricePerNight']
         , 'lowestAverageDormPricePerNight':body[idx]['lowestAverageDormPricePerNight'] if isinstance(body[idx]['lowestAverageDormPricePerNight'],dict) else body[idx]['lowestAverageDormPricePerNight']
         , 'lowestAveragePrivatePricePerNight':body[idx]['lowestAveragePrivatePricePerNight'] if isinstance(body[idx]['lowestAveragePrivatePricePerNight'],dict) else body[idx]['lowestAveragePrivatePricePerNight']
         , 'isNew':body[idx]['isNew']
         , 'overview':body[idx]['overview']
         , 'isElevate':body[idx]['isElevate']
         , 'hostelworldRecommends':body[idx]['hostelworldRecommends']
         , 'position':body[idx]['position']
         , 'hwExtra':body[idx]['hwExtra']
         , 'fabSort':body[idx]['fabSort']['rank1']
         , 'veryPopular': check_json_value(body[idx],'veryPopular')
         #, 'rooms_privates': 0 if len(body[idx]['rooms']['privates'])>0 else len(body[idx]['rooms']['privates'])
         #, 'rooms_dorms': 0 if len(body[idx]['rooms']['dorms'])>0 else len(body[idx]['rooms']['dorms'])
        }
        size = len(body[idx]['facilities'])
        facilities = {}
        for category in range(size):
            category_type = body[idx]['facilities'][category]['id'].replace('FACILITYCATEGORY','')
            for item in (body[idx]['facilities'][category]['facilities']):
                facilities['{}_{}'.format(category_type,item['id'])]=1
        tmp_dict.update(facilities)
        complete_df = pd.concat([complete_df,pd.DataFrame(tmp_dict,index=[0])])
        complete_df = complete_df.fillna(0)
    return complete_df


def parse_review_apiurl(data):
    n_reviews_current_page = len(data['reviews'])
    df_reviews = pd.DataFrame()
    for idx in range(n_reviews_current_page):
        base = data['reviews'][idx]
        tmp_dict = {
         'review_id' : base['id']
         ,'date_stay':base['date']
         ,'notes':base['notes']
         #,'ownerComment':base['ownerComment']
         ,'disliked':base['disliked']
         ,'liked':base['liked']
         #,'groupInformation_age':base['groupInformation']['age']
         #,'groupInformation_groupTypeCode':base['groupInformation']['groupTypeCode']
         ,'groupInformation_tripTypeCodes':base['groupInformation']['tripTypeCodes']
         ,'rating_atmosphere':base['rating']['atmosphere']
         ,'rating_cleanliness':base['rating']['cleanliness']
         ,'rating_facilities':base['rating']['facilities']
         ,'rating_location':base['rating']['location']
         ,'rating_overall':base['rating']['overall']
         ,'rating_safety':base['rating']['safety']
         ,'rating_staff':base['rating']['staff']
         ,'rating_value':base['rating']['value']
         ,'recommended':base['recommended']
        }
        df_reviews = pd.concat([df_reviews,pd.DataFrame(tmp_dict,index=[0])])
    return df_reviews

def parse_review_get_request(data):
    n_reviews_current_page = len(data['reviews'])
    df_reviews = pd.DataFrame()
    for idx in range(n_reviews_current_page):
        base = data['reviews'][idx]
        tmp_dict = {
         'review_id' : base['id']
         #,'notes':base['notes']
         ,'ownerReply':base['ownerReply']
         ,'reviewer_ageGroup': base['reviewer']['ageGroup']
         ,'reviewer_gender': base['reviewer']['gender']
         ,'reviewer_id': base['reviewer']['id']
         ,'reviewer_nationality' : base['reviewer']['nationality']
         ,'reviewer_rank': base['reviewer']['rank']
         ,'reviewer_totalReviews':base['reviewer']['totalReviews']
         ,'reviewer_username':base['reviewer']['username']
         ,'summary_keyword': base['summary']['keyword']
         ,'summary_overall': base['summary']['overall']
         ,'summary_status': base['summary']['status']
         #,'summary_stayed': base['summary']['stayed']
        }
        df_reviews = pd.concat([df_reviews,pd.DataFrame(tmp_dict,index=[0])])
    return df_reviews
