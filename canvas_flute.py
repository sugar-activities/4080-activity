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
import pango

import modele
import canvas_instrument

#------------------------------------------------------------------------------

class CanvasFlute(canvas_instrument.CanvasInstrument):

	def __dessinerCercle(self, gc, dr, psx, psy, lar, hau, etat, rap=1.0):
		"""
		@param gc:
		@param dr:
		@param psx: position en X de la case englobante
		@param psy: position en Y de la case
		@param lar: largeur de la case
		@param hau: hauteur de la case
		@param etat: ouvert, bouche, demi-bouche ou rien
		@param rap: place occupee dans la case
		"""
		dim = int(rap*(lar+hau)/3)
		pex = int(psx+(lar-dim)/2)
		pey = int(psy+(hau-dim)/2)
		amn = 0
		amx = 360 * 64
		aml = int((amn+amx)/2)
		if etat == modele.FLU_BOU:
			gc.set_foreground(self.atn)
			dr.draw_arc(gc, True, pex, pey, dim, dim, amn, amx)
			gc.set_foreground(self.atn)
			dr.draw_arc(gc, False, pex, pey, dim, dim, amn, amx)
		elif etat == modele.FLU_OUV:
			gc.set_foreground(self.atb)
			dr.draw_arc(gc, True, pex, pey, dim, dim, amn, amx)
			gc.set_foreground(self.atn)
			dr.draw_arc(gc, False, pex, pey, dim, dim, amn, amx)
		elif etat == modele.FLU_DEM:
			gc.set_foreground(self.atb)
			dr.draw_arc(gc, True, pex, pey, dim, dim, amn, amx)
			gc.set_foreground(self.atn)
			dr.draw_arc(gc, True, pex, pey, dim, dim, amn, aml)
			gc.set_foreground(self.atn)
			dr.draw_arc(gc, False, pex, pey, dim, dim, amn, amx)

	def __definirCasesEnglobantes(self, psx, psy, lar, hau):
		"""
		@param psx: position en X de la case englobante
		@param psy: position en Y de la case englobante
		@param lar: largeur de la case englobante
		@param hau: hauteur de la case englobante
		@rtype: retourne la liste des cases englobantes pour chaque trou
		"""
		lis = []
		lcs = lar/2
		hcs = hau/2
		# decalage pour un trou centre (en X)
		dcx = int((lar-lcs)/2)
		# decalage pour deux trous centres (en X)
		dec = int(3.0*dcx/4.0)
		dgx = int(dcx-dec)
		ddx = int(dcx+dec)
		# decalage en Y
		dcy = int((hau-hcs)/2)
		# calcul des coordonnees
		lpx = [dcx,dcx,dcx,dcx,dcx,dcx,dcx,dcx,dgx,ddx,dgx,ddx]
		lpx = map(lambda x:psx+x,lpx)
		lpy = [0,1,2,3,4,5,6,7,8,8,10,10]
		psy += dcy
		lpy = map(lambda y:psy+hau*y,lpy)
		lis = range(0,len(lpy))
		lis = map(lambda ind:[lpx[ind], lpy[ind], lcs, hcs], lis)
		return lis

	def __dessiner(self, widget, event):
		# Recuperation du nombre de notes de l'ensemble
		nno = len(self.ens)
		if nno > 0:
			# Recuperation du contexte graphique, des dimensions...
			rec, lar, hau, dr, gc, pl, cm = self.get_contexte_graphique(widget)
			# Recherche des possibilites de jeu des notes de l'ensemble
			liste, lisNH, lisNB, nbrCOL = self.get_solutions(self.ens, self.ins)
			# note (2 lignes) + 3 separations + 10 lignes de trous 
			nbrLIG = 14
			psx, psy, lno, hno = self.calculer_taille(lar, hau, self.rpx, self.rpy, 5, nbrLIG, nbrCOL, nbrLIG, 0.7)
			lar = lno * nbrCOL
			hau = hno * nbrLIG
			# calcul des cases englobantes
			lce = self.__definirCasesEnglobantes(psx, psy+2*hno, lno, hno)
			rap = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.7,1.0,0.7]
			# Tracage du tableau
			prs = modele.Son(liste[0])
			dcy = nbrLIG * hno
			ddx = 0
			# pour chaque note de l'ensemble
			lisNOT = range(nno)
			for ind in lisNOT:
				# affichage du rectangle
				nbrPOS = lisNB[ind]
				lcs, hcs, csx, dcx = self.afficher_rectangle(gc, dr, nbrPOS, 2, lno, hno, psx, psy, dcy)
				# affichage de la note
				note = liste[ind]
				brd, rmp, etat = self.afficher_note(gc, dr, pl, prs, note, psx, psy, lcs, hcs, 0.8, 0.8, csx, lno, 5)
				# affichage des lignes de separation
				ply = int(psy+hcs+1.75*hno)
				self.tracer_ligne_horizontale_centree(gc, dr, psx, ply, lcs, 0.75, brd)
				ply = int(psy+hcs+9.75*hno)
				self.tracer_ligne_horizontale_centree(gc, dr, psx, ply, lcs, 0.75, brd)
				# pour chaque possibilite pour la note
				elt = lisNH[ind]
				if elt == []:
					ddx += lno
					psx += lno
				for pos in elt:
					# pour chaque trou
					for ind in range(len(pos)):
						let = pos[ind]
						pex, pey, lcs, hcs = lce[ind]
						self.__dessinerCercle(gc, dr, pex+ddx, pey, lcs, hno, let, rap[ind])
					ddx += lno
					psx += lno
			return False

	#----------------------------------------------------------------------

	def __init__(self, flu, lar = 600, hau = 200, ens = "", rpx = 0.95, rpy = 0.95):
		super(CanvasFlute,self).__init__(lar,hau,ens,rpx,rpy)
		self.setInstrument(flu)
		self.refEVT = self.connect("expose-event", self.__dessiner)
		self.show()
