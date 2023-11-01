from distutils.core import setup
setup(
  name = 'latk',         # How you named your package folder (MyLib)
  packages = ['latk'],   # Chose the same as "name"
  version = '2.9.0',      # Start with a small number and increase it with every change you make
  license='apache-2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Lightning Artist Toolkit for volumetric animation',   # Give a short description about your library
  author = 'Nick Fox-Gieg',                   # Type in your name
  author_email = 'nick@fox-gieg.com',      # Type in your E-Mail
  url = 'https://fox-gieg.com',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/LightningArtist/latkpy/archive/refs/tags/2.9.0.tar.gz',    # I explain this later on
  keywords = ['animation', 'blender', 'drawing'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      'numpy'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Multimedia :: Graphics :: 3D Modeling',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
  ],
)