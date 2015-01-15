import pypandoc
import os
from bs4 import BeautifulSoup
import re

'''
#  Not doing this part because urllib2 doesn't support ssl/https.
import urllib2
import re

def get_course_from_url():
    """
    This would work if urllib2 supported ssl. It doesn't. Sigh :(
    """
    url = urllib2.urlopen(str(raw_input("What URL would you like to pull from?")))
    content = url.read()
    soup = BeautifulSoup(content)
    for a in soup.findAll('a',href=True):
        if re.findall('syllabus', a['href']):
            print "Found the Syllabus:", a['href']
'''

def read_course_html(course):
    """
    Opens the course's HTML file with BeautifulSoup, and
    returns it.
    """
    course = course.decode('utf-8')  # is this necessary?
    lines = BeautifulSoup(open(course))
    return lines


def find_course_units(course_file):
    """
    Finds each of the course's units and returns a list
    with each unit as an item in the list.
    """

    unit_list = []

    for i in range(20):
        unit_x = course_file.find(id='%s_unit' % i)
        if unit_x is None:
            pass
        elif len(unit_x) > 0:
            unit_x = str(unit_x)
            unit_list.append(unit_x)
    return unit_list


def write_unit_to_file(unit_list, file_format):
    """
    Writes the contents of the unit to a separate file.
    format argument describes the filetype.
    """
    count = 0
    for i in unit_list:
        to_write = str(i)  # [1:-1] was not necessary
        count += 1
        if count <= 9:
            output = open('Unit0%d.%s' % (count, file_format), 'w')
        else:
            output = open('Unit%d.%s' % (count, file_format), 'w')
        output.write(to_write)
        output.close()
    return count


def html_to_markdown(num_of_units):
    """
    Converts HTML to markdown based on how many units a course has.
    """
    for count in range(1, num_of_units + 1):
        output = open('Unit0%d.md' % count, 'w')
        if count <= 9:
            to_write = pypandoc.convert("Unit0%d.html" % count, "markdown_strict").encode('utf-8')
        else:
            to_write = pypandoc.convert("Unit0%d.html" % count, "markdown_strict").encode('utf-8')
        output.write(to_write)
        output.close()


def get_course_intro(course_file):
    """
    Locates the introductory section of the course syllabus.
    """
    whole_course = str(course_file)
    new_whole_course = whole_course.split('\n')
    for line in new_whole_course:
        if 'Course Syllabus for' in line:
            start_line = new_whole_course.index(line)
        if 'id="overview"' in line:
            end_line = new_whole_course.index(line)
    intro_list = new_whole_course[start_line:end_line]
    intro_string = '\n'.join(intro_list)
    return intro_string


def course_intro_to_html_and_md(intro_string):
    """
    Converts the course intro into html and markdown.
    """
    output = open('Intro.html', 'w')
    output.write(intro_string)
    output.close()

    md_output = open('Intro.md', 'w')
    to_write = pypandoc.convert('Intro.html', 'markdown_strict').encode('utf-8')
    md_output.write(to_write)
    md_output.close()

# Okay, this next part is a mess, but I'll clean it up next and make it its own function that will just take the
# html file of the syllabus and output everything else.

course_name = "arth110"
# course_name = str(raw_input("What is the name of the course file you'd like to process? "))
if not os.path.exists(course_name):
    os.makedirs(course_name)
course_doc = read_course_html("%s.html" % course_name)
course_units = find_course_units(course_doc)
os.chdir(course_name)
unit_count = write_unit_to_file(course_units, "html")
#  writes each unit to an html file, and returns how many units there are so pandoc knows what to do
html_to_markdown(unit_count)
intro = get_course_intro(course_doc)
course_intro_to_html_and_md(intro)