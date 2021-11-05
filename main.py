from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

# Open requirements.txt and split lines
f = open("requirements.txt", "r")
list_requirements = f.read()[3:].splitlines()
list_versions = list()

# Remove versions from requirements
for requirement in list_requirements:
    requirement_split = requirement.split('==')
    list_requirements[list_requirements.index(requirement)] = requirement_split[0]
    list_versions.append(requirement_split[1])

# Open the new requirements-descripted file to write
os.remove("requirements-descripted.txt") if os.path.exists("requirements-descripted.txt") else None
f = open("requirements-descripted.txt", "a",  encoding='utf8')
for requirement in list_requirements:
    # Request one by one requirement on PyPi
    soup = BeautifulSoup(urlopen("https://pypi.org/project/{}/".format(requirement)), features="lxml")
    result = soup.find_all("div", {"class": "sidebar-section"})

    # Loop for every div containing 'sidebar-section' class
    for res in result:
        # If the div has one of the infos that we need
        if 'Author' in res.text or 'Maintainer' in res.text or 'Requires' in res.text or 'License' in res.text:
            str_split = res.text.split('\n')
            author, maintainer, requires, use_license = None, None, None, None
            for arg in str_split:
                if 'Author' in arg:
                    author = arg
                elif 'Maintainer' in arg:
                    maintainer = arg
                elif 'Requires' in arg:
                    requires = arg
                elif 'License' in arg:
                    use_license = arg

            # Get and Write the data on file
            str_display = '{} - {}\n'.format(requirement, list_versions[list_requirements.index(requirement)])
            if author:
                str_display += author + '\n'
            if maintainer:
                str_display += maintainer + '\n'
            if use_license:
                str_display += use_license + '\n'
            if requires:
                str_display += requires + '\n'
            if author or maintainer or use_license or requires:
                f.write(str_display)
                f.write('\n')
            break
f.close()
