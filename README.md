# Web-Crawler
Python codes that together perform the data extraction process of a certain site(craigslist) and store it in Mongo.

<br>

## Details
first we do a get on our desired URL with requests library and then, parse it using beautifulsoup (from bs4 library)
at last , we have diffrent options for saving these results : 1- as a JSON file in local storage 2- in MongoDB

<br>

### Mainly used libraries
```
pip install requests, bs4
```
