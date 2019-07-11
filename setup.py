#!/usr/bin/env python

import os
from setuptools import setup, find_packages

VERSION = '0.0.4'

ENTRY_POINTS = {
    'orange3.addon': (
        'oshap = orangecontrib.oshap',
    ),
    # Entry point used to specify packages containing tutorials accessible
    # from welcome screen. Tutorials are saved Orange Workflows (.ows files).
    'orange.widgets.tutorials': (
        # Syntax: any_text = path.to.package.containing.tutorials
    ),

    # Entry point used to specify packages containing widgets.
    'orange.widgets': (
        # Syntax: category name = path.to.package.containing.widgets
        # Widget category specification can be seen in
        #    orangecontrib/datafusion/widgets/__init__.py
        'Shap = orangecontrib.oshap.widgets',
    ),

    # Widget help
    "orange.canvas.help": (
        'html-index = orangecontrib.oshap.widgets:WIDGET_HELP_PATH',
    )
}


if __name__ == '__main__':
    setup(
        name="orange3-shap",
        description="Orange3 add-on for exploring shap values.",
        long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
        version=VERSION,
        author='Jean-Baptiste Poullet',
        author_email='jeanbaptistepoullet@gsk.com',
        url='https://github.com/jpoullet2000/orange3-shap',
        license='CC-BY-NC-3.0',
        keywords=[
            'shap',
            'orange3 add-on'
        ],
        packages=find_packages(),
        package_data={
            "orangecontrib.oshap.widgets": ["icons/*.png",
                                                 "*.js"],
        },
        install_requires=[
            'Orange3',
            'pandas',  # statsmodels requires this but doesn't have it in dependencies?
            'numpy',
            'scipy>=0.17',
            'shap>=0.28.5'
        ],
        entry_points=ENTRY_POINTS,
        test_suite='orangecontrib.oshap.tests.suite',
        namespace_packages=['orangecontrib'],
        zip_safe=False,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: X11 Applications :: Qt',
            'Environment :: Plugins',
            'Programming Language :: Python',
            'License :: Other/Proprietary License',
            'Operating System :: OS Independent',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'Topic :: Scientific/Engineering :: Visualization',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Developers',
        ]
)
