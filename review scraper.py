from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime as dt

# Initialize lists
names=[]
review_dates_original = []
review_dates = []
review_ratings = []
review_texts = []


# Set Trustpilot page numbers to scrape here
from_page = 1
to_page = 45



for i in range(from_page, to_page + 1):
    response = requests.get(
        f"https://www.trustpilot.com/review/www.dugood.org?page={i}")
    web_page = response.text
    soup = BeautifulSoup(web_page, "html.parser")
    #name=soup.find(id='business-unit-title').get_text()
    # the total view count for company
    total=soup.find(id='business-unit-title').get_text()
    
    for review in soup.find_all(class_="paper_paper__1PY90 paper_square__lJX8a card_card__lQWDv card_noPadding__D8PcU styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ"):
        # Company name
        # name = review.find(class_="link_internal__7XN06 link_disabled__mIxH1 typography_typography__QgicV typography_weight-inherit__iX6Fc typography_fontstyle-inherit__ly_HV link_notUnderlined__szqki typography_color-inherit__TlgPO breadcrumb_breadcrumbLink__p1PMo")
        # name.append(name.getText())
        #name = soup.find_all('div', {'class','displayName'})
        # names = soup.find_all('span', {'class': 'multi-size-header__big'})
        # name.append(names)
        #Review dates
        review_date_original = review.select_one(selector="time")
        review_dates_original.append(review_date_original.getText())
        
        # Convert review date texts into Python datetime objects
        review_date = review.select_one(
            selector="time").getText().replace("Updated ", "")
        if "hours ago" in review_date.lower() or "hour ago" in review_date.lower():
            review_date = dt.datetime.now().date()
        elif "a day ago" in review_date.lower():
            review_date = dt.datetime.now().date() - dt.timedelta(days=1)
        elif "days ago" in review_date.lower():
            review_date = dt.datetime.now().date(
            ) - dt.timedelta(days=int(review_date[0]))
        else:
            review_date = dt.datetime.strptime(review_date, "%b %d, %Y").date()
        review_dates.append(review_date)

        # Review ratings
        review_rating = review.find(
            class_="star-rating_starRating__4rrcf star-rating_medium__iN6Ty").findChild()
        review_ratings.append(review_rating["alt"])

        # When there is no review text, append "" instead of skipping so that data remains in sequence with other review data e.g. review_title
        review_text = review.find(
            class_="typography_typography__QgicV typography_body__9UBeQ typography_color-black__5LYEn typography_weight-regular__TWEnf typography_fontstyle-normal__kHyN3")
        if review_text == None:
            review_texts.append("")
        else:
            review_texts.append(review_text.getText())
        #1 only return 3 review
    # for review in soup.find_all(class_="typography_typography__QgicV typography_h1__Xmcta typography_color-blue-dark__4_Kf_ typography_weight-regular__TWEnf typography_fontstyle-normal__kHyN3 title_title__i9V__"):
    #           # Company name
    #             name = review.find(
    #                       class_="typography_typography__QgicV typography_h1__Xmcta typography_weight-heavy__E1LTj typography_fontstyle-normal__kHyN3 title_displayName__TtDDM")
    #             names.append(name.getText())
#2 
        for review in soup.find_all(class_="styles_categoriesListLongTextElement__JQ3zi"):
          # Company name
            name = review.find(class_="typography_typography__QgicV typography_bodysmall__irytL typography_weight-heavy__E1LTj typography_fontstyle-normal__kHyN3")
            names.append(name.getText())         

#3
        # for review in soup.find_all(class_="typography_typography__QgicV typography_h1__Xmcta typography_color-blue-dark__4_Kf_ typography_weight-regular__TWEnf typography_fontstyle-normal__kHyN3 title_title__i9V__ title_titleCompact__tdgAa"):
        #     # Company name
        #     name = review.find(class_="typography_typography__QgicV typography_h1__Xmcta typography_weight-heavy__E1LTj typography_fontstyle-normal__kHyN3 title_displayName__TtDDM")
        #     names.append(name.getText())         
            
       
            



# # Create final dataframe from lists
df_reviews = pd.DataFrame(list(zip(names,review_dates, review_ratings, review_texts)),
                          columns=['companyName','datePublished','ratingValue', 'reviewBody'])
print("The total review is "+total.split(" ")[3])
print(df_reviews)
df_reviews.to_csv('trustpilot.csv')