from setuptools import setup, find_namespace_packages

with open("README.md", 'r') as readme_handle:
	long_description = readme_handle.read()

setup(
	name='checkInvest',
	author='Coutinho de Souza',
	author_email='gvscou@protonmail.com',
	version='1.0.0',
	descripition='A CTL for managing one expenses and investiments',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/GvsCou/checkInvest',
	install_requires=[
		'cryptonator==0.0.4',
		'yahooquery==2.2.15'
	],
	keywords='checkInvest, finance, expense-manager',
	packages=find_namespace_packages(),
	entry_points={
	'console_scripts': [
		'checkinv = checkInvest.main:main'
		]
	},
	package_data={
		"": ['currency-format.json']
	},
	python_requires='>=3.8'
	

)
