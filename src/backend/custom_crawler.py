from bs4 import BeautifulSoup

class CustomCrawler():

    # Constructor method 
    def __init__(self):
        self.__resultsArray = None

    # Return last results
    def getArrayResults(self) -> list|None:
        return self.__resultsArray
    
    # Initiate beautiful shop to parse html
    def parseHTML(self, dataToParse) -> None:
        soup = BeautifulSoup(dataToParse, "html.parser")
        self.__resultsArray = self.__crawlData(soup) 

    ########## Private methods

    # Get the first 30 entries with title, rank, score and comments
    def __crawlData(self, soupObject):
        web_array = []
        for item in soupObject.find_all("tr", {"class" : "athing"}, limit=30):
            entry_title = self.__setTitleAndRank(item)
            entry_info = self.__score_and_comments(item)
            entry_title.update(entry_info)
            web_array.append(entry_title)
        return web_array

    # Get the title and rank
    def __setTitleAndRank(self, item):
        item_info = item.find_all("span", class_= ["rank", "titleline"])
        rank = self.__parseData(item_info[0].text, "rank")
        title = item_info[-1].find("a").text
        return {'rank': rank, "title" : title}

    # Get the score and comments
    def __score_and_comments(self, item):
        item_info = item.next_sibling.find("span", {"class" : "subline"})
        if(item_info == None):
            return {"score" : 0, "comments" : 0}
        item_info = item_info.find_all(["span", "a"])
        score = self.__parseData(item_info[0].text, "score")
        comments = self.__parseData(item_info[-1].text, "comments")
        return {"score" : score, "comments" : comments}
    
    # Parse rank, score and comments from original HTML to data
    def __parseData(self, value: str, parser: str) -> int:
        try:
            match parser:
                case "rank":
                    unparsedValue = value.split(".")[0]
                    parsedValue = int(unparsedValue)
                case "score":
                    unparsedValue = value.split(" ")[0]
                    parsedValue = int(unparsedValue)
                case "comments":
                    value
                    unparsedValue = value.split('\xa0')[0]
                    parsedValue = int(unparsedValue)
        except Exception:
            return 0
        else:
            return parsedValue
    