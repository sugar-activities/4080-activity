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

from modele import *
from modele_data import *
from commun import *

import canvas_clarinette

#------------------------------------------------------------------------------

class ComposantClarinette:
	
	def __gerer(self, widget, data):
		tracer("ComposantClarinette", "__gerer")
		prm = int(self.comboPD.get_active_text())
		nbr = int(self.comboPN.get_active_text())
		ins = self.comboTI.get_active_text()
		ens = ajouterNotes(self.ens, prm, nbr)
		lnt = ens.getTexte(MOD_OCT)
		ins = self.liste.getInstrument(ins)
		self.canvas.setNotesInstrument(lnt, ins)
	
	#----------------------------------------------------------------------
	
	def getNom(self):
		return TXT_ONG_CLA
	
	def getContainer(self):
		return self.container

	def update(self, ens):
		tracer("ComposantClarinette", "update")
		ens = Ensemble("", ens)
		if self.ens == None or ens != self.ens:
			self.ens = ens
			self.__gerer(None, None)

	#----------------------------------------------------------------------

	def __init__(self, notes):
		tracer("ComposantClarinette", "__init__")
		self.liste = ListeClarinettes()
		self.noms = self.liste.getListeNoms()
		instrument = self.liste.getInstrument(self.noms[0])
		self.canvas = canvas_clarinette.CanvasClarinette(instrument)
		lisPRE = ['0','1','2']
		lisNBR = ['1','2']
		labelPD, self.comboPD = definirLabelCombo(TXT_OCT_PRM, lisPRE)
		labelPN, self.comboPN = definirLabelCombo(TXT_OCT_NBR, lisNBR)
		self.comboPD.set_active(lisPRE.index('0'))
		self.comboPN.set_active(lisNBR.index('1'))
		labelTI, self.comboTI = definirLabelCombo(TXT_TYP_TON, self.liste.getListeNoms())
		toolbar = definirTOOLBAR([labelPD, self.comboPD, "", labelPN, self.comboPN, "", labelTI, self.comboTI])
		paned = definirVBOX([toolbar], False, False)
		scr = definirScrolledWindow(self.canvas, 'with_viewport')
		self.container = definirVPANED(paned, scr)
		self.ens = None
		self.update(notes)
		self.hPD = self.comboPD.connect("changed" , self.__gerer, None)
		self.hPN = self.comboPN.connect("changed" , self.__gerer, None)
		self.hTI = self.comboTI.connect("changed" , self.__gerer, None)
