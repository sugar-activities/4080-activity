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
from modele_data import *
from commun import *

import canvas_quadrant

#------------------------------------------------------------------------------

class ComposantQuadrant:
	
	#----------------------------------------------------------------------
	
	def getNom(self):
		return TXT_ONG_QUA
	
	def getContainer(self):
		return self.container

	def update(self, ens):
		tracer("ComposantQuadrant", "update")
		ens = Ensemble("", ens)
		if self.ens == None or ens != self.ens:
			self.ens = ens
			self.canvas.setNotes(self.ens)

	#----------------------------------------------------------------------

	def __init__(self, notes):
		tracer("ComposantQuadrant", "__init__")
		self.ens = None
		self.canvas = canvas_quadrant.CanvasQuadrant()
		self.container = definirVBOX([self.canvas])
		self.update(notes)
