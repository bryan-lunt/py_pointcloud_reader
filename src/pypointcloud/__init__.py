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

def _parse_header(header_string,header_type="plain",dtype=str):
	"""Type one of "plain", "list", or "listlist".
	"""
	header_string = header_string.strip()
	if header_type == "plain":
		return dtype(header_string.strip().strip('"'))

	if header_type.startswith("list") and header_string.startswith("[") and header_string.endswith("]"):
		header_string = header_string[1:-1]
		#A list type
	if header_type == "list":
		return map(dtype,map(lambda x:x.strip().strip('"'), header_string.split(",")))
	elif header_type == "listlist":
		return [map(dtype,map(lambda x:x.strip().strip('"'), i.split(","))) for i in header_string.split(";")]
	raise Exception("Invalid header_type?")	

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


    headers["cohort_names"] = _parse_header(headers["cohort_names"],"list",str)
    headers["cohort_times"] = _parse_header(headers["cohort_times"],"list",float)
    headers["srclist"] = _parse_header(headers["srclist"],"list",str)
    headers["embryospergene"] = _parse_header(headers["embryospergene"],"listlist",int)

    headers["column_info"] = _parse_header(headers["column_info"],"listlist")

    headers["column"] = _parse_header(headers["column"],"list",str)
    n_cols = len(headers["column"])
    headers["nuclear_count"] = _parse_header(headers["nuclear_count"],"plain",int)


    data = _np.zeros((headers["nuclear_count"],len(headers["column"])-1))

    headline = infile.readline().strip()
    while(headline):
        foo = map(float, headline.split(","))
        data[int(foo[0])-1, : ] = foo[1:n_cols]
        other_data.append(foo[n_cols:])
        headline = infile.readline().strip()

    
    return (headers, data, other_data)
