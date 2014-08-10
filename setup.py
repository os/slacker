from setuptools import setup


setup(name='slacker',
      version='0.2.0',
      packages=['slacker'],
      description='Slack API client',
      author='Oktay Sancak',
      author_email='oktaysancak@gmail.com',
      url='http://github.com/os/slacker/',
      install_requires=['requests >= 2.2.1'],
      license='http://www.apache.org/licenses/LICENSE-2.0',
      keywords='slack api')
