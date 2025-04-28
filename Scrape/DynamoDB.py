from Amazon import findProduct
from datetime import datetime

#'Model', 'Brand', 'VRAM', 'Price', 'Date', 'Link', 'Title'
def uploadDailyAverage(dailyModelData):
    
    Model = dailyModelData[0]["Model"]
    Date = str(datetime.today())
    NumListings = len(dailyModelData)
    AvgPrice = sum(item["Price"] for item in dailyModelData) / NumListings


def uploadRawListings(dailyModelData):

    dailyModelData.sort(key=lambda item: item["Price"])
    cheapest3 = dailyModelData[:3]

# avg = uploadDailyAverage(findProduct("RTX 5070"))

# print(avg)