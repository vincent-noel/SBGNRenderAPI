import os, sys

# Adding this directory to python path
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "sbgnrender"))

# Importing our application
from RendererAPI import api as application

