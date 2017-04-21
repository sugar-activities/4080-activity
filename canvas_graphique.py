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

#------------------------------------------------------------------------------

class CanvasGraphique(gtk.DrawingArea):
	
	#----------------------------------------------------------------------------
	
	def svg_str_to_pixbuf(self, txt, lar, hau):
		"""
		Methode permettant de transformer un SVG/XML en Pixbuf
		de taille (lar, hau).
		
		@param txt: le contenu du svg (xml => format texte)
		@param lar: la largeur en pixel du Pixbuf a creer
		@param hau: la hauteur en pixel du Pixbuf a creer
		"""
		pbl = gtk.gdk.PixbufLoader('svg')
		pbl.set_size(lar, hau)
		pbl.write(txt)
		pbl.close()
		pix = pbl.get_pixbuf()
		return pix
	
	def sauver_image(self, nom, qua="100"):
		"""
		Methode permettant de sauver le contenu du DrawingArea
		dans un fichier JPEG.
		
		@param nom: le nom de l'image sauvegardee
		@param qua: la qualite de compression de l'image
		"""
		win = self.window
		if win != None:
			rec = self.get_allocation()
			lar = rec[2]
			hau = rec[3]
			col = self.get_colormap()
			pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, 0, 8, lar, hau)
			pixbuf.get_from_drawable(win, col, 0, 0, 0, 0, lar, hau)
			pixbuf.save(nom, "jpeg", {"quality":qua})

	#----------------------------------------------------------------------------

	def centrer(self, pos, dim, rap):
		"""
		Methode permettant de centrer un segment S2 par rapport a un segment
		S1. 
		
		La methode retourne la position et la dimension du segment S2.
		
		@param pos: la position du segement S1
		@param dim: la dimension du segment S1
		@param rap: la partie de S1 utilisee
		"""
		dec = dim * (1.0 - rap) / 2.0
		pos = int(pos + dec)
		dim = int(rap * dim)
		return pos, dim
	
	def centrer_ligne(self, pos, dm1, dm2):
		"""
		Methode permettant de centrer un segment S2 par rapport a un
		un autre segment S1.
		
		La methode retourne la position et le decalage du segment S2.
		
		@param pos: position du segment S1
		@param dm1: longueur du segment S1
		@param dm2: longueur du segment S2
		"""
		dec = int((dm1 - dm2) / 2.0)
		pos += dec
		return pos, dec
	
	def centrer_partie(self, psx, psy, lar, hau, rpx, rpy):
		"""
		Methode permettant de centrer un objet rectangulaire O2
		par rapport a un autre objet rectangulaire O1. 
		
		La methode retourne la position (X,Y) et la dimension (X, Y)
		du rectangle O2
		
		@param psx: la position en X de O1
		@param psy: la position en Y de O1
		@param lar: la dimension en X de O1
		@param hau: la dimension en Y de O1
		@param rpx: la partie utilisee de la largeur de O1
		@param rpy: la partie utilisee de la hauteur de O1
		"""	
		pex, lex = self.centrer(psx, lar, rpx)
		pey, ley = self.centrer(psy, hau, rpy)
		return pex, pey, lex, ley
	
	def centrer_rectangle(self, psx, psy, lar, hau, lrc, hrc):
		"""
		Methode permettant de centrer un rectangle de dimensions (lrc, hrc)
		dans un rectangle positionne en (psx, psy) et de dimensions (lar, hau).
		"""
		psx, dcx = self.centrer_ligne(psx, lar, lrc)
		psy, dcy = self.centrer_ligne(psy, hau, hrc)
		return psx, psy, dcx, dcy
	
	def decaler_polygone(self, lpt, dec):
		"""
		Decalage de chaque coordonnee du polygone (definie par rapport
		a l'origine du repere).
		
		@param lpt: liste des points du polygone
		@param dec: decalage en X et Y
		"""
		res = []
		for elt in lpt:
			res.append((elt[0]+dec[0],elt[1]+dec[1]))
		return res
	
	#----------------------------------------------------------------------------
	
	def get_contexte_graphique(self, widget):
		"""
		Recuperation des dimensions du widget (l'ecran), du contexte graphique,
		du layout (pour les textes) et initialisation des couleurs.

		@param widget: pour recuperer les informations sur le contexte graphique
		"""
		rec = widget.get_allocation()
		lar = rec.width
		hau = rec.height
		dr = widget.window
		gc = dr.new_gc()
		pl = self.create_pango_layout("")
		cm = widget.get_colormap()
		self.initialiser_couleurs(cm)
		return rec, lar, hau, dr, gc, pl, cm
	
	def initialiser_couleurs(self, cm):
		"""
		Methode initialisant les couleurs :
		- creation des couleurs;
		- association avec la colormap du widget.
		
		@param cm: le colormap du widget 'canvas'
		"""
		lis = ["#9F9","#8E8","#7E7","#6D6","#5D5","#4C4","#3B3","#1A1","#070"]
		lis = map(lambda e:gtk.gdk.color_parse(e), lis)
		self.acp = map(lambda e : cm.alloc_color(e, False, True), lis)
		utj = gtk.gdk.color_parse("#FF9")
		utg = gtk.gdk.color_parse("#777")
		utb = gtk.gdk.color_parse("#FFF")
		utn = gtk.gdk.color_parse("#000")
		utr = gtk.gdk.color_parse("#E66")
		self.atj = cm.alloc_color(utj, False, True)
		self.atg = cm.alloc_color(utg, False, True)
		self.atb = cm.alloc_color(utb, False, True)
		self.atn = cm.alloc_color(utn, False, True)
		self.atr = cm.alloc_color(utr, False, True)

	def get_couleur_remplissage(self, etat):
		"""
		Retourne la couleur associee a l'etat qui peut etre soit la
		force d'un intervalle ou bien directement une couleur
		(noir ou blanc).

		@param etat: une couleur ou un etat (qualite d'un intervalle)
		"""
		if etat == self.COUL_NOIR:
			col = self.atn
		elif etat == self.COUL_BLANC:
			col = self.atb
		else:
			col = self.acp[etat]
		return col

	#----------------------------------------------------------------------------

	def calculer_taille(self, lar, hau, rpx, rpy, minCOL, minLIG, nbrCOL, nbrLIG, rap=0.2):
		"""
		Methode de calcul des dimensions des cases d'une grille contenant un nombre
		minimum de colonnes et de lignes. Les dimensions sont equilibrees suivant la
		variable 'rap' et sont definies sur une partie d'une zone rectangulaire

		@param lar: largeur de la zone rectangulaire
		@param hau: hauteur de la zone rectangulaire
		@param rpx: partie de la zone rectangulaire a utiliser en X
		@param rpy: partie de la zone rectangulaire a utiliser en Y
		@param minCOL: nombre minimum de colonnes dans la grille
		@param minLIG: nombre minimum de lignes dans la grille
		@param nbrCOL: nombre souhaite de colonnes dans la grille
		@param nbrLIG: nombre souhaite de lignes dans la grille
		"""
		# largeur et hauteur utilisable de la zone
		ldu = int(rpx * lar)
		hdu = int(rpy * hau)
		# calcul des largeur/hauteur d'une sous-zone
		lno = int(ldu / max(minCOL,nbrCOL))
		hno = int(hdu / max(minLIG,nbrLIG))
		# verficiation des disproportions entre largeur et hauteur de la 
		# sous-zone (calcul du rapport min/max)
		vmn = min(lno,hno)
		vmx = max(lno,hno)
		vrp = float(vmx - vmn)/float(vmx)
		# plus vrp est proche de 0 est plus les dimensions sont proches
		if vrp > rap:
			# rap * vmx = vmx - vmn => vmx * (1-rap) = vmn
			vmx = int(vmn / (1.0-rap))
			if lno > hno:
				lno = vmx
				hno = vmn
			else:
				lno = vmn
				hno = vmx
		# calcul de la position de la premiere sous-zone
		psx = int((lar - nbrCOL * lno) / 2)
		psy = int((hau - nbrLIG * hno) / 2)
		return psx, psy, lno, hno

	#----------------------------------------------------------------------------

	def tracer_ligne_horizontale_centree(self, gc, dr, psx, psy, lar, rpx, brd):
		"""
		Methode permettant de tracer une ligne horizontale centree sur
		une partie d'un segment horizontal.

		@param psx: position de la zone en X
		@param psy: position de la zone en Y
		@param lar: largeur de la zone (segment)
		@param rpx: definition de la partie utilisable du segment
		@param brd: couleur de trace de la ligne
		"""
		pex, lex = self.centrer(psx, lar, rpx)
		gc.set_foreground(brd)
		dr.draw_line(gc, pex, psy, pex+lex-1, psy)

	def tracer_ellipse_centre(self, gc, dr, psx, psy, lar, hau, rpx, rpy, rmp, brd):
		"""
		Methode de trace d'une ellipse centree dans une partie d'une zone 
		rectangulaire.

		@param psx: position en X de la zone rectangulaire
		@param psy: position en Y de la zone rectangulaire
		@param lar: largeur de la zone rectangulaire
		@param hau: hauteur de la zone rectangulaire
		@param rpx:
		@param rpy: definition de la partie utilisable de cette zone
		@param rmb: couleur de remplissage
		@param brd: couleur de bordure
		"""
		pex, pey, dex, dey = self.centrer_partie(psx, psy, lar, hau, rpx, rpy)
		tcp = 360*64
		gc.set_foreground(rmp)
		dr.draw_arc(gc, True, pex, pey, dex, dey, 0, tcp)
		gc.set_foreground(brd)
		dr.draw_arc(gc, False, pex, pey, dex, dey, 0, tcp)
		
	def tracer_texte_centre(self, gc, dr, pl, col, psx, psy, lar, hau, nbl, txt, fnt="Arial", sty="Bold"):
		"""
		@param col: couleur du texte
		@param psx: position en X de la zone rectangulaire
		@param psy: position en Y de la zone rectangulaire
		@param lar: largeur de la zone rectangulaire
		@param hau: hauteur de la zone rectangulaire
		@param nbl: nombre de caracteres sur la zone
		@param txt: le texte a ecrire
		@param fnt: nom de la fonte
		@param sty: style de la fonte
		"""
		# taille minimale de la fonte
		tmn = 6
		# tpc est la taille de la fonte qui est fonction des dimensions de la zone et 
		# du nombre maximal de caracteres. 
		tpc = str(max(int(min(lar,hau)/(3*nbl)),tmn))
		pl.set_font_description(pango.FontDescription(fnt + " " + sty + " " + tpc))
		pl.set_text(txt)
		# ecriture du texte au centre de la zone
		pll, plh = pl.get_pixel_size()
		pex, pey, dcx, dcy = self.centrer_rectangle(psx, psy, lar, hau, pll, plh)
		gc.set_foreground(col)
		dr.draw_layout(gc, pex, pey, pl)

	def tracer_rectangle_texte_centre(self, gc, dr, pl, fnd, col, psx, psy, lar, hau, nbl, txt, fnt="Arial", sty="Bold"):
		"""
		(fnd,col) : couleurs de fond et du texte
		(psx,psy,lar,hau) : zone rectangulaire accueillant le texte
		(nbl,txt) : nombre de caracteres sur la zone et le texte a ecrire
		(fnt,sty) : fonte et style
		"""
		# taille minimale de la fonte
		tmn = 6
		# calcul des position/dimension du texte
		tpc = str(max(int(min(lar,hau)/(3*nbl)),tmn))
		pl.set_font_description(pango.FontDescription(fnt + " " + sty + " " + tpc))
		pl.set_text(txt)
		pll, plh = pl.get_pixel_size()
		pex, pey, dcx, dcy = self.centrer_rectangle(psx, psy, lar, hau, pll, plh)
		# calcul des position/dimension du rectangle (entourant le texte)
		tnx = pex - dcx / 2
		tny = pey - 2
		pll += dcx
		plh += 3
		# trace du rectangle puis du texte
		gc.set_foreground(fnd)
		dr.draw_rectangle(gc, True, tnx, tny, pll, plh)
		gc.set_foreground(col)
		dr.draw_layout(gc, pex, pey, pl)

	def afficher_rectangle(self, gc, dr, nbrCOL, nbrLIG, lno, hno, psx, psy, dcy):
		lcs = lno * nbrCOL
		hcs = hno * nbrLIG
		csx = psx + (lcs-lno) / 2
		dcx = lno * nbrCOL
		gc.set_foreground(self.atn)
		dr.draw_rectangle(gc, False, psx, psy, dcx, dcy)
		return lcs, hcs, csx, dcx

	def afficher_note(self, gc, dr, pl, prs, note, psx, psy, lcs, hcs, rpx, rpy, csx, lno, nbc):
		txt = note.getTexte(modele.MOD_OCT)
		etat = prs.getConsonnance(note)
		rmp = self.get_couleur_remplissage(etat)
		brd = self.atn
		self.tracer_ellipse_centre(gc, dr, psx, psy, lcs, hcs, rpx, rpy, rmp, brd)
		if etat == modele.INT_TON:
			col = self.atb
		else:
			col = self.atn
		self.tracer_texte_centre(gc, dr, pl, col, csx, psy, lno, hcs, nbc, txt)
		return brd, rmp, etat

	#----------------------------------------------------------------------

	def __init__(self, lar, hau, rpx = 0.95, rpy = 0.95):
		"""
		@param lar: largeur du canvas
		@param hau: hauteur du canvas
		@param ens: ensemble de notes
		@param rpx: partie horizontale de la zone utilisee 
		@param rpy: partie verticale de la zone utilisee 
		"""
		super(CanvasGraphique,self).__init__()
		self.COUL_NOIR = "NO"
		self.COUL_BLANC = "BL"
		self.rpx = rpx
		self.rpy = rpy
		self.set_size_request(lar, hau)
		self.show()
