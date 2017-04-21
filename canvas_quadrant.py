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

import math
import pygtk
import gtk
import pango

from commun import *
import modele

from canvas_graphique import *

class CanvasQuadrant(CanvasGraphique):

	def __dessiner(self, widget, event):
		rec, lar, hau, dr, gc, pl, cm = self.get_contexte_graphique(widget)
		dim = min(lar, hau)
		pex, pey, lex, ley = self.centrer_partie((lar-dim)/2, (hau-dim)/2, dim, dim, self.rpx, self.rpy)
		# dessin du cercle principal
		tcp = 360*64
		gc.set_foreground(self.atb)
		dr.draw_arc(gc, True, pex, pey, lex, ley, 0, tcp)
		gc.set_foreground(self.atn)
		dr.draw_arc(gc, False, pex, pey, lex, ley, 0, tcp)
		# calcul des coordonnes des 12 centre sur le cercle
		nbr = modele.NOMBRE_NOTES_OCTAVE
		lis = range(nbr)
		dec = (2.0 * math.pi) / 12.0
		ang = -math.pi / 2.0
		pmx = lar / 2.0
		pmy = hau / 2.0
		lpc = []
		lpr = []
		for elt in lis:
			psx = int(pmx + 0.5*lex * math.cos(ang))
			psy = int(pmy + 0.5*ley * math.sin(ang))
			lpc.append([psx, psy])
			ang += dec 
			if self.deg[elt]:
				lpr.append((psx,psy))
		# trace du polygone avec couleur
		gc.set_foreground(self.atj)
		dr.draw_polygon(gc, True, lpr)
		# trace des lignes entre chaque point
		gc.set_foreground(self.atn)
		lsi = range(nbr)
		for pt1 in lsi:
			lsf = range(pt1+1,nbr)
			for pt2 in lsf:
				if self.deg[pt1] and self.deg[pt2]:
					dr.draw_line(gc, lpc[pt1][0], lpc[pt1][1], lpc[pt2][0], lpc[pt2][1])
		# trace des points sur le cercle avec ou sans note/degre
		lis = range(nbr)
		gc.set_foreground(self.atn)
		nbl = 3
		ltx = int(lex / 5)
		hty = int(ltx / 2)
		dia = int(min(ltx,hty)/nbl)
		ray = int(dia/2)
		lsn = self.ens.getListe()
		psn = 0
		for ind in lis:
			elt = lpc[ind]
			if self.deg[ind]:
				txt = " %s / %s " %(modele.LISTE_NOMS_DEGRES[ind], lsn[psn].getTexte(modele.MOD_NOT))
				psn += 1
				psx = elt[0]-ltx/2
				psy = elt[1]-hty/2
				self.tracer_rectangle_texte_centre(gc, dr, pl, self.atn, self.atb, psx, psy, ltx, hty, nbl, txt)
			else:
				gc.set_foreground(self.atn)
				dr.draw_arc(gc, True, elt[0]-ray, elt[1]-ray, dia, dia, 0, tcp)

	def setNotes(self, ens):
		assert type(ens) == list or type(ens) in [unicode, str] or ens.__class__.__name__ == "Ensemble"
		if ens.__class__.__name__ != "Ensemble" :
			self.ens = modele.Ensemble("", ens)
		else:
			self.ens = ens
		self.deg = [False] * modele.NOMBRE_NOTES_OCTAVE
		lson = self.ens.getListe()
		lson = map(lambda e:e.getNote(), lson)
		lson = map(lambda e:e-lson[0], lson)
		for ind in lson:
			self.deg[ind] = True
		self.queue_draw()

	#----------------------------------------------------------------------

	def __init__(self, lar = 600, hau = 200, ens = "", rpx = 0.80, rpy = 0.80):
		"""
		@param lar: largeur du canvas
		@param hau: hauteur du canvas
		@param rpx: partie horizontale de la zone utilisee 
		@param rpy: partie verticale de la zone utilisee 
		"""
		super(CanvasQuadrant,self).__init__(lar, hau, rpx, rpy)
		self.setNotes(ens)
		self.refEVT = self.connect("expose-event", self.__dessiner)
		self.show()
