siglican
========

A static gallery generator plugin for Pelican, based on the Sigal
Colorbox/Galleria static site generator.

##How To
1. Put this folder into your Pelican plugins directory. Add 'siglican' to
   PLUGINS in pelicanconf.py.
2. Create a 'siglican' directory in your base directory, at the same level as
   'content'. Drag 'colorbox' or 'galleria' from the 'themes' directory into
   this folder. Also create an 'images' subdirectory under 'siglican'.
3. Create album and image metadata, as desired.
4. Create theme directory inside of 'siglican'. Use the colorbox or galleria
   theme as a starting point. Make sure that your Pelican theme's base.html
   template has a 'head' block defined before </head>.

Example directory tree:
```
   /site
     /content/*
     /plugins/siglican/*.py
     /siglican
       /images
         /album1
         /album2
         /...
       /[colorbox|galleria]
         /static/*
         /templates/album.html
```

##Pelican settings

## To Do
1. Update galleria theme to work.
2. Unit tests.
3. Logging cleanup.
4. Update colorbox/galleria example themes to deal better with nested albums.
5. General code and documentation cleanup.
   
##Credits
* Around 2/3 of the core Python code is ported from [Sigal v0.8.0](http://sigal.saimon.org/) by Simon Conseil.
* Heavily leverages Pelican, Jinja2, Colorbox, and Galleria.
* Pelican integration by Scott Boone (sawall@github).