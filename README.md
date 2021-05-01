# py-hostelworld
> Unofficial hostelworld API created using REST endpoints and some creativity.

## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Status](#status)
* [Contact](#contact)

## General info
Over the last week, I have been working on a hostelworld/airbnb/booking.com aggregatator as I am building a web service that lets you find the cheapest accomodation close to your gps location (or set location). Personally, I love hostels. They're the best options for solo backpackers as they're as cheap as they can get, but, more importantly and more often than not, they are filled with likeminded people who are looking for the next adventure. In my second solo trip to South East Asia, I literally jumped between 20 different hostels in 35 days. Why so many in such short time? I wanted to check out as many hostels as possible so that during my next 'perfect' trip, I would know which palaces to go back to and which ones to avoid. Nevertheless, all of them were unique in their own way.
Me being me, it is only natural that I would look into how many actual hostels are out there and analyse the data to see if I can gain some useful insights. Building this API is hte first step of that process.

## Technologies
The code is written in python comprinsing a collection of REST calls.

## Setup
- After cloning the repo. pip install the requirements.txt.
- Following the above changes, you can execute the script via terminal: python main.py

## Usage Examples
Instantiate the class
```python
hw = Hostelworld()
```
Show me all the hostels in South Africa
```python
hw.get_hostel_by_country_name('South Africa')
```
![HostelByCountryName](imgs/get_hostel_by_country_name.png)

Show me all the hostels in Hanoi
```python
hw.get_hostel_by_country_name('South Africa')
```
![HostelByCountryName](imgs/get_hostel_by_country_name.png)


## Features
List of features ready and TODOs for future development
* Awesome feature 1
* Awesome feature 2
* Awesome feature 3

To-do list:
* Search Hostels per
* Check availability per hostels defined city
* Update package to pypi.org

## Status
Project is: _in progress_



