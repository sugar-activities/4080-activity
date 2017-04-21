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

from modele import *
from commun import *
from canvas_flute import *
from canvas_guitare import *
from canvas_harmonica import *
from canvas_piano import *
from canvas_clarinette import *
from canvas_quadrant import *

#------------------------------------------------------------------------------

c_lar = 640
c_hau = 340

def testCanvasFlute(tonalite, notes, lar=c_lar, hau=c_hau):
	window = gtk.Window()
	inst = modele.Flute(tonalite)
	canv = CanvasFlute(inst, lar, hau, notes)
	window.add(canv)
	#window.fullscreen()
	window.connect("destroy", gtk.main_quit)
	window.show_all()
	gtk.main()
	
def testCanvasGuitare(cases, accordage, notes, lar=c_lar, hau=c_hau):
	window = gtk.Window()
	inst = modele.Guitare(cases, accordage)
	canv = CanvasGuitare(inst, lar, hau, notes)
	canv.setDoigte([0,0,0,0,0,0])
	window.add(canv)
	#window.fullscreen()
	window.connect("destroy", gtk.main_quit)
	window.show_all()
	gtk.main()

def testCanvasHarmonica(notes, lar=c_lar, hau=c_hau):
	window = gtk.Window()
	inst = modele.HarmonicaCHR()
	canv = CanvasHarmonica(inst, lar, hau, notes)
	window.add(canv)
	#window.fullscreen()
	window.connect("destroy", gtk.main_quit)
	window.show_all()
	gtk.main()

def testCanvasPiano(notes, lar=c_lar, hau=c_hau):
	window = gtk.Window()
	canv = CanvasPiano(lar, hau, notes)
	window.add(canv)
	#window.fullscreen()
	window.connect("destroy", gtk.main_quit)
	window.show_all()
	gtk.main()

def testCanvasClarinette(notes, lar=c_lar, hau=c_hau):
	window = gtk.Window()
	inst = modele.Clarinette()
	canv = CanvasClarinette(inst, lar, hau, notes)
	window.add(canv)
	#window.fullscreen()
	window.connect("destroy", gtk.main_quit)
	window.show_all()
	gtk.main()

def testCanvasQuadrant(notes, lar=c_lar, hau=c_hau):
	window = gtk.Window()
	canv = CanvasQuadrant(lar, hau, notes)
	window.add(canv)
	#window.fullscreen()
	window.connect("destroy", gtk.main_quit)
	window.show_all()
	gtk.main()

def testCanvasGuitarePiano(cases, accordage, notes, lar=c_lar, hau=c_hau):
	window = gtk.Window()
	inst = modele.Guitare(cases, accordage)
	cnv1 = CanvasGuitare(inst, lar, 3*hau/4, notes)
	cnv1.setDoigte([0,0,0,0,0,0])
	ens = Ensemble("", notes)
	ens = ajouterNotes(ens, 1, 2)
	cnv2 = CanvasPiano(lar, hau/4, ens)
	obj = definirVPANED(cnv1,cnv2)
	window.add(obj)
	#window.fullscreen()
	window.connect("destroy", gtk.main_quit)
	window.show_all()
	gtk.main()

def testCanvasGuitareHarmonica(cases, accordage, notes, lar=c_lar, hau=c_hau):
	window = gtk.Window()
	inst = modele.Guitare(cases, accordage)
	cnv1 = CanvasGuitare(inst, lar, hau/2, notes)
	cnv1.setDoigte([0,0,0,0,0,0])
	inst = modele.HarmonicaCHR()
	ens = Ensemble("", notes)
	ens = ajouterNotes(ens, 0, 3)
	ens.decaler(-12)
	cnv2 = CanvasHarmonica(inst, lar, hau/2, ens)
	obj = definirVPANED(cnv1,cnv2)
	window.add(obj)
	#window.fullscreen()
	window.connect("destroy", gtk.main_quit)
	window.show_all()
	gtk.main()

#------------------------------------------------------------------------------

if __name__ == "__main__":
	SET_AFF(MOD_NOT)
	SET_CMP(MOD_OCT)
	notes = "Sol0 La0 Si0 Do#1 Ré1 Mi1 Fa#1" 
	testCanvasFlute("Do", notes)
	testCanvasGuitare(19, [4,9,14,19,23,28], notes)
	testCanvasHarmonica(notes)
	testCanvasPiano(notes)
	testCanvasClarinette(notes)
	testCanvasGuitarePiano(19, [4,9,14,19,23,28], notes)
	testCanvasGuitareHarmonica(19, [4,9,14,19,23,28], notes)
	testCanvasQuadrant(notes)
