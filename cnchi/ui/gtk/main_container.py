#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  main_container.py
#
#  Copyright © 2016 Antergos
#
#  This file is part of The Antergos Build Server, (AntBS).
#
#  AntBS is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  AntBS is distributed in the hope that it will be useful,
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
#  along with AntBS; If not, see <http://www.gnu.org/licenses/>.

from ui.base_widgets import Stack

from .pages import (
    check,
    desktop,
    features,
    keymap,
    slides,
    timezone,
    user_info,
    welcome,
    location,
    summary
)

from .pages.installation import (
    advanced,
    alongside,
    ask,
    automatic,
    zfs
)


class MainContainer(Stack):
    """
    Main entry-point for GTK Pages UI.

    Class Attributes:
        all_pages (list): List of initialized pages for the UI.
        See `Stack.__doc__`

    """

    all_pages = None

    def __init__(self, name='main_container', *args, **kwargs):
        """
        Attributes:
            Also see `Stack.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, *args, **kwargs)

        if self.all_pages is None:
            self.all_pages = []

        self.current_stack = None
        self.current_grp = None
        self.current_page = None

        self.next_page = None
        self.prev_page = None
        self.page_count = 0
        self.all_pages = []

        self.pages_loaded = False

        self.top_level_pages = []
        self.pages = {}

    def get_top_pages(self):
        return [p for p in self.pages if not isinstance(self.pages[p], dict)]

    def get_sub_stacks(self):
        top_pages = self.get_top_pages()
        return [self.pages[p]['pages'] for p in self.pages if p not in top_pages]

    def get_sub_pages(self):
        sub_stacks = self.get_sub_stacks()
        return [p for x in sub_stacks for p in x]

    def get_page(self, page_name):
        return self.pages[page_name]

    def get_sub_page(self, page_name, sub_page_name):
        return self.pages[page_name][sub_page_name]

    def set_sub_page(self, page_name, sub_page_name, page):
        self.pages[page_name][sub_page_name] = page

    def get_page_count(self):
        return len(self.pages)

    def loaded(self):
        return self.pages_loaded

    def prepare_current_page(self):
        if self.current_page:
            self.current_page.prepare('forwards')

    def get_current_page(self):
        return self.current_page

    def set_current_page(self, page):
        self.current_page = page

    def get_current_page_name(self):
        if self.current_page:
            return self.current_page.name
        else:
            return None

    def get_next_page(self):
        if self.current_page:
            return self.current_page.get_next_page()
        else:
            return None

    def get_current_stack(self):
        return self.current_stack

    def set_current_stack(self, current_stack):
        self.current_stack = current_stack

    def pre_load_pages(self):
        """ Just load the first two screens (the other ones will be loaded later)
        We do this to reduce Cnchi's initial startup time. """
        self.pages = dict()
        self.pages["location_grp"] = {'title': 'Location',
                                      'prev_page': 'check',
                                      'next_page': 'location',
                                      'pages': ['location', 'timezone', 'keymap']}

        self.pages["check"] = check.Check()
        self.pages["welcome"] = welcome.Welcome()

        self.current_page = self.pages["welcome"]

    def load_all(self):
        """ Load pages """
        self.pages["location_grp"]["location"] = location.Location(name="location", parent=self)
        if not self.pages["location_grp"].get('timezone', False):
            self.pages["location_grp"]["timezone"] = timezone.Timezone(name="timezone",
                                                                       parent=self)

        self.pages["desktop_grp"] = {'title': 'Desktop Selection',
                                     'prev_page': 'location_grp',
                                     'next_page': 'desktop',
                                     'pages': ['desktop', 'features']}

        if self.settings.get('desktop_ask') or True:
            self.pages["location_grp"]["keymap"] = keymap.Keymap(name="keymap", is_last=True)
            self.pages["desktop_grp"]["desktop"] = desktop.DesktopAsk(name="desktop")
            self.pages["desktop_grp"]["features"] = features.Features(name="features",
                                                                      is_last=True)
        else:
            self.pages["location_grp"]["keymap"] = keymap.Keymap(name="keymap",
                                                                 next_page='features',
                                                                 is_last=True)
            self.pages["desktop_grp"]["features"] = features.Features(name="features",
                                                                      prev_page='location_grp',
                                                                      is_last=True)

        self.pages["disk_grp"] = {'title': 'Disk Setup',
                                  'prev_page': 'desktop_grp',
                                  'next_page': 'ask',
                                  'pages': ['ask', 'automatic', 'alongside', 'advanced', 'zfs']}

        self.pages["disk_grp"]["ask"] = ask.InstallationAsk(name="ask")

        self.pages["disk_grp"]["automatic"] = automatic.InstallationAutomatic(name="automatic",
                                                                              is_last=True)

        if self.settings.get("enable_alongside"):
            self.pages["disk_grp"]["alongside"] = alongside.InstallationAlongside(name="alongside")
        else:
            self.pages["disk_grp"]["alongside"] = None

        self.pages["disk_grp"]["advanced"] = advanced.InstallationAdvanced(name="advanced",
                                                                           is_last=True)

        self.pages["disk_grp"]["zfs"] = zfs.InstallationZFS(name="zfs", is_last=True)

        self.pages["user_info"] = user_info.UserInfo(name="user_info")
        self.pages["summary"] = summary.Summary(name="summary")
        self.pages["slides"] = slides.Slides(name="slides")
