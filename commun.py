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

import time

import pygtk
import gtk
import pango

import modele

#------------------------------------------------------------------------------

import logging
import logging.handlers

#LOG_FILENAME = "./theorìe.logs.txt"
#logger = logging.getLogger('MyLogger')
#logger.setLevel(logging.DEBUG)
#handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=50000, backupCount=5)
#logger.addHandler(handler)

#------------------------------------------------------------------------------

TXT_FNT_REF = "Arial 12 Bold"

#------------------------------------------------------------------------------

TXT_TIT_APP = _("Musical theory - Musical instruments")

TXT_CMP_MOD = _("Comparison mode")
TXT_CMP_QUI = _("Compared to")

TXT_CMP_GAM = _("scales")
TXT_CMP_ACC = _("chords")
TXT_CMP_INF = _("contained")
TXT_CMP_EGA = _("equal")
TXT_CMP_SUP = _("contains")

TXT_GAM = _("Scale")
TXT_ACC = _("Chord")
TXT_TON = _("Key")
TXT_FND = _("Root")
TXT_MOD = _("Mode")
TXT_REN = _("Inversion")
TXT_REL = _("Parallel")
TXT_NOT = _("Tones")
TXT_INT = _("Intervals")

TXT_TYP_TON = _("Tonality")
TXT_TYP_INS = _("Instrument")
TXT_TYP_GUI = _("Tuning")
TXT_TYP_NBC = _("Cases")
TXT_TYP_DGT = _("Fingering")
TXT_TIT_TEN = _("Tension")

TXT_TIT_CMP = _("To compare")
TXT_TIT_NOT = _("Tone")
TXT_TIT_DEG = _("Degrees")

TXT_LIS_NOT = _("Tones list")
TXT_ENS_NOT = _("Tones set")

TXT_ONG_THE = _("Theory")
TXT_ONG_INS = _("Instruments")

TXT_ONG_QUA = _("Quadrant")
TXT_ONG_CMP = _("Comparisons")
TXT_ONG_REC = _("Ear training")
TXT_ONG_ECO = _("Playing")

TXT_ONG_PIA = _("Piano")
TXT_ONG_HAR = _("Harmonica")
TXT_ONG_FLU = _("Recorder")
TXT_ONG_GUI = _("Guitar")
TXT_ONG_CLA = _("Clarinet")

TXT_ONG_GAM = _("Scales")
TXT_ONG_ACC = _("Chords")
TXT_ONG_NOT = _("Tones")

TXT_OCT_PRM = _("First octave")
TXT_OCT_NBR = _("Number of octaves")

TXT_DGT_4E6 = _("4 tones, 6 cases")
TXT_DGT_3E5 = _("3 tones, 5 cases")
TXT_DGT_EGG = _("left, left")
TXT_DGT_EGD = _("left, right")

TXT_DEG_OCT = _("Octave")
TXT_DEG_UNI = _("Unison")

TXT_ABR_OCT = _("Oct.")
TXT_CHX_NOM = _("the names")
TXT_CHX_EDT = _("in half tones")

TXT_HAR_SOU = _("Blo")
TXT_HAR_ASP = _("Asp")

TXT_REC_LIS = _("Listen")
TXT_REC_INT = _("Intervals recognition")
TXT_REC_NOT = _("Notes recognition")
TXT_REC_LII = _("Listen to this interval and try to identify it")
TXT_REC_LNI = _("Listen to this note and try to identify it")

TXT_REC_SUC = _("Try number %d : good, this is a %s indeed !")
TXT_REC_ERR = _("Try number %d : error, this is not a %s !")

#------------------------------------------------------------------------------

ESPACE = 4

def definirButton(txt):
	obj = gtk.Button(txt)
	obj.show()
	return obj

def definirArrow(sens):
	obj = gtk.Arrow(sens, gtk.SHADOW_ETCHED_IN)
	return obj

def definirToggleButton(txt):
	obj = gtk.ToggleButton(txt)
	obj.show()
	return obj

def definirCheckButton(txt):
	obj = gtk.CheckButton(txt, True)
	obj.show()
	return obj

def definirCombo(lis):
	obj = gtk.combo_box_new_text()
	for elt in lis:
		obj.append_text(elt)
	obj.set_active(0)
	obj.show()
	return obj
	
def definirLabel(nom):
	obj = gtk.Label(nom)
	obj.show()
	return obj

def definirVSeparator():
	obj = gtk.VSeparator()
	obj.show()
	return obj

def definirHSeparator():
	obj = gtk.HSeparator()
	obj.show()
	return obj

def definirLabelCombo(nom, lis):
	label = definirLabel(nom + " ")
	combo = definirCombo(lis)
	return label, combo

def definirROW(lab, rnd, typ, pos):
	tvc = gtk.TreeViewColumn(lab)
	tvc.pack_start(rnd, True)
	tvc.add_attribute(rnd, typ, pos)
	return tvc

def definirFrame(tit, elt):
	obj = gtk.Frame(tit)
	if elt != None:
		obj.add(elt)
	obj.set_border_width(ESPACE)
	obj.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
	obj.set_label_align(0.0,0.5)
	obj.show()
	return obj

def definirScrolledWindow(elt, viewport = None, xpa = gtk.POLICY_AUTOMATIC, ypa = gtk.POLICY_AUTOMATIC):
	obj = gtk.ScrolledWindow()
	if viewport == None:
		obj.add(elt)
	else:
		obj.add_with_viewport(elt)
	obj.set_policy(xpa, ypa)
	obj.show()
	return obj

def definirNotebook(posTIT, lisNOM, lisOBJ, pagSEL):
	pcd = pango.FontDescription(TXT_FNT_REF)
	obj = gtk.Notebook()
	obj.set_scrollable(True)
	obj.set_show_tabs(True)
	obj.set_show_border(True)
	obj.set_tab_pos(posTIT)
	for ind in range(len(lisNOM)):
		nom = lisNOM[ind]
		val = lisOBJ[ind]
		lab = gtk.Label(nom)
		lab.modify_font(pcd)
		obj.append_page(val, lab)
	obj.set_current_page(pagSEL)
	obj.show()
	return obj

def definirHBOX(lis, expand = True, fill = True):
	obj = gtk.HBox(False, ESPACE)
	for elt in lis:
		obj.pack_start(elt, expand, fill, ESPACE)
	obj.show()
	return obj

def definirVBOX(lis, expand = True, fill = True):
	obj = gtk.VBox(False, ESPACE)
	for elt in lis:
		obj.pack_start(elt, expand, fill, ESPACE)
	obj.show()
	return obj

def definirHPANED(haut, bas):
	obj = gtk.HPaned()
	obj.add1(haut)
	obj.add2(bas)
	obj.show()
	return obj

def definirVPANED(haut, bas):
	obj = gtk.VPaned()
	obj.add1(haut)
	obj.add2(bas)
	obj.show()
	return obj

def definirTOOLBAR(lis):
	tlb = gtk.Toolbar()
	tlb.set_show_arrow(True)
	tlb.set_orientation(gtk.ORIENTATION_HORIZONTAL)
	tlb.set_border_width(ESPACE)
	for elt in lis:
		if elt != "":
			tlb.append_widget(elt, "", "private")
		else:
			tlb.append_space()
	tlb.show()
	return tlb

#------------------------------------------------------------------------------

def disconnectEVENT(widget, handle):
	try:
		widget.disconnect(handle)
	except:
		pass

#------------------------------------------------------------------------------

def formater(deb, sep, fin, lis):
	txt = str(deb) + str(lis[0])
	lis = lis[1:]
	for elt in lis:
		txt += str(sep) + str(elt)
	txt += fin
	return txt

def ajouterNotes(ens, vpo, vno):
	ens = modele.Ensemble("", ens.getListe())
	nbr = len(ens)
	if nbr > 0:
		dec = modele.NOMBRE_NOTES_OCTAVE
		for voc in range(vno-1):
			for ind in range(nbr):
				elt = modele.Son(ens.getListe()[ind])
				elt.decaler(dec)
				ens.ajouter(elt)
			dec += modele.NOMBRE_NOTES_OCTAVE
		elt = modele.Son(ens.getListe()[0])
		elt.decaler(dec)
		ens.ajouter(elt)
		ens.decaler(vpo*modele.NOMBRE_NOTES_OCTAVE)
	return ens

#------------------------------------------------------------------------------

def tracer(classe, methode, message=""):
	temps = time.strftime("%H:%M:%S")
	mesg = "%s : %s.%s() : %s" %(temps, classe, methode, message)
	#logger.debug(mesg)
	print mesg
