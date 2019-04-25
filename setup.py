from setuptools import setup


with open('README.rst') as f:
    readme = f.read()


setup(
    name='slacker',
    version='0.13.0',
    packages=['slacker'],
    description='Slack API client',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='Oktay Sancak',
    author_email='oktaysancak@gmail.com',
    url='http://github.com/os/slacker/',
    install_requires=['requests >= 2.2.1'],
    license='http://www.apache.org/licenses/LICENSE-2.0',
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='slack api'
)
