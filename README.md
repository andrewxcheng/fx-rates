# fx-rates
The following guide will demonstrate how to scrape FX rates from online payment providers, such as Convera, illustrating the magnitude of the FX margins baked into the rates.
## Obtaining FX Rates From Convera
### Step 1: Opening students.convera.com
The first step to obtaining an FX rate from Convera is to type in the country of the school. Once the country field is completed, Convera will populate the drop-down list of institutions with all the schools from that institution.
### Step 2: Selecting an institution
Once the list of available institutions is created, the school can be selected. This step takes us to the next page of the process.
### Step 3: Select a country and payment amount
Convera then provides the option to select a currency and the payment amount.
### Step 4: Comparing the FX rates
We can then compare the FX rates by calculating the implied FX rate and then marking the baked-in spread.
## Program Framework
The Convera tool is composed of two input/output functions.

The first function has the following structure:
- Input: School country (ex. USA)
- Output: Available schools for that country (ex. Cornell, Harvard, Yale...)

After this function is run, the user can then select a school from the list that was just generated, going to the second function:
- Input: School country, school name
- Output: FX rates for a desired list of currencies

This second function is what provides a dataframe with all the FX rates. This dataframe can then be printed or exported as a spreadsheet.
## Managing Cookies
To navigate between the pages, Convera uses request and response cookies. These cookies effectively serve as keys to access the next webpage, creating a chain of pages.
Take the following process as an example of how keys can form a chain of pages:
- Site A: Visiting this site gives CookieA.
- Site B: CookieA is required to access this site. Once this site is accessed, CookieB is given to the user.
- Site C: CookieB is required to access this site. Once this site is accessed, CookieC is given to the user.
- Site D: CookieC is required to access this site. This site then contains the information that we are aiming to scrape.

Therefore, to access Site D and its information, we need to start at Site A and go through the chain of sites to finally access Site D. It is impossible to access Site D directly, as it requires a cookie from the previous site, which requires a cookie from the previous site, and so on. 

In Convera's case, the two tokens that act as these keys to create the chain are called:
- AWSALBTGCORS
- AWSALBCORS

These need to be taken from a previous page and then fed into the HTML headers of the following page to access the next page. 
## Using Selenium
To access all the pages, Convera requires a session ID. This token will expire in a short period, so the program must obtain a new token from Convera's website each time. Selenium is used to retrieve this initial session ID token. After it is retrieved, the rest of the data scraping can be processed using the requests package.

The two tokens that are required to access the database are:
- JSESSIONID
- ak_bmsc

These are taken from the initial Selenium scrape, and then stored as variables to use in later requests made. 
