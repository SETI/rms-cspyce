import numpy as np


SPICE_CELL_HEADER_DESCRIPTOR = np.dtype([
    # Many of these names clash with built-in properties of an array, so we've suffixed
    # all of them with an underscore
    ("_dtype", np.int32),
    ("_length", np.int32),
    ("_size", np.int32),
    ("_card", np.int32),
    ("_isSet", np.int32),
    ("_adjust", np.int32),
    ("_init", np.int32),
    ("_base", np.int64),
    ("_data", np.int64),
], align=True)

SPICE_CELL_INT = 2
SPICE_CELL_DOUBLE = 1
SPICE_CELL_CHAR = 0

class SpiceCell:
    CONTROL_SIZE = 6

    @staticmethod
    def create_spice_cell(my_type, size=1000, length=30):
        length = length if my_type == SPICE_CELL_CHAR else 0
        return SpiceCell(typeno=my_type, size=size, length=length)

    @staticmethod
    def as_spice_cell(my_type, record):
        if isinstance(record, SpiceCell) and record._header._dtype == my_type:
            return record
        return SpiceCell(data=record, typeno=my_type)

    def __init__(self, data=None, typeno=None, size: int = 0, length: int = 0):
        if data is None:
            if typeno is None or size == 0 or (type == SPICE_CELL_DOUBLE and length == 0):
                raise ValueError("You must specify either an array, "
                                 "or else type, size, and length (for characters)")

        if typeno is None:
            data = np.asarray(data)
            if data.dtype.kind == 'f':
                typeno = SPICE_CELL_DOUBLE
            elif data.dtype.kind in 'bis':
                typeno = SPICE_CELL_INT
            elif data.dtype.kind in 'SU':
                typeno = SPICE_CELL_CHAR
                data = np.asarray(data, dtype='S')
                length = max(2, length, max(len(x) for x in data.ravel()) + 1)
            else:
                raise ValueError("array has unknown type")

        if typeno == SPICE_CELL_INT:
            array_descriptor = np.dtype(np.int32)
        elif typeno == SPICE_CELL_DOUBLE:
            array_descriptor = np.dtype(np.double)
        elif typeno == SPICE_CELL_CHAR:
            array_descriptor = np.dtype(("S", length))
            length = max(2, length)
        else:
            raise ValueError(f"Bad type {typeno} passed to SpiceCell init")

        if data is not None:
            data = np.asarray(data, dtype=array_descriptor)
            size = max(size, len(data) + 6)  # add a little bit of spare room

        self._header = np.rec.array(None, SPICE_CELL_HEADER_DESCRIPTOR, 1)[0]
        self._descriptor = array_descriptor

        self._header._dtype = typeno
        self._header._length = length
        self._header._size = size
        self._header._card = 0
        self._header._isSet = True
        self._header._adjust = False
        self._header._init = False

        self.__grow_array(size, init=True)

        if data is not None:
            self._user_data[:len(data)] = data
            self._header._card = len(data)

    def __getitem__(self, index):
        # Handle negative indexing
        if -self.card <= index < 0:
            index += self.card
        return self._user_data[index]

    def __setitem__(self, index, value):
        # Handle negative indexing
        if -self.card <= index < 0:
            index += self.card
        self._user_data[index] = value

    def __len__(self):
        return self._header._card.item()

    def __iter__(self):
        for i in range(self.card):
            yield self[i]

    def clear(self):
        self.card = 0

    def append(self, value):
        if self.card == self.size:
            self.__grow_array(max(10, 2 * self.size))
        self[self.card] = value
        self.card += 1

    def extend(self, values):
        values = np.asarray(values, self._descriptor)
        count = len(values)
        if self.card + count > self.size:
            self.__grow_array(max(self.card + count + 10, 2 * self.size))
        self._user_data[self.card : self.card + count] = values
        self.card += count

    def __iadd__(self, values):
        self.extend(values)
        return self

    @property
    def size(self):
        return self._header._size.item()

    @size.setter
    def size(self, size):
        assert isinstance(size, int) and size > 0
        self.__grow_array(size)

    @property
    def card(self):
        return len(self)

    @card.setter
    def card(self, value):
        assert isinstance(value, int) and 0 <= value <= self.size
        self._header._card = value

    def as_array(self):
        return self._user_data[0:self.card]

    def as_intervals(self):
        return self.as_array().reshape(-1, 2)

    def __str__(self):
        typename = ['char', 'double', 'int'][self._header._dtype]
        return f"<SpiceCell {typename} {self._header._card}/{self._header._size} {self.as_array()}>"

    def __repr__(self):
        return self.__str__()

    def __grow_array(self, size, init=False):
        if init:
            self._data = np.zeros(size + self.CONTROL_SIZE, dtype=self._descriptor)
        else:
            self._data.resize(size + self.CONTROL_SIZE, refcheck=False)
        self._user_data = self._data[6:]
        self._header._size = size
        self._header._card = min(size, self._header._card)
        self._header._base = self._data.ctypes.data
        self._header._data = self._user_data.ctypes.data
        assert self._header._data - self._header._base == self.CONTROL_SIZE * self._descriptor.itemsize

    @property
    def base(self):
        # Returns the underlying array for which array[0] is the header. Swig calls this.
        return self._header.base
