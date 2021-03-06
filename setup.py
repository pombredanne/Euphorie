from setuptools import setup, find_packages

version = '6.1'

setup(name="Euphorie",
      version=version,
      description="Euphorie Risk Assessment tool",
      long_description=open("README.rst").read(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python :: 2 :: Only",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords="",
      author="Wichert Akkerman",
      author_email="wichert@simplon.biz",
      url="http://euphorie.readthedocs.org/en/latest/",
      license="GPL",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "Plone >=4.0b1",
          "Zope2 >=2.12",
          'AccessControl >= 3.0',
          "Products.CMFEditions >=2.0b8",
          "Products.PasswordResetTool >=2.0.3",
          'Products.membrane >=2.1.3',
          "collective.indexing >=1.1",
          "SQLAlchemy >=0.5.2",
          "decorator",
          "five.grok",
          "htmllaundry [z3cform] >=1.1dev-r11183",
          "lxml",
          "plone.app.dexterity",
          "plone.app.folder",
          "plone.app.imaging",
          "plone.app.redirector >= 1.0.12dev-r27477",
          "plone.app.vocabularies",
          "plone.app.z3cform",
          "plone.behavior >=1.0b4",
          "plone.dexterity >=1.0b6",
          "plone.directives.dexterity",
          "plone.directives.form",
          "plone.formwidget.namedfile",
          "plone.memoize",
          "plone.namedfile[blobs]",
          "repoze.formapi >=0.4.2",
          "setuptools",
          "simplejson",
          "z3c.form >= 2.1.0",
          "z3c.schema",
          "z3c.saconfig",
          "zope.app.schema",
          "zope.configuration >= 3.6",
          "zope.i18nmessageid",
          "zope.interface",
          "zope.schema",
          "NuPlone >=1.3.1",
          "plone.uuid",
          "pyrtf-ng",
          "z3c.appconfig >=1.0",
          "openpyxl",
      ],
      tests_require=[
          "collective.testcaselayer >=1.6",
          "Products.PloneTestCase >=0.9.9",
          'mock',
          ],
      extras_require={
              "sphinx": ["Sphinx >=1.0",
                         "repoze.sphinx.autointerface",
                         ],
              "tests": ["collective.testcaselayer",
                        "Products.PloneTestCase >=0.9.9",
                        "mock",
                       ],
      },
      entry_points="""
      [z3c.autoinclude]
      target = plone

      [zopectl.command]
      initdb = euphorie.deployment.commands.initdb:main
      xmlimport = euphorie.deployment.commands.xmlimport:main
      """,
      )
