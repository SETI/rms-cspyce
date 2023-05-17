################################################################################
# Usage: python make_vectorize_i.py
#
# This progrmm generates file vectorize.i by creating a macro that defines the
# inline code for the signature of each SWIG interface to a CSPICE function.
#
# The generated file consists of the following:
#
# 1. An exact copy of the file vectorize_header.text
# 2. A sequence of SWIG macro defintions, one for any VECTOR_ macro found in the
#    file cspyce0.i.  This program looks for VECTOR_ at the start of line, and
#    treats everything up to the initial parenthesis as the name of the macro.
#    Each macro name defines a sequence of input arguments followed by a
#    sequence of output arguments.
#
# This program interprets the name of the macro and defines a SWIG inline
# function that handles that sequence of arguments.
################################################################################

from __future__ import annotations

import os
import re
from collections import Counter
from dataclasses import dataclass


class Indent:
    spaces: int

    def __init__(self, spaces):
        self.spaces = spaces

    def __str__(self):
        return ' ' * self.spaces

    def __enter__(self):
        self.spaces += 4

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.spaces -= 4


@dataclass
class Arg:
    key: str
    has_variable_multi_dimensions: bool = False

    def __post_init__(self):
        if self.key[0] in 'de' and len(self.key) > 1:
            if not (self.key[1:].islower() or self.key[1:].isupper()):
                raise ValueError(f'Unexpected mixed case key "{self.key}"')
            self.has_variable_multi_dimensions = self.key[1:].islower()


class InArg(Arg):
    name: str
    rank: int
    dim_names: list[str]

    def expand_key(self, counter, ijkdict, fullname):
        lookup_key = (self.key[0], len(self.key))
        counter[lookup_key] += 1
        my_id = counter[lookup_key]
        if self.key == 's':
            self.name = f'str{my_id}'
            self.rank = 0
        elif self.key == 'i':
            self.name = f'k{my_id}'
            self.rank = 0
        elif self.key == 'b':
            self.name = f'b{my_id}'
            self.rank = 0
        elif self.key[0] in 'de':
            self.name = f'in{len(self.key)}{my_id}'
            self.rank = len(self.key)
            self.dim_names = [f'{self.name}_dim{i + 1}' for i in range(self.rank)]
            if self.has_variable_multi_dimensions:
                for k in range(1, self.rank):
                    ijkdict[self.key[k]] = self.dim_names[k]
        else:
            raise ValueError('Unrecognized input arg in ' + fullname)

    def get_declaration(self):
        if self.key == 's':
            return 'ConstSpiceChar *' + self.name
        elif self.key == 'i':
            return 'SpiceInt ' + self.name
        elif self.key == 'b':
            return 'SpiceBoolean ' + self.name
        else:
            my_type = "ConstSpiceDouble *" if self.key[0] == 'd' else "SpiceDouble *"
            main_declaration = f'{my_type}{self.name}'
            dim_declarations = [f'int {dim}' for dim in self.dim_names]
            return ', '.join((main_declaration, *dim_declarations))

    def get_call(self, sizer_count):
        if self.rank == 0:
            return self.name

        if sizer_count == 1:
            indexer = 'i'
        else:
            indexer = f'i % {self.dim_names[0]}'

        if self.rank == 1:
            result = f'{self.name}[{indexer}]'
        else:
            multiplicands = [f'({indexer})', *self.dim_names[1:]]
            result = f'{self.name} + {" * ".join(multiplicands)}'
            if self.has_variable_multi_dimensions:
                result = ', '.join((result, *self.dim_names[1:]))

        return result


class OutArg(Arg):
    name: str
    rank: int
    dim_names: list[str]
    dim_values: list[str]

    def expand_key(self, counter, ijkdict, fullname):
        lookup_key = (self.key[0], len(self.key))
        counter[lookup_key] += 1
        my_id = counter[lookup_key]
        if self.key == 'i':
            self.name = f'int{my_id}'
            self.rank = 1
            self.dim_names = [f'{self.name}_dim1']
            self.dim_values = ['maxdim']
        elif self.key == 'b':
            self.name = f'bool{my_id}'
            self.rank = 1
            self.dim_names = [f'{self.name}_dim1']
            self.dim_values = ['maxdim']
        elif self.key[0] == 'd':
            self.name = f'out{len(self.key)}{counter[lookup_key]}'
            self.rank = len(self.key)
            self.dim_names = [f'{self.name}_dim{k}' for k in range(1, self.rank + 1)]
            size_args = list(self.key[1:])
            if self.has_variable_multi_dimensions:
                size_args = [ijkdict[letter] for letter in size_args]
            self.dim_values = ['maxdim', *size_args]
        else:
            raise ValueError('Unrecognized input arg in ' + fullname)

    def get_declaration(self):
        my_type = dict(i='SpiceInt', b='SpiceBoolean').get(self.key, 'SpiceDouble')
        main_declaration = f'{my_type} **{self.name}'
        dims_declarations = [f'int *{name}' for name in self.dim_names]
        return ', '.join((main_declaration, *dims_declarations))

    def get_malloc(self):
        if self.key == 'i':
            return 'SpiceInt', 'size'
        elif self.key == 'b':
            return 'SpiceBoolean', 'size'
        else:
            return 'SpiceDouble', ' * '.join(['size', *self.dim_values[1:]])

    def get_call(self, _sizer_count):
        multiplier = ' * '.join(['i', *self.dim_values[1:]])
        buffer_arg = f'{self.name}_buffer + {multiplier}'
        if self.has_variable_multi_dimensions:
            return ', '.join([buffer_arg,  *self.dim_names[1:]])
        else:
            return buffer_arg


class MacroGenerator:
    def __init__(self, fullname, file):
        if not fullname.startswith('VECTORIZE_'):
            raise ValueError('Invalid name: ' + fullname)
        argstring = fullname[len('VECTORIZE_'):]
        inarg_keys, outarg_keys, use_return = self.parse_argstring(argstring)

        ijkdict = {}  # Maps lowercase indices (i,j,k) to input argument names
        in_counter = Counter()
        out_counter = Counter()

        inargs = [InArg(key) for key in inarg_keys]
        outargs = [OutArg(key) for key in outarg_keys]
        for arg in inargs:
            arg.expand_key(in_counter, ijkdict, fullname)
        for arg in outargs:
            arg.expand_key(out_counter, ijkdict, fullname)

        self.fullname = fullname
        self.file = file
        self.inargs = inargs
        self.outargs = outargs
        self.use_return = use_return
        self.indent = Indent(0)

    def out(self, string=""):
        if not string:
            self.file.write("\n")
        else:
            self.file.write(str(self.indent) + string + "\n")

    @staticmethod
    def parse_argstring(argstring):
        (inarg_string, outarg_string) = argstring.split('__')
        # Extract a RETURN indicator
        use_return = outarg_string.startswith('RETURN')
        if use_return:
            outarg_string = outarg_string[len('RETURN_')]
        # Replace '2d' with 'd','d', etc.
        arg_keys = []
        for arg_string in (inarg_string, outarg_string):
            parts = arg_string.split('_')
            parsed = []
            for part in parts:
                if part[0] in '23456789':
                    count = int(part[0])
                    part = part[1:]
                    parsed += count * [part]
                else:
                    parsed.append(part)

            arg_keys.append(parsed)
        (inarg_keys, outarg_keys) = arg_keys
        return inarg_keys, outarg_keys, use_return

    def generate_code(self):
        out = self.out
        out()
        letters = self.__get_out_letters()
        out(f'%define {self.fullname}({", ".join(["NAME", "FUNC", *letters])})\n')
        out('%apply (void RETURN_VOID) {void NAME ## _vector};\n')
        out('%inline %{')
        with self.indent:
            out('void NAME ## _vector(')
            with self.indent:
                all_args = [*self.inargs, *self.outargs]
                for k, arg in enumerate(all_args):
                    suffix = ') {' if k == len(all_args) - 1 else ','
                    out(f'{arg.get_declaration()}{suffix}')
            with self.indent:
                self.write_body()

            out("}")
        out('%}\n')
        out('%enddef\n')
        out('/' + 78 * '*' + '/')

    def write_body(self):
        out = self.out

        # Get maximum leading dimensions
        self.get_maxdim_and_size()
        # Set all ouput vars to the values they'll have if allocation fails.
        self.generate_initialize_output_vars()
        # Allocate output arrays
        self.generate_output_buffer_allocation()
        # Loop through values
        out('for (int i = 0; i < size; i++) {')
        with self.indent:
            self.generate_cspice_call()
        # End of loop
        out('}')
        # And we're done.

    def get_maxdim_and_size(self):
        out = self.out
        sizers = [arg.dim_names[0] for arg in self.inargs if arg.rank > 0]
        out(f'int maxdim = {sizers[0]};')
        for sizer in sizers[1:]:
            out(f'if (maxdim < {sizer}) maxdim = {sizer};')
        out()
        out(f'int size = (maxdim == 0 ? 1 : maxdim);')
        for sizer in sizers:
            out(f'{sizer} = ({sizer} == 0 ? 1 : {sizer});')
        out()

    def generate_initialize_output_vars(self):
        for arg in self.outargs:
            initialize_dimensions = [f'*{name} = {value};'
                                     for name, value in zip(arg.dim_names, arg.dim_values)]
            self.out(' '.join(initialize_dimensions))
        self.out()

    def generate_output_buffer_allocation(self):
        out = self.out
        last_name = None
        for arg in self.outargs:
            type, count = arg.get_malloc()
            name = arg.name
            if not last_name:
                out(f'{type} *{name}_buffer = ({type} *)PyMem_Malloc({count} * sizeof({type}));')
            else:
                out(f'{type} *{name}_buffer = {last_name}_buffer ? ({type} *)PyMem_Malloc({count} * sizeof({type})) : NULL;')
            last_name = name
        for arg in self.outargs:
            out(f'*{arg.name} = {arg.name}_buffer;')
        # Handle an error
        out(f'if (!{last_name}_buffer) {{')
        with self.indent:
            out('handle_malloc_failure("NAME" "_vector");')
            out('return;')
        out('}')
        out()

    def generate_cspice_call(self):
        out = self.out
        if self.use_return:
            out(f'{self.outargs[0].name}_buffer[i] = FUNC(')
        else:
            out(f'FUNC(')
        # Insert input arguments into function
        funcargs = [*self.inargs, *self.outargs] if not self.use_return else self.inargs
        sizer_count = sum(arg.rank > 0 for arg in self.inargs)
        with self.indent:
            for k, arg in enumerate(funcargs):
                suffix = ',' if k < len(funcargs) - 1 else ");"
                out(f'{arg.get_call(sizer_count)}{suffix}')

    def __get_out_letters(self):
        out_letters = []
        for arg in self.outargs:
            for c in arg.key[1:]:
                if c in 'IJKLMN':
                    out_letters.append(c)
        if out_letters != sorted(out_letters):
            raise ValueError(f'Out letters in {self.fullname} are not sorted.  ')
        return out_letters


HEADER = """
/****************************************************************************************
* cspyce0/vectorize.i
*
* This file is automatically generated by program make_vectorize.py. Do not modify.
* To regenerate:
*     python make_vectorize.py
*
* See make_vectorize.py for more information.
*/
"""


APPLY_TEMPLATE_LINES = [
    "%apply (ConstSpiceDouble *IN_ARRAY01, int DIM1) {(ConstSpiceDouble *in1@, int in1@_dim1)};",
    "%apply (ConstSpiceDouble *IN_ARRAY12, int DIM1, int DIM2) {(ConstSpiceDouble *in2@, int in2@_dim1, int in2@_dim2)};",
    "%apply (ConstSpiceDouble *IN_ARRAY23, int DIM1, int DIM2, int DIM3) {(ConstSpiceDouble *in3@, int in3@_dim1, int in3@_dim2, int in3@_dim3)};",
    "%apply (SpiceDouble *IN_ARRAY01, int DIM1) {(SpiceDouble *in1@, int in1@_dim1)};",
    "%apply (SpiceDouble *IN_ARRAY12, int DIM1, int DIM2) {(SpiceDouble *in2@, int in2@_dim1, int in2@_dim2)};",
    "%apply (SpiceDouble *IN_ARRAY23, int DIM1, int DIM2, int DIM3) {(SpiceDouble *in3@, int in3@_dim1, int in3@_dim2, int in3@_dim3)};",
    "%apply (ConstSpiceChar *CONST_STRING) {(ConstSpiceChar *str@)};",
    "%apply (SpiceDouble **OUT_ARRAY01, int *SIZE1) {(SpiceDouble **out1@, int *out1@_dim1)};",
    "%apply (SpiceDouble **OUT_ARRAY12, int *SIZE1, int *SIZE2) {(SpiceDouble **out2@, int *out2@_dim1, int *out2@_dim2)};",
    "%apply (SpiceDouble **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3) {(SpiceDouble **out3@, int *out3@_dim1, int *out3@_dim2, int *out3@_dim3)};",
    "%apply (SpiceInt **OUT_ARRAY01, int *SIZE1) {(SpiceInt **int@, int *int@_dim1)};",
    "%apply (SpiceBoolean **OUT_ARRAY01, int *SIZE1) {(SpiceBoolean **bool@, int *bool@_dim1)};",
]


def create_vectorize_header_file(output_file, input_files=None):
    if input_files is None:
        directory = os.path.dirname(os.path.abspath(__file__))
        input_files = [os.path.join(directory, f) for f in os.listdir(directory)
                       if re.match(r'cspyce0.*\.i', f)]
        if not input_files:
            raise FileNotFoundError(f"No files matching pattern found in {directory}")

    # Print the header
    with open(output_file, 'w') as f:
        # Copy the header
        f.write(HEADER.lstrip())
        f.write('\n')

        # Generate the apply templates
        for line in APPLY_TEMPLATE_LINES:
            for i in range(1, 10):
                f.write(line.replace('@', str(i)) + "\n")
            f.write("\n")

        seen = set()
        for input_file in input_files:
            # Print a macro for each line starting with VECTORIZE found in the file
            with open(input_file) as g:
                for line in g:
                    if line.startswith("VECTORIZE"):
                        name = line[:line.index('(')]
                        if name not in seen:
                            MacroGenerator(name, f).generate_code()
                            seen.add(name)


if __name__ == '__main__':
    create_vectorize_header_file('vectorize.i')
