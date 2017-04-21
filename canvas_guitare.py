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

from commun import *
import modele
import canvas_instrument

#------------------------------------------------------------------------------

class CanvasGuitare(canvas_instrument.CanvasInstrument):

	def __rechercherCaseNote(self, corde, cases, note, instr):
		"""
		Retourne la premiere case avec la note en question
		(sans considerer l'octave).
		"""
		case = 0
		for indice in cases:
			son = instr.getSon(corde, indice)
			if son.getNote() == note.getNote():
				case = indice
				break
		return case

	def __calculerExtremites(self, note, instr, dia=True):
		"""
		Recherche la premiere note sur la corde grave et
		la premiere ou derniere note sur la corde aigue.
		"""
		# calcul du debut de doigte sur la corde grave
		lis = range(instr.nbrCAS+1)
		cmin = self.__rechercherCaseNote(0, lis, note, instr)
		# calcul de la fin du doigte sur la corde aigue
		if dia:
			lis.reverse()
		cmax = self.__rechercherCaseNote(instr.nbrCRD-1, lis, note, instr)
		return cmin, cmax

	def __calculerDoigteEXT(self, note, instr, dia=True):
		"""
		Pour le calcul des doigtes en diagonales ou en barres :
		calcul des extremites sur la corde grave et la corde
		aigue puis calcul des doigtes intermediaires par
		nombre moyen de notes par corde constant.
		"""
		cmin, cmax = self.__calculerExtremites(note, instr, dia)
		# calcul du chemin intermediaire
		rap = (cmax - cmin) / (instr.nbrCRD - 1.0)
		doigte = map(lambda e: int(cmin+e*rap), range(instr.nbrCRD))
		# retour du doigte initial calcule
		return doigte

	def __calculerDoigteNBR(self, note, instr, maxNOT, maxCAS):
		"""
		Calcul du doigte en appliquant la regle suivante :
		on passe a la corde suivante des que le nombre
		maximum de notes ou de cases par corde est atteint.
		"""
		cmin, cmax = self.__calculerExtremites(note, instr)
		# calcul du chemin intermediaire
		lisNOT = self.ens.getListe()
		doigte = [cmin] * instr.nbrCRD
		lisCRD = range(instr.nbrCRD-1)
		for crd in lisCRD:
			cmin = min(doigte[crd]+1, instr.nbrCAS+1)
			cmax = min(doigte[crd]+1+maxCAS, instr.nbrCAS+1)
			lisCAS = range(cmin, cmax)
			nbrNOT = 1
			for cas in lisCAS:
				son = instr.getSon(crd, cas)
				if son in lisNOT:
					nbrNOT += 1
				if nbrNOT > maxNOT:
					break
			lisCAS = range(0,instr.nbrCAS+1)
			for cas in lisCAS:
				val = instr.getSon(crd+1, cas)
				if val.getValeur() == son.getValeur():
					doigte[crd+1] = cas
					break
		# retour du doigte initial calcule
		return doigte

	def __calculerDoigteInitial(self, note, instr, doigte):
		"""
		Calcul du doigte initial en fonction du doigte demande.
		"""
		if doigte == TXT_DGT_4E6:
			return self.__calculerDoigteNBR(note, instr, 4, 6)
		elif doigte == TXT_DGT_3E5:
			return self.__calculerDoigteNBR(note, instr, 3, 5)
		elif doigte == TXT_DGT_EGG:
			return self.__calculerDoigteEXT(note, instr, False)
		else:
			return self.__calculerDoigteEXT(note, instr, True)

	def __changerDoigte(self, psx, psy, px1, py1, lar, hau, lcs, hcs):
		"""
		L'utilisateur a clique sur une case de la guitare pour changer
		le doigte.
		"""
		px2 = px1 + lar
		py2 = py1 + hau
		if px1 <= psx <= px2 and py1 <= psy <= py2:
			nbr_cas = self.ins.getNombreDeCases()+1
			nbr_crd = self.ins.getNombreDeCordes()
			cas = int((psx - px1) * nbr_cas / lar)
			crd = int((psy - py1 - 0.5 * hcs) * nbr_crd / hau)
			crd = nbr_crd - 1 - crd
			if 0 <= cas <= nbr_cas and 0 <= crd < nbr_crd:
				self.ins.setDoigteCorde(cas, crd)

	def __afficherOmbreCorde(self, gc, dr, psx, psy, lar_cas, hau_cas, nbr_crd, num_crd, deb_cas, fin_cas):
		psx += deb_cas * lar_cas
		psy += int(((nbr_crd-num_crd)-0.5) * hau_cas)
		gc.set_foreground(self.atj)
		lar = lar_cas * (fin_cas - deb_cas + 1)
		dr.draw_rectangle(gc, True, psx, psy, lar, hau_cas)

	def __afficherCorde(self, gc, dr, psx, psy, lar_cas, hau_cas, nbr_crd, nbr_cas, num_crd):
		px1 = psx + lar_cas
		px2 = psx + (nbr_cas+1) * lar_cas
		pyd = psy + num_crd * hau_cas
		if num_crd > nbr_crd / 2:
			gc.set_foreground(self.atn)
		else:
			gc.set_foreground(self.atg)
		dr.draw_line(gc, px1, pyd, px2, pyd)

	def __afficherFrette(self, gc, dr, psx, psy, lar_cas, hau_cas, nbr_crd, num_cas, sillet):
		pxd = psx + lar_cas * (num_cas + 1)
		py1 = psy + hau_cas
		py2 = psy + hau_cas * nbr_crd
		gc.set_foreground(self.atn)
		if sillet:
			for ind in range(1,4):
				dr.draw_line(gc, pxd-ind, py1, pxd-ind, py2)
		dr.draw_line(gc, pxd, py1, pxd, py2)
		
	def __afficherEllipse(self, gc, dr, psx, psy, lar_cas, hau_cas, rap, num_crd, num_cas, rmp, brd):
  		psx += int((num_cas - 0.5) * lar_cas)
  		psy += int((num_crd - 0.5) * hau_cas)
		self.tracer_ellipse_centre(gc, dr, psx, psy, lar_cas, hau_cas, rap, rap, brd, rmp)
		
	def __afficherGuitare(self, gc, dr, psx, psy, lar_cas, hau_cas, instr):
		nbr_cas = instr.getNombreDeCases()
		nbr_crd = instr.getNombreDeCordes()
		lis_crd = range(0, nbr_crd)
		lis_cas = range(0, nbr_cas)
		# Trace de l'ombre
		for x in lis_crd:
			dmin, dmax = self.ins.getDoigteCorde(x)
			self.__afficherOmbreCorde(gc, dr, psx, psy, lar_cas, hau_cas, nbr_crd, x, dmin, dmax)
		# Trace des cordes
		for x in lis_crd:
			self.__afficherCorde(gc, dr, psx, psy, lar_cas, hau_cas, nbr_crd, nbr_cas, x+1)
		# Trace du sillet
		self.__afficherFrette(gc, dr, psx, psy, lar_cas, hau_cas, nbr_crd, 0, True)
  		# Trace des frettes
  		for x in lis_cas:
    			self.__afficherFrette(gc, dr, psx, psy, lar_cas, hau_cas, nbr_crd, x+1, False)
		# Trace des ellipses
		psx += lar_cas / 2 + 1
		psy += hau_cas / 2 + 1
		rap = 0.2
		pmn = 1
		pmx = nbr_crd - 1
		pml = (pmn + pmx) / 2 
		for x in range(3, 10, 2):
			if x <= nbr_cas:
				self.__afficherEllipse(gc, dr, psx, psy, lar_cas, hau_cas, rap, pml, x, self.atr, self.atr)
		x = 12
		if x <= nbr_cas:
			self.__afficherEllipse(gc, dr, psx, psy, lar_cas, hau_cas, rap, pmn, 12, self.atr, self.atr)
			self.__afficherEllipse(gc, dr, psx, psy, lar_cas, hau_cas, rap, pmx, 12, self.atr, self.atr)
		for x in range(15, 21, 2):
			if x <= nbr_cas:
				self.__afficherEllipse(gc, dr, psx, psy, lar_cas, hau_cas, rap, pml, x, self.atr, self.atr)

	def __afficherNotes(self, gc, dr, pl, psx, psy, lar_cas, hau_cas, instr, notes):
		nbr_cas = instr.getNombreDeCases()
		nbr_crd = instr.getNombreDeCordes()
		old = modele.GET_CMP()
		modele.SET_CMP(modele.MOD_NOT)
		notes = notes.getListe()
		pny = psy + hau_cas/2
		psx += lar_cas / 2
		lis = range(0, nbr_crd)
		lis.reverse()
		note = notes[0]
		for crd in lis:
			pnx = psx - lar_cas / 2
			for cas in range(0, nbr_cas + 1):
				son = instr.getSon(crd, cas)
				trv = son in notes
				if trv:
					txt = son.getTexte(modele.MOD_OCT)
					eta = note.getConsonnance(son)
					fnd = self.get_couleur_remplissage(eta)
					if son == note:
						col = self.atb
					else:
						col = self.atn
					self.tracer_rectangle_texte_centre(gc, dr, pl, fnd, col, pnx, pny, lar_cas, hau_cas, 5, txt, "Arial", "Bold")
				pnx += lar_cas
			pny += hau_cas
		modele.SET_CMP(old)

	def __dessiner(self, widget, event):
		# recuperation des dimensions de la zone graphique
		rec, lar, hau, dr, gc, pl, cm = self.get_contexte_graphique(widget)
		# calcul des dimensions de la zone utilisable
		lgu = int(self.rpx * lar)
		hgu = int(self.rpy * hau)
		# affichage du fond
		gc.set_foreground(self.atb)
		dr.draw_rectangle(gc, True, 0, 0, lar, hau)
		# trace de la guitare
		nbr_cas = self.ins.getNombreDeCases()
		nbr_crd = self.ins.getNombreDeCordes()
		lar_cas = int(lgu / float(nbr_cas+1))
		hau_cas = int(hgu / float(nbr_crd))
		hau_cas = min(hau_cas, int(1.5 * lar_cas))
		hgu = hau_cas * nbr_crd
		# centrage de la guitare
		psx = (lar - lgu) / 2
		psy = (hau - hgu) / 2
		psy -= hau_cas/2
		# calcul du doigte
		clic = (event.type == gtk.gdk.BUTTON_PRESS)
		if clic:
			self.__changerDoigte(event.x, event.y, psx, psy, lgu, hgu, lar_cas, hau_cas)
		else:
			liste = self.ens.getListe()
			if len(liste) > 0:
				note = liste[0]
			else:
				# si pas de notes, on defini la note de reference a Mi
				note = modele.Son(4) 
			doigte = self.__calculerDoigteInitial(note, self.ins, self.__doigte)
			self.ins.setDoigte(doigte, 0)
		self.__afficherGuitare(gc, dr, psx, psy, lar_cas, hau_cas, self.ins)
		if self.ens != None and self.ens != []:
			self.__afficherNotes(gc, dr, pl, psx, psy, lar_cas, hau_cas, self.ins, self.ens)
		return False
	
	#----------------------------------------------------------------------
	
	def setDoigte(self, doigte):
		self.__doigte = doigte
		self.queue_draw()
	
	#----------------------------------------------------------------------
	
	def __init__(self, obj, lar = 600, hau = 300, ens = "", rpx = 0.95, rpy = 0.95):
		"""
		(lar, hau) dimensions dela zone graphique
		nbr est le nombre d'octaves
		ens est l'ensemble de notes a afficher
		(rpx, rpy) partie de la zone utilisee
		"""
		super(CanvasGuitare,self).__init__(lar,hau,ens,rpx,rpy)
		self.__rec = None
		self.setInstrument(obj)
		self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
		self.connect("expose-event", self.__dessiner)
		self.connect("button-press-event", self.__dessiner)
		self.show()
