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

from ConfigParser import *
import string

#------------------------------------------------------------------------------
# Constantes
#------------------------------------------------------------------------------

# Modes de comparaison entre les ensembles de notes
FNC_INF = lambda x,y:x<=y   # inferieur (inclus)
FNC_EGA = lambda x,y:x==y   # egal
FNC_SUP = lambda x,y:x>=y   # superieur (contenant)

# Purete des intervalles
INTERVALLE_PURETE = [8,1,2,3,5,6,0,7,4,3,2,1]
INT_TON = max(INTERVALLE_PURETE)

# Nombre de notes dans une octave
NOMBRE_NOTES_OCTAVE = 12;

# Liste des noms des notes
LISTE_NOMS_NOTES = [_('C'), _('C#'), _('D'), _('D#'), _('E'), _('F'), _('F#'), _('G'), _('G#'), _('A'), _('A#'), _('B')]

# Liste des noms des degres
LISTE_NOMS_DEGRES = [_('Fnd'), _('2m'), _('2M'), _('3m'), _('3M'), _('4J'), _('5-'), _('5J'), _('6m'), _('6M'), _('7m'), _('7M')]

# Comparaison des notes suivant la note seule ou en tenant compte de l'octave
MOD_NOT = 0     # comparaison/affichage sans tenir compte de l'octave
MOD_OCT = 1     # comparaison/affichage en tenant compte de l'octave

# Initialisation d'un degre
DEG_SEL = '1'

#------------------------------------------------------------------------------

def verifierBornes(val, vmin, vmax):
	if val > vmax:
		val = vmax
	elif val < vmin:
		val = vmin
	return val

#------------------------------------------------------------------------------

def GET_NOTE(note):
	assert note != None and (type(note) in [unicode, str, int] or note.__class__.__name__ == 'Son')
	if type(note) in [str, unicode]:
		note = LISTE_NOMS_NOTES.index(note)
	elif note.__class__.__name__ == 'Son':
		note = note.getNote()	
	note = note % NOMBRE_NOTES_OCTAVE
	assert 0 <= note and note < NOMBRE_NOTES_OCTAVE
	return note

def GET_MODE(mode):
	assert mode != None and type(mode) in [unicode, str, int]
	if type(mode) in [unicode, str]:
		mode = LISTE_NOMS_DEGRES.index(mode)
	mode = mode % NOMBRE_NOTES_OCTAVE
	assert 0 <= mode and mode < NOMBRE_NOTES_OCTAVE 
	return mode

#------------------------------------------------------------------------------

def SET_CMP(cmp):
	global __MODE_CMP
	assert cmp != None and type(cmp) == int and cmp in [MOD_NOT, MOD_OCT]
	__MODE_CMP = cmp

def GET_CMP():
	global __MODE_CMP	
	return __MODE_CMP

def SET_AFF(aff):
	global __MODE_AFF
	assert aff != None and type(aff) == int and aff in [MOD_NOT, MOD_OCT]
	__MODE_AFF = aff

def GET_AFF():
	global __MODE_AFF
	return __MODE_AFF

#------------------------------------------------------------------------------

SET_AFF(MOD_NOT)
SET_CMP(MOD_OCT)

#------------------------------------------------------------------------------
# Classe "CordeVibrante"
#------------------------------------------------------------------------------

class CordeVibrante:
		
	# (dn / do) = (fo / fn)
		
	def __init__(self, lng, frq):
		self.__lng = float(lng)
		self.__frq = float(frq)
		
	def calculerPosition(self, frq):
		# dn = do * (1 -fo/fn) 
		assert self.__frq <= frq
		dis =  self.__lng * (1.0 - self.__frq / float(frq))
		return dis
	
	def calculerFrequence(self, pos):
		# dn/do = 1-fo/fn => fo/fn = 1-dn/do => fn/fo = 1/(1-dn/do)
		# => fn = fo/(1-dn/do)
		assert 0.0 <= pos <= self.__lng
		frq = self.__frq / (1.0 - float(pos) / self.__lng)
		return frq

#------------------------------------------------------------------------------
# Classe "Son"
#------------------------------------------------------------------------------

class Son:

	def __calculerOctave(self, valeur):
		"""
		Calcul de l'octave d'un son.
		"""
		assert valeur != None and type(valeur) == int and valeur >= 0
		return (valeur / NOMBRE_NOTES_OCTAVE)

	def __calculerNote(self, valeur):
		"""
		Calcul de la note d'un son.
		"""
		assert valeur != None and type(valeur) == int and valeur >= 0
		return (valeur % NOMBRE_NOTES_OCTAVE)

 	def __calculerValeur(self, note, octave = 0):
		"""
		Calcul d'un son a partir d'une note et d'un octave.
		"""
		assert note != None and type(note) == int and note >= 0 
		assert octave != None and type(octave) == int and octave >= 0
		return (note + NOMBRE_NOTES_OCTAVE * octave)

	#----------------------------------------------------------------------

	def __comparer(self, son, mode):
		"""
		Comparaison de deux notes suivant un mode de comparaison.
		"""
		assert son != None
		assert type(son) in [int, unicode, str] or son.__class__.__name__ == "Son"
		if type(son) in [unicode, str]:
			son = Son(son, 0)
		if mode == MOD_NOT:
			note1 = self.getNote()
			note2 = son.getNote()
		else:
			note1 = self.getValeur()
			note2 = son.getValeur()
		return cmp(note1, note2)

	#----------------------------------------------------------------------

	def __getQualite(self, son, qua):
		son = Son(son)
		tonique = self.getNote()
		note = son.getNote()
		if note < tonique:
			note += NOMBRE_NOTES_OCTAVE
		diff = note - tonique
		return qua[diff]

	#----------------------------------------------------------------------

	def getValeur(self):
		return self.__valeur

	def getNote(self):
		return self.__calculerNote(self.__valeur)

	def getOctave(self):
		return self.__calculerOctave(self.__valeur)

	#----------------------------------------------------------------------

	def setOctave(self, val):
		assert val != None and type(val) == int and val >= 0
		self.__valeur = self.__calculerValeur(self.getNote(), val)

	def setNote(self, val):
		val = GET_NOTE(val)
		self.__valeur = self.__calculerValeur(val, self.getOctave())

	def setValeur(self, note = 0, octave = 0):
		assert note != None and (type(note) in [unicode, str] or type(note) == int or note.__class__.__name__ == 'Son')
		assert octave != None and type(octave) == int and octave >= 0
		# note est une chaine de caracteres
		if type(note) in [unicode, str]:
			note = note.strip()
			val = -1
			lis = range(NOMBRE_NOTES_OCTAVE)
			lis.reverse()
			for ind in lis:
				elt = LISTE_NOMS_NOTES[ind]
				pos = note.find(elt)
				if pos == 0:
					txt = note[0:len(elt)]
					val = ind
					if len(elt) < len(note):
						txt = note[len(elt):]
						txt = int(txt)
						assert txt >= 0
						octave += txt
					break
			assert val >= 0
			self.__valeur = self.__calculerValeur(val, octave)
		# note est un entier
		elif type(note) == int:
			self.__valeur = self.__calculerValeur(note, octave)
		# note est une instance de la classe 'Son'
		elif note.__class__.__name__ == 'Son':
			self.__valeur = self.__calculerValeur(note.getValeur(), octave)
			
	#----------------------------------------------------------------------

	def decaler(self, dec):
		assert dec != None and type(dec) == int
		self.__valeur += dec
		assert 0 <= self.__valeur

	#----------------------------------------------------------------------

	def getTexte(self, aff = GET_AFF()):
		txt = LISTE_NOMS_NOTES[self.getNote()]
		if aff == MOD_OCT:
			txt += str(self.getOctave())
		return txt

	def getConsonnance(self, son):
		return self.__getQualite(son, INTERVALLE_PURETE)

	#----------------------------------------------------------------------

	def __lt__(self, son):
		return self.__comparer(son, GET_CMP()) < 0

	def __le__(self, son):
		return self.__comparer(son, GET_CMP()) <= 0

	def __gt__(self, son):
		return self.__comparer(son, GET_CMP()) > 0
		
	def __ge__(self, son):
		return self.__comparer(son, GET_CMP()) >= 0

	def __cmp__(self, son):
		return self.__comparer(son, GET_CMP())

	def __eq__(self, son):
		if son == None:
			return False
		else:
			return self.__comparer(son, GET_CMP()) == 0
		
	def __ne__(self, son):
		if son == None:
			return True
		else:
			return self.__comparer(son, GET_CMP()) != 0

	#----------------------------------------------------------------------

	def __str__(self):
		return self.getTexte()

	def __init__(self, note = 0, octave = 0):
		self.setValeur(note, octave)

#------------------------------------------------------------------------------
# Classe "Ensemble"
#------------------------------------------------------------------------------

class Ensemble:

	def __ajouter(self, obj):
		# Le test d'appartenance est fonction du retour de GET_CMP
		assert obj != None
		son = Son(obj)
		if son not in self.__lis:
			self.__lis.append(son)

	def __retirer(self, obj):
		# Le test d'appartenance est fonction du retour de GET_CMP
		assert obj != None
		son = Son(obj)
		if son in self.__lis:
			self.__lis.remove(son)

	def __compter(self, ens):
		"""
		Retourne le nombre de notes pour chaque ensemble
		(l'instance et l'ensemnble passe en parametre)
		et le nombre de notes communes.
		"""
		if ens == None or ens == []:
			ens = Ensemble('', [])
		elif type(ens) in [unicode, str, list]:
			ens = Ensemble('', ens)
		assert ens.__class__.__name__ == 'Ensemble'
		nb1 = len(self.__lis)
		lis = ens.getListe()
		nb2 = len(lis)
		nbr = 0
		for son in self.__lis:
			if son in lis:
				nbr += 1
		return nb1, nb2, nbr

	#----------------------------------------------------------------------

	def getTension(self, dec = None):
		nbr = len(self.__lis)
		frc = 0.0
		ntc = 0
		ten = 0
		lis = range(nbr)
		# cft est pour rendre plus important les premieres
		# comparaisons par rapport a la premiere note, puis
		# la seconde, ...
		cft = map(lambda e : 1.0/(e+1.0), lis)
		if nbr > 0:
			for ini in lis:
				si = Son(self.__lis[ini])
				if dec != None:
				  si.decaler(dec)
				cf = cft[ini]
				for cou in range(ini+1,nbr):
					ntc += 1
					sc = self.__lis[cou]
					pro = si.getConsonnance(sc)
					frc += pro * cf
			mxq = max(INTERVALLE_PURETE)
			ten = int(100*(1.0 - frc/float(ntc*mxq)))
		return ten

	def getDifferences(self, ens):
		"""
		Calcule le nombre de demi-tons minimum (en fonction des renversements)
		qui separe deux accords.
		"""
		lis1 = self.getListe()
		lis2 = ens.getListe()
		fnc = lambda e: e.getNote()
		lis1 = map(fnc, lis1)
		lis2 = map(fnc, lis2)
		lis1.sort()
		lis2.sort()
		dif = 32767
		nbr1 = len(lis1) 
		nbr2 = len(lis2)
		ite1 = range(nbr1) 
		ite2 = range(nbr2)
		for ind in ite2:
			prem = lis2[0]
			lis2 = lis2[1:nbr2]
			lis2.append(prem)
			val = 0
			for ind in ite1:
				val1 = lis1[ind]
				val2 = lis2[ind % nbr2]
				val += abs(val1 - val2)
			dif = min(dif, val)        
		return dif  

	def getNotesDEC(self, deb, dec, nbr):
		"""
		Retourne un nouvel ensemble de notes constitue de la note 
		'deb' de l'ensemble initial et d'une note tous les 'dec'
		notes de l'ensemble (pour l'harmonisation par exemple) 
		"""
		assert nbr > 0 and deb >= 0 and dec > 0
		lng = len(self.__lis)
		pos = deb
		ens = Ensemble()
		ajt = 0
		for ind in range(nbr):
			pos %= lng
			ens.ajouter(Son(self.__lis[pos].getValeur() + ajt))
			pos += dec
			if pos >= lng:
				ajt += NOMBRE_NOTES_OCTAVE
		return ens
		
	def getNotesSEP(self, deb, nbr):
		"""
		Retourne un nouvel ensemble de notes constitue de la note 
		'deb' de l'ensemble initial et d'une note au moins toutes 
		tierces mineures [3 demi-tons] (pour l'harmonisation par exemple) 
		"""
		assert nbr > 0 and deb >= 0
		lng = len(self.__lis)
		ens = Ensemble()
		pos = deb % lng
		prc = self.__lis[pos].getValeur()
		ens.ajouter(Son(prc))
		for ind in range(1, nbr):
			dif = 0
			while dif < 3:
				val = self.__lis[pos].getValeur()
				dif = val - prc
				while dif < 0:
					dif += NOMBRE_NOTES_OCTAVE
					val += NOMBRE_NOTES_OCTAVE
				if dif < 3:
					pos = (pos+1) % lng
			prc = val
			ens.ajouter(Son(val))
		return ens

	def getNombre(self):
		return len(self.__lis)

	def getListe(self):
		return self.__lis

	def getNom(self):
		return self.__nom

	def getTexte(self, aff = GET_AFF()):
		txt = ""
		for elt in self.__lis:
			txt += elt.getTexte(aff) + " "
		return txt

	def getOctaves(self):
		"""
		Retourne les octaves min et max des notes de l'ensemble.
		"""
		nbr = self.getNombre()
		if nbr == 0:
			vmin = 0
			vmax = 0
		else:
			vmin = self.__lis[0].getOctave()
			vmax = vmin
			for ind in range(1,nbr):
				val = self.__lis[ind].getOctave()
				vmin = min(vmin, val)
				vmax = max(vmax, val)
		return vmin, vmax

	#----------------------------------------------------------------------

	def setNom(self, nom):
		assert nom != None and type(nom) in [unicode, str]
		self.__nom = nom.strip()

	#----------------------------------------------------------------------

	def decaler(self, dec):
		assert dec != None and type(dec) == int
		for son in self.__lis:
			son.decaler(dec);

	def ajouter(self, obj):
		assert obj != None
		if type(obj) in [unicode, str]:
			obj = obj.strip()
			if obj != "":
				lis = obj.split()
				for son in lis:
					self.__ajouter(son)
		elif type(obj) == list:
			for son in obj:
				self.__ajouter(son)
		elif obj.__class__.__name__ == 'Son':
			self.__ajouter(obj)
		else:
			assert obj.__class__.__name__ == "Ensemble"
			# ici la methode 'getListe' doit renvoyer une liste 
			# d'instances de Son
			lis = obj.getListe()
			for son in lis:
				self.__ajouter(son)
		# le tri tient compte du retour de GET_CMP
		self.__lis.sort()
		
	def retirer(self, obj):
		assert obj != None
		if type(obj) in [unicode, str]:
			obj = obj.strip()
			lis = obj.split()
			for son in lis:
				self.__retirer(son)
		elif type(obj) == list:
			for son in obj:
				self.__retirer(son)
		elif obj.__class__.__name__ == 'Son':
			self.__retirer(obj)
		else:
			assert obj.__class__.__name__ == "Ensemble"
			# ici la methode 'getListe' doit renvoyer une liste 
			# d'instances de Son
			lis = obj.getListe()
			for son in lis:
				self.__retirer(son)

	#----------------------------------------------------------------------

	def __lt__(self, lis):
		"""
		Redefinition de l'inclusion stricte des ensembles de notes.
		"""
		nb1, nb2, nbr = self.__compter(lis)
		return (nbr == nb1 and nb1 < nb2)

	def __le__(self, lis):
		"""
		Redefinition de l'inclusion large des ensembles de notes.
		"""
		nb1, nb2, nbr = self.__compter(lis)
		return (nbr == nb1 and nb1 <= nb2)

	def __gt__(self, lis):
		# contenance stricte
		nb1, nb2, nbr = self.__compter(lis)
		return (nbr == nb2 and nb1 > nb2)

	def __ge__(self, lis):
		# contenance
		nb1, nb2, nbr = self.__compter(lis)
		return (nbr == nb2 and nb1 >= nb2)

	def __eq__(self, lis):
		"""
		Redefinition de l'egalite des ensembles de notes
		"""
		nb1, nb2, nbr = self.__compter(lis)
		return (nbr == nb1 and nb1 == nb2)

	def __ne__(self, lis):
		"""
		Redefinition de l'inegalite des ensembles de notes
		"""
		nb1, nb2, nbr = self.__compter(lis)
		return (nbr != nb1 or nb1 != nb2)

	def __cmp__(self, ens):
		"""
		La comparaison s'effectue sur le nombre de notes puis
		sur le nom.
		"""
		assert ens != None
		if type(ens) in [unicode, str, list]:
			ens = Ensemble('', ens)
		nb1 = len(self.__lis)
		nb2 = len(ens.getListe())
		ret = 0
		if nb1 < nb2:
			ret = -1
		elif nb1 > nb2:
			ret = +1
		elif self.__nom < ens.getNom():
			ret = -1
		elif self.__nom > ens.getNom():
			ret = +1
		else:
			ret = 0
		return ret

	#----------------------------------------------------------------------
	
	def comparer(self, fncCMP, lisDEG):
		"""
		Fonction permettant de retourner les harmonisations de gamme,
		les équivalences de gammes ou d'accords : comparer un ensemble
		de notes a une liste de degres.
		"""
		res = []
		if self.getNombre() > 0:
			for deg in lisDEG:
				ens = deg.getNotes(0, 0, False)
				for son in LISTE_NOMS_NOTES:
					SET_CMP(MOD_NOT)
					if fncCMP(self, ens):
						res.append(NoteDegres(son, deg))
					SET_CMP(MOD_OCT)
					ens.decaler(1)
		return res

	def improviser(self, lisDEG):
		res = []
		if self.getNombre() > 0:
			ton = (self.getListe()[0]).getNote()
			for deg in lisDEG:
				lisDGS = deg.getDegresSEL()
				for mod in lisDGS:
					ens = deg.getNotes(ton, mod, True)
					if FNC_INF(self, ens):
						res.append(ens)
		return res

	#----------------------------------------------------------------------

	def __str__(self):
		txt = self.__nom.strip()
		if len(txt) > 0:
			txt += ' :'
		for son in self.__lis:
			txt += ' ' + str(son)
		return txt

	def __len__(self):
		return self.getNombre()

	def __init__(self, nom='', lis=[]):
		self.__lis = []
		self.setNom(nom)
		self.ajouter(lis)


#------------------------------------------------------------------------------
# Classe "Degres"
#------------------------------------------------------------------------------

class Degres:

	def getNom(self):
		return self.__nom

	def getTexte(self, mod = 0):
		degres = self.getDegresSEL(mod)
		txt = string.join(degres, " ")
		return txt

	def getDegre(self, ind):
		"""
		Retourne vrai si le degre 'ind' est selectionne.
		"""
		ind = GET_MODE(ind)
		return self.__degres[ind]

	def getDegres(self):
		return self.__degres

	def getDegresMode(self, mode = 0):
		mode = GET_MODE(mode)
		assert self.getDegre(mode)
		lis = [True]
		nbr = len(self.__degres)
		for ind in range(1,nbr):
			pos = (mode+ind)%nbr
			lis.append(self.__degres[pos])
		return lis

	def getDegresSEL(self, mode = 0):
		dgm = self.getDegresMode(mode)
		nbr = len(dgm)
		lis = []
		for ind in range(nbr):
			if dgm[ind]:
				lis.append(LISTE_NOMS_DEGRES[ind])
		return lis

	def getDegresT10(self, mode = 0):
		dgm = self.getDegresMode(mode)
		nbr = len(dgm)
		txt = ""
		for ind in range(nbr):
			if dgm[ind]:
				txt += "1"
			else:
				txt += "0"
		return txt

	def getDegresEDT(self, mode = 0):
		dgm = self.getDegresMode(mode)
		nbr = len(dgm)
		lis = []
		der = 0
		for ind in range(1,nbr):
			if dgm[ind]:
				val = ind - der
				der = ind
				lis.append(val)
		lis.append(NOMBRE_NOTES_OCTAVE - der)
		return lis

	def getNombre(self):
		nbr = 0
		for elt in self.__degres:
			if elt == True:
				nbr += 1
		return nbr

	#----------------------------------------------------------------------

	def setNom(self, nom):
		assert nom != None and type(nom) in [unicode, str]
		self.__nom = nom.strip()

	def setDegre(self, ind, val):
		assert 0 <= ind and ind < NOMBRE_NOTES_OCTAVE
		assert type(val) == bool
		ind = GET_MODE(ind)
		self.__degres[ind] = val

	def setDegres(self, deg):
		self.__degres = []
		if deg == None :
			self.__degres = [False] * NOMBRE_NOTES_OCTAVE
			self.__degres[0] = True
		else:
			# les degres sont initialises par une chaine de 12
			# caracteres contentant des 0 et des 1; le premier
			# caracteres (la tonique) est forcement egal a 1
			# (DEG_SEL) 
			assert type(deg) in [unicode, str]
			deg = deg.strip()
			assert len(deg) == NOMBRE_NOTES_OCTAVE
			assert deg[0] == DEG_SEL
			for let in deg:
				self.__degres.append(let == DEG_SEL)

	def setNomsDesModes(self, ndm):
		self.__modes = ndm

	#----------------------------------------------------------------------

	def getNotes(self, son, mode = 0, relatif = True):
		SET_CMP(MOD_OCT)
		mode = GET_MODE(mode) 
		assert relatif != None and type(relatif) == bool
		ens = Ensemble()
		# si le mode n'existe pas on selectionne le premier 
		# mode (tonique)
		if not self.__degres[mode]:
			mode = 0
		# calcul et ajout de la note initiale et definition du nom
		son = Son(son, 1)
		txt = "%s %s [%s]" %(son.getTexte(), self.getNom(), LISTE_NOMS_DEGRES[mode])
		if relatif and mode > 0:
			txt += " (*)"
		ens.setNom(txt)
		if not relatif and mode > 0:
			son.decaler(mode)
		ens.ajouter(son)
		# calcul et ajout des notes suivantes
		lis = range(1, NOMBRE_NOTES_OCTAVE)
		for let in lis:
			if self.__degres[(let + mode) % NOMBRE_NOTES_OCTAVE]:
				val = Son(son, 0)
				val.decaler(let)
				ens.ajouter(val)
		return ens

	def getNomMode(self, ind):
		if self.__modes != None and ind >= 0 or ind < len(self.__modes):
			return self.__modes[ind]
		else:
			return None

	def getListeNomsModes(self):
		return self.__modes
			
	#----------------------------------------------------------------------

	def __str__(self):
		txt = self.getNom()
		if len(txt) > 0:
			txt += ' : '
		txt += self.getTexte()
		return txt

	def __len__(self):
		return self.getNombre()

	def __init__(self, deg, nom='', ndm=None):
		self.setDegres(deg)
		self.setNom(nom)
		self.setNomsDesModes(ndm)

#------------------------------------------------------------------------------
# Classe "ListeDegres"
#------------------------------------------------------------------------------

class ListeDegres:

	def ajouter(self, deg):
		self.__liste.append(deg)
		
	def getDegres(self, idt):
		assert type(idt) in [unicode, str] or type(idt)== int
		if type(idt) in [unicode, str]:
			for deg in self.__liste:
				if string.upper(deg.getNom()) == string.upper(idt):
					return deg
		else:
			return self.__liste[idt]
		return None

	def getListeDegres(self, nbr=None):
		assert nbr == None or type(nbr) == int
		if nbr == None:
			return self.__liste
		else:
			liste = [deg for deg in self.__liste if deg.getNombre() == nbr]
			return liste

	def getListeNomsDegres(self, nbr=None):
		liste = self.getListeDegres(nbr)
		lis = map(lambda e:e.getNom(), liste)
		return lis

	def getNombre(self):
		return len(self.__liste)

	#----------------------------------------------------------------------

	def __len__(self):
		return self.getNombre()

	def __init__(self):
		self.__liste = []

#------------------------------------------------------------------------------
# Classe "NoteDegres"
#------------------------------------------------------------------------------

class NoteDegres:
	
	def getSon(self):
		return self.__son
	
	def getDegres(self):
		return self.__degres	
	
	def getNotes(self, mode = 0, relatif = True):
		return self.__degres.getNotes(self.__son, mode, relatif)
	
	def getNombre(self):
		return len(self.__degres)
	
	def comparer(self, fncCMP, lisDEG, mod, rel):
		ens = self.getNotes(mod, rel)
		lis = ens.comparer(fncCMP, lisDEG)
		return lis

	#----------------------------------------------------------------------

	def __str__(self):
		return str(self.getNotes(0, False))

	def __len__(self):
		return self.getNombre()

	def __init__(self, son, degres):
		self.__son = Son(son)
		self.__degres = degres

#------------------------------------------------------------------------------
# Classe 'Guitare'
#------------------------------------------------------------------------------

class Guitare:
	
	def __verifierAccordage(self):
		"""
		Pour s'assurer que l'accordage de la guitare est correct :
		la note de la corde a vide n est strictement inferieure
		a la note de la corde a vide suivante.
		"""
		if self.lisACC[0] < 0:
			self.lisACC[0] = 0
		for ind in range(1,self.nbrCRD):
			if self.lisACC[ind-1] >= self.lisACC[ind]:
				self.lisACC[ind] = self.lisACC[ind-1]+1
	
	def __verifierDoigte(self, crd):
		"""
		Le doigte si necessaire est re-equilibre en fonction
		de la corde de reference.
		"""
		# verification des bornes des doigtes
		self.doigteDEB = map(lambda e:verifierBornes(e,0,self.nbrCAS), self.doigteDEB)
		# la note du doigte de la corde de reference doit etre strictement
		# inferieure a la note de la derniere case de la cordre suivante
		if crd < self.nbrCRD-1:
			val = self.lisACC[crd] + self.doigteDEB[crd]
			val -= self.lisACC[crd+1] + self.nbrCAS
			if val >= 0:
				# diminution du doigte de la corde de reference
				self.doigteDEB[crd] = max(self.doigteDEB[crd]-(val+1), 0)
		# la note du doigte de la corde de reference doit etre strictement 
		# inferieure a la note de la derniere case de la corde precedente
		if crd > 0:
			val = self.lisACC[crd] + self.doigteDEB[crd]
			val -= self.lisACC[crd-1] + self.nbrCAS
			if val > 1:
				# diminution du doigte de la corde de reference
				self.doigteDEB[crd] = max(self.doigteDEB[crd]-(val-1), 0)
		# re-equilibrage des cordes superieures
		lis = range(crd+1, self.nbrCRD)
		for ind in lis:
			val2 = self.lisACC[ind] + self.doigteDEB[ind]
			val1 = self.lisACC[ind-1] + self.doigteDEB[ind-1]
			dif = val2 - val1
			if dif <= 0:
				# impossible car la note du doigte de la corde (n)
				# doit etre strictement superieur a celle du doigte
				# de la corde (n-1) => augmentation du doigte de
				# la corde traitee
				self.doigteDEB[ind] -= dif-1
			else:
				dif += self.doigteDEB[ind-1] - self.nbrCAS
				if dif > 0:
					self.doigteDEB[ind] -= (dif-1)
		# re-equilibrage des cordes inferieures
		lis = range(0, crd-1)
		lis.reverse()
		for ind in lis:
			val2 = self.lisACC[ind+1] + self.doigteDEB[ind+1]
			val1 = self.lisACC[ind] + self.doigteDEB[ind]
			dif = val2 - val1
			if dif <= 0:
				# impossible sinon interruption du chemin
				# re-equilibrage de la corde 'ind'
				self.doigteDEB[ind] += dif-1
			else:
				dif += self.doigteDEB[ind] - self.nbrCAS
				if dif > 0:
					self.doigteDEB[ind] += dif-1
		# calcul de la fin du doigte sur chaque corde
		lis = range(0, self.nbrCRD-1)
		for ind in lis:
			val2 = self.lisACC[ind+1] + self.doigteDEB[ind+1]
			val1 = self.lisACC[ind] + self.doigteDEB[ind]
			nbc = val2 - val1 - 1
			self.doigteFIN[ind] = self.doigteDEB[ind] + nbc
		# pour s'arreter a la premiere note (a partir du debut du
		# doigte) de la derniere corde (corde aigue)
		note = self.getSon(0, self.doigteDEB[0])
		lis = range(self.doigteDEB[self.nbrCRD-1], self.nbrCAS+1)
		pos = self.nbrCAS
		for ind in lis:
			son = self.getSon(self.nbrCRD-1, ind)
			if note.getNote() == son.getNote():
				pos = ind
				break
		self.doigteFIN[self.nbrCRD-1] = pos
		# par securite
		self.doigteDEB = map(lambda e:verifierBornes(e,0,self.nbrCAS), self.doigteDEB)
		self.doigteFIN = map(lambda e:verifierBornes(e,0,self.nbrCAS), self.doigteFIN)

	def __initialiserDoigte(self):
		self.doigteDEB = [0] * self.nbrCRD
		self.doigteFIN = [self.nbrCAS] * self.nbrCRD
		self.__verifierDoigte(0)
	
	def __init__(self, nbrCAS, lisACC):
		assert nbrCAS > 0
		assert lisACC != None and type(lisACC) == list and len(lisACC) > 0
		self.nbrCAS = nbrCAS
		self.nbrCRD = len(lisACC)
		self.lisACC = lisACC
		self.__verifierAccordage()
		self.__initialiserDoigte()
		
	def getNombreDeCases(self):
		return self.nbrCAS
		
	def getNombreDeCordes(self):
		return self.nbrCRD
		
	def getAccordage(self):
		return self.lisACC
		
	def getAccordageTexte(self):
		acc = Ensemble("", self.lisACC)
		txt = acc.getTexte(MOD_NOT)
		return txt
		
	def setNombreDeCases(self, nbrCAS):
		assert type(nbrCAS) == int or type(nbrCAS) in [unicode, str]
		nbrCAS = int(nbrCAS)
		assert nbrCAS > 0
		self.nbrCAS = int(nbrCAS)
		self.__verifierDoigte(0)
		
	def setDoigte(self, doigte, crd):
		self.doigteDEB = doigte
		self.__verifierDoigte(crd)
		
	def setDoigteCorde(self, doigte, crd):
		self.doigteDEB[crd] = doigte
		self.__verifierDoigte(crd)
		
	def getDoigte(self):
		return self.doigteDEB
				
	def getDoigteCorde(self, crd):
		return self.doigteDEB[crd], self.doigteFIN[crd]
		
	def getSon(self, crd, cas):
		assert crd >= 0 and crd < self.nbrCRD
		assert cas >= 0 and cas <= self.nbrCAS
		val = self.lisACC[crd] + cas
		return Son(val)
	
#------------------------------------------------------------------------------
# Classe 'Harmonica' (chromatique)
#------------------------------------------------------------------------------
	
HAR_ALV_SOU = "S"
HAR_ALV_ASP = "A"

HAR_TIR_REL = "R"
HAR_TIR_APP = "A"

HAR_SOU_REL = HAR_ALV_SOU + HAR_TIR_REL
HAR_SOU_APP = HAR_ALV_SOU + HAR_TIR_APP
HAR_ASP_REL = HAR_ALV_ASP + HAR_TIR_REL
HAR_ASP_APP = HAR_ALV_ASP + HAR_TIR_APP
	
HAR_LIS_ALV = [HAR_ALV_SOU, HAR_ALV_ASP]
HAR_LIS_TIR = [HAR_TIR_REL, HAR_TIR_APP]
	
class HarmonicaCHR:	
	
	def getSon(self, trou, alv, tir):
		assert alv in HAR_LIS_ALV
		assert tir in HAR_LIS_TIR
		assert trou > 0
		trou -= 1
		deca = int(trou / 4) * NOMBRE_NOTES_OCTAVE
		trou = trou % 4
		conf = alv + tir
		son = Son(self.__dico[conf][trou])
		son.decaler(deca)
		return son

	def searchSon(self, son, vmin = 1, vmax = 16):
		son = Son(son)
		res = []
		lisTR = range(vmin, vmax)
		for trou in lisTR:
			for alv in HAR_LIS_ALV:
				for tir in HAR_LIS_TIR:
					obj = self.getSon(trou, alv, tir)
					if obj == son:
						res.append([trou, alv, tir])
		return res
	
	def __init__(self):
		cfg = SafeConfigParser()
		cfg.read('./config/harmonicas.txt')
		lis = cfg.items('Chromatiques')
		self.__dico = {}
		for elt in lis:		
			cle = elt[0].strip().upper()
			val = elt[1].strip().split(',')
			val = map(lambda e:Son(int(e.strip())), val)
			self.__dico[cle] = val
	
#------------------------------------------------------------------------------
# Classe 'Harmonica' (diatonique)
#------------------------------------------------------------------------------
	
HAR_ALT_AUC = "N"  # pas d'alteration
HAR_ALT_BN1 = "1"  # alteration d'un demi-ton
HAR_ALT_BN2 = "2"  # alteration d'un ton
HAR_ALT_BN3 = "3"  # alteration d'un ton et demi
HAR_ALT_OVB = "B"  # alteration de type overblow
HAR_ALT_OVD = "D"  # alteration de type overdraw

HAR_SOU_AUC = HAR_ALV_SOU + HAR_ALT_AUC
HAR_SOU_BN1 = HAR_ALV_SOU + HAR_ALT_BN1
HAR_SOU_BN2 = HAR_ALV_SOU + HAR_ALT_BN2
HAR_SOU_OVB = HAR_ALV_SOU + HAR_ALT_OVB

HAR_ASP_AUC = HAR_ALV_ASP + HAR_ALT_AUC
HAR_ASP_BN1 = HAR_ALV_ASP + HAR_ALT_BN1
HAR_ASP_BN2 = HAR_ALV_ASP + HAR_ALT_BN2
HAR_ASP_BN3 = HAR_ALV_ASP + HAR_ALT_BN3
HAR_ASP_OVD = HAR_ALV_ASP + HAR_ALT_OVD

HAR_LIS_ALT = [HAR_ALT_AUC, HAR_ALT_BN1, HAR_ALT_BN2, HAR_ALT_BN3, HAR_ALT_OVB, HAR_ALT_OVD]

class HarmonicaDIA:	
	
	def getSon(self, trou, alv, alt):
		assert trou >= 1 and trou <= self.__nbr
		assert alv in HAR_LIS_ALV
		assert alt in HAR_LIS_ALT
		trou -= 1
		conf = alv + alt
		son = None
		if conf in self.__dico.keys():
			son = self.__dico[conf][trou]
			if son != None:
				son = Son(son)
		return son

	def searchSon(self, son):
		son = Son(son)
		res = []
		lisTR = range(1, self.__nbr + 1)
		for trou in lisTR:
			for alv in HAR_LIS_ALV:
				for alt in HAR_LIS_ALT:
					obj = self.getSon(trou, alv, alt)
					if obj != None and obj == son:
						res.append([trou, alv, alt])
		return res
	
	def __init__(self, son):
		self.__nbr = 10
		cfg = SafeConfigParser()
		cfg.read('./config/harmonicas.txt')
		lis = cfg.items('Diatoniques')
		self.__dico = {}
		for elt in lis:		
			cle = elt[0].strip().upper()
			val = elt[1].strip().split(',')
			val = map(lambda e:e.strip(), val)
			val = map(lambda e: Son(int(e)) if e not in ['', None] else None, val)
			self.__dico[cle] = val
		note = Son(son).getNote()
		for key in self.__dico.keys():
			for son in self.__dico[key]:
				if son != None:
					son.decaler(note)
	
#------------------------------------------------------------------------------
# Classe des flutes a bec
#------------------------------------------------------------------------------

FLU_BOU = "B"       # bouche
FLU_DEM = "D"       # a moitie bouche
FLU_OUV = "O"       # ouvert

FLU_DGT_BAR = "B"   # doigte baroque
FLU_DGT_MOD = "M"   # doigte moderne

class Flute:

	def getSon(self, conf):
		lis = self.__dico.keys()
		for elt in lis:
			if conf in self.__dico[elt]:
				son = Son(elt)
				son.decaler(self.__note)
				return son
		return None

	def searchSon(self, son):
		lis = self.__dico.keys()
		for elt in lis:
			note = Son(elt)
			note.decaler(self.__note)
			if son == note:
				return self.__dico[elt]
		return []

	def __doigte(self, section):
		cfg = SafeConfigParser()
		cfg.read('./config/flutes.txt')
		lis = cfg.items(section)
		self.__dico = {}
		for elt in lis:		
			cle = int(elt[0].strip())
			val = elt[1].strip().split(',')
			val = map(lambda e:e.strip(), val)
			self.__dico[cle] = val

	def __init__(self, son=0, dgt=FLU_DGT_BAR):
		self.__note = GET_NOTE(son)
		if dgt == FLU_DGT_BAR:
			self.__doigte('Baroque')
		else:
			self.__doigte('Moderne')

#------------------------------------------------------------------------------
# Classe des clarinettes
#------------------------------------------------------------------------------

class Clarinette:
	
	def getSon(self, cle):
		lis = self.__dico.keys()
		for elt in lis:
			if cle in self.__dico[elt]:
				son = Son(elt)
				son.decaler(self.__note)
				return son
		return None

	def searchSon(self, son):
		lis = self.__dico.keys()
		for elt in lis:
			note = Son(elt)
			note.decaler(self.__note)
			if son == note:
				return self.__dico[elt]
		return []
	
	def __init__(self, son=0):
		son = GET_NOTE(son)
		dif = son - NOMBRE_NOTES_OCTAVE
		if dif < -GET_NOTE(4):
			self.__note = son
		else:
			self.__note = dif
		cfg = SafeConfigParser()
		cfg.read('./config/clarinettes.txt')
		lis = cfg.items('Ut')
		self.__dico = {}
		for elt in lis:		
			cle = int(elt[0].strip())
			val = elt[1].strip().split(',')
			val = map(lambda e:e.strip(), val)
			self.__dico[cle] = val

#------------------------------------------------------------------------------
# Classe des trompettes
#------------------------------------------------------------------------------

PIS_SNS = 0
PIS_GAU = 1
PIS_MIL = 2
PIS_DRO = 4

class Trompette:
	
	def getSon(self, son, pis):
		son = Son(son)
		dec = self.pistons[pis]
		if son.getValeur() >= dec:
			son.decaler(-dec)
			return son
		return None
	
	def searchSon(self, son):
		lis = []
		for ssp in self.sons:
			for pis in self.pistons:
				vds = self.getSon(ssp, pis)
				if vds == son:
					lis.append([ssp, pis])
		return lis
	
	def __init__(self, son = 0):
		self.sons = [Son(0), Son(7), Son(12), Son(16), Son(19), Son(22), Son(24)]
		self.pistons = {}
		self.pistons[PIS_SNS] = 0
		self.pistons[PIS_GAU] = 2
		self.pistons[PIS_MIL] = 1
		self.pistons[PIS_DRO] = 3
		self.pistons[PIS_GAU+PIS_MIL] = self.pistons[PIS_GAU] + self.pistons[PIS_MIL]
		self.pistons[PIS_GAU+PIS_DRO] = self.pistons[PIS_GAU] + self.pistons[PIS_DRO]
		self.pistons[PIS_DRO+PIS_MIL] = self.pistons[PIS_DRO] + self.pistons[PIS_MIL]
		self.pistons[PIS_GAU+PIS_DRO+PIS_MIL] = self.pistons[PIS_GAU+PIS_DRO] + self.pistons[PIS_MIL]
