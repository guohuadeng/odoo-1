# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2015-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name' : 'Open Record in New Tab',
    'version' : '1.0',
    'depends' : ['sale'],
    'author' : 'BrowseInfo',
    "price": "15",
    "currency": "EUR",
    'category': 'Extra Tools',
    'summary': 'Easy to open record as link on new tab of Browser',
    'description': """
This module add a new button in all tree view.
========================================================================

When one click on new tab icon it will open selected record in form view in new tab.
Open Link in New tab, Open Record in new Tab.
    """,
    'license':'OPL-1',

    'website': 'http://www.browseinfo.in/',
    'data': ['views/new_tab.xml'],
    'qweb' : ['static/src/xml/base.xml'],
    'installable': True,
    'auto_install': False,
"images":['static/description/Banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
