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

#------------------------------------------------------------------------------

from modele import *
from modele_data import *
from commun import *

#------------------------------------------------------------------------------

class ComposantComparaison:
	
	def __masquerSortIndicator(self, lis):
		for elt in lis:
			elt.set_sort_indicator(False)
	
	def __trierTAB(self, col):
		self.__masquerSortIndicator(self.__lisCOL)
		num = self.__lisCOL.index(col)
		if col.get_sort_order() == gtk.SORT_ASCENDING:
			order = gtk.SORT_DESCENDING
		else:
			order = gtk.SORT_ASCENDING
		col.set_sort_indicator(True)
		col.set_sort_order(order)
		self.tableMDL.set_sort_column_id(num, order)
	
	def __definirCOL(self, lab, cel, typ, num):
		col = definirROW(lab, cel, typ, num)
		col.set_clickable(True)
		col.set_sort_indicator(False)
		col.set_sort_order(gtk.SORT_ASCENDING)
		col.connect("clicked", self.__trierTAB)
		return col
	
	def __definirTAB(self, labFND, labDEG, labNOT, labNDI, labNDT, labTEN):
		tabMDL = gtk.ListStore(str, str, str, str, str, int)
		tabVUE = gtk.TreeView(tabMDL)
		celRND = gtk.CellRendererText()
		tvcTON = self.__definirCOL(labFND, celRND, "text", 0)
		tvcDEG = self.__definirCOL(labDEG, celRND, "text", 1)
		tvcNOT = self.__definirCOL(labNOT, celRND, "text", 2)
		tvcNDI = self.__definirCOL(labNDI, celRND, "text", 3)
		tvcNDT = self.__definirCOL(labNDT, celRND, "text", 4)
		tvcTEN = self.__definirCOL(labTEN, celRND, "text", 5)
		self.__lisCOL = [tvcTON, tvcDEG, tvcNOT, tvcNDI, tvcNDT, tvcTEN]
		for elt in self.__lisCOL:
			tabVUE.append_column(elt)
		tabVUE.show()
		scrWIN = definirScrolledWindow(tabVUE)
		return tabMDL, tabVUE, scrWIN

	def __definirCMP(self, titFRM, labTON, labDEG, labNOT, labNDI, labNDT, labTEN, labMCP, labCPA, lisMCP, lisCPA):
		labelMCP, comboMCP = definirLabelCombo(labMCP, lisMCP)
		labelCPA, comboCPA = definirLabelCombo(labCPA, lisCPA)
		tableMDL, tableVUE, scrWIN = self.__definirTAB(labTON, labDEG, labNOT, labNDI, labNDT, labTEN)
		toolbar = definirTOOLBAR([labelMCP, comboMCP, "", labelCPA, comboCPA])
		boxSEL = definirVBOX([toolbar], False, False)
		boxSEL = definirVPANED(boxSEL, scrWIN)
		return boxSEL, comboMCP, comboCPA, tableMDL, tableVUE

	#----------------------------------------------------------------------
	
	def __gerer(self, widget, data):
		tracer("ComposantComparaison", "__gerer")
		self.tableMDL.clear()
		self.__masquerSortIndicator(self.__lisCOL)
		if len(self.ens) >= 2:
			mcp = self.comboMCP.get_active_text()
			cpa = self.comboCPA.get_active_text()
			mcp = self.dicMCP[mcp]
			cpa = self.dicCPA[cpa]
			lnd = self.ens.comparer(mcp, cpa)
			for elt in lnd:
				deg = elt.getDegres()
				ens = elt.getNotes()
				ton = elt.getSon().getTexte()
				nom = deg.getNom()
				txt = ens.getTexte()
				ndi = deg.getDegresSEL(0)
				ndt = deg.getDegresEDT(0)
				ten = ens.getTension()
				ndi = formater("", " ", "", ndi)
				ndt = formater("", " ", "", ndt)
				self.tableMDL.append([ton, nom, txt, ndi, ndt, ten])	
		
	#----------------------------------------------------------------------
	
	def getNom(self):
		return TXT_ONG_CMP
	
	def getContainer(self):
		return self.container

	def update(self, ens):
		ens = Ensemble("", ens)
		if self.ens == None or self.ens != ens:
			self.ens = ens
			self.__gerer(None, None)

	#----------------------------------------------------------------------

	def __init__(self, notes):
		tracer("ComposantComparaison", "__init__")
		self.lisGAM = LISTE_GAMMES
		self.lisACC = LISTE_ACCORDS
		self.dicMCP = {TXT_CMP_INF:FNC_INF, TXT_CMP_EGA:FNC_EGA, TXT_CMP_SUP:FNC_SUP}
		self.dicCPA = {TXT_CMP_GAM:self.lisGAM.getListeDegres(), TXT_CMP_ACC:self.lisACC.getListeDegres()}
		lisMCP = self.dicMCP.keys()
		lisCPA = self.dicCPA.keys()
		boxSEL, self.comboMCP, self.comboCPA, self.tableMDL, self.tableVUE = self.__definirCMP(TXT_TIT_CMP, TXT_TIT_NOT, TXT_TIT_DEG, TXT_LIS_NOT, TXT_INT, TXT_INT, TXT_TIT_TEN, TXT_CMP_MOD, TXT_CMP_QUI, lisMCP, lisCPA)
		self.container = boxSEL
		self.ens = None
		self.update(notes)
		self.hMCP = self.comboMCP.connect("changed" , self.__gerer, None)
		self.hCPA = self.comboCPA.connect("changed" , self.__gerer, None)

