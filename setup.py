from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='Projet_OD-AntDum',
      version='1.0.1',
      description='Tools for making game with pygame',
      author='AntDum',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author_email='',
      url='https://github.com/AntDum/projet_od',
      project_urls={
        "Bug Tracker": "https://github.com/AntDum/projet_od/issues",
        "Source": 'https://github.com/AntDum/projet_od'
      },
      packages=['projet_od', 'projet_od.gui', 'projet_od.state', 'projet_od.particule', 'projet_od.screen', 'projet_od.physics'],
      requires=['pygame'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires=">=3.6"
     )