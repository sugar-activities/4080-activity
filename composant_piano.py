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
from commun import *

import canvas_piano

#------------------------------------------------------------------------------

class ComposantPiano:
	
	def __gerer(self, widget, data):
		tracer("ComposantPiano", "__gerer")
		nbr = int(self.comboPN.get_active_text())
		ens = ajouterNotes(self.ens, 0, nbr)
		self.instrument.setNotes(ens.getTexte(MOD_OCT))
	
	#----------------------------------------------------------------------
	
	def getNom(self):
		return TXT_ONG_PIA
	
	def getContainer(self):
		return self.container

	def update(self, ens):
		tracer("ComposantPiano", "update")
		ens = Ensemble("", ens)
		if self.ens == None or ens != self.ens:
			self.ens = ens
			self.__gerer(None, None)

	#----------------------------------------------------------------------

	def __init__(self, notes):
		tracer("ComposantPiano", "__init__")
		self.instrument = canvas_piano.CanvasPiano()
		lisNBR = ['1','2']
		labelPN, self.comboPN = definirLabelCombo(TXT_OCT_NBR, lisNBR)
		self.comboPN.set_active(lisNBR.index('1'))
		toolbar = definirTOOLBAR([labelPN, self.comboPN])
		paned = definirVBOX([toolbar], False, False)
		self.container = definirVPANED(paned, self.instrument)
		self.ens = None
		self.update(notes)
		self.hPN = self.comboPN.connect("changed" , self.__gerer, None)
