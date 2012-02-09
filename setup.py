from setuptools import setup, find_packages 
version = '0.2.1'
tests_require = ['plone.app.testing']

setup(name='mooball.viewlets.contactform',
      version=version,
      description="Contact Form viewlet",
      long_description="",
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Roman Joost',
      author_email='roman@mooball.net',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['mooball','mooball.viewlets'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Products.statusmessages',
          'plone.app.dexterity',
          'plone.formwidget.captcha',
          'setuptools',
      ],
      extras_require=dict(tests=tests_require),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],

      )
