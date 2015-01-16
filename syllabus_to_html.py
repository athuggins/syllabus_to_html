import pypandoc
import os
from bs4 import BeautifulSoup

'''
#  Not doing this part because urllib2 doesn't support ssl/https.
import urllib2

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
        # find each unit using the div tag id 'X_unit'
        unit_x = course_file.find(id='%s_unit' % i)
        if unit_x is None:
            pass
        elif len(unit_x) > 0:
            # convert the contents of the unit to a string, add it to the unit list
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
        to_write = str(i)
        count += 1
        if count <= 9:
            # write Unit01-09.html/md, for units 1-9
            output = open('Unit0%d.%s' % (count, file_format), 'w')
        else:
            # write Unit10-20.html/md, for units 10-20
            output = open('Unit%d.%s' % (count, file_format), 'w')
        output.write(to_write)
        output.close()
    return count


def html_to_markdown(num_of_units):
    """
    Converts HTML to markdown based on how many units a course has.
    """
    for count in range(1, num_of_units + 1):
        # the if/else is necessary so that the unit files are formatted properly
        # and you don't get Unit1.html or Unit010.html
        if count <= 9:
            output = open('Unit0%d.md' % count, 'w')
            to_write = pypandoc.convert("Unit0%d.html" % count, "markdown_strict").encode('utf-8')
        else:
            output = open('Unit%d.md' % count, 'w')
            to_write = pypandoc.convert("Unit%d.html" % count, "markdown_strict").encode('utf-8')
        output.write(to_write)
        output.close()


def get_course_intro(course_file):
    """
    Locates the introductory section of the course syllabus.
    """
    whole_course = str(course_file)
    new_whole_course = whole_course.split('\n')
    for line in new_whole_course:
        # course syllabus files alwyas begin with this line
        if 'Course Syllabus for' in line:
            start_line = new_whole_course.index(line)
        # course intros stop here, where the 'Course Overview' section begins
        if 'id="overview"' in line:
            end_line = new_whole_course.index(line)
    # puts each line of the html file into a big list
    intro_list = new_whole_course[start_line:end_line]
    # brings the list back together into a string with each line of the html on a new line
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



def leroy_jenkins():
    """
    Let's do this.
    """
    course_name = str(raw_input("What is the name of the course file you'd like to process? "))

    # makes a new directory based on the course's name
    if not os.path.exists(course_name):
        os.makedirs(course_name)

    # opens the course html file
    course_doc = read_course_html("%s.html" % course_name)

    # finds how many units the course has
    course_units = find_course_units(course_doc)

    # goes to the course directory
    os.chdir(course_name)

    # writes an html file for each unit, then converts each one to markdown
    unit_count = write_unit_to_file(course_units, "html")
    html_to_markdown(unit_count)

    # processes the course intro
    intro = get_course_intro(course_doc)
    course_intro_to_html_and_md(intro)

    print "All done! Check the '%s' folder for all the files for your course." % course_name


leroy_jenkins()