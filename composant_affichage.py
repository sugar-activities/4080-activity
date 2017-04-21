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

import pygtk
pygtk.require('2.0')
import gtk

#------------------------------------------------------------------------------

from modele import *
from commun import *

#------------------------------------------------------------------------------

class ComposantAffichage:
	
	def getNom(self):
		return self.nom
	
	def getContainer(self):
		return self.container

	def update(self, ens):
		tracer("ComposantAffichage", "update")
		ens = Ensemble("", ens)
		if self.ens == None or ens != self.ens:
			self.ens = ens
			page_num = self.notebook.get_current_page()
			self.__gerer(None, None, page_num, None)

	def __gerer(self, widget, page, page_num, user_param):
		tracer("ComposantAffichage", "__gerer")
		# en fonction de l'onglet selectionne
		# on affecte l'ensemble de notes au bon
		# composant
		comp = self.listeCMP[page_num]
		if self.ens == None:
			comp.update("")
		else:
			comp.update(self.ens)

	def __init__(self, nom, notes, modules, orient=gtk.POS_RIGHT):
		tracer("ComposantAffichage", "__init__")
		self.nom = nom
		self.listeNOM = []
		self.listeCNT = []
		self.listeCMP = modules
		for comp in modules:
			self.listeNOM.append(comp.getNom())
			self.listeCNT.append(comp.getContainer())
		self.notebook = definirNotebook(orient, self.listeNOM, self.listeCNT, 0)
		self.container = definirVBOX([self.notebook], True, True)
		self.ens = None
		self.update(notes)
		self.hNB = self.notebook.connect("switch-page" , self.__gerer, None)
		
