from distutils.core import setup
setup(
  name = 'latkpy',         # How you named your package folder (MyLib)
  packages = ['latkpy'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Lightning Artist Toolkit for volumetric animation',   # Give a short description about your library
  author = 'Nick Fox-Gieg',                   # Type in your name
  author_email = 'nick@fox-gieg.com',      # Type in your E-Mail
  url = 'https://lightningartist.org',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/LightningArtist/latkpy/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['animation', 'blender', 'drawing'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      'json',
      'math',
      'numpy',
      'zipfile',
      'io',
      'os',
      'json',
      'uuid',
      'struct',
      'contextlib',
      'collections',
      'random',
      'functools',
      'sys'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)