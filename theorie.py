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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

#------------------------------------------------------------------------------

import initialisations
import jouer_notes

import os
import pygtk
import gtk
from gtk.gdk import *

from sugar.activity import activity

#------------------------------------------------------------------------------

from modele import *
from commun import *
from composant_selection import *
from composant_affichage import *
from composant_degres import *
from composant_notes import *
from composant_comparaison import *
from composant_harmonica import *
from composant_flute import *
from composant_guitare import *
from composant_clarinette import *
from composant_piano import *
from composant_reconnaitre import *
from composant_ecouter import *
from composant_quadrant import *

#------------------------------------------------------------------------------

class Theorie(activity.Activity):

	def __keyPress(self, widget, event):
		key = gtk.gdk.keyval_name(event.keyval)
		if key == 'KP_Page_Up':
			widget.get_toplevel().child_focus(gtk.DIR_TAB_BACKWARD)
			return True
		elif key == 'KP_Page_Down':
			widget.get_toplevel().child_focus(gtk.DIR_TAB_FORWARD)
			return True
		return False

	def __del__(self):
		jouer_notes.delPygameMixer()

	def __init__(self, handle):
		# initialisations
		activity.Activity.__init__(self, handle)
		self.set_title(TXT_TIT_APP)
		toolbox = activity.ActivityToolbox(self)
		self.set_toolbox(toolbox)
		toolbox.show()
		# initialisation de pygame.mixer
		jouer_notes.iniPygameMixer()
		# creation des composants
		SET_AFF(MOD_NOT)
		SET_CMP(MOD_OCT)
		# creation des onglets gammes, accords, notes
		compGAM = ComposantGammes()
		compACC = ComposantAccords()
		compNOT = ComposantNotes()
		compSEL = ComposantSelection("", [compGAM, compACC, compNOT], gtk.POS_TOP)
		# recuperation des dimensions de l'ecran
		lar = screen_width()
		hau = screen_height()
		tracer("ComposantTheorie", "__init__", "Résolution = %d %d" %(lar, hau))
		# recuperation des notes initiales
		notes = compGAM.getNotes()
		# creation des onglets instruments et theorie
		compCMP = ComposantComparaison(notes)
		compREC = ComposantReconnaitre(notes)
		compECO = ComposantEcouter(notes)
		compQUA = ComposantQuadrant(notes)
		compHAR = ComposantHarmonica(notes)
		compFLU = ComposantFlute(notes)
		compGUI = ComposantGuitare(notes)
		compCLA = ComposantClarinette(notes)
		compPIA = ComposantPiano(notes)
		compINS = ComposantAffichage(TXT_ONG_INS, notes, [compGUI, compHAR, compFLU, compCLA, compPIA], gtk.POS_BOTTOM)
		compTHE = ComposantAffichage(TXT_ONG_THE, notes, [compQUA, compREC, compECO, compCMP], gtk.POS_BOTTOM)
		compAFF = ComposantAffichage("", notes, [compINS, compTHE], gtk.POS_TOP)
		panedUI = definirVPANED(compSEL.getContainer(), compAFF.getContainer())
		# liaison 'evenement' entre les deux zones
		compSEL.addObserver(compAFF)
		# ajout de l'ensemble dans la fenetre et affichage
		self.set_canvas(panedUI)
		# gestion des evenements 'clavier'
		self.connect('key-press-event', self.__keyPress)
