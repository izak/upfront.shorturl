from setuptools import setup, find_packages

version = '0.1'

setup(
    name='upfront.shorturl',
    version=version,
    description="Provide an auto-complete Change Note field for CMFEditions",
    long_description=open("README").read(),
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        ],
    keywords='url shortener redirector',
    author='Izak Burger, Upfront Systems',
    author_email='isburger@gmail.com',
    url='https://github.com/izak/upfront.shorturl',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir = {'' : 'src'},
    namespace_packages=['upfront'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Products.CMFPlone',
    ],
    entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
    """,
    setup_requires=["PasteScript"],
    paster_plugins = ["ZopeSkel"],
    )
