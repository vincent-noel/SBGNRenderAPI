from setuptools import setup
import os

files = [os.path.join("/".join(dp.split("/")[1:]), f) for dp, dn, filenames in os.walk("sbgnrender/app") for f in filenames]
files += [os.path.join("/".join(dp.split("/")[1:]), f) for dp, dn, filenames in os.walk("sbgnrender/node_modules/cytoscape-context-menus") for f in filenames]
files += [os.path.join("/".join(dp.split("/")[1:]), f) for dp, dn, filenames in os.walk("sbgnrender/node_modules/cytoscape-panzoom/") for f in filenames]

setup(name='sbgnrender',
    version="1.0.0a3",
    author="Vincent Noël",
    author_email="contact@vincent-noel.fr",
    description="A SBGN rendering library",
	install_requires = ['selenium'],
	packages=['sbgnrender'],
    package_data={'sbgnrender': ['index.html'] + files},
    include_package_data=True
)