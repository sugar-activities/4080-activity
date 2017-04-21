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

from commun import *
from observable import *

#------------------------------------------------------------------------------

class ComposantSelection(Observable):
	
	def getNom(self):
		return self.nom
	
	def getContainer(self):
		return self.container

	def update(self, prm):
		tracer("ComposantSelection", "update")
		self.notifyObservers(prm)

	def __gerer(self, widget, page, page_num, user_param):
		tracer("ComposantSelection", "__gerer")
		# 'widget' est l'onglet (notebook)
		# 'page_num' est l'indice de la page selectionnee dans l'onglet
		obj = self.listeCMP[page_num]
		prm = obj.getNotes()
		self.notifyObservers(prm)

	def __init__(self, nom, modules, orient):
		tracer("ComposantSelection", "__init__")
		Observable.__init__(self)
		self.nom = nom
		self.listeNOM = []
		self.listeCNT = []
		self.listeCMP = modules
		for comp in modules:
			self.listeNOM.append(comp.getNom())
			self.listeCNT.append(comp.getContainer())
			comp.addObserver(self)
		self.notebook = definirNotebook(orient, self.listeNOM, self.listeCNT, 0)
		self.container = definirVBOX([self.notebook], True, True)
		self.hNB = self.notebook.connect("switch-page" , self.__gerer, None)
