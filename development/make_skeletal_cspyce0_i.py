# Quick-and-dirty program to read the cspice *.c files and write a skeletal
# version of the associated .i file.

import os
ROOT = '/Users/Shared/NAIF/cspice-N0067/src/cspice/'
FILES = '/Users/mark/Desktop/CSPYCE-0067/support/'

f = open(FILES + 'N0066_cspyce0_implemented.txt')
old_funcs = {x.strip() for x in f.readlines()}
f.close()

f = open(FILES + 'N0067_names.txt')
new_funcs = {x.strip() for x in f.readlines()}
f.close()

new_funcs -= old_funcs
new_funcs = list(new_funcs)
new_funcs.sort()

# First pass includes failures in output; second pass doesn't
if not 'failures' in globals():
    failures = {}

for name in new_funcs:
    if name in failures:
        continue

    # Read the file
    filename = ROOT + name + '_c.c'
    if not os.path.exists(filename):
        print('/**** NOT FOUND: ' + filename + '****/\n')
        failures[name] = 'FILE NOT FOUND'
        continue

    f = open(filename)
    recs = f.readlines()
    f.close()

    # Begin header
    print('/' + 71 * '*')

    # Procedure description
    for rec in recs:
        if '-Procedure' in rec:
            print('* ' + rec.rstrip() + '\n*')
            break

    # Abstract
    for k,rec in enumerate(recs):
        if '-Abstract' in rec:
            for rec2 in recs[k:]:
                if '-Disclaimer' in rec2:
                    break
                print('* ' + rec2.strip())

    # Declaration
    for k,rec in enumerate(recs):
        if rec.startswith('*/'):
            break

    recs2 = recs[k+1:]
    for k,rec in enumerate(recs2):
        if not rec.strip():
            continue
        if '#include' in rec:
            continue
        if '#undef' in rec:
            continue
        break

    rec = recs2[k]
    assert '(' in rec
    parts = rec.strip().partition('(')
    return_type = parts[0].split()[0]

    # Declared function name and type
    print('* ' + parts[0].strip() + ' (')

    # Declaration of first argument
    rec = parts[2].strip()
    while (' [' in rec):        # remove spaces before dimensions
        rec = rec.replace(' [', '[')
    while (' ]' in rec):
        rec = rec.replace(' ]', ']')
    rec = rec.replace('[*', '[')
    print('*       ' + rec)

    if rec.endswith(')') or rec.endswith(','):
        rec = rec[:-1].rstrip()
    parts = rec.split()

    arglist_failure = False
    if parts == ['void'] or parts == []:
        arg_types = ['void']
        arg_names = []
        arg_stars = []
    elif len(parts) >= 2 and len(parts) <= 3:
        arg_types = [parts[0]]
        arg_names = [parts[-1]]
        arg_stars = [parts[1]] if len(parts) > 2 else ['']

        if arg_names[-1][0] == '*':
            arg_names[-1] = arg_names[-1][1:]
            arg_stars[-1] = '*'
    else:
        arglist_failure = True
        failures[name] = 'ARGUMENT LIST INTERPRETATION FAILURE'
        arg_types = []
        arg_names = []
        arg_stars = []

    # Declaration of subsequent arguments
    for rec in recs2[k+1:]:
        rec = rec.strip()
        if not rec:
            break

        while (' [' in rec):        # remove spaces before dimensions
            rec = rec.replace(' [', '[')
        while (' ]' in rec):
            rec = rec.replace(' ]', ']')
        rec = rec.replace('[*', '[')
        print('*       ' + rec)

        if rec.endswith(')') or rec.endswith(','):
            rec = rec[:-1].rstrip()

        if '(' in rec or ')' in rec:
            arglist_failure = True
        else:
            parts = rec.split()
            arg_types += [parts[0]]
            arg_names += [parts[-1]]
            arg_stars.append(parts[1] if len(parts) > 2 else '')

            if arg_names[-1][0] == '*':
                arg_names[-1] = arg_names[-1][1:]
                arg_stars[-1] = '*'

    any_floats = 'SpiceDouble' in arg_types
    any_cells = 'SpiceCell' in arg_types
    cell_count = 0
    cell_name = ''
    if any_cells:
        k = arg_types.index('SpiceCell')
        cell_name = arg_names[k]
        cell_count = len([a for a in arg_types if a == 'SpiceCell'])

    print('*')

    for k,rec in enumerate(recs2):
        if 'VARIABLE' in rec:
            break

    rec = rec.strip()
    rec = rec.replace('VARIABLE', 'Variable')
    rec = rec.replace('DESCRIPTION', 'Description')
    print('* -Brief_I/O\n*\n* ' + rec)

    window_found = False
    cell_is_output = False
    has_input = False
    has_inout = False
    has_output = False
    arg_io = {n.split('[')[0]:'?' for n in arg_names}
    for rec in recs2[k+1:]:
        rec = rec.strip()
        if not rec:
            break
        print('* ' + rec.strip())

        guess = rec.split()[0]
        if ' O ' in rec:
            has_output = True
            if guess in arg_io:
                arg_io[guess] = 'O'
        if ' I ' in rec:
            has_input = True
            if guess in arg_io:
                arg_io[guess] = 'I'
        if ' I-O ' in rec or ' I/O ' in rec:
            has_inout = True
            has_output = True
            if guess in arg_io:
                arg_io[guess] = 'I-O'

        if cell_name and rec.startswith(cell_name) and cell_count == 1:
            if 'window' in rec.lower():
                window_found = True
            if ' O ' in rec or ' I-O ' in rec:
                cell_is_output = True

    print(71*'*' + '/\n')

    # End of header

    if any_cells or arglist_failure:
        print('%rename (' + name + ') my_' + name + '_c;\n')
    else:
        print('%rename (' + name + ') ' + name + '_c;\n')

    if return_type == 'void':
        print('%apply (void RETURN_VOID) {void ' + name + '_c};')
    elif return_type == 'SpiceBoolean':
        print('%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean ' + name + '_c};')
    elif return_type == 'SpiceInt':
        print('%apply (SpiceInt RETURN_INT) {SpiceInt ' + name + '_c};')
    elif return_type == 'SpiceDouble':
        print('%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble ' + name + '_c};')
    else:
        print('//!!! No return declaration')

    for k, arg_name in enumerate(arg_names):
      arg_type = arg_types[k]
      arg_star = arg_stars[k]
      inout = arg_io[arg_name.split('[')[0]]
      if inout == '?':
        print('%apply () {};  // Attention needed for ' + arg_name)

      elif inout == 'I':
        if arg_star:
          if '[' in arg_name:
            print('%apply () {};  // Attention needed for ' + arg_name)
          elif arg_type == 'ConstSpiceChar':
            print('%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *' + arg_name + '};')
          elif arg_type == 'SpiceChar' and arg_stars[k]:
            print('%apply (SpiceChar *IN_STRING) {ConstSpiceChar *' + arg_name + '};')
          elif (k < len(arg_types) - 2
                and arg_types[k+1] == 'SpiceInt' and not arg_stars[k+1]
                and arg_types[k+2] == 'SpiceInt' and not arg_stars[k+2]):
            print('%apply (' + arg_type + ' *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2) {(' +
                  arg_type + '*' + arg_name + ', SpiceInt ' + arg_names[k+1] +
                                              ', SpiceInt ' + arg_names[k+2] + ')};')
          else:
            print('%apply () {};  // Attention needed for ' + arg_name)

        elif '][' in arg_name:
          if '[]' not in arg_name:
            print('%apply (' + arg_type + ' IN_ARRAY2[ANY][ANY]) {' + arg_type + ' ' + arg_name + '};')
          elif len(arg_name.split('[]')) == 1:
            if k > 0 and arg_types[k-1] == 'SpiceInt' and not arg_stars[k-1]:
              print('%apply (SpiceInt DIM1, ' + arg_type + 'IN_ARRAY2[ANY][ANY]) {(SpiceInt ' +
                    arg_names[k-1] + ', ' + arg_type + ' ' + arg_name.replace('[]','[1]') + ')};')
            else:
              print('%apply () {};  // Attention needed for ' + arg_name)

        elif '[' in arg_name:
          if '[]' in arg_name:
            print('%apply () {};  // Attention needed for ' + arg_name)
          else:
            print('%apply (' + arg_type + ' IN_ARRAY1[ANY]) {' + arg_type + ' ' + arg_name + '};')
        else:
            pass        # declaration not needed

      elif inout == 'O':
        if arg_star:
          if '[' in arg_name:
            print('// Attention needed for ' + arg_name)
          elif arg_type == 'SpiceChar':
            if k > 0 and arg_types[k-1] == 'SpiceInt' and not arg_stars[k-1]:
              print('%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY]) ' +
                    '{(SpiceInt ' + arg_names[k-1] + ', SpiceChar ' + arg_name + '[1024])};')
          elif k > 0 and arg_types[k-1] == 'SpiceInt' and not arg_stars[k-1]:
              print('%apply (SpiceInt DIM1, ' + arg_type + ' OUT_ARRAY1[ANY]) ' +
                    '{(SpiceInt ' + arg_names[k-1] + ', ' + arg_type + ' ' + arg_name + '[1024])};')

        elif '][' in arg_name:
          if '[]' not in arg_name:
            print('%apply (' + arg_type + ' OUT_ARRAY2[ANY][ANY]) {' + arg_type + ' ' + arg_name + '};')
          else:
            print('%apply () {};  // Attention needed for ' + arg_name)

        elif '[' in arg_name:
          if '[]' not in arg_name:
            print('%apply (' + arg_type + ' OUT_ARRAY1[ANY]) {' + arg_type + ' ' + arg_name + '};')
          else:
            print('%apply () {};  // Attention needed for ' + arg_name)

        elif arg_type == 'ConstSpiceChar':
            print('%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *' + arg_name + '};')
        elif arg_type == 'SpiceCell' and cell_is_output and cell_count == 1:
          if window_found:
            print('%apply (int OUT_ARRAY1[ANY], int *SIZE1) {(int ' + arg_name + '[1000], int *id_count)};')
          else:
            print('%apply (SpiceDouble OUT_ARRAY2[ANY][ANY], int *SIZE1) {(SpiceDouble ' + arg_name + '[1000][2], int *intervals)};')
        elif arg_type == 'ConstSpiceEllipse':
            print('%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble ' + arg_name + '[NELLIPSE]};')
        elif arg_type == 'ConstSpicePlane':
            print('%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble ' + arg_name + '[NPLANE]};')
        else:
            print('%apply () {};  // Attention needed for ' + arg_name)
      elif inout == 'I-O':
        if arg_type == 'SpiceCell':
          if window_found:
            print('%apply (SpiceDouble OUT_ARRAY2[ANY][ANY], int *SIZE1) {(SpiceDouble ' + arg_name + '[1000][2], int *intervals)};')
          else:
            print('%apply (SpiceInt OUT_ARRAY1[ANY], int *SIZE1) {(SpiceInt ' + arg_name + '[1000], int *id_count)};')
        else:
            print('%apply () {};  // Attention needed for ' + arg_name)
      else:
            print('%apply () {};  // Attention needed for ' + arg_name)

    print()

    if arglist_failure:
        failures[name] = 'ARGUMENT INTERPRETATION FAILURE'
        print('---------------- ERROR: ARGUMENT INTERPRETATION FAILURE -------------\n')

    elif any_cells:
      if cell_count > 1:
        failures[name] = 'MULTIPLE CELLS'
        print('---------------- ERROR: MULTIPLE CELLS -------------\n')
      elif not cell_is_output:
        failures[name] = 'CELL IS NOT OUTPUT'
        print('---------------- ERROR: CELL IS NOT OUTPUT -------------\n')
      else:
        print('%inline %{')
        if window_found:
            print('    /* Helper function to create a 2-D array of results */')
        else:
            print('    /* Helper function to create an array of results */')
        print('    void my_' + name + '_c(', end='')

        if cell_count > 1:
            print('\n---------------- MULTIPLE CELLS -------------\n')
        else:
            pref = (15+len(name)) * ' '
            for k in range(len(arg_types)):
                if k > 0:
                    print(pref, end='')
                end = ',' if k < len(arg_types) - 1 else ') {'
                if arg_types[k] == 'SpiceCell':
                    if window_found:
                        print('SpiceDouble ' + cell_name + '[1000][2], int *intervals' + end)
                    else:
                        print('SpiceInt ' + cell_name + '[1000], int *id_count' + end)
                else:
                    print(arg_types[k] + ' ' + arg_stars[k] + arg_names[k] + end)

            print()
            print('        int j;')
            if window_found:
                temp_name = 'coverage'
                print('        SPICEDOUBLE_CELL(coverage, 2*1000);\n')
                print('        scard_c(0, &coverage);')
            else:
                temp_name = 'id_values'
                print('        SPICEINT_CELL(id_values, 1000);\n')
                print('        scard_c(0, &id_values);')

            new_args = list(arg_names)
            k = new_args.index(cell_name)
            new_args[k] = '&' + temp_name
            print('        ' + name + '_c(' + ', '.join(new_args) + ');\n')

            if window_found:
                print('        *intervals = (int) card_c(&coverage) / 2;')
                print('        for (j = 0; j < *intervals; j++) {')
                print('            wnfetd_c(&coverage, j, &(array[j][0]), &(array[j][1]));')
            else:
                print('        *id_count = card_c(&id_values);')
                print('        for (j = 0; j < *id_count; j++) {')
                print('            ' + cell_name + '[j] = SPICE_CELL_ELEM_I(&id_values, j);')
            print('        }')
            print('    }')

        print('%}\n')

    elif arg_names:
        print('extern ' + return_type + ' ' + name + '_c(')
        longest = max([len(a) for a in arg_types])
        for k in range(len(arg_types)):
          end = ',' if k < len(arg_types)-1 else ''
          arg_type = arg_types[k]
          arg_name = arg_names[k]
          arg_star = arg_stars[k]
          right = arg_name
          if arg_star and '[' not in arg_name:
            if arg_type == 'ConstSpiceChar':
                right = 'CONST_STRING'
            elif arg_type == 'SpiceChar' and arg_io[arg_name.split('[')[0]] == 'I':
                right = 'IN_STRING'
            elif arg_type == 'SpiceBoolean':
                right = 'OUT_BOOLEAN'
            elif arg_type == 'SpiceDouble':
                right = 'OUTPUT'
            elif arg_type == 'SpiceInt':
                right = 'OUTPUT'
          print(8*' ' + arg_type.ljust(longest+1) + arg_star + right + end)
        print(');\n')

    else:
        print('extern ' + return_type + ' ' + name + '_c(void);\n')

    if any_floats and not arglist_failure and not any_cells:
        print('//Vector version\nVECTORIZE_xxx(' + name + ', ' + name + '_c)\n')

print('/' + 70*'*' + '/')

