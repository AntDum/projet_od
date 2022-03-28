from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='project_od-AntDum',
      version='1.0.2',
      description='Tools for making game with pygame',
      author='AntDum',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author_email='',
      url='https://github.com/AntDum/project_od',
      project_urls={
        "Bug Tracker": "https://github.com/AntDum/project_od/issues",
        "Source": 'https://github.com/AntDum/project_od'
      },
      packages=['project_od', 'project_od.gui', 'project_od.particule', 'project_od.screen', 'project_od.physics', 'project_od.map', 'project_od.ia'],
      requires=['pygame'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires=">=3.9"
     )