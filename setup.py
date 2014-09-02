from setuptools import setup, find_packages
import os

version = '1.0'

long_description = (
    open('README.md').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='customer.lascatalinascr_com',
      version=version,
      description="Custom Implementations of the propertyshelf MLS embedding for lascatalinascr.com",
      long_description=long_description,
      # Get more strings from
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Jens Krause',
      author_email='jens@propertyshelf.com',
      url='https://github.com/propertyshelf/customer.lascatalinascr_com',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['customer'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      )
