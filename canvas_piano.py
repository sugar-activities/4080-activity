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

import modele
import canvas_instrument

#------------------------------------------------------------------------------

class CanvasPiano(canvas_instrument.CanvasInstrument):

	def __positionNoteClavier(self, note):
		"""
		Retourne la note non diesee la plus proche de la note
		passee en parametre (inferieure) i.e une touche blanche
		inferieure ou egale a la note. Cela sert pour calculer
		les position des touches blanches et noires.
		"""
		assert 0 <= note and note < modele.NOMBRE_NOTES_OCTAVE
		if note in [0,1]:
			pos = 0
		elif note in [2,3]:
			pos = 1
  		elif note in [4]:
			pos = 2
		elif note in [5,6]:
			pos = 3
		elif note in [7,8]:
			pos = 4
		elif note in [9,10]:
			pos = 5
		else:
			pos = 6
		return pos
	
	def __initialiserDieses(self, lar, hau):
		"""
		Definition des polygones pour chaque touche differente 
		du clavier : 3 touches blanches et une touche noire.
		"""
		assert lar >= 0 and hau >= 0
		# dimension des touches "diese"
		ltd = lar / 2
		htd = (5 * hau / 8) + 1
		assert ltd >= 0 and htd >= 0
		# position des touches "diese"
		min = (lar - ltd) / 2 + 1
		max = min + ltd - 1
		lar -= 1
		# pour les touches blanches (diese a gauche, a droite puis au centre)
		self.__xyg = [(min,0),(lar,0),(lar,hau),(0,hau),(0,htd),(min,htd),(min,0)]
		self.__xyd = [(0,0),(max,0),(max,htd),(lar,htd),(lar,hau),(0,hau),(0,0)]
		self.__xyc = [(min,0),(max,0),(max,htd),(lar,htd),(lar,hau),(0,hau),(0,htd),(min,htd),(min,0)]
		# pour les touches noires
		min = min+ltd
		max = min+ltd
		htd -= 1
		if max < min:
			min = 0
			max = 0
		self.__xyn = [(min,0),(max,0),(max,htd),(min,htd),(min,0)]
	
	def __afficherNote(self, dr, gc, cm, psx, psy, lar, note, etat):
		son = note % modele.NOMBRE_NOTES_OCTAVE
		ocv = note / modele.NOMBRE_NOTES_OCTAVE
		assert 0 <= ocv
		pos = self.__positionNoteClavier(son) + ocv * 7
		psx += pos * lar
		lis = []
		if son in [4,11]:
			# touches blanches avec touche noire a gauche (mi, si)
			lis = self.decaler_polygone(self.__xyg, (psx, psy))
			gc.set_foreground(self.get_couleur_remplissage(etat))
			dr.draw_polygon(gc, True, lis)
		elif son in [0,5]:
			# touches blanches avec touche noire a droite (do, fa)
			lis = self.decaler_polygone(self.__xyd, (psx, psy))
			gc.set_foreground(self.get_couleur_remplissage(etat))
			dr.draw_polygon(gc, True, lis)
		elif son in [2,7,9]:
			# touches blanches avec touches noires a droite et a gauche (re, sol, la)
			lis = self.decaler_polygone(self.__xyc, (psx, psy))
			gc.set_foreground(self.get_couleur_remplissage(etat))
			dr.draw_polygon(gc, True, lis)
		else:
			# touches noires (do#, re#, fa#, sol#, la#)
			lis = self.decaler_polygone(self.__xyn, (psx, psy))
			gc.set_foreground(self.get_couleur_remplissage(etat))
			dr.draw_polygon(gc, True, lis)
		gc.set_foreground(self.get_couleur_remplissage(self.COUL_NOIR))
		dr.draw_polygon(gc, False, lis)
	
	def __dessiner(self, widget, event):
		# recuperation des dimensions de la zone graphique
		rec, lar, hau, dr, gc, pl, cm = self.get_contexte_graphique(widget)
		# calcul du nombre d'octaves
		vmin, vmax = self.ens.getOctaves()
		dif = vmax-vmin+1
		nbr = max(2, dif)
		# calcul des dimensions des touches : 
		# - fonction de la zone graphique utilisable
		# - fonction du nombre de touches blanches :
		#   nombre d'octaves * 7 touches blanches.
		ltc = int(self.rpx * lar / (nbr * 7))
		htc = int(self.rpy * hau)
		if htc > 2*ltc:
			htc = 2 * ltc
		else:
			ltc = htc/2
		nbr = dif
		# calcul du decalage du clavier pour centrage
		psx = (lar - 7 * nbr * ltc) / 2
		psy = (hau - htc) / 2
		#
		self.__initialiserDieses(ltc, htc)
		liste = self.ens.getListe()
		prs = None
		if len(liste) >= 1:
			prs = modele.Son(liste[0])
		for ind in range(nbr * modele.NOMBRE_NOTES_OCTAVE):
			note = modele.Son(ind)
			if prs != None:
				note.decaler(prs.getOctave() * modele.NOMBRE_NOTES_OCTAVE)
			son = note.getNote()
			if note in liste:
				etat = prs.getConsonnance(note)
			elif son in [0,2,4,5,7,9,11]:
				etat = self.COUL_BLANC
			else:
				etat = self.COUL_NOIR
			self.__afficherNote(dr, gc, cm, psx, psy, ltc, ind, etat)
		return False

	#----------------------------------------------------------------------
	
	def __init__(self, lar = 600, hau = 200, ens = "", rpx = 0.95, rpy = 0.95):
		"""
		@param lar: largeur de la zone graphique
		@param hau: hauteur de la zone graphique
		@param ens: l'ensemble de notes a afficher
		@param rpx: partie de la largeur utilisee
		@param rpy: partie de la hauteur utilisee
		"""
		super(CanvasPiano,self).__init__(lar,hau,ens,rpx,rpy)
		self.connect("expose-event", self.__dessiner)
		self.show()
