# -*- coding: utf-8 -*-

#
# Copyright (c) 2013 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import deque
from redhat_support_tool.helpers.confighelper import _
from redhat_support_tool.helpers.launchhelper import LaunchHelper
from redhat_support_tool.plugins import HiddenCommand, InteractivePlugin
import logging

__author__ = 'Nigel Jones <nigjones@redhat.com>'

logger = logging.getLogger("redhat_support_tool.helpers.genericprompt")


class GenericPrompt(InteractivePlugin, HiddenCommand):
    '''A generic interactive prompt that can be called by plugins.

    In some cases it may be wise from a UI perspective to trigger a second,
    interactive prompt outside of the current plugin.

    Usage:
        ObjectDisplayOptions should be used when interacting with this helper,
        the object component used in the ObjectDisplayOption passed to
        LaunchHelper when launching this plugin should be a dict with the
        following data:
            'lhplugin':  class of the plugin to pass prompt options to
            'type':  string of type of data displayed (i.e. Recommendations,
                     Varieties, Instruments, ...)
            'options':  a deque() of ObjectDisplayOptions for use in the plugin
                        prompts

        The object item in the ObjectDisplayOptions for the options, is a dict
        with the following data:
            'pt_str':  string passed to LaunchHelper class (i.e. a knowledge
                       base article ID) - blank string allowed
            'pt_obj':  an object to be passed in an ObjectDisplayOption to the
                       called LaunchHelper class.
                       If not used, should be set to None
    '''
    plugin_name = 'genericprompt'
    ALL = _("Generic prompt")
    _submenu_opts = None
    metadata = None

    def get_sub_menu_options(self):
        return self._submenu_opts

    def insert_obj(self, metadata):
        '''
        Allow insertion of a package object by launchhelper (when selecting
        from the list generated by list_kerneldebugs.py)
        '''
        self.metadata = metadata

    def postinit(self):
        prompttype = self.metadata['type'].lower()
        self.partial_entries = _('%s of %s %s displayed. Type'
                                 ' \'m\' to see more.') % ('%s', '%s',
                                                           prompttype)
        self.end_of_entries = _('No more %s to display') % (prompttype)
        self._submenu_opts = self.metadata['options']

    def interactive_action(self, display_option=None):
        try:
            dopt_metadata = display_option.stored_obj
            lh = LaunchHelper(self.metadata['lhplugin'])
            if dopt_metadata['pt_obj']:
                display_option.stored_obj = dopt_metadata['pt_obj']
                lh.run(dopt_metadata['pt_str'], display_option)
            else:
                lh.run(dopt_metadata['pt_str'])
        except:
            raise
