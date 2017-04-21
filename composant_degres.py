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
from observable import *

import jouer_notes

#------------------------------------------------------------------------------

class ComposantDegres(Observable):
	
	def getContainer(self):
		return self.container

	def getNotes(self):
		return self.notes

	def __nom(self, txt):
		return txt.split(":")[1].strip()	

	def __init_components(self, nomDEG, nomNOT, nomMOD, lisDEG):
		self.tooltips = gtk.Tooltips()
		lisNOM = []
		lisNBR = range(2, NOMBRE_NOTES_OCTAVE)
		for nbr in lisNBR:
			lisTMP = lisDEG.getListeNomsDegres(nbr)
			lisTMP = map(lambda e: "[%d] :  %s" %(nbr, e), lisTMP)
			lisTMP.sort()
			lisNOM += lisTMP
		lisTON = LISTE_NOMS_NOTES
		lisMOD = lisDEG.getDegres(self.__nom(lisNOM[0])).getDegresSEL()
		#
		labelDEG, comboDEG = definirLabelCombo(nomDEG, lisNOM)
		labelTON, comboTON = definirLabelCombo(nomNOT, lisTON)
		labelMOD, comboMOD = definirLabelCombo(nomMOD, lisMOD)
		checkREL = definirCheckButton("_" + TXT_REL)
		labelNOT = definirLabel(TXT_NOT + " : ")
		texteNOT = definirButton("")
		texteTEN = definirLabel("")
		texteINT = definirLabel("")
		texteIDT = definirLabel("")
		#
		lisTLB = [labelDEG, comboDEG, ""]
		lisTLB += [labelTON, comboTON, ""]
		lisTLB += [labelMOD, comboMOD, ""]
		lisTLB += [checkREL]
		tlb1 = definirTOOLBAR(lisTLB)
		tlb2 = definirTOOLBAR([labelNOT, texteNOT, texteTEN])
		self.container = definirVBOX([tlb1, tlb2], True, True)
		#
		self.comboDEG = comboDEG
		self.comboTON = comboTON
		self.comboMOD = comboMOD
		self.checkREL = checkREL
		self.texteNOT = texteNOT
		self.texteTEN = texteTEN
		self.lisDEG = lisDEG
		self.tlbNOT = tlb2

	def __jouer(self, widget, data):
		if self.ens != None:
			lis = self.ens.getListe()
			lis = map(lambda e: Son(e), lis)
			val = Son(lis[0])
			val.decaler(12)
			lis.append(val)
			jouer_notes.jouerNotesSEQ(lis, 600)	

	def __init_events(self):
		self.hDEG = self.comboDEG.connect("changed" , self.__gerer, None)
		self.hTON = self.comboTON.connect("changed" , self.__gerer, None)
		self.hMOD = self.comboMOD.connect("changed" , self.__gerer, None)
		self.hREL = self.checkREL.connect("clicked" , self.__gerer, None)
		self.hCJN = self.texteNOT.connect("clicked" , self.__jouer, None)
		self.hKJN = self.texteNOT.connect("key-press-event", self.__keyPress)
		self.hKEY = self.checkREL.connect("key-press-event", self.__keyPress)

	def __update_combo(self, combo, liste, modes, defaut):
		for ind in range(NOMBRE_NOTES_OCTAVE):
			combo.remove_text(0)
		nbr = len(liste)
		lis = range(nbr)
		for ind in lis:
			nom = liste[ind]
			if modes != None and len(modes) >= 0 and ind < len(modes) and modes[ind] not in [None, '']:
				nom = "%s : %s" %(nom, modes[ind]) 
			combo.append_text(nom)
		combo.set_active(defaut)

	def __keyPress(self, widget, event):
		key = gtk.gdk.keyval_name(event.keyval)
		if key in ['KP_Home', 'KP_End']:
			if widget == self.checkREL:
				# etat de la case a cocher des modes
				active = widget.get_active()
				widget.set_active(not active)
				return True
			elif widget == self.texteNOT:
				# jeu des notes
				self.__jouer(None, None)
				return True
		return False

	def __gerer(self, widget, data):
		tracer("ComposantDegres", "__gerer")
		nom = self.__nom(self.comboDEG.get_active_text())
		ton = self.comboTON.get_active_text()
		chk = self.checkREL.get_active()
		deg = self.lisDEG.getDegres(nom)
		#
		if widget == self.comboDEG or widget == None:
			sel = deg.getDegresSEL()
			ndm = deg.getListeNomsModes()
			if widget != None:
				self.comboMOD.handler_block(self.hMOD)
			self.__update_combo(self.comboMOD, sel, ndm, 0)
			if widget != None:
				self.comboMOD.handler_unblock(self.hMOD)
		mod = self.comboMOD.get_active_text().split(":")[0].strip()
		self.ens = deg.getNotes(ton, mod, chk)
		self.ens.decaler(-NOMBRE_NOTES_OCTAVE)
		ldn = self.ens.getTexte(MOD_NOT)
		self.texteNOT.set_label(ldn)
		tns = self.ens.getTension()
		txt = " [%s = %d]" %(TXT_TIT_TEN, tns)
		self.texteTEN.set_text(txt)
		liste = deg.getDegresSEL(mod)
		txt = "%s : " %(TXT_INT)
		sep = ", "
		tx1 = "\n- %s : " %(TXT_CHX_NOM)
		tx2 = " [, %s]" %(TXT_ABR_OCT)
		txt += formater(tx1, sep, tx2, liste)
		deb = str(liste[0])
		liste = deg.getDegresEDT(mod)
		nbr = len(liste)
		der = liste[nbr - 1]
		sep = " + "
		liste = liste[0:nbr-1]
		der = " [+ %d]" %(der)
		deb = "\n- %s : %s%s" %(TXT_CHX_EDT, deb, sep)
		txt += formater(deb, sep, der, liste)
		self.tooltips.set_tip(self.tlbNOT, txt, None)
		self.notes = self.ens.getTexte(MOD_OCT)
		self.notifyObservers(self.notes)
				
	def __init__(self, nomDEG, nomNOT, nomMOD, lisDEG):
		tracer("ComposantDegres", "__init__")
		Observable.__init__(self)
		self.__init_components(nomDEG, nomNOT, nomMOD, lisDEG)
		self.__gerer(None, None)
		self.__init_events()

#------------------------------------------------------------------------------

class ComposantGammes(ComposantDegres):
	
	def getNom(self):
		return TXT_ONG_GAM
	
	def __init__(self):
		ComposantDegres.__init__(self, TXT_GAM, TXT_TON, TXT_MOD, LISTE_GAMMES)

#------------------------------------------------------------------------------

class ComposantAccords(ComposantDegres):
	
	def getNom(self):
		return TXT_ONG_ACC

	def __jouer(self, widget, data):
		if self.ens != None:
			lis = self.ens.getListe()
			lis = map(lambda e: Son(e), lis)
			jouer_notes.jouerNotesMIX(lis, 1000)
			jouer_notes.jouerNotesSEQ(lis, 600)
			
	def __keyPress(self, widget, event):
		key = gtk.gdk.keyval_name(event.keyval)
		if key in ['KP_Home', 'KP_End']:
			# jeu des notes
			self.__jouer(None, None)
			return True
		return False

	def __init__(self):
		ComposantDegres.__init__(self, TXT_ACC, TXT_FND, TXT_REN, LISTE_ACCORDS)
		self.texteNOT.handler_block(self.hCJN)
		self.texteNOT.handler_block(self.hKJN)
		self.hJOU = self.texteNOT.connect("clicked" , self.__jouer, None)
		self.hKPE = self.texteNOT.connect("key-press-event", self.__keyPress)
