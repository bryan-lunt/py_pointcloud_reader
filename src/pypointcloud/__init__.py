#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as _np
import re as _re
_entry_finder = _re.compile("^# ([^ ]+) = (.*)$")

def read_vpc(infile):
    headers = dict()
    data = None
    other_data = list()

    headline = infile.readline()
    while(headline != None):
        amatch = _entry_finder.match(headline)
        if amatch is not None:
            match_key, val_string = amatch.groups()
            headers[match_key] = val_string

        if (not headline.startswith("#")):
            infile.seek(infile.tell() - len(headline))
            break
        headline = infile.readline()


    headers["cohort_names"] = map(lambda x: x[1:-1], headers["cohort_names"][1:-1].split(","))
    headers["cohort_times"] = map(float, headers["cohort_times"][1:-1].split(","))
    headers["srclist"] = map(lambda x:x[1:-1], headers["srclist"][1:-1].split(","))
    headers["embryospergene"] = map(lambda x: map(int, x.split(",")), headers["embryospergene"][1:-1].split(";"))

    headers["column_info"] = map(lambda x: tuple(map(lambda y: y[1:-1], x.split(","))), headers["column_info"][1:-1].split(";"))

    headers["column"] = map(lambda x:x[1:-1],headers["column"][1:-1].split(","))
    n_cols = len(headers["column"])
    headers["nuclear_count"] = int(headers["nuclear_count"])


    data = _np.zeros((headers["nuclear_count"],len(headers["column"])-1))

    headline = infile.readline().strip()
    while(headline):
        foo = map(float, headline.split(","))
        data[int(foo[0])-1, : ] = foo[1:n_cols]
        other_data.append(foo[n_cols:])
        headline = infile.readline().strip()

    
    return (headers, data, other_data)
