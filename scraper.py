import requests
from bs4 import BeautifulSoup

# This would be for ONE specific theatre, but it can be easily modified to loop through multiple theatres
def scrape_theatre_sofia():
    url = "https://teatrosofia.es/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    shows = []

     # You need to look at Theatre A's website HTML to find the right tags and classes!
    # Let's imagine each show is in a <div class="show-listing">
    for show_listing in soup.find_all('div', class_='show-listing'):
        title = show_listing.find('h2').text # Assuming title is in an <h2> tag
        description = show_listing.find('p', class_='desc').text # Assuming description is in a <p> with class 'desc'
        dates = show_listing.find('span', class_='dates').text

        show = {
            'title': title,
            'description': description,
            'dates': dates,
            'theatre': 'Theatre A',
            'source_url': url,
            'unique_id': f"theatreA_{title}_{dates}" # Create a unique ID for this specific run of the show
        }
        shows.append(show)

    return shows

# You would have similar functions: scrape_theatre_B(), scrape_critic_reviews()