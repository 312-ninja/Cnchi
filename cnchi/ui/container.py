#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  container.py
#
#  Copyright © 2016 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

import logging
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ui.base_widget import BaseWidget


class Container(BaseWidget, Gtk.Container):
    """
      Base class for the main components of Cnchi's UI (pages and page stacks).

    """

    params = None
    params_initialized = False

    def __init__(self, template_dir='', name='', parent=None, *args, **kwargs):
        super().__init__(template_dir=template_dir, name=name, parent=parent, *args, **kwargs)

        logging.debug("Loading '%s' %s", name, self.__class__.name)

        if self.params is None:
            self.params = {}

        self.children = []

        params = ['callback_queue', 'disable_tryit', 'top_nav_buttons', 'header',
                  'sub_nav_buttons', 'main_progressbar', 'process_list']

        if not self.params_initialized:
            self.params_initialized = True
            for param in params:
                if param not in self.params:
                    self.params[param] = None

