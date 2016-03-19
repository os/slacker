from setuptools import setup


setup(
    name='slacker',
    version='0.9.9',
    packages=['slacker'],
    description='Slack API client',
    author='Oktay Sancak',
    author_email='oktaysancak@gmail.com',
    url='http://github.com/os/slacker/',
    install_requires=['requests >= 2.2.1'],
    license='http://www.apache.org/licenses/LICENSE-2.0',
    test_suite='tests',
    classifiers=(
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ),
    keywords='slack api'
)
