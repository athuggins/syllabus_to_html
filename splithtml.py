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


def write_unit_to_file(unit_list):
    """
    Writes the contents of the unit to a separate html file.
    """
    count = 0
    for i in unit_list:
        to_write = str(i)[1:-1]
        count += 1
        if count <= 9:
            output = open('Unit0%d.html' % count, 'w')
        else:
            output = open('Unit%d.html' % count, 'w')
        output.write(to_write)
        output.close()


def read_course_html(course):
    """
    Opens the course's HTML file with BeautifulSoup, and
    returns it.
    """
    lines = BeautifulSoup(open(course))
    return lines


course_doc = read_course_html("arth110.html")
course_units = find_course_units(course_doc)
write_unit_to_file(course_units)