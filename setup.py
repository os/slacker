from setuptools import setup

import slacker


setup(name=slacker.__title__,
      version=slacker.__version__,
      packages=['slacker'],
      description='Slack API client',
      author=slacker.__author__,
      author_email='oktaysancak@gmail.com',
      url='http://github.com/os/slacker/',
      install_requires=['requests >= 2.2.1'],
      license=slacker.__license__,
      keywords='slack api')
