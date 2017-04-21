#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------

# Copyright 2008-2009 : François Sénéquier
# Email : francois.senequier@netcourrier.com

# This file is part of 'Theorie'.
#
# 'Theorie' is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# 'Theorie' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 'Theorie'.  If not, see <http://www.gnu.org/licenses/>.

#------------------------------------------------------------------------------

try:
	import psyco
	psyco.full()
	print "'Psyco' active !"
except ImportError:
	print "'Psyco' introuvable !"

#------------------------------------------------------------------------------

try:
	import gc
	gc.enable()
	gc.collect()
	print "Execution du ramasse-miettes !"
except:
	print "Erreur du ramasse-miettes !"

#------------------------------------------------------------------------------

try:
	import os, sys, time
	import locale, gettext
	if os.name == 'nt':
		lang = os.getenv('LANG')
		if lang is None:
			default_lang, default_enc = locale.getdefaultlocale()
			if default_lang:
				lang = default_lang
		if lang:
			os.environ['LANG'] = lang
	pathname = os.path.dirname(sys.argv[0])
	subdir   = "/locale"
	localdir = os.path.abspath(pathname) + subdir
	domain   = "messages"
	codeset  = "utf-8"
	gettext.bind_textdomain_codeset(domain, codeset)
	gettext.install("messages", localdir)
	print "Internationalisation activee (%s) !" %(os.name)
except:
	print "Erreur du module d'internationalisation !"
