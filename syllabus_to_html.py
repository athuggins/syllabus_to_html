import pypandoc
from bs4 import BeautifulSoup


def find_course_units(course_file):
    """
    Finds each of the course's units and returns a list
    with each unit as an item in the list.
    """

    unit_list = []

    for i in range(20):
        unit_x = course_file.find_all(id='%s_unit' % i)
        if len(unit_x) > 0:
            unit_list.append(unit_x)

    return unit_list


def write_unit_to_file(unit_list, format):
    """
    Writes the contents of the unit to a separate file.
    format argument describes the filetype.
    """
    count = 0
    for i in unit_list:
        to_write = str(i)[1:-1]
        count += 1
        if count <= 9:
            output = open('Unit0%d.%s' % (count, format), 'w')
        else:
            output = open('Unit%d.%s' % (count, format), 'w')
        output.write(to_write)
        output.close()
    return count


def read_course_html(course):
    """
    Opens the course's HTML file with BeautifulSoup, and
    returns it.
    """
    lines = BeautifulSoup(open(course))
    return lines


def html_to_markdown(num_of_units):
    """
    Converts HTML to markdown based on how many units a course has.
    """
    for count in range(num_of_units):
        if count <= 9:
            output = open('Unit0%d.md' % count, 'w')
            to_write = pypandoc.convert("Unit0%d.html" % count, "markdown_strict").encode('utf-8')
            output.write(to_write)
            output.close()
#   for count in range(num_of_units):
#       output = open('Unit01.md', 'w')
#       to_write = pypandoc.convert("Unit01.html", "markdown_strict").encode('utf-8')
#       output.write(to_write)
#       output.close()



course_doc = read_course_html("arth110.html")
course_units = find_course_units(course_doc)
unit_count = write_unit_to_file(course_units, "html")
# writes each unit to an html file, and returns how many units there are so pandoc knows what to do
html_to_markdown(unit_count)