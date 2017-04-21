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

#------------------------------------------------------------------------------s

from ConfigParser import *
from modele import *

#------------------------------------------------------------------------------
# Classes des listes des gammes et des accords
#------------------------------------------------------------------------------

class ListeEchelles(ListeDegres):

	def __init__(self, ficCFG):
		ListeDegres.__init__(self)
		cfg = SafeConfigParser()
		cfg.read(ficCFG)
		lis = cfg.items('Echelles')
		for elt in lis:
			deg = elt[0].strip()
			val = elt[1].strip()
			tab = val.split('|')
			nom = _(tab[0].strip())
			nmd = None
			if len(tab) == 2:
				nmd = tab[1].split(',')
				nmd = map(lambda e:_(e.strip()), nmd)
			self.ajouter(Degres(deg, nom, nmd))
	
#------------------------------------------------------------------------------
# Classes des instruments
#------------------------------------------------------------------------------
	
class ListeHarmonicas:

	def __init__(self):
		self.__listeNOM = []
		self.__listeINS = []
		self.__listeNOM.append(_("Chromatic harmonica"))
		self.__listeINS.append(HarmonicaCHR())
		for ref in [0, 2, 4, 5, 7, 9, 11]:
			txt = "%s : %s" %(_("Diatonic harmonica"), LISTE_NOMS_NOTES[ref])
			self.__listeNOM.append(txt)
			self.__listeINS.append(HarmonicaDIA(ref))
	
	def getListeNoms(self):
		return self.__listeNOM
	
	def getInstrument(self, nom):
		ind = self.__listeNOM.index(nom)
		return self.__listeINS[ind]
	
class ListeFlutes:

	def __init__(self):
		self.__listeNOM = []
		self.__listeINS = []
		for ref in [_('C'), _('F')]:
			txt = "%s : %s" % (_("Recorder (baroque fingering)"), ref)
			self.__listeNOM.append(txt)
			self.__listeINS.append(Flute(ref, FLU_DGT_BAR))
			txt = "%s : %s" % (_("Recorder (modern fingering)"), ref)
			self.__listeNOM.append(txt)
			self.__listeINS.append(Flute(ref, FLU_DGT_MOD))

	def getListeNoms(self):
		return self.__listeNOM
	
	def getInstrument(self, nom):
		ind = self.__listeNOM.index(nom)
		return self.__listeINS[ind]

class ListeGuitares:

	def __init__(self, nbc = 19):
		self.__listeNOM = []
		self.__listeINS = []
		cfg = SafeConfigParser()
		cfg.read('./config/guitares.txt')
		lsc = cfg.sections()
		lis = []
		for elt in lsc:
			lis += cfg.items(elt)
		acc = {}
		for elt in lis:
			val = elt[0].strip().split(",")
			cle = elt[1].strip()
			val = map(lambda e:int(e.strip()), val)
			acc[_(cle)] = val
		fnc = lambda x: x-1
		lis = acc.keys()
		lis.sort()
		for obj in lis:
			ins = Guitare(nbc, map(fnc, acc[obj]))
			nom = obj + ' : ' + ins.getAccordageTexte()
			self.__listeNOM.append(nom)
			self.__listeINS.append(ins)

	def getListeNoms(self):
		return self.__listeNOM
	
	def getInstrument(self, nom):
		ind = self.__listeNOM.index(nom)
		return self.__listeINS[ind]

class ListeClarinettes:

	def __ajouter(self, nom, ref):
		self.__listeNOM.append("%s : %s" %(_("Clarinet"), nom))
		self.__listeINS.append(Clarinette(ref))

	def __init__(self):
		self.__listeNOM = []
		self.__listeINS = []
		self.__ajouter(_("B flat"), 10)
		self.__ajouter(_("A")     ,  9)
		self.__ajouter(_("G")     ,  7)
		self.__ajouter(_("F")     ,  5)
		self.__ajouter(_("E flat"),  3)
		self.__ajouter(_("D")     ,  2)
		self.__ajouter(_("C")     ,  0)
	
	def getListeNoms(self):
		return self.__listeNOM
	
	def getInstrument(self, nom):
		ind = self.__listeNOM.index(nom)
		return self.__listeINS[ind]

#------------------------------------------------------------------------------

LISTE_GAMMES  = ListeEchelles('./config/gammes.txt')
LISTE_ACCORDS = ListeEchelles('./config/accords.txt')
