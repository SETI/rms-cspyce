import collections

import numpy as np

SPICE_CELL_HEADER_DESCRIPTOR = np.dtype([
    # Many of these names clash with built in properties of an array, so we've suffixed
    # all of them with an underscore
    ("dtype_", np.int32),
    ("length_", np.int32),
    ("size_", np.int32),
    ("card_", np.int32),
    ("isSet_", np.int32),
    ("adjust_", np.int32),
    ("init_", np.int32),
    ("base_", np.int64),
    ("data_", np.int64),
], align=True)

SPICE_CELL_INT = 2
SPICE_CELL_DOUBLE = 1
SPICE_CELL_CHAR = 0

class SpiceCell:
    CONTROL_SIZE = 6

    @staticmethod
    def create_spice_cell(my_type, size=1000, length=30):
        length = length if my_type == SPICE_CELL_CHAR else 0
        return SpiceCell(my_type, size=size, length=length)

    @staticmethod
    def as_spice_cell(my_type, record):
        if isinstance(record, SpiceCell) and record._header.dtype_ == my_type:
            return record
        return SpiceCell(my_type, data=record)

    def __init__(self, typeno = None, size:int = 0, length:int = 0, data=None):
        if data is None:
            if typeno is None or  size == 0  or (type == SPICE_CELL_DOUBLE and length == 0):
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

        self._header.dtype_ = typeno
        self._header.length_ = length
        self._header.size_ = size
        self._header.card_ = 0
        self._header.isSet_ = True
        self._header.adjust_ = False
        self._header.init_ = False

        self.__grow_array(size, init=True)

        if data is not None:
            self._user_data[:len(data)] = data
            self._header.card_ = len(data)

    def __getitem__(self, index):
        return self._user_data[index]

    def __setitem__(self, index, value):
        self._user_data[index] = value

    def __len__(self):
        return self._header.card_.item()

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

    @property
    def size(self):
        return self._header.size_.item()

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
        self._header.card_ = value

    def as_array(self):
        return self._user_data[0:self.card]

    def as_intervals(self):
        return self.as_array().reshape(-1, 2)

    def __str__(self):
        typename = ['char', 'float', 'int'][self._header.dtype_]
        return f"<SpiceCell {typename} {self._header.card_}/{self._header.size_} {self.as_array()}>"

    def __repr__(self):
        return self.__str__()

    def __grow_array(self, size, init=False):
        if init:
            self._data = np.zeros(size + self.CONTROL_SIZE, dtype=self._descriptor)
        else:
            self._data.resize(size + self.CONTROL_SIZE, refcheck=False)
        self._user_data = self._data[6:]
        self._header.size_ = size
        self._header.card_ = min(size, self._header.card_)
        self._header.base_ = self._data.ctypes.data
        self._header.data_ = self._user_data.ctypes.data
        assert self._header.data_ - self._header.base_ == self.CONTROL_SIZE * self._descriptor.itemsize

    @property
    def base(self):
        # Returns the underlying array for which array[0] is the header.  Swig calls this.
        return self._header.base

if __name__ == '__main__':
    x = SpiceCell(data=range(10))
    x.append(15)
    x.extend(range(20, 50))
    print(x)
