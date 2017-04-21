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

import initialisations
import commun

import jouer_notes

from modele import *
from modele_data import *

#------------------------------------------------------------------------------

def afficherListeDegres(dgs, ton):
	"""
	@param dgs: liste des degres
	@param ton: fondamentale
	"""
	lis = dgs.getListeNomsDegres()
	lis.sort()
	for nom in lis:
		deg = dgs.getDegres(nom)
		ens = deg.getNotes(ton, 0, True)
		dgn = deg.getNom().strip()
		ldi = commun.formater('', ' ', '', deg.getDegresEDT())
		dgi = deg.getTexte().strip()
		ens = ens.getTexte().strip()
		print "%s %s %s %s" %(dgn.ljust(16), ldi.ljust(16), dgi.ljust(16), ens)
	print "\n"

#------------------------------------------------------------------------------

def afficherTousLesDegresModes(lis, nbr=None):
	lisDEG = lis.getListeNomsDegres(nbr)
	lisDEG.sort()
	print "\n", "Nombre d'echelles = ", len(lisDEG)
	res = {}
	for nom in lisDEG:
		deg = lis.getDegres(nom)
		degSEL = deg.getDegresSEL(0)
		for mod in degSEL:
			txt = deg.getDegresT10(mod)
			nts = deg.getNotes(0, mod, True)
			dgt = deg.getTexte(mod)
			val = "%s > %s" %(dgt, nts)
			if txt not in res.keys():
				res[txt] = [val]
			else:
				res[txt].append(val)
	lis = res.keys()
	lis.sort()
	print "Nombre de variations = ", len(lis)
	for elt in lis:
		print "\n"
		les = res[elt]
		for val in les:
			print val
	print "\n"

#------------------------------------------------------------------------------

def afficherNotesDegres(lis, nom, ton, mod, rel):
	"""
	@param lis: liste des echelles
	@param nom: nom de l'echelle
	@param ton: tonique
	@param mod: mode
	@param rel: ramene a la tonique ?
	"""
	deg = lis.getDegres(nom)
	ens = deg.getNotes(ton, mod, rel)
	tns = ens.getTension()
	nom = deg.getNom()
	sel = deg.getDegresSEL(mod)
	bin = deg.getDegresT10(mod)
	edt = deg.getDegresEDT(mod)
	print nom, ens, tns, sel, bin, edt
	print "\n"

#------------------------------------------------------------------------------

def afficherEquivalences(lis, nom, ton, fnc):
	"""
	@param lis: liste des echelles
	@param nom: nom de l'echelle
	@param ton: tonique
	@param fnc: fonction de comparaison
	"""
	deg = lis.getDegres(nom)
	obj = NoteDegres(ton, deg)
	res = obj.comparer(fnc, lis.getListeDegres(), 0, False)
	for elt in res:
		print elt
	print "\n"

#------------------------------------------------------------------------------

def afficherImprovisations(ldg, lda, ton, deg):
	deg = lda.getDegres(deg)
	ens = deg.getNotes(ton, 0, True)
	lis = ens.improviser(ldg.getListeDegres())
	print "Improviser sur %s : " %(str(ens))
	for elt in lis:
		print "\t%s" %(str(elt))
	print "\n"

#------------------------------------------------------------------------------

def testCadence251(lisGAM, lisACC):
	deg2 = lisACC.getDegres(_("m7"))	
	deg5 = lisACC.getDegres(_("7"))	
	deg1 = lisACC.getDegres(_("7M"))
	deg7 = lisACC.getDegres(_("m7(5b)"))
	ens1 = deg1.getNotes(0).getListe()	
	ens2 = deg2.getNotes(2).getListe()
	ens3 = deg2.getNotes(4).getListe()	
	ens4 = deg1.getNotes(5).getListe()
	ens5 = deg5.getNotes(7).getListe()	
	ens6 = deg2.getNotes(9).getListe()	
	ens7 = deg7.getNotes(11).getListe()	
	ens7  = ens7 + ens7
	ens24 = ens2 + ens4
	ens36 = ens3 + ens6
	ens7.sort()
	ens24.sort()
	ens36.sort()
	jouer_notes.jouerNotesMIX(ens2 , 1600)
	jouer_notes.jouerNotesSEQ(ens24, 400)
	jouer_notes.jouerNotesMIX(ens5 , 1600)
	jouer_notes.jouerNotesSEQ(ens7 , 400)
	jouer_notes.jouerNotesMIX(ens1 , 1600)
	jouer_notes.jouerNotesSEQ(ens36, 400)
	jouer_notes.jouerNotesMIX(ens1 , 1600)
	jouer_notes.jouerNotesSEQ(ens36, 400)

#------------------------------------------------------------------------------

def testHarmonicaChromatique():
	ins = HarmonicaCHR()
	for ind in range(1,8):
		for alv in HAR_LIS_ALV:
			for tir in HAR_LIS_TIR:
				print ind, alv, tir, ins.getSon(ind, alv, tir).getTexte(MOD_OCT)
	for note in range(0,26):
		print Son(note).getTexte(MOD_OCT), ins.searchSon(note)
	
def testHarmonicaDiatonique(ref):
	ins = HarmonicaDIA(ref)
	for ind in range(1,10):
		for alv in HAR_LIS_ALV:
			for alt in HAR_LIS_ALT:
				son = ins.getSon(ind, alv, alt)
				txt = ""
				if son != None:
					txt = ins.getSon(ind, alv, alt).getTexte(MOD_OCT)
					print ind, alv, alt, txt
	dec = GET_NOTE(ref)
	for note in range(0,25):
		son = Son(note+dec)
		print son.getTexte(MOD_OCT), ins.searchSon(son)
	
def testFlute(ref):
	ins = Flute(ref)
	for note in range(0,25):
		son = Son(note)
		print son.getTexte(MOD_OCT), ins.searchSon(son)
		
def testerTrompette(nbc = 24):
	import string
	obj = Trompette()
	for ind in range(nbc):
		son = Son(ind)
		lis = obj.searchSon(son)
		if lis != None:
			txt = str(son) + ' [' + str(son.getValeur()) + ']'
			print str(len(lis)) + " possibilité(s) pour " + txt
			for elt in lis:
				s = str(elt[0])
				v = elt[0].getValeur()
				p = elt[1]
				d = obj.pistons[elt[1]]
				print '\t%-4s [%-2d] : Pistons %-1d [%1d demi-tons]' % (s,v,p,d)

#------------------------------------------------------------------------------

def testCordeVibrante():
	corde = CordeVibrante(100, 440)
	for prc in range(0,100,10):
		frq = corde.calculerFrequence(prc)
		print "Frequence " + str(prc) + "% = " + str(frq)
	old = 0
	for frq in range(0,24):
		val = int(440.0 * 2.0**(frq/12.0))
		pos = float(corde.calculerPosition(val))
		print "Position " + str(val) + " Hz = " + str(round(pos,1)) + " %"
		print "Difference = " + str(round(pos-old,1))
		old = pos

#------------------------------------------------------------------------------

if __name__ == "__main__":
	
	SET_AFF(MOD_NOT)
	SET_CMP(MOD_OCT)

	lisGAM = LISTE_GAMMES
	lisACC = LISTE_ACCORDS
	
	afficherListeDegres(lisGAM, _("C"))
	afficherListeDegres(lisACC, _("C"))
	afficherTousLesDegresModes(lisGAM)
	afficherTousLesDegresModes(lisACC)
	afficherNotesDegres(lisGAM, _("Major"), _("C"), 0, True)
	afficherEquivalences(lisGAM, _("Major"), _("C"), FNC_EGA)
	afficherImprovisations(lisGAM, lisACC, _("C"), _("7M(5#)"))
	afficherImprovisations(lisGAM, lisACC, _("C"), _("9"))

	testHarmonicaChromatique()
	testHarmonicaDiatonique(_("C"))
	testFlute(0)
	testerTrompette(24)

	testCordeVibrante()

	#jouer_notes.iniPygameMixer()
	#testCadence251()
	#jouer_notes.delPygameMixer()
