#!/usr/bin/env python

surf_111_2x2 = {'H':'ontop','O':'fcc','C':'fcc','N':'fcc',
                'CH':'fcc', 'NH': 'fcc','OH':'bridge','OOH':'fcc',
               'CH2':'bridge', 'NH2': 'bridge', 'OH2': 'fcc',
               'CH3':'ontop', 'NH3':'fcc'} #2x2

surf_111_3x3 = { 'O':'fcc','C':'fcc', 'N':'fcc', 'H':'ontop',
                'CH':'fcc', 'NH': 'fcc', 'OH':'bridge','OOH':'fcc',
                'CH2':'bridge', 'NH2': 'bridge', 'OH2': 'ontop',
                'NH3':'ontop','CH3':'ontop'} # 3x3

surf_111_root3 = {'C':'bridge', 'CH':'bridge', 'O':'ontop', 'N':'bridge',
                  'CH2':'bridge','H':'ontop', 'NH3':'ontop', 'NH2':'bridge',
                  'OH2':'bridge', 'NH':'bridge',
                  'OH':'bridge', 'OOH':'bridge', 'CH3':'fcc'}

surf_100_3x3 = {'C':'hollow', 'H':'bridge','N':'bridge','O':'bridge', #3x3
                'CH':'hollow', 'NH': 'hollow','OH':'bridge','OOH':'hollow',
                'CH2':'bridge', 'NH2': 'bridge', 'OH2': 'ontop',
                'CH3':'ontop', 'NH3':'ontop'}

surf_100_2x2 = {'C':'hollow', 'N':'hollow', 'H':'bridge','O':'bridge', #2x2
                'CH':'hollow', 'NH': 'hollow','OH':'bridge','OOH':'hollow',
                'CH2':'bridge', 'NH2': 'bridge', 'OH2': 'ontop',
                'CH3':'ontop', 'NH3':'ontop'}

all_surf = {'111_3x3':surf_111_3x3, '111_2x2':surf_111_2x2,
            '111_1x1':surf_111_root3, '100_3x3':surf_100_3x3,
            '100_2x2':surf_100_2x2}
