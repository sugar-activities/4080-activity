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
import gtk
import pango

import modele
import canvas_graphique

#------------------------------------------------------------------------------

class CanvasInstrument(canvas_graphique.CanvasGraphique):
	
	#----------------------------------------------------------------------------

	def get_solutions(self, ens, ins):
		"""
		Methode permettant de retrouver tous les doigtes d'un instrument pour
		un ensemble de notes

		@param ens: ensemble de notes
		@param ins: instrument
		"""
		# - liste est la liste des sons
		# - lisNH est la liste des possibilites pour chaque son de 'liste'
		# - lisNB est le nombre de solutions pour chaque son : pour la
		#   representation graphique, au moins une colonne meme s'il n'y a
		#   pas de solutions)
		# - nbrCOL est le nombre total de solutions pour tous les sons
		liste = ens.getListe()
		lisNH = map(ins.searchSon, liste)
		lisNB = map(lambda e:max(1, len(e)), lisNH)
		nbrCOL = sum(lisNB)
		return liste, lisNH, lisNB, nbrCOL

	#----------------------------------------------------------------------
	
	def setNotes(self, ens):
		assert type(ens) == list or type(ens) in [unicode, str] or ens.__class__.__name__ == "Ensemble"
		if ens.__class__.__name__ != "Ensemble" :
			self.ens = modele.Ensemble("", ens)
		else:
			self.ens = ens
		self.queue_draw()

	def setInstrument(self, ins):
		assert ins != None
		self.ins = ins
		self.queue_draw()

	def setNotesInstrument(self, ens, ins):
		assert type(ens) == list or type(ens) in [unicode, str] or ens.__class__.__name__ == "Ensemble"
		assert ins != None
		if ens.__class__.__name__ != "Ensemble" :
			self.ens = modele.Ensemble("", ens)
		else:
			self.ens = ens
		self.ins = ins
		self.queue_draw()

	#----------------------------------------------------------------------

	def __init__(self, lar, hau, ens = "", rpx = 0.95, rpy = 0.95):
		"""
		@param lar: largeur du canvas
		@param hau: hauteur du canvas
		@param ens: ensemble de notes
		@param rpx: partie horizontale de la zone utilisee 
		@param rpy: partie verticale de la zone utilisee 
		"""
		super(CanvasInstrument,self).__init__(lar, hau, rpx, rpy)
		self.setNotes(ens)
		self.set_size_request(lar, hau)
		self.show()
