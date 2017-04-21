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

import copy

from commun import *
from modele import *
from modele_data import *
import jouer_notes

#------------------------------------------------------------------------------

class ComposantNOT:

	def getContainer(self):
		return self.container

	def __del__(self):
		tracer("ComposantNOT", "__del__")
		nbr = len(self.lisBUT)
		lis = range(nbr)
		for ind in lis:
			disconnectEVENT(self.lisBUT[ind], self.hSON[ind])
			disconnectEVENT(self.lisBUT[ind], self.hSKP[ind])

	def __keyPress(self, widget, event):
		key = gtk.gdk.keyval_name(event.keyval)
		if key in ['KP_Home', 'KP_End']:
			self.__ecouter(widget, None)

	def __ecouter(self, widget, data):
		ind = self.lisBUT.index(widget)
		if ind >= 0:
			fic = self.lisFIC[ind]
			nom = self.lisNOM[ind]
			jouer_notes.jouerEchantillonsMIX([fic], 600, False)

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
		self.container = definirHBOX(self.lisBUT, True, True)

	def __init_events(self):
		self.hSON = map(lambda e:e.connect("clicked", self.__ecouter, None), self.lisBUT)
		self.hSKP = map(lambda e:e.connect("key-press-event", self.__keyPress), self.lisBUT)

	def __init__(self, ens):
		tracer("ComposantNOT", "__init__")
		self.ens = Ensemble("", ens)
		self.__init_components()
		self.__init_events()

#------------------------------------------------------------------------------

class ComposantINT:

	def getContainer(self):
		return self.container

	def __del__(self):
		tracer("ComposantINT", "__del__")
		nbr = len(self.lisBUT)
		lis = range(nbr)
		for ind in lis:
			disconnectEVENT(self.lisBUT[ind], self.hSON[ind])
			disconnectEVENT(self.lisBUT[ind], self.hSKP[ind])

	def __keyPress(self, widget, event):
		key = gtk.gdk.keyval_name(event.keyval)
		if key in ['KP_Home', 'KP_End']:
			self.__ecouter(widget, None)

	def __ecouter(self, widget, data):
		ind = self.lisBUT.index(widget)
		if ind >= 0:
			fdr = self.lisFIC[0]
			fic = self.lisFIC[ind]
			jouer_notes.jouerEchantillonsMIX([fdr, fic], 600, False)

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
		self.container = definirHBOX(self.lisBUT, True, True)

	def __init_events(self):
		self.hSON = map(lambda e:e.connect("clicked", self.__ecouter, None), self.lisBUT)
		self.hSKP = map(lambda e:e.connect("key-press-event", self.__keyPress), self.lisBUT)

	def __init__(self, ens):
		tracer("ComposantINT", "__init__")
		self.ens = Ensemble("", ens)
		self.__init_components()
		self.__init_events()

#-------------------------------------------------------------------------------

class ComposantREN:

	def getContainer(self):
		return self.container

	def __del__(self):
		tracer("ComposantREN", "__del__")
		nbr = len(self.lisBUT)
		lis = range(nbr)
		for ind in lis:
			disconnectEVENT(self.lisBUT[ind], self.hSON[ind])
			disconnectEVENT(self.lisBUT[ind], self.hSKP[ind])

	def __keyPress(self, widget, event):
		key = gtk.gdk.keyval_name(event.keyval)
		if key in ['KP_Home', 'KP_End']:
			self.__ecouter(widget, None)

	def __ecouter(self, widget, data):
		ind = self.lisBUT.index(widget)
		if ind >= 0:
			nbr = len(self.lisFIC)
			fdr = self.lisFIC[nbr-1]
			fic = self.lisFIC[ind]
			jouer_notes.jouerEchantillonsMIX([fdr, fic], 600, False)

	def __init_components(self):
		# recuperation de la liste des sons, des noms, des boutons et des
		# fichiers
		self.lisSON = self.ens.getListe()
		refSON = self.lisSON[0]
		refVAL = refSON.getValeur()
		octSON = Son(refVAL + NOMBRE_NOTES_OCTAVE)
		self.lisSON.append(octSON)
		lisVAL = map(lambda e:NOMBRE_NOTES_OCTAVE-e.getValeur()+refVAL, self.lisSON)
		lisNDG = copy.copy(LISTE_NOMS_DEGRES)
		lisNDG[0] = TXT_DEG_UNI
		lisNDG.append(TXT_DEG_OCT)
		self.lisNOM = map(lambda e:lisNDG[e], lisVAL)
		nbr = len(self.lisNOM)
		for ind in range(nbr):
			self.lisNOM[ind] = ("%s\n[%s %s]") %(self.lisNOM[ind], str(self.lisSON[ind]), str(refSON))
		self.lisBUT = map(lambda e:definirButton(e), self.lisNOM)
		self.lisFIC = jouer_notes.transformerNotes(self.lisSON, True)
		# construction des widgets
		self.container = definirHBOX(self.lisBUT, True, True)

	def __init_events(self):
		self.hSON = map(lambda e:e.connect("clicked", self.__ecouter, None), self.lisBUT)
		self.hSKP = map(lambda e:e.connect("key-press-event", self.__keyPress), self.lisBUT)

	def __init__(self, ens):
		tracer("ComposantREN", "__init__")
		self.ens = Ensemble("", ens)
		self.__init_components()
		self.__init_events()

#-------------------------------------------------------------------------------

class ComposantHAR:

	def getContainer(self):
		return self.container

	def __del__(self):
		tracer("ComposantHAR", "__del__")
		nbr = len(self.lisBUT)
		lis = range(nbr)
		for ind in lis:
			disconnectEVENT(self.lisBUT[ind], self.hSON[ind])
			disconnectEVENT(self.lisBUT[ind], self.hSKP[ind])

	def __definirTexte(self, ens, ndg, ren=None):
		txt = ndg.getNotes().getNom()
		txt = txt.strip().split()
		txt = txt[0:len(txt)-1]
		txt = string.joinfields(txt)
		ens.setNom("")
		ldn = map(lambda e: str(e).strip(), ens.getListe())
		ldn = string.join(ldn, " ")
		if ren == None:
			txt = "%s:\n%s\n[%s]" %(TXT_ACC, txt, ldn)
		else:
			txt = "%s:\n%s / %s\n[%s]" %(TXT_ACC, txt, ren, ldn)
		ens.setNom(txt)
		return ens

	def __harmoniser(self, ens, ndn):
		# recuperation de la liste des accords ayant 'ndn' notes
		lisACC = LISTE_ACCORDS
		ldg = lisACC.getListeDegres(ndn)
		# recherche pour chaque note de l'ensemble d'un accord pouvant
		# faire partie de l'harmonisation de la gamme
		nbr = len(ens)
		res = []
		lnt = ens.getListe()
		for ind in range(nbr):
			# recherche de l'accord
			sen = ens.getNotesDEC(ind, 2, ndn)
			lis = sen.comparer(FNC_EGA, ldg)
			evt = lnt[ind].getNote()
			rla = filter(lambda e: evt == e.getSon().getNote(), lis)
			elt = None
			# 1. on cherche l'eventuel accord de ndn notes qui commence
			#    par la note elle-meme 
			# 2. sinon on cherche un renversement d'un accord avec les ndn notes
			# 3. sinon on prend juste les notes
			if len(rla) > 0:
				sen = self.__definirTexte(sen, rla[0])
			elif len(lis) > 0:
				sen = self.__definirTexte(sen, lis[0], str(lnt[ind]))
			else:
				txt = map(lambda e: str(e).strip(), sen.getListe())
				txt = string.join(txt, " ")
				sen.setNom("%s:\n%s" %(TXT_ONG_NOT, txt))
			res.append(sen)
		return res

	def __keyPress(self, widget, event):
		key = gtk.gdk.keyval_name(event.keyval)
		if key in ['KP_Home', 'KP_End']:
			self.__ecouter(widget, None)

	def __ecouter(self, widget, data):
		ind = self.lisBUT.index(widget)
		if ind >= 0:
			jouer_notes.jouerNotesMIX(self.lisNOT[ind], 600, True, False)

	def __init_components(self):
		# recuperation de la liste des sons, des noms, des boutons et des
		# fichiers
		self.lisSON = self.ens.getListe()
		self.lisENS = self.__harmoniser(self.ens, self.nbr)
		self.lisNOT = map(lambda e:e.getListe(), self.lisENS)
		self.lisNOM = map(lambda e:e.getNom(), self.lisENS)
		self.lisBUT = map(lambda e:definirButton(e), self.lisNOM)
		# construction des widgets
		self.container = definirHBOX(self.lisBUT, True, True)

	def __init_events(self):
		self.hSON = map(lambda e:e.connect("clicked", self.__ecouter, None), self.lisBUT)
		self.hSKP = map(lambda e:e.connect("key-press-event", self.__keyPress), self.lisBUT)

	def __init__(self, ens, nbr):
		tracer("ComposantHAR", "__init__")
		self.nbr = nbr
		self.ens = Ensemble("", ens)
		self.__init_components()
		self.__init_events()

#-------------------------------------------------------------------------------

class ComposantEcouter:

	def getNom(self):
		return TXT_ONG_ECO

	def getContainer(self):
		return self.container

	def update(self, ens):
		tracer("ComposantEcouter", "update")
		ens = Ensemble("", ens)
		if self.ens == None or ens != self.ens:
			for elt in self.vbox.get_children():
				self.vbox.remove(elt)
			self.ens = ens
			if ens != "":
				nbr = len(self.ens)
				self.vbox.add(ComposantNOT(self.ens).getContainer())
				self.vbox.add(ComposantINT(self.ens).getContainer())
				self.vbox.add(ComposantREN(self.ens).getContainer())
				if nbr >= 5:
					self.vbox.add(ComposantHAR(self.ens, 3).getContainer())
				if nbr >= 7:
					self.vbox.add(ComposantHAR(self.ens, 4).getContainer())

	def __init__(self, notes):
		tracer("ComposantEcouter", "__init__")
		self.ens = Ensemble("", notes)
		nbr = len(self.ens)
		lis = []
		lis.append(ComposantNOT(self.ens))
		lis.append(ComposantINT(self.ens))
		lis.append(ComposantREN(self.ens))
		if nbr >= 5:
			lis.append(ComposantHAR(self.ens, 3))
		if nbr >= 7:
			lis.append(ComposantHAR(self.ens, 4))
		lis = map(lambda e:e.getContainer(), lis)
		self.vbox = definirVBOX(lis)
		self.container = definirScrolledWindow(self.vbox, 'with_viewport')

