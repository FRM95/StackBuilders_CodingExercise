Coding exercise (Stack Builders application process)
===================================
Hey! Welcome to my Stack Builders coding exercise.

## Objective
The main objective related to this exercise is: Using the language that you feel most proficient in, create a web crawler using scraping techniques to extract the first 30 entries from https://news.ycombinator.com/. You'll only care about the number, the title, the points, and the number of comments for each entry.

Also, a couple of filtering operations were needed:
* Filter all previous entries with more than five words in the title ordered by the number of comments first.
* Filter all previous entries with less than or equal to five words in the title ordered by points.

When counting words, consider only the spaced words and exclude any symbols. For instance, the phrase “This is - a self-explained example” should be counted as having 5 words. 

The solution should store usage data, including at least the request timestamp and a field to identify the applied filter. You are free to include any additional fields you deem relevant to track user interaction and crawler behavior. The chosen storage mechanism could be a database, cache, or any other suitable tool.

## Solution
Implemented a basic Flask-app solution to crawl data from the endpoint. Data storage is implemented based on flask-cache library.

The Flask-app contains multiple endpoints, mostly related to exercise operations like downloading (crawling data), filtering data, saving data, and displaying results.
In addition to that, I've built some JS methods to enable UX/UI functionalities.

Btw: I'm sorry for the UI interface, I couldn't build something better with that much time :pensive:

## Installation

Clone this repository. 

- Build the docker image with the next command (you'll need to have Docker on your machine):

		docker build -t app-flask .
  
- Run the image with the next command:

		docker run -p 5000:5000 app-flask

After deploying the docker container, access the app in the http://127.0.0.1:5000 url.

## Usage

#### Request new data (big one blue) by clicking on 'Request new data' button.
<img src="https://github.com/user-attachments/assets/acb17555-3953-4cd8-95a8-ea4fd5755c48" alt="drawing" width="600"/>

#### Crawled data will be displayed.
<img src="https://github.com/user-attachments/assets/65d3cad3-648f-45aa-9837-43aaf1cb215e" alt="drawing" width="600"/>

#### Press 'Apply filter 1/Apply filter 2' buttons to apply your desired option. Click on 'Show original data' to reset the filter and get back to your crawled data.
<img src="https://github.com/user-attachments/assets/41fb35c2-b4cb-4920-8d83-64d3baa59c40" alt="drawing" width="600"/>

#### Save your crawled data by clicking on 'Save data' button.
<img src="https://github.com/user-attachments/assets/64e1b42d-780c-4ce1-ba2b-a09cd1e3aca7" alt="drawing" width="500"/>

## Storage

As said before, data is stored using Flask-Cache 'FileSystemCache' system file. With a threshold of 100 items (capacity) and a default timeout of 600 seconds.
Cached files are saved in a folder called 'tmp', which follows this path: 'app/src/tmp' in the app container.

## Thanks to the HR/Technical team
Thank you so much for giving me this challenge. It was a pleasure to create this solution for such a creative coding exercise. :blush:
  
