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

try:
	import pygame
except:
		print "Erreur d'importation du module Pygame !"

#------------------------------------------------------------------------------

def iniPygameMixer():
	try:
		pygame.mixer.pre_init(44100,-16,1,1024*4)
		pygame.mixer.init()
		nbr = pygame.mixer.get_num_channels()
		print "Module Pygame initialise : %s canaux disponibles" %(nbr)
	except:
		print "Erreur d'initialisation du module Pygame !"

def delPygameMixer():
	try:
		pygame.mixer.quit()
		print "Pygame desactive : OK !"
	except:
		print "Pygame desactive : erreur !"	

#------------------------------------------------------------------------------

def jouerEchantillonsMIX(lisFIC, maxTPS=1000, wait=True):
	"""
	Methode permettant de jouer le mixage de plusieurs echantillons references 
	par leurs noms (fichier)

	@param lisFIC: liste des noms des echantillons
	"""
	try:
		lisSON = map(lambda e: pygame.mixer.Sound(e), lisFIC)
		for son in lisSON:
			son.play(0, maxTPS)
		if wait:
			while pygame.mixer.get_busy():
				pass
		for son in lisSON:
			del son
	except:
		print "Erreur de lecture des sons suivants : %s" %(str(lisFIC))

def jouerEchantillonsSEQ(lisFIC, maxTPS=1000):
	"""
	Methode permettant de jouer sequentiellement plusieurs echantillons 
	references par leurs noms (fichier)

	@param lisFIC: liste des noms des echantillons
	"""
	try:
		lisSON = map(lambda e: pygame.mixer.Sound(e), lisFIC)
		for son in lisSON:
			son.play(0, maxTPS)
			while pygame.mixer.get_busy():
				pass
		for son in lisSON:
			del son
	except:
		print "Erreur de lecture des sons suivants : %s" %(str(lisFIC))


#------------------------------------------------------------------------------

def formater(val):
	"""
	Methode permettant de definir automatique le nom du fichier son a partir de
	sa valeur : 15 => ogg/not_15.ogg
	"""
	return 'ogg/not_%d.ogg' %(val)

def transformerNotes(lisSON, dec=True):
	"""
	Les fichiers ogg des notes representent deux octaves completes de Do a 	Do.
	Les noms des fichiers ogg associes aux notes commencent a 12 (1ere octave).
	On recherche le minimum des octaves sur la liste de sons et on la ramene a
	la premiere octave (decalage des valeurs). Les noms des fichiers peuvent
	ensuite etre definis a partir de la valeur du son.
	"""
	if dec:
		lisOCT = map(lambda e: e.getOctave(), lisSON)
		difOCT = min(lisOCT) - 1
		if difOCT <> 0:
			dec = -difOCT * 12
			for son in lisSON:
				son.decaler(dec)
	lisSON = map(lambda e: e.getValeur(), lisSON)
	lisSON = map(lambda e: formater(e), lisSON)
	return lisSON

#------------------------------------------------------------------------------

def jouerNotesMIX(lisSON, maxTPS=1000, dec=True, wait=True):
	lisVAL = transformerNotes(lisSON, dec)
	jouerEchantillonsMIX(lisVAL, maxTPS, wait)

def jouerNotesSEQ(lisSON, maxTPS=1000, dec=True):
	lisVAL = transformerNotes(lisSON, dec)
	jouerEchantillonsSEQ(lisVAL, maxTPS)
