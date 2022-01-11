#   wye
#   tee, but produces graphs via matplotlib
#   Copyright (C) 2021 Evan Berkowitz
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
from wye.style import style

class _Queue:
    
    def __init__(self, maxSize=float('Inf')):
        self.data=[]
        self.maxSize = maxSize
        if self.maxSize <= 0:
            self.maxSize = float('Inf')
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, key):
        return self.data[key]
    
    def put(self, item):
        self.data.append(item)
        if(len(self.data) > self.maxSize):
            self.data = self.data[-self.maxSize:]
    
    append = put
    
    def __iter__(self):
        return self.data.__iter__()

class Artist:

    def __init__(self, ax, args, data):
        self.ax = ax
        
        parser = argparse.ArgumentParser(allow_abbrev=False)
        
        parser.add_argument(f'--{data}', type=int, nargs='+', default=[0])
        parser.add_argument('--color', type=str, nargs='+', default=style['colors'])
        parser.add_argument('--linestyle', type=str, nargs='*', default=[style['linestyle']])
        
        parser.add_argument('--xscale', default='linear')
        parser.add_argument('--yscale', default='linear')
        
        parser.add_argument('--xlabel', type=str, default='')
        parser.add_argument('--ylabel', type=str, default='')
        parser.add_argument('--title', type=str, default='')
        
        parser.add_argument('--hline', type=float, nargs='*', default=[])
        parser.add_argument('--hspan', type=float, nargs=2)
        parser.add_argument('--vline', type=float, nargs='*', default=[])
        parser.add_argument('--vspan', type=float, nargs=2)

        parser.add_argument('--last',  type=int, default=0)
        
        self.args, _ = parser.parse_known_args(args)
        
        ax.set_xscale(self.args.xscale)
        ax.set_yscale(self.args.yscale)
        ax.set_xlabel(self.args.xlabel)
        ax.set_ylabel(self.args.ylabel)
        ax.set_title(self.args.title)
        
        for h in self.args.hline:
            self.ax.axhline(h, color='black')
        for v in self.args.vline:
            self.ax.axvline(v, color='black')
        if self.args.hspan:
            self.ax.axhspan(self.args.hspan[0], self.args.hspan[1], color='gray', alpha=0.25)
        if self.args.vspan:
            ax.axvspan(self.args.vspan[0], self.args.vspan[1], color='gray', alpha=0.25)
        
        self.data = {label: _Queue(self.args.last) for label in vars(self.args)[data]}
    
    def update_data(self, i, fields):
        for f in self.data:
            self.data[f].append(float(fields[f]))
    
    def update_figure(self, ):
        self.ax.relim()
        self.ax.autoscale_view()
    
    def clear_data(self, ):
        for f in self.data:
            self.data[f] = _Queue(self.args.last)
        self.x = []

