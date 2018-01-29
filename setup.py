from distutils.core import setup
setup(
  name = 'neatdata',
  packages = ['neatdata'], # this must be the same as the name above
  version = '0.4',
  description = 'Cleaning code',
  long_description='Cleans a dataset following the strategy described here: http://data-in-model-out.com/2018/01/07/understand-data-cleaning/',
  author = 'Peter Myers',
  author_email = 'peterjmyers1@gmail.com',
  url = 'https://github.com/Peter-32/neatdata', # use the URL to the github repo
  download_url = 'https://github.com/Peter-32/neatdata/archive/0.4.tar.gz', # I'll explain this in a second
  keywords = ['cleaning', 'data cleaning', 'classification'],
  classifiers = [
  'Development Status :: 3 - Alpha',
'Topic :: Scientific/Engineering :: Artificial Intelligence',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3',
'Programming Language :: Python :: 3.2',
'Programming Language :: Python :: 3.3',
'Programming Language :: Python :: 3.4',
'Programming Language :: Python :: 3.5',
'Programming Language :: Python :: 3.6',
  ],
  install_requires=['nbformat', 'sklearn', 'numpy', 'pandas'],
  python_requires='>=3',
  license='MIT'
)
