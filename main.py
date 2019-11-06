from youtube_scraper import *


while True:
    execute_youtube_scraper()
    flag = input("Want to analyze another YouTube channel? (y/n): ").lower()

    if flag == 'y':
        continue
    else:
        break

