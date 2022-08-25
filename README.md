<h1 id="topBanner" align="center">
  
  <img src="https://github.com/stephen-becker/Scraper-Program/blob/master/Assets/web_scraper_logo.png" alt="GitHub README banner"/>
</h1>

<div align="center">
  
[![](https://img.shields.io/github/v/tag/Stephen-Becker/Scraper-Program?label=latest%20version&logo=Github&style=flat-square)](https://github.com/stephen-becker/Scraper-Program/releases/latest) [![](https://img.shields.io/github/last-commit/Stephen-Becker/Scraper-Program/master?color=blue&logo=github&style=flat-square)](https://github.com/stephen-becker/Scraper-Program/commits/master) [![](https://img.shields.io/github/issues/Stephen-Becker/Scraper-Program?color=red&logo=github&style=flat-square)](https://github.com/stephen-becker/Scraper-Program/issues)

[Features](#features)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Get Started](#getstarted)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Planned](#planned)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Issues](https://github.com/stephen-becker/Scraper-Program/issues)


**[Web Scraper](https://github.com/stephen-becker/Scraper-Program)** is a tool I built for fun to see the capabilities of some Python libraries and to learn and experience the involvement of web scraping.

</div>

<h2 id="features" align="center">  
  Features
</h2>

Web Scraper currently is limited from its full potential. The current way I have it setup is to scrape products off multiple pages from specificed websites. Once it grabs all items related to the search keyword, it proceeds to dump and organized (by price) json file into an output directory. 

Basic Web Scraper features includes...

- Scraping current selection of websites (Newegg, BestBuy)
- Finding products on those websites
- Settings limits on pages scraping, or adding a wait time to delay each scan
- Including out of stock items into your output file
- Selecting which website to scan

Instructions found below in the [Get Started](#getstarted) section to operate this program.

<h2 id="getstarted" align="center">  
  Get Started
</h2>

In order to get the program running you must have the dependencies (which are listed in 'requirements.txt')

To install the required dependencies type the command (ensure you are in the correct project file path):

`pip install -r requirements.txt` - *installs necessary dependencies for Web Scraper to work*

Afterwards run the program like you would anyother Python program:

`python scraper.py` - *runs the program*

Input what you would like to search, do note, the search keyword is not case-sensitive but has to be pretty exact otherwise some other results maybe returned that you weren't looking for.

**SOME NOTES/DISCLAIMERS**
- Depending on internet connection and other factors, loading times for getting the page can take a lot of time
- In its current form, the websites are currently restricted to two - Newegg and BestBuy, as scraping for products isn't really practical anymore considering API's are widley used to gather product information
- The out of stock feature is a hit or miss in its current form, I am still working on getting it fully functional
- I am unable to add most other e-commerce websites due to 'robots.txt' on most sites restricting me from scraping
- Although it hasn't happened to me or on my machines, you could potentially be ip-blocked if too many requests are put through, I mean you would have to put a lot through though
- I am not responible for damage done to your machine, just have to put this although no destructive/harmful code is present to the best of my knowledge

<h2 align="center" id="planned">  
  Planned
</h2>
Everything below is subject to change, but these are feature I am considering releasing in the future.

- Convert json file to a more user-friendly reable UI system or file type (*it's painful when you have to read a really long json file*)
- More user configuration options
- More attributes returned when scraping products (reviews, images, etc.)

<div align="center">

Have a suggestion for some options, or want to report a bug? Open an [issue](https://github.com/stephen-becker/Scraper-Program/issues)!

[Authors](https://github.com/Stephen-Becker/Scraper-Program/graphs/contributors)

</div>

[release]:https://github.com/Stephen-Becker/Scraper-Program/releases/latest "Latest Release (external link)"
[issues]:https://github.com/stephen-becker/Scraper-Program/issues "Issues (external link)"
