from setuptools import setup, find_packages

setup(
    name='django-eventy',
    version=__import__('eventy').__version__,
    license="BSD",

    install_requires = [
        'django-extensions',
        ],

    description='A really simple event manager with no recurring abilities for django.',
    long_description=open('README.md').read(),

    author='Colin Powell',
    author_email='colin@onecardinal.com',

    url='http://github.com/powellc/django-eventy',
    download_url='http://github.com/powellc/django-eventy/downloads',

    include_package_data=True,

    packages=['eventy'],

    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
