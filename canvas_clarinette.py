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

class CanvasClarinette(canvas_instrument.CanvasInstrument):

	def __get_clarinette(self, svg, cle, lar, hau):
		for let in cle:
			svg = svg.replace('#Couleur' + let, '#FD0')
		svg = svg.replace('#Couleur', '#ffffff')
		pix = self.svg_str_to_pixbuf(svg, lar, hau)
		return pix

	def __dessiner(self, widget, event):
		# Recuperation du nombre de notes de l'ensemble
		nno = len(self.ens)
		if nno > 0:
			# Recuperation du contexte graphique, des dimensions...
			rec, lar, hau, dr, ct, pl, cm = self.get_contexte_graphique(widget)
			# Recherche des possibilites de jeu des notes de l'ensemble
			liste, lisNH, lisNB, nbrCOL = self.get_solutions(self.ens, self.ins)
			nbrLIG = 5
			# Calcul de la taille des cases et de la position du 
			# tableau, de la taille de la fonte
			psx, psy, lno, hno = self.calculer_taille(lar, hau, self.rpx, self.rpy, 5, nbrLIG, nbrCOL, nbrLIG, 0.5)
			lar = lno * nbrCOL
			hau = hno * nbrLIG
			# Tracage du tableau
			prs = modele.Son(liste[0])
			dcy = nbrLIG * hno
			# pour chaque note de l'ensemble
			lisNOT = range(nno)
			for ind in lisNOT:
				# affichage du rectangle
				nbrPOS = lisNB[ind]
				lcs, hcs, csx, dcx = self.afficher_rectangle(ct, dr, nbrPOS, 1, lno, hno, psx, psy, dcy)
				# affichage de la note
				note = liste[ind]
				brd, rmp, etat = self.afficher_note(ct, dr, pl, prs, note, psx, psy, lcs, hcs, 0.8, 0.8, csx, lno, 5)
				# trace des clarinettes
				elt = lisNH[ind]
				if elt == []:
					psx += lno
				dmy = (nbrLIG - 1) * hno
				for pos in elt:
					if pos != None and pos != []:
						pix = self.__get_clarinette(self.__svg, pos, lno, dmy)
						dr.draw_pixbuf(ct, pix, 0, 0, psx, psy+hno, lno, dmy)
						pix = None
					psx += lno
		return False

	#----------------------------------------------------------------------

	def __init__(self, ins, lar = 600, hau = 200, ens = "", rpx = 0.95, rpy = 0.95, nom='svg/clarinette.svg'):
		super(CanvasClarinette, self).__init__(lar,hau,ens,rpx,rpy)
		self.__svg = open(nom, 'r').read()
		self.setInstrument(ins)
		self.refEVT = self.connect("expose-event", self.__dessiner)
		self.show()
