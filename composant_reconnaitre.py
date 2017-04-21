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

import random
import time
import copy

from commun import *
from modele import *
from modele_data import *
import jouer_notes

#------------------------------------------------------------------------------

class ComposantNOT:

	def getContainer(self):
		return self.container

	def __keyPress(self, widget, event):
		key = gtk.gdk.keyval_name(event.keyval)
		if key in ['KP_Home', 'KP_End']:
			if widget == self.butECO:
				self.__ecouter(widget, None)
			else:
				self.__essayer(widget, None)

	def __recommencer(self, widget, data):
		"""
		Quand on recommence une partie :
		- on selectionne un son qui n'est pas le precedent son tire au sort
		- on desactive les boutons de choix tant que le son n'a pas ete ecoute
		"""
		random.seed(time.time())
		fin = len(self.lisFIC) - 1
		if fin == 0:
			self.indSEL = 0
		else:
			while True:
				ind = random.randint(0, fin)
				if self.indSEL == None or self.indSEL != ind:
					self.indSEL = ind
					break
		self.essais = 0
		self.ecoute = False
		for elt in self.lisBUT:
			elt.set_sensitive(self.ecoute)
		self.butECO.grab_focus()

	def __ecouter(self, widget, data):
		"""
		Quand on ecoute le son :
		- si pour la partie on ecoute le son pour la premiere fois,
		  on efface la zone de reponse (le bravo precedent s'il existe)
		  puis on active tous les boutons
		- on joue le son tire au hasard
		"""
		if not self.ecoute:
			self.txtREP.set_label("")
			self.ecoute = True
			for elt in self.lisBUT:
				elt.set_sensitive(self.ecoute)
		fic = self.lisFIC[self.indSEL]
		jouer_notes.jouerEchantillonsMIX([fic], 600)	

	def __essayer(self, widget, data):
		"""
		Essai d'une note :
		- recuperation de la note choisie
		- lecture de la note
		- affichage de la reponse : 
		  si bonne reponse => preparation d'une nouvelle partie 
		  (nouveau son)
		"""
		ind = self.lisBUT.index(widget)
		if ind >= 0:
			nbr = self.essais + 1
			fic = self.lisFIC[ind]
			nom = self.lisNOM[ind]
			jouer_notes.jouerEchantillonsMIX([fic], 600)
			if ind == self.indSEL:
				self.__recommencer(None, None)
				self.txtREP.set_label(TXT_REC_SUC %(nbr, nom))
			else:
				self.essais = nbr
				self.txtREP.set_label(TXT_REC_ERR %(nbr, nom))

	def __init_components(self):
		# recuperation de la liste des sons, des noms, des boutons et des
		# fichiers
		self.lisSON = self.ens.getListe()
		sonREF = Son(self.lisSON[0].getValeur() + NOMBRE_NOTES_OCTAVE)
		self.lisSON.append(sonREF)
		self.lisNOM = map(lambda e:str(e), self.lisSON)
		self.lisBUT = map(lambda e:definirButton(e), self.lisNOM)
		self.lisFIC = jouer_notes.transformerNotes(self.lisSON, True)
		# construction des widgets
		titQCM = definirLabel(self.tit)
		cntNOT = definirHBOX(self.lisBUT, True, True)
		self.butECO = definirButton(TXT_REC_LIS)
		txtINF = definirLabel(_(TXT_REC_LNI))
		self.txtREP = definirLabel("")
		ligECO = definirHBOX([txtINF, self.butECO], True, True)
		ecrCNT = definirVBOX([titQCM, cntNOT, ligECO, self.txtREP], True, True)
		# definition des attributs
		self.container = ecrCNT
		self.indSEL = None

	def __init_events(self):
		self.hECO = self.butECO.connect("clicked" , self.__ecouter, None)
		self.hEKP = self.butECO.connect("key-press-event", self.__keyPress)
		self.hSON = map(lambda e:e.connect("clicked", self.__essayer, None), self.lisBUT)
		self.hSKP = map(lambda e:e.connect("key-press-event", self.__keyPress), self.lisBUT)

	def __del__(self):
		tracer("rec.ComposantNOT", "__del__")
		disconnectEVENT(self.butECO, self.hECO)
		disconnectEVENT(self.butECO, self.hEKP)
		nbr = len(self.lisBUT)
		lis = range(nbr)
		for ind in lis:
			disconnectEVENT(self.lisBUT[ind], self.hSON[ind])
			disconnectEVENT(self.lisBUT[ind], self.hSKP[ind])

	def __init__(self, ens):
		tracer("rec.ComposantNOT", "__init__")
		self.tit = "%s :" %(TXT_REC_NOT)
		self.ens = Ensemble("", ens)
		self.__init_components()
		self.__init_events()
		self.__recommencer(None, None)

#------------------------------------------------------------------------------

class ComposantINT:

	def getContainer(self):
		return self.container

	def __keyPress(self, widget, event):
		key = gtk.gdk.keyval_name(event.keyval)
		if key in ['KP_Home', 'KP_End']:
			if widget == self.butECO:
				self.__ecouter(widget, None)
			else:
				self.__essayer(widget, None)

	def __recommencer(self, widget, data):
		"""
		Quand on recommence une partie :
		- on selectionne un son qui n'est pas le precedent son tire au sort
		- on desactive les boutons de choix tant que le son n'a pas ete ecoute
		"""
		random.seed(time.time())
		fin = len(self.lisFIC) - 1
		if fin == 0:
			self.indSEL = 0
		else:
			while True:
				ind = random.randint(0, fin)
				if self.indSEL == None or self.indSEL != ind:
					self.indSEL = ind
					break
		self.essais = 0
		self.ecoute = False
		for elt in self.lisBUT:
			elt.set_sensitive(self.ecoute)
		self.butECO.grab_focus()

	def __ecouter(self, widget, data):
		"""
		Quand on ecoute le son :
		- si pour la partie on ecoute le son pour la premiere fois,
		  on efface la zone de reponse (le bravo precedent s'il existe)
		  puis on active tous les boutons
		- on joue le son tire au hasard
		"""
		if not self.ecoute:
			self.txtREP.set_label("")
			self.ecoute = True
			for elt in self.lisBUT:
				elt.set_sensitive(self.ecoute)
		fdr = self.lisFIC[0]
		fic = self.lisFIC[self.indSEL]
		jouer_notes.jouerEchantillonsMIX([fdr, fic], 800)	
		jouer_notes.jouerEchantillonsSEQ([fdr, fic], 600)

	def __essayer(self, widget, data):
		"""
		Essai d'une note :
		- recuperation de la note choisie
		- lecture de la note
		- affichage de la reponse : 
		  si bonne reponse => preparation d'une nouvelle partie 
		  (nouveau son)
		"""
		ind = self.lisBUT.index(widget)
		if ind >= 0:
			nbr = self.essais + 1
			fdr = self.lisFIC[0]
			fic = self.lisFIC[ind]
			nom = self.lisNOM[ind].replace("\n", " : ")
			jouer_notes.jouerEchantillonsMIX([fdr, fic], 800)
			jouer_notes.jouerEchantillonsSEQ([fdr, fic], 600)
			if ind == self.indSEL:
				self.__recommencer(None, None)
				self.txtREP.set_label(TXT_REC_SUC %(nbr, nom))
			else:
				self.essais = nbr
				self.txtREP.set_label(TXT_REC_ERR %(nbr, nom))

	def __init_components(self):
		# recuperation de la liste des sons, des noms, des boutons et des
		# fichiers
		self.lisSON = self.ens.getListe()
		refSON = self.lisSON[0]
		refVAL = refSON.getValeur()
		octSON = Son(refVAL + NOMBRE_NOTES_OCTAVE)
		self.lisSON.append(octSON)
		lisVAL = map(lambda e:e.getValeur()-refVAL, self.lisSON)
		lisNDG = copy.copy(LISTE_NOMS_DEGRES)
		lisNDG[0] = TXT_DEG_UNI
		lisNDG.append(TXT_DEG_OCT)
		self.lisNOM = map(lambda e:lisNDG[e], lisVAL)
		nbr = len(self.lisNOM)
		for ind in range(nbr):
			self.lisNOM[ind] = ("%s\n[%s %s]") %(self.lisNOM[ind], str(refSON), str(self.lisSON[ind]))
		self.lisBUT = map(lambda e:definirButton(e), self.lisNOM)
		self.lisFIC = jouer_notes.transformerNotes(self.lisSON, True)
		# construction des widgets
		titQCM = definirLabel(self.tit)
		cntNOT = definirHBOX(self.lisBUT, True, True)
		self.butECO = definirButton(TXT_REC_LIS)
		txtINF = definirLabel(TXT_REC_LII)
		self.txtREP = definirLabel("")
		ligECO = definirHBOX([txtINF, self.butECO], True, True)
		ecrCNT = definirVBOX([titQCM, cntNOT, ligECO, self.txtREP], True, True)
		# definition des attributs
		self.container = ecrCNT
		self.indSEL = None

	def __init_events(self):
		self.hECO = self.butECO.connect("clicked" , self.__ecouter, None)
		self.hEKP = self.butECO.connect("key-press-event", self.__keyPress)
		self.hSON = map(lambda e:e.connect("clicked", self.__essayer, None), self.lisBUT)
		self.hSKP = map(lambda e:e.connect("key-press-event", self.__keyPress), self.lisBUT)

	def __del__(self):
		tracer("rec.ComposantINT", "__del__")
		disconnectEVENT(self.butECO, self.hECO)
		disconnectEVENT(self.butECO, self.hEKP)		
		nbr = len(self.lisBUT)
		lis = range(nbr)
		for ind in lis:
			disconnectEVENT(self.lisBUT[ind], self.hSON[ind])
			disconnectEVENT(self.lisBUT[ind], self.hSKP[ind])
		
	def __init__(self, ens):
		tracer("rec.ComposantINT", "__init__")
		self.tit = "%s :" % (TXT_REC_INT)
		self.ens = Ensemble("", ens)
		self.__init_components()
		self.__init_events()
		self.__recommencer(None, None)

#------------------------------------------------------------------------------

class ComposantReconnaitre:

	def getNom(self):
		return TXT_ONG_REC

	def getContainer(self):
		return self.container

	def update(self, ens):
		ens = Ensemble("", ens)
		if self.ens == None or ens != self.ens:
			for elt in self.vbox.get_children():
				self.vbox.remove(elt)
			self.ens = ens
			if ens != "":
				hau = ComposantNOT(ens)
				bas = ComposantINT(ens)
				self.vbox.add(hau.getContainer())
				self.vbox.add(bas.getContainer())

	def __init__(self, notes):
		tracer("ComposantReconnaitre", "__init__")
		self.ens = Ensemble("", notes)
		hau = ComposantNOT(self.ens)
		bas = ComposantINT(self.ens)
		self.vbox = definirVBOX([hau.getContainer(), bas.getContainer()])
		self.container = definirScrolledWindow(self.vbox, 'with_viewport')

