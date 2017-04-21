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

import initialisations

import pygtk
import gtk

from modele import *
from modele_data import *
from commun import *
from composant_flute import *
from composant_guitare import *
from composant_harmonica import *
from composant_piano import *
from composant_clarinette import *
from composant_comparaison import *
from composant_degres import *
from composant_notes import *
from composant_selection import *
from composant_affichage import *
from composant_qcm import *

#------------------------------------------------------------------------------

def testComposantClarinette(notes):
	win = gtk.Window()
	obj = ComposantClarinette(notes)
	win.add(obj.getContainer())
	win.connect("destroy", gtk.main_quit)
	win.fullscreen()
	win.show_all()
	gtk.main()
		
def testComposantFlute(notes):
	win = gtk.Window()
	obj = ComposantFlute(notes)
	win.add(obj.getContainer())
	win.connect("destroy", gtk.main_quit)
	win.fullscreen()
	win.show_all()
	gtk.main()

def testComposantGuitare(notes):
	win = gtk.Window()
	obj = ComposantGuitare(notes)
	win.add(obj.getContainer())
	win.connect("destroy", gtk.main_quit)
	win.fullscreen()
	win.show_all()
	gtk.main()

def testComposantHarmonica(notes):
	win = gtk.Window()
	obj = ComposantHarmonica(notes)
	win.add(obj.getContainer())
	win.connect("destroy", gtk.main_quit)
	win.fullscreen()
	win.show_all()
	gtk.main()
		
def testComposantPiano(notes):
	win = gtk.Window()
	obj = ComposantPiano(notes)
	win.add(obj.getContainer())
	win.connect("destroy", gtk.main_quit)
	win.fullscreen()
	win.show_all()
	gtk.main()

def testComposantDegres():
	obj = ComposantAccords()
	win = gtk.Window()
	win.add(obj.getContainer())
	win.connect("destroy", gtk.main_quit)
	win.fullscreen()
	win.show_all()
	gtk.main()

def testComposantNotes():
	obj = ComposantNotes()
	win = gtk.Window()
	win.add(obj.getContainer())
	win.connect("destroy", gtk.main_quit)
	win.fullscreen()
	win.show_all()
	gtk.main()

def testComposantComparaison(notes):
	win = gtk.Window()
	obj = ComposantComparaison(notes)
	win.add(obj.getContainer())
	win.connect("destroy", gtk.main_quit)
	win.fullscreen()
	win.show_all()
	gtk.main()

def testComposantSelection():
	compGAM = ComposantGammes()
	compACC = ComposantAccords()
	compNOT = ComposantNotes()
	composant = ComposantSelection("", [compGAM, compACC, compNOT], gtk.POS_TOP)
	win = gtk.Window()
	win.add(composant.getContainer())
	win.connect("destroy", gtk.main_quit)
	win.fullscreen()
	win.show_all()
	gtk.main()

def testComposantAffichage(notes):
	compINS = ComposantAffichage(TXT_ONG_INS, notes, [ComposantGuitare(notes), ComposantHarmonica(notes), ComposantPiano(notes),ComposantFlute(notes),ComposantClarinette(notes)], gtk.POS_TOP)
	compTHE = ComposantComparaison(notes)
	compAFF = ComposantAffichage("", notes, [compINS, compTHE], gtk.POS_TOP)
	composant = definirHBOX([compAFF.getContainer()])
	win = gtk.Window()
	win.add(composant)
	win.connect("destroy", gtk.main_quit)
	win.fullscreen()
	win.show_all()
	gtk.main()

def testComposantQCM(ton, nom):
	lis = ListeGammes()
	deg = lis.getDegres(nom)
	ens = deg.getNotes(ton, 0, False)
	com = ComposantQCM(ens)
	win = gtk.Window()
	win.add(com.getContainer())
	win.connect("destroy", gtk.main_quit)
	win.set_size_request(700, 300)
	win.show_all()
	gtk.main()

#------------------------------------------------------------------------------

if __name__ == "__main__":
	SET_AFF(MOD_NOT)
	SET_CMP(MOD_OCT)
	#testComposantFlute("Do0 Ré0 Mi0 Fa0 Sol0 La0 Si0")
	#testComposantGuitare("Do0 Ré0 Mi0 Fa0 Sol0 La0 Si0")
	#testComposantHarmonica("Do0 Ré0 Mi0 Fa0 Sol0 La0 Si0")
	#testComposantPiano("Do0 Ré0 Mi0 Fa0 Sol0 La0 Si0")
	#testComposantClarinette("Mi0 Fa0 Sol0 La0 Si0")
	#testComposantDegres()
	#testComposantNotes()
	#testComposantComparaison("Mi0 Sol0 Si0 Ré1 Fa1")
	#testComposantSelection()
	#testComposantAffichage("Mi0 Sol0 Si0 Ré1 Fa1")
	testComposantQCM("Sol", "Bartok")
