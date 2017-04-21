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

from commun import *
import modele
import canvas_instrument

#------------------------------------------------------------------------------

class CanvasHarmonica(canvas_instrument.CanvasInstrument):
	
	def __initialiserPolygones(self, lar, hau, rpx = 0.6, rpy = 0.6):
		"""
		Initialisation des polygones : triangle vers le haut, triangle
		vers le bas et tirette.
		"""
		assert lar >= 0 and hau >= 0
		lex = rpx * lar
		ley = rpy * hau
		dcx = int((lar - lex)/2)
		dcy = int((hau - ley)/2)
		minx = dcx
		maxx = lar-dcx
		milx = int((minx+maxx)/2)
		minx = dcx
		maxx = lar-dcx
		miny = dcy
		maxy = hau-dcy
		mily = int((miny+maxy)/2)
		self.__sou = [(minx,maxy),(maxx,maxy),(milx,miny)]
		self.__asp = [(minx,miny),(maxx,miny),(milx,maxy)]
		infy = int(mily - 0.25 * ley)+1
		supy = int(mily + 0.25 * ley)
		milx += int(milx/4)
		self.__tir = [(minx,infy),(milx,infy),(milx,miny),(maxx,miny),(maxx,maxy),(milx,maxy),(milx,supy),(minx,supy),(minx,infy)]

	def __dessiner(self, widget, event):
		# Recuperation du nombre de notes de l'ensemble
		nno = len(self.ens)
		if nno > 0:
			# Recuperation du contexte graphique, des dimensions...
			rec, lar, hau, dr, gc, pl, cm = self.get_contexte_graphique(widget)
			# Recherche des possibilites de jeu des notes de l'ensemble
			liste, lisNH, lisNB, nbrCOL = self.get_solutions(self.ens, self.ins)
			nbrLIG = 4
			# Calcul de la taille des cases et de la position du 
			# tableau, de la taille de la fonte
			psx, psy, lno, hno = self.calculer_taille(lar, hau, self.rpx, self.rpy, 5, nbrLIG, nbrCOL, nbrLIG, 0.5)
			lar = lno * nbrCOL
			hau = hno * nbrLIG
			self.__initialiserPolygones(lno, hno)
			# Tracage du tableau
			prs = modele.Son(liste[0])
			dcy = nbrLIG * hno
			# pour chaque note de l'ensemble
			lisNOT = range(nno)
			for ind in lisNOT:
				# affichage du rectangle
				nbrPOS = lisNB[ind]
				lcs, hcs, csx, dcx = self.afficher_rectangle(gc, dr, nbrPOS, 1, lno, hno, psx, psy, dcy)
				# affichage de la note
				note = liste[ind]
				brd, rmp, etat = self.afficher_note(gc, dr, pl, prs, note, psx, psy, lcs, hcs, 0.8, 0.8, csx, lno, 5)
				# affichage des alveoles, souffler/aspirer, alterations
				elt = lisNH[ind]
				if elt == []:
					psx += lno
				for pos in elt:
					if pos != None and pos != []:
						pty = psy
						# numero d'alveole
						pty += hno
						rmp = self.atb
						self.tracer_ellipse_centre(gc, dr, psx, pty, lno, hno, 0.8, 0.8, rmp, brd)
						self.tracer_texte_centre(gc, dr, pl, self.atn, psx, pty, lno, hno, 4, str(pos[0]))
						# souffler / aspirer
						pty += hno
						tpx, tpy, tdx, tdy = self.centrer_partie(psx, pty, lno, hno, 0.5, 0.5)
						if pos[1] == modele.HAR_ALV_SOU:
							pol = self.decaler_polygone(self.__sou, (psx, pty))
							gc.set_foreground(self.atb)
							dr.draw_polygon(gc, True, pol)
							gc.set_foreground(self.atn)
							dr.draw_polygon(gc, False, pol)
							col = self.atn
							tpy += int(tdy/4)
							txt = TXT_HAR_SOU
						else:
							pol = self.decaler_polygone(self.__asp, (psx, pty))
							gc.set_foreground(self.atn)
							dr.draw_polygon(gc, True, pol)
							col = self.atb
							tpy -= int(tdy/4)
							txt = TXT_HAR_ASP
						self.tracer_texte_centre(gc, dr, pl, col, tpx+1, tpy, tdx, tdy, len(txt)+1, txt)
						# alteration
						pty += hno
						if pos[2] == modele.HAR_TIR_APP:
							pol = self.decaler_polygone(self.__tir, (psx, pty))
							gc.set_foreground(self.atn)
							dr.draw_polygon(gc, True, pol)
						elif pos[2] == modele.HAR_ALT_BN1:
							self.tracer_texte_centre(gc, dr, pl, self.atn, psx, pty, lno, hno, 3, "b1")
						elif pos[2] == modele.HAR_ALT_BN2:
							self.tracer_texte_centre(gc, dr, pl, self.atn, psx, pty, lno, hno, 3, "b2")
						elif pos[2] == modele.HAR_ALT_BN3:
							self.tracer_texte_centre(gc, dr, pl, self.atn, psx, pty, lno, hno, 3, "b3")
						elif pos[2] == modele.HAR_ALT_OVB:
							self.tracer_texte_centre(gc, dr, pl, self.atn, psx, pty, lno, hno, 3, "ob")
						elif pos[2] == modele.HAR_ALT_OVD:
							self.tracer_texte_centre(gc, dr, pl, self.atn, psx, pty, lno, hno, 3, "od")
					psx += lno
		return False

	#----------------------------------------------------------------------

	def __init__(self, har, lar = 600, hau = 200, ens = "", rpx = 0.95, rpy = 0.95):
		super(CanvasHarmonica,self).__init__(lar, hau, ens, rpx, rpy)
		self.setInstrument(har)
		self.refEVT = self.connect("expose-event", self.__dessiner)
		self.show()
