"""
Python library for Query of Valve Servers over a range of IPs

"""
try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='valve-range-query-3',

	version='2.0.3',

	description='Python library for Query of Valve Servers over a range of IPs',
	long_description=long_description,

	# The project's main homepage.
	url='https://github.com/incontestableness/valve-range-query-3',

	# Author details
	author='incontestableness',
	author_email='whyistherumg0ne@protonmail.com',

	packages = ['valverangequery'],


	license='MIT',

	classifiers=[
		'Development Status :: 4 - Beta',

		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',

		'License :: OSI Approved :: MIT License',

		'Programming Language :: Python :: 3.7',
	],

	keywords='valve query servers counter strike csgo team fortress tf2 left for dead l4d2'

)
