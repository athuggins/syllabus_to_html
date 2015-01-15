from bs4 import BeautifulSoup
import urllib


def find_syllabus_link():
    course_page = urllib.urlopen(str(raw_input("What URL would you like to pull from?" )))
    print course_page

find_syllabus_link()