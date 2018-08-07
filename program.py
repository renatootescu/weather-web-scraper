import requests
import bs4
import collections

WeatherReport = collections.namedtuple('WeatherReport', 'cond, temp, scale, loc')


def main():
    print_the_header()

    location = input('What city do you want the weather for (e.g.: Bucharest)? ')

    html = get_html_from_web(location)
    report = get_weather_from_html(html)

    print('The weather in {} will be {}, with a temperature of {} {}'.format(
        report.loc,
        report.cond,
        report.temp,
        report.scale))

    # display for the forecast


def print_the_header():
    print('-----------------------------')
    print('        Weather App')
    print('-----------------------------')
    print()


def get_html_from_web(city):
    url = 'https://www.wunderground.com/weather-forecast/{}'.format(city)
    response = requests.get(url)
    return response.text


def get_weather_from_html(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    loc = soup.find(class_='region-content-header').find('h1').get_text()
    condition = soup.find(class_='condition-icon').get_text()
    temp = soup.find(class_='wu-unit-temperature').find(class_='wu-value').get_text()
    scale = soup.find(class_='wu-unit-temperature').find(class_='wu-label').get_text()

    loc = cleanup_text(loc)
    loc = find_city_and_state_from_location(loc)
    condition = cleanup_text(condition)
    temp = cleanup_text(temp)
    scale = cleanup_text(scale)

    report = WeatherReport(cond=condition, temp=temp, scale=scale, loc=loc)
    return report


def cleanup_text(text: str):
    if not text:
        return text

    text = text.strip()
    return text


def find_city_and_state_from_location(loc: str):
    parts = loc.split(',')
    return parts[0].strip()


if __name__ == '__main__':
    main()
    
