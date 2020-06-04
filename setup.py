#coding using encoding utf-8
#stup instagram bot for farm likes and followers
#follow me on instagram/arfy.slowy

from setuptools import setup
from os import path

#io support pyhton 2.7
#for pyhton3 can skip this import
from io import open as io_open
import re

summary_name = "Tool automated instagram interact";
project_homepage = "https://github.io/slowy07/instagrambot"
here_path = path.abspath(path.dirname(__file__))

def readall(*args):
    with io open(path.join(here,*args), encoding="utf-8") as fp:
        return fp.read()

with open("requirements.txt") as f:
    depencies = f.read().splitlines()

documentation = readall("README.md")
metadata = dict(
    re.findall(r"""__([a-z]+)__ = "([^"]+)""", readall("instagrambot", "__init__.py"))
)

setup(
    name = "instagrambot",
    version = metadata["version"],
    description = summary,
    long_description = documentation,
    long_description_content_type = "text/markdown"
    author = "arfy slowy"
    author_email = "slowy.arfy@gmail.com"
    license = "GPLv3"
    url = project_homepage,
    maintaner = "instagram on facebook"
    donwload_url =(project_homepage + "/archive/master.zip"),
    project_urls{
        "How Tos": (project_homepage + "/tree/master/docs"),
        "Example": (project_homepage + "/tree/master/quickstart_templates"),
        "Bug Reports": (project_homepage + "/issues"),
        "Funding": "free license"
        "Source": (project_homepage + "/tree/master/instagrambot"),
    },

    packages = ['instagrambot']
    package_data = {
            "instagrambot":[
                "icons/windows/*.ico",
                "icons/linux/*.png",
                "icons/mac/*.icns",
                "firefox_extension/",
                "plugins/",
            ]
    },
    keywords = (
        "instagrambot python instagram automation \
         marketing promotion bot selenium"
    ),
    classifiers =[
        "Development Status :: beta",
        "Environment :: Console",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Environment :: Web Environment",
        "Intented Audience :: End User/Desktop",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Programming Language :: Pyhton",
        "Programming Language :: Javscript",
        "Programming Language :: SQL",
        "Topic :: Utilities",
        "Topic :: Software Development :: BuildTools",
        "Programming Language :: Pyhton :: 3",
        "Programming Language :: Pyhton :: 3.4",
        "Programming Language :: Pyhton :: 3.5",
        "Programming Language :: Pyhton :: 3.6",
        "Programming Language :: Pyhton :: 3.7",
        "Natural Language :: English",
    ],
    install_requires = dependecies,
    extras_require ={"test": ["tox","virtualenv","tox-venv"]},
    pyhton_requires = ">=3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    platforms = ["win32", "linux", "linux2", "darwin"],
    zip_safe = False,
    entry_points ={"console_scripts":[]},
)
