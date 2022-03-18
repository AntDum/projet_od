from distutils.core import setup

setup(name='Projet_OD',
      version='1.0',
      description='Pygame utilities',
      author='OD',
      author_email='OD',
      url='',
      packages=['projet_od', 'projet_od.gui', 'projet_od.state', 'projet_od.particule'],
      requires=['pygame'],
      python_requires=">=3.6"
     )