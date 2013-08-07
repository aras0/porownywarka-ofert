from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name = 'PorownywarkaOfert',
    version = '0.1',
    author = 'saraCzelusniak',
    author_email = 'saraCzelusniak@bitbucket.org',
    url = '',
    description = 'Porownywanie ofert',
    long_description = long_description,
    package_dir = {'' : 'src'},
    #setuptools.find_packages()
    packages = ['porownywarkaOfert'],
    classifiers = [
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 2.7.3',
          'Natural Language :: Polish',
    ],
    include_package_data = True,
)