from distutils.core import setup
setup(
    name = "mxp",
    packages = ["mxp"],
    version = "0.1.3",
    description = "qPCR fileformat reader",
    author = "Florian FInkernagel",
    author_email = "finkernagel@imt.uni-marburg.de",
    url = "http://www.imt.uni-marburg.de",
    keywords = ["qPCR", "MXP"],
    install_requires=[
                  'olefile',
                  'pandas',
                        ],

    classifiers = [
        "Programming Language :: Python",
        #"Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = """\
Support code to read qPCR machine file formats,
such as the .mxp file format created by MxPro.

Currently reads files from 300 and 305er machines.
"""
)
