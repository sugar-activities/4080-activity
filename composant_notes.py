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

from modele import *
from commun import *
from observable import *
from canvas_piano import *

import jouer_notes

#------------------------------------------------------------------------------

class ComposantNotes(Observable):

	def getNom(self):
		return TXT_ONG_NOT

	def getContainer(self):
		return self.container

	def getNotes(self):
		return self.notes

	def __jouer(self, widget, data):
		if self.notes != None and self.notes.strip() != "":
			lis = self.notes.split()
			lis = map(lambda e: Son(e), lis)
			jouer_notes.jouerNotesSEQ(lis, 600)	

	def __keyPress(self, widget, event):
		key = gtk.gdk.keyval_name(event.keyval)
		if key in ['KP_Home', 'KP_End']:
			if widget == self.texteNOT:
				# jeu des notes
				self.__jouer(None, None)
				return True
			elif widget in self.listeNOT:
				# selection d'une note
				active = widget.get_active()
				widget.set_active(not active)
				return True
		return False

	def __gerer(self, widget, data):
		tracer("ComposantNotes", "__gerer")
		txt = " "
		ens = " "
		oct = 0
		ref = LISTE_NOMS_NOTES[0]
		lis = range(len(self.listeNOT))
		for ind in lis:
			obj = self.listeNOT[ind]
			nom = obj.get_label()
			if cmp(nom, ref) == 0 and ind > 0:
				oct += 1
			if obj.get_active():
				txt += "%s " %(nom)
				ens += "%s%d " %(nom, oct)
		if txt.strip() == "":
			txt = "    "
		self.texteNOT.set_label(txt)
		self.notes = ens
		self.notifyObservers(ens)

	def __renommer(self, widget, data):
		debNOT = self.comboTRS.get_active()
		lisBUT = self.listeNOT
		assert len(lisBUT) == NOMBRE_NOTES_OCTAVE
		lin = range(NOMBRE_NOTES_OCTAVE)
		lis = map(lambda e : (e + debNOT) % NOMBRE_NOTES_OCTAVE, lin)
		for ind in lin:
			lisBUT[ind].set_label(LISTE_NOMS_NOTES[lis[ind]])
		self.__gerer(widget, data)

	def __init_components(self):
		# definition de la liste des boutons
		self.listeNOT = []
		for txt in LISTE_NOMS_NOTES:
			obj = definirToggleButton(txt)
			obj.set_active(False)
			self.listeNOT.append(obj)
		labelNOT = definirLabel(TXT_NOT + " : ")
		self.texteNOT = definirButton("   ")
		labelTRS, self.comboTRS = definirLabelCombo(_("Transposition"), LISTE_NOMS_NOTES)
		tlbNOT = definirHBOX(self.listeNOT, True, True)
		tlbNOT = definirTOOLBAR([tlbNOT])
		tlbTRS = definirTOOLBAR([labelTRS, self.comboTRS])
		tlbENS = definirTOOLBAR([labelNOT, self.texteNOT])
		lig1 = definirHBOX([tlbNOT, tlbTRS], True, True)
		lig2 = definirHBOX([tlbENS])
		self.container = definirVBOX([lig1, lig2], False, False)

	def __init_events(self):
		# association des evenement des boutons a une methode
		self.hNOT = map(lambda e:e.connect("toggled", self.__gerer, None), self.listeNOT)
		self.hNKP = map(lambda e:e.connect("key-press-event", self.__keyPress), self.listeNOT)
		# transposition des notes
		self.hCLN = self.comboTRS.connect("changed", self.__renommer, None)
		# le jeu des notes est declanche soit par clic, soit par clavier
		self.hJOU = self.texteNOT.connect("clicked" , self.__jouer, None)
		self.hKJN = self.texteNOT.connect("key-press-event", self.__keyPress)

	def __init__(self):
		Observable.__init__(self)
		self.notes = ""
		self.__init_components()
		self.__init_events()
