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

import canvas_guitare

#------------------------------------------------------------------------------

SENS_GAU = "G"
SENS_DRO = "D"
SENS_HAU = "H"
SENS_BAS = "B"

#------------------------------------------------------------------------------

class ComposantGuitare:
	
	def __gerer(self, widget, data):
		tracer("ComposantGuitare", "__gerer")
		ins = self.comboTI.get_active_text()
		nbc = self.comboNC.get_active_text()
		dgt = self.comboDG.get_active_text()
		ins = self.liste.getInstrument(ins)
		ins.setNombreDeCases(nbc)
		self.canvas.setInstrument(ins)
		self.canvas.setNotes(self.ens.getTexte(MOD_OCT))
		self.canvas.setDoigte(dgt)
	
	#----------------------------------------------------------------------
	
	def getNom(self):
		return TXT_ONG_GUI
	
	def getContainer(self):
		return self.container

	def update(self, ens):
		tracer("ComposantGuitare", "update")
		ens = Ensemble("", ens)
		if self.ens == None or ens != self.ens:
			self.ens = ens
			self.__gerer(None, None)

	#----------------------------------------------------------------------

	def __init__(self, notes, nbcMIN=15, nbcMAX=24, nbcDEF=19, guiDEF=21):
		tracer("ComposantGuitare", "__init__")
		assert nbcMIN <= nbcDEF <= nbcMAX
		self.liste = ListeGuitares()
		noms = self.liste.getListeNoms()
		cases = range(nbcMIN,nbcMAX+1)
		cases = map(str, cases)
		doigtes = [TXT_DGT_4E6,TXT_DGT_3E5,TXT_DGT_EGG,TXT_DGT_EGD]
		instr = self.liste.getInstrument(noms[guiDEF])
		instr.setNombreDeCases(nbcDEF)
		self.canvas = canvas_guitare.CanvasGuitare(instr)
		labelTI, self.comboTI = definirLabelCombo(TXT_TYP_GUI, noms)
		labelNC, self.comboNC = definirLabelCombo(TXT_TYP_NBC, cases)
		labelDG, self.comboDG = definirLabelCombo(TXT_TYP_DGT, doigtes)
		self.comboTI.set_active(guiDEF)
		toolbar = definirTOOLBAR([labelTI, self.comboTI, "", labelNC, self.comboNC, "", labelDG, self.comboDG])
		paned = definirVBOX([toolbar], False, False)
		self.comboNC.set_active(nbcDEF-nbcMIN)
		self.container = definirVPANED(paned, self.canvas)
		self.ens = None
		self.update(notes)
		self.hTI = self.comboTI.connect("changed" , self.__gerer, None)
		self.hNC = self.comboNC.connect("changed" , self.__gerer, None)
		self.hDG = self.comboDG.connect("changed" , self.__gerer, None)
