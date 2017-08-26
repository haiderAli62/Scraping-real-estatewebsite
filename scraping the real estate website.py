import requests
from bs4 import BeautifulSoup
import pandas

source = requests.get(r"http://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")

soup = BeautifulSoup(source.content , "html.parser")

find_pages = soup.find_all("a" , class_ = "Page")
pages = find_pages[-1].text
base_url = "http://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
li = []
for i in range(0,int(pages)*10,10):
    s = base_url+str(i)+".html"
    new_src = requests.get(s)
    soup = BeautifulSoup(new_src.content , "html.parser")
    for div in soup.find_all("div" , class_ = "propertyRow"):
        details = {}
        details["Price"] = div.find("h4").text.replace("\n","").replace(" ","")
        details["Address"] = div.find_all("span" , class_ ="propAddressCollapse")[0].text
        details["Locality"] = div.find_all("span" , class_ ="propAddressCollapse")[1].text
        try:
            details["Bed"] = div.find("span" , class_ = "infoBed").find("b").text
        except:
           details["Bed"] = None

        try:
           details["Bath"] = div.find("span" , class_ = "infoValueFullBath").find("b").text
        except:
             details["Bath"] = None

        try:
            details["Area"] = div.find("span" , class_="infoSqFt").find("b").text
        except:
           details["Area"] = None
        li.append(details)

df = pandas.DataFrame(li)
df.to_csv("details.csv")
#print(len(li))




            
