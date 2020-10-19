from setuptools import setup
import os

files = [os.path.join("/".join(dp.split("/")[1:]), f) for dp, dn, filenames in os.walk("sbgnrender/app") for f in filenames]
files += [os.path.join("/".join(dp.split("/")[1:]), f) for dp, dn, filenames in os.walk("sbgnrender/node_modules/cytoscape-context-menus") for f in filenames]
files += [os.path.join("/".join(dp.split("/")[1:]), f) for dp, dn, filenames in os.walk("sbgnrender/node_modules/cytoscape-panzoom/") for f in filenames]

setup(name='sbgnrender',
    version="1.0.0a9",
    author="Vincent Noël",
    author_email="contact@vincent-noel.fr",
    description="A SBGN rendering library",
    long_description="""
# SBGNRender Python library
This library is using Selenium to control ChromeDriver, to run a JS website rendering SBGN (based on Newt)

To install it, the simplest way is via PyPI :
```
sudo pip3 install sbgnrender
```

After installing the library, usage is the following : 
```
from sbgnrender import renderSBGN

renderSBGN(
    input_file,  // Path as a string
    output_file, // Path as a string
    format,      // Format as a string : svg, png, jpg
    scale,       // Scale of the network (default 1 for svg, 3 for jpg/png)
    bg,          // Background color as HTML String (ex #fff for white), None for transparent (available for png/svg),
    max_width,   // Maximum width in pixels
    min_width,   // Minimum width in pixels
    quality,     // Quality (available for jpg),
    layout,      // Perform automatic layout
    verbose      // True | False
)
```

This library depends on ChromeDriver, which can be installed on ubuntu/debian systems with 
```
sudo apt install chromium-chromedriver
```

On Ubuntu 19.x and later, chromium installation is using snap package manager, which causes a problem while writing and accessing temporary files. The current workaround is to change chromium temporary directory permissions with : 
```
sudo chmod 711 /tmp/snap.chromium
```
This is just a temporary which you will have to do at startup (after having run chrome at least once) everytime. If somebody knows a trick, contributions are welcome
    """,
    long_description_content_type="text/markdown",
    url="https://github.com/vincent-noel/SBGNRenderAPI",
	install_requires = ['selenium'],
	packages=['sbgnrender'],
    package_data={'sbgnrender': ['index.html'] + files},
    include_package_data=True
)