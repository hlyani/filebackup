from setuptools import setup, find_packages


setup(name='filebackup',
      version='1.0',
      description='for test',
      author='hl',
      author_email='hl@test.com',
      url='http://hlyani.github.io',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'yani = filebackup.filebackup:main',
              ],
      },)
