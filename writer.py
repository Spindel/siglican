# -*- coding:utf-8 -*-

# Copyright (c) 2009-2014 - Simon Conseil
# Copyright (c)      2013 - Christophe-Marie Duquesne

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

# Copyright (c) 2014 - Scott Boone
# This is a copy of Sigal's Writer module with minor changes to the names of 
# settings keys for siglican.

from __future__ import absolute_import

import codecs
import jinja2
import logging
import os
import sys

from distutils.dir_util import copy_tree
from jinja2 import Environment, FileSystemLoader, ChoiceLoader, PrefixLoader
from jinja2.exceptions import TemplateNotFound

from .pkgmeta import __url__ as sigal_link
from .utils import url_from_path

class Writer(object):
    """Generate html pages for each directory of images."""
    
    def __init__(self, settings, theme=None, index_title=''):
        self.settings = settings
        self.output_dir = settings['SIGAL_DESTINATION']
        self.index_title = index_title
        self.logger = logging.getLogger(__name__)
        
        # check for a custom theme in ./sigal/themes, if not found, look for a
        # default in the sigal_theme/themes plugin directory
        self.theme = settings['SIGAL_THEME']
        default_themes = os.path.normpath(os.path.join(
                         os.path.abspath(os.path.dirname(__file__)), 'themes'))
        self.logger.debug("siglican: custom theme: %s", self.theme)
        self.logger.debug("siglican: default themedir: %s", default_themes)
        if not os.path.exists(self.theme):
            self.theme = os.path.join(default_themes, os.path.basename(self.theme))
            if not os.path.exists(self.theme):
                raise Exception("siglican: unable to find theme: %s" %
                                 os.path.basename(self.theme))
        
        self.logger.info("siglican theme: %s", self.theme)
        
        # pelican theme path merged with siglican theme path 
        theme_paths = [ os.path.join(self.theme, 'templates'),
                        os.path.join(self.settings['THEME'], 'templates') ]
        
        # setup jinja env
        env_options = {'trim_blocks': True}
        try:
            if tuple(int(x) for x in jinja2.__version__.split('.')) >= (2, 7):
                env_options['lstrip_blocks'] = True
        except ValueError:
            pass
        
        ### note: removed the default loader since sigal default templates 
        ###       were only used for google analytics, which have been
        ###       removed from the siglican plugin port
        env = Environment(loader=FileSystemLoader(theme_paths),
                          **env_options)
                
        try:
            self.template = env.get_template('album.html')
        except TemplateNotFound:
            self.logger.error('siglican: template album.html not found')
            sys.exit(1)
        
        # Copy the theme files in the output dir
        self.theme_path = os.path.join(settings['OUTPUT_PATH'], self.output_dir,
                                       'static')
        copy_tree(os.path.join(self.theme, 'static'), self.theme_path)
        
    def generate_context(self, album):
        """Generate the context dict for the given path."""
        
        albumdict = {
                        'SIGAL_ALBUM': album,
                        'SIGAL_INDEX_TITLE': self.index_title,
                        'SIGAL_LINK': sigal_link,
                        'SIGAL_THEME_NAME': os.path.basename(self.theme),
                        'SIGAL_THEME_URL': url_from_path(
                                           os.path.relpath(self.theme_path,
                                                           album.dst_path))
                    }
        albumdict.update(self.settings) 
        return albumdict
    
    def write(self, album):
        """Generate the HTML page and save it."""

        page = self.template.render(**self.generate_context(album))
        output_file = os.path.join(album.dst_path, album.output_file)
        self.logger.debug("siglican: write output_file: %s",output_file)

        with codecs.open(output_file, 'w', 'utf-8') as f:
            f.write(page)