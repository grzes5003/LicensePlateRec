from distutils.core import setup
from core.manager.Manager import Manager

setup(name='Distutils',
      version='1.0',
      description='Python Distribution Utilities',
      author='Some Guy',
      author_email='mail@example.com',
      packages=['core.manager', 'core.dataClasses', 'core', 'core.actorClasses'],
      install_requires=[]
      )

Manager.run()
