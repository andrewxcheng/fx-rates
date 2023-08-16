import pandas as pd 
import requests
from seleniumrequests import Chrome
import json
import yfinance as yf

#Set-up: These lines set up the code and underlying assumptions
YJSESSIONID = ""
ak_bmsc = ""
baseccys = {"USA":"USD","CAN":"CAD","AUS":"AUD","GBR":"GBP"}
country_dict = {"CAN":{"CHN":"CNY","IND":"INR","USA":"USD","KOR":"KRW","HKG":"HKD","TWN":"TWD","TUR":"TRY","JPN":"JPY","PAK":"PKR","NGA":"NGN","IDN":"IDR","VNM":"VND","SAU":"SAR","BGD":"BDT","MYS":"MYR"},
                "AUS":{"CHN":"CNY","IND":"INR","NPL":"NPR","BRA":"BRL","VNM":"VND","ARE":"AED","KOR":"KRW","COL":"COP","IDN":"IDR","THA":"THB","HKG":"HKD","ZAF":"ZAR","FRA":"EUR","JPN":"JPY","USA":"USD"},
                "GBR":{"CHN":"CNY","IND":"INR","SAU":"SAR","CAN":"CAD","VNM":"VND","JPN":"JPY","BRA":"BRL","MEX":"MXN","USA":"USD","TUR":"TRY","FRA":"EUR","IDN":"IDR","ARE":"AED","SGP":"SGD","ZAF":"ZAR"},
                "USA":{"CHN":"CNY","IND":"INR","SAU":"SAR","CAN":"CAD","VNM":"VND","JPN":"JPY","BRA":"BRL","MEX":"MXN","GBR":"GBP","TUR":"TRY","FRA":"EUR","IDN":"IDR","ARE":"AED","SGP":"SGD","ZAF":"ZAR"}}
df = pd.DataFrame(columns=["CCY","500-Rate","MktRate","CompRate","Margin", "Method"])

#Function 1: when this function is called, it opens Convera and obtains all the schools available for a select country (USA, Canada, UK, AUS, etc.)
def start_up_convera(country_code):

    #following section opens Convera with chrome
    driver = Chrome()
    driver.get("https://students.convera.com/") #uses Selenium to open the Convera home webpage

    #following section obtains a list of cookies from Convera
    cookie = {l["name"]: l["value"] for l in driver.get_cookies()} #from the Convera page, takes the cookies to be used as keys for the following pages

    #following section stores the required cookies to access the next page
    ak_bmsc = cookie["ak_bmsc"] #obtains the ak_bmsc cookie, which is required to query the other pages
    YJSESSIONID = cookie["JSESSIONID"] #obtains the JSESSIONID cookie, which is required to query the other pages

    #following section opens the next page of Convera with the country code
    url_school = "https://students.convera.com/geo-buyer/services/institution/"+country_code #sets the next query's webpage to be the country-page, to obtain the list of schools for a given country
    headers_school = {"Accept": "application/json, text/plain, */*",
                      "Accept-Encoding": "gzip, deflate, br",
                      "Accept-Language": "en-US,en;q=0.9",
                      "Cookie": "JSESSIONID="+YJSESSIONID+"; "
                                "LANG=en_GB; "
                                "ak_bmsc="+ak_bmsc+"; "
                                "CookiesAccepted=true; "
                                "QuantumMetricSessionID=ce18dd359df32c2323244a0bc97f9ab3; "
                                "QuantumMetricUserID=1dfb44c270c9b0bbbc656a1e33c48c8b; "
                                "AWSALBTGCORS=tHjXtcsUfKgK304sUBbU0Szl72T7yluiSlW7rARSjPhbliNWV7td3bLc5E4fzGz6pd2+naiManNYT4A3Pv3gofmV5D6ACekI6Mv9zwX/OH4RI+N1LmZf8/dcgX1n65HOLK060zbS+SlQuf6r6yzpFW55mADMcTO2LRKZZFMuim3FQN7FBIQ=; "
                                "AWSALBCORS=MdBGoZz3Bt8VMJVoH7ANnnAqm4T0Y1ZWvVMp/RkaAV3k0ixL3Ut+CkZJPWBiP3RMByzkSZizL2K5oh4mCBhn4Sh5P96CX7le+jCxEi4Phh2pQwPkxg2Q7QqyynAP; "
                                "bm_sv=EF0B994B316BBB3F120C69C9C5FDAC09~YAAQDsR7aEQqEhOJAQAA/FRNZRQYu33iw81SlfFHMwdgGngCtQ49k+VgC+Vqbc3qIY9bCOvV/YjPtzPkBzcuwHQdlnoonmR+KI5wfIldb9DKeFfZGG3/ZGKP3YwJQFXCmXlIjNncC8dCMCF7YZDMx1MrwHVbixTDAoMJ1EAvMZ296SMLcDRoMyxq5A93nrziu2fR7HljoftVkG30sD+5XkHXdc4iWsP8caNP65GplfcX4aw2xrcweAESq1Kz5rK42Cs=~1	",
                    "Referer":"https://students.convera.com/"}

    #loads the list of available schools as a Python dictionary
    school_json = requests.get(url_school,headers=headers_school).text #obtains the json file of schools from the website
    school_dict = json.loads(school_json)["sellers"] #loads in the json file as a Python dictionary

    #creates list of schools
    school_list = []
    for school in school_dict:
        school_list.append(school["name"])

    #function outputs the list of schools
    return(school_list)

#Function 2: given a confirmed school name, output the currency pairs 
def find_school(country_code,school_name):
    
    #Page 1
    #following section sets up the next page to be queried 
    url_school = "https://students.convera.com/geo-buyer/services/institution/"+country_code
    headers_school = {"Accept": "application/json, text/plain, */*",
                      "Accept-Encoding": "gzip, deflate, br",
                      "Accept-Language": "en-US,en;q=0.9",
                      "Cookie": "JSESSIONID="+YJSESSIONID+"; "
                                "LANG=en_GB; "
                                "ak_bmsc="+ak_bmsc+"; "
                                "CookiesAccepted=true; "
                              "QuantumMetricSessionID=ce18dd359df32c2323244a0bc97f9ab3; "
                                "QuantumMetricUserID=1dfb44c270c9b0bbbc656a1e33c48c8b; "
                                "AWSALBTGCORS=tHjXtcsUfKgK304sUBbU0Szl72T7yluiSlW7rARSjPhbliNWV7td3bLc5E4fzGz6pd2+naiManNYT4A3Pv3gofmV5D6ACekI6Mv9zwX/OH4RI+N1LmZf8/dcgX1n65HOLK060zbS+SlQuf6r6yzpFW55mADMcTO2LRKZZFMuim3FQN7FBIQ=; "
                                "AWSALBCORS=MdBGoZz3Bt8VMJVoH7ANnnAqm4T0Y1ZWvVMp/RkaAV3k0ixL3Ut+CkZJPWBiP3RMByzkSZizL2K5oh4mCBhn4Sh5P96CX7le+jCxEi4Phh2pQwPkxg2Q7QqyynAP; "
                                "bm_sv=EF0B994B316BBB3F120C69C9C5FDAC09~YAAQDsR7aEQqEhOJAQAA/FRNZRQYu33iw81SlfFHMwdgGngCtQ49k+VgC+Vqbc3qIY9bCOvV/YjPtzPkBzcuwHQdlnoonmR+KI5wfIldb9DKeFfZGG3/ZGKP3YwJQFXCmXlIjNncC8dCMCF7YZDMx1MrwHVbixTDAoMJ1EAvMZ296SMLcDRoMyxq5A93nrziu2fR7HljoftVkG30sD+5XkHXdc4iWsP8caNP65GplfcX4aw2xrcweAESq1Kz5rK42Cs=~1	",
                    "Referer":"https://students.convera.com/"}

    #following section finds the school code (a 10-digit number) from the school name
    school_json = requests.get(url_school,headers=headers_school).text
    school_location = school_json.find(school_name) #finds the school
    school = school_json[school_location-20:school_location-10]

    #following section sets up the cookies for the next page
    XJSESSIONID = YJSESSIONID
    awsalbtgcors0to1 = requests.post(url_school, headers=headers_school).cookies["AWSALBTGCORS"]
    awsalbcors0to1 = requests.post(url_school, headers=headers_school).cookies["AWSALBCORS"]  # this cookie facilitates the transition from site 0 to 1

    #Page 2
    #following section sets up the next page to be queried
    url1 = "https://students.convera.com/geo-buyer/services/session/create?sellerId="+str(school)
    headers1 = {"Authority": "students.convera.com",
    "Method":"GET",
    "Path":"/geo-buyer/services/session/create?sellerId="+str(school),
    "Scheme":"https",
    "Accept":"application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language":"en-US,en;q=0.9",
    "Cookie":"JSESSIONID="+XJSESSIONID+"; "
             "LANG=en_GB; CookiesAccepted=true; "
             "ak_bmsc="+ak_bmsc+"; "
             "QuantumMetricSessionID=ce18dd359df32c2323244a0bc97f9ab3; "
             "QuantumMetricUserID=1dfb44c270c9b0bbbc656a1e33c48c8b; "
             "AWSALBTGCORS="+awsalbtgcors0to1+"; "
             "AWSALBCORS="+awsalbcors0to1+"; "
             "bm_sv=EF0B994B316BBB3F120C69C9C5FDAC09~YAAQDsR7aEQqEhOJAQAA/FRNZRQYu33iw81SlfFHMwdgGngCtQ49k+VgC+Vqbc3qIY9bCOvV/YjPtzPkBzcuwHQdlnoonmR+KI5wfIldb9DKeFfZGG3/ZGKP3YwJQFXCmXlIjNncC8dCMCF7YZDMx1MrwHVbixTDAoMJ1EAvMZ296SMLcDRoMyxq5A93nrziu2fR7HljoftVkG30sD+5XkHXdc4iWsP8caNP65GplfcX4aw2xrcweAESq1Kz5rK42Cs=~1	",
    "Referer": "https://students.convera.com/"}
    
    #following section obtains the cookies from this page to transition to the next page
    awsalbtgcors1to2 = requests.post(url1,headers=headers1).cookies["AWSALBTGCORS"] #this cookie facilitates the transition from site 1 to 2
    awsalbcors1to2 = requests.post(url1,headers=headers1).cookies["AWSALBCORS"]  #this cookie facilitates the transition from site 1 to 2
    JSESSIONID = requests.get(url1,headers=headers1).cookies["JSESSIONID"]

    #Page 3
    #following section sets up the next page to be queried
    url2 = "https://students.convera.com/geo-buyer/services/spI18n/load/en_GB/"+str(school)
    headers2 = {"Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": "LANG=en_GB; "
              "ak_bmsc="+ak_bmsc+"; "
              "CookiesAccepted=true;"
              "QuantumMetricSessionID=ce18dd359df32c2323244a0bc97f9ab3; "
              "QuantumMetricUserID=1dfb44c270c9b0bbbc656a1e33c48c8b; "
              "AWSALBTGCORS="+awsalbtgcors1to2+"; "
              "AWSALBCORS="+awsalbcors1to2+"; "
              "JSESSIONID="+JSESSIONID+"; "
              "bm_sv=EF0B994B316BBB3F120C69C9C5FDAC09~YAAQDsR7aEQqEhOJAQAA/FRNZRQYu33iw81SlfFHMwdgGngCtQ49k+VgC+Vqbc3qIY9bCOvV/YjPtzPkBzcuwHQdlnoonmR+KI5wfIldb9DKeFfZGG3/ZGKP3YwJQFXCmXlIjNncC8dCMCF7YZDMx1MrwHVbixTDAoMJ1EAvMZ296SMLcDRoMyxq5A93nrziu2fR7HljoftVkG30sD+5XkHXdc4iWsP8caNP65GplfcX4aw2xrcweAESq1Kz5rK42Cs=~1",
    "Referer": "https://students.convera.com/"}

    #following section obtains the cookies from this page to transition to the next page
    awsalbtgcors2to3 = requests.post(url2,headers=headers2).cookies["AWSALBTGCORS"]
    awsalbcors2to3 = requests.post(url2,headers=headers2).cookies["AWSALBCORS"]

    #Page 4
    #following section sets up the next page to be queried
    url3 = "https://students.convera.com/geo-buyer/_assets/logo?sellerId="+str(school)+"&asset=debtorPortalBackground"
    headers3 = {"Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": "LANG=en_GB; "
              "ak_bmsc="+ak_bmsc+"; "
              "CookiesAccepted=true; "
              "QuantumMetricSessionID=ce18dd359df32c2323244a0bc97f9ab3; "
              "QuantumMetricUserID=1dfb44c270c9b0bbbc656a1e33c48c8b; "
              "JSESSIONID="+YJSESSIONID+"; "
              "institution="+str(school)+"; "
              "AWSALBTGCORS="+awsalbtgcors2to3+"; "
              "AWSALBCORS="+awsalbcors2to3+"; "
              "bm_sv=EF0B994B316BBB3F120C69C9C5FDAC09~YAAQDsR7aEQqEhOJAQAA/FRNZRQYu33iw81SlfFHMwdgGngCtQ49k+VgC+Vqbc3qIY9bCOvV/YjPtzPkBzcuwHQdlnoonmR+KI5wfIldb9DKeFfZGG3/ZGKP3YwJQFXCmXlIjNncC8dCMCF7YZDMx1MrwHVbixTDAoMJ1EAvMZ296SMLcDRoMyxq5A93nrziu2fR7HljoftVkG30sD+5XkHXdc4iWsP8caNP65GplfcX4aw2xrcweAESq1Kz5rK42Cs=~1",
    "Referer":"https://students.convera.com/"}

    #following section obtains the cookies from this page to transition to the next page
    awsalbtgcors3to4 = requests.post(url3,headers=headers3, json = {"sellerId":school, "asset":"debtorPortalBackground"}).cookies["AWSALBTGCORS"]
    awsalbcors3to4 = requests.post(url3,headers=headers3, json = {"sellerId":school, "asset":"debtorPortalBackground"}).cookies["AWSALBCORS"]

    #Page 5
    #this for loop will repeat for every ccy that we are looking for, as defined in line 10-13
    for country in country_dict[country_code].keys():
        #following section sets up the site to be queried
        url4 = "https://students.convera.com/geo-buyer/services/session/capture/services"
        headers4 = {"Accept":"application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Length":"127",
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": "LANG=en_GB; "
                    "ak_bmsc="+ak_bmsc+"; "
                    "CookiesAccepted=true; "
                    "QuantumMetricSessionID=ce18dd359df32c2323244a0bc97f9ab3; "
                    "QuantumMetricUserID=1dfb44c270c9b0bbbc656a1e33c48c8b; "
                    "JSESSIONID="+JSESSIONID+"; "
                    "institution="+str(school)+"; "
                    "AWSALBTGCORS="+awsalbtgcors3to4+"; "
                    "AWSALBCORS="+awsalbcors3to4+"; "
                    "bm_sv=EF0B994B316BBB3F120C69C9C5FDAC09~YAAQDsR7aEQqEhOJAQAA/FRNZRQYu33iw81SlfFHMwdgGngCtQ49k+VgC+Vqbc3qIY9bCOvV/YjPtzPkBzcuwHQdlnoonmR+KI5wfIldb9DKeFfZGG3/ZGKP3YwJQFXCmXlIjNncC8dCMCF7YZDMx1MrwHVbixTDAoMJ1EAvMZ296SMLcDRoMyxq5A93nrziu2fR7HljoftVkG30sD+5XkHXdc4iWsP8caNP65GplfcX4aw2xrcweAESq1Kz5rK42Cs=~1",
        "Origin": "https://students.convera.com",
        "Referer": "https://students.convera.com/"}

        #following section obtains the cookies from this page to transition to the next page
        awsalbtgcors4to5 = requests.post(url4,headers=headers4, json = {"country":country,
                                                            "debtorGroup":"All",
                                                            "services":[{"id":school,"pledgedAmount":500,"providerClientId":"null","priority":1}]}).cookies["AWSALBTGCORS"]
        awsalbcors4to5 = requests.post(url4,headers=headers4, json = {"country":country,
                                                             "debtorGroup":"All",
                                                             "services":[{"id":school,"pledgedAmount":500,"providerClientId":"null","priority":1}]}).cookies["AWSALBCORS"]

        #Page 6
        #following section sets up the site to be queried
        urlX = "https://students.convera.com/geo-buyer/services/buyer/pay/initiatePayment"
        headersX = {"Authority": "students.convera.com",
        "Method":"GET",
        "Path": "/geo-buyer/services/buyer/pay/initiatePayment",
        "Scheme": "https",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "LANG=en_GB; "
                    "CookiesAccepted=true; "
                    "QuantumMetricUserID=1dfb44c270c9b0bbbc656a1e33c48c8b; "
                    "institution="+str(school)+"; "
                    "ak_bmsc="+ak_bmsc+"; "
                    "QuantumMetricSessionID=ce18dd359df32c2323244a0bc97f9ab3; "
                    "JSESSIONID="+JSESSIONID+"; "
                    "AWSALBTGCORS="+awsalbtgcors4to5+"; "
                    "AWSALBCORS="+awsalbcors4to5,
        "Referer": "https://students.convera.com/"}

        #following section obtains all currency quotes for the ccy that we are looking for in this iteration of the loop
        response = requests.get(urlX,headers=headersX).text
        response_dict = json.loads(response)["currencyQuoteList"]   
        print (response_dict)
        avail = 0 
        for ccycode in response_dict: #this loops through every curr1ency in the list of currency offers
            for quote in ccycode['initiateQuoteResponseList']:
                #following section attempts to get the market rate from Yahoo Finance
                try: #program tries to pull rate by using direct CCY to CCY pair
                    yfinancepull = yf.download(tickers = (baseccys[country_code]+country_dict[country_code][country]+'=X') ,period ='1d', interval = '1m').tail(1)
                    mktvalue = yfinancepull.iloc[0,yfinancepull.columns.get_loc("Close")]
                except: #sometimes, CCY to CCY pair is not a market traded currency, and we must go through USD to derive an exchange rate
                    yfinancepull = yf.download(tickers = ("USD"+country_dict[country_code][country]+'=X') ,period ='1d', interval = '1m').tail(1)
                    basetousd = yfinancepull.iloc[0,yfinancepull.columns.get_loc("Close")]
                    yfinancepull = yf.download(tickers = ("USD"+baseccys[country_code]+'=X') ,period ='1d', interval = '1m').tail(1)
                    usdtomkt = yfinancepull.iloc[0,yfinancepull.columns.get_loc("Close")]
                    mktvalue = basetousd/usdtomkt
                
                #following section adds the currency pair to the table
                if quote["buyerCurrency"] == country_dict[country_code][country]:
                    compvalue = quote["buyerAmount"]/500
                    margin = ((compvalue/mktvalue)-1)
                    df.loc[len(df.index)] = [quote["buyerCurrency"], quote["buyerAmount"], round(mktvalue,3), round(compvalue,3), (str(round(margin*100,2))+"%"), quote["paymentType"]["description"]]
                    print("Completed "+country_dict[country_code][country])
                    avail = 1
        
        #if no rates are available, then fill a row with NAs
        if avail == 0:
            df.loc[len(df.index)] = [country_dict[country_code][country],"NA",round(mktvalue,3),"NA","NA","NA"]
            print("Completed "+country_dict[country_code][country])
    return(df)

#main
counter = 1

#runs the country search option
country_options = list(baseccys.keys())
for x in country_options:
    print (counter, x)
    counter += 1
country_code = country_options[int(input("Enter the number of the corresponding country: "))-1]

#runs the school search function
search_school = input("Enter a school: ")
all_schools_list = start_up_convera(country_code)
counter = 1
search_results = []
for x in all_schools_list:
    if search_school.upper() in x.upper():
        search_results.append(x)
for x in search_results:
    print (counter, x)
    counter += 1
final_search_school = search_results[int(input("Enter the number of the corresponding school: "))-1]

#prints the table output
print(find_school(country_code,final_search_school))
