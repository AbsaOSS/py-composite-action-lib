from setuptools import setup, find_packages

setup(
    name='PyCompositeActionLib',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    description='A Python library for composite actions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Miroslav Pojer',
    author_email='miroslav.pojer@absa.africa',
    url='https://github.com/AbsaOSS/py-composite-action-lib',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Build Tools',
        'Environment :: Console',
        'Environment :: Other Environment',
    ],
)