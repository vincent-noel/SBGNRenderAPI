from setuptools import setup, find_packages
import os

files = [os.path.join("/".join(dp.split("/")[1:]), f) for dp, dn, filenames in os.walk("sbgnrender/app") for f in filenames]
files += [os.path.join("/".join(dp.split("/")[1:]), f) for dp, dn, filenames in os.walk("sbgnrender/node_modules/cytoscape-context-menus") for f in filenames]
files += [os.path.join("/".join(dp.split("/")[1:]), f) for dp, dn, filenames in os.walk("sbgnrender/node_modules/cytoscape-panzoom/") for f in filenames]

# from pathlib import Path

# datadir = Path(__file__).parent
# print(datadir)
# files = [str(p.relative_to(datadir)) for p in os.walk("app")]
# # files += [str(p.relative_to(datadir)) for p in datadir.rglob('node_modules/cytoscape-context-menus/*')]
# # files += [str(p.relative_to(datadir / 'node_modules' / 'cytoscape-panzoom')) for p in datadir.rglob('*')]

print(files)
setup(name='sbgnrender',
    version="1.0.0a1",
    author="Vincent Noël",
    author_email="contact@vincent-noel.fr",
    description="A SBGN rendering library",
	install_requires = ['selenium'],
	packages=['sbgnrender'],
    # package_dir={'sbgnrender': 'src/mypkg'},
    
    # Ça marche presque, il faut juste bien faire la liste complete des sous dossiers de 
    package_data={'sbgnrender': [
        # 'app/css/*', 'app/img/*', 'app/js/*', 'app/bundle.js', 
        'index.html', 
        # 'app/img/align/*', 'app/img/edges/*', 'app/img/nodes/*', 'app/img/tabs/*', 'app/img/toolbar/*', 
        # 'node_modules/cytoscape-context-menus/cytoscape-context-menus.css',
        # 'node_modules/cytoscape-panzoom/font-awesome-4.0.3/css/font-awesome.css',
        # 'node_modules/cytoscape-panzoom/cytoscape.js-panzoom.css'
    ] + files},
    include_package_data=True
)