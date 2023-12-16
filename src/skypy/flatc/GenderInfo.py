# automatically generated by the FlatBuffers compiler, do not modify

# namespace: 

import flatbuffers
from flatbuffers.compat import import_numpy
from typing import Any
np = import_numpy()

class GenderInfo(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls) -> int:
        return 2

    # GenderInfo
    def Init(self, buf: bytes, pos: int):
        self._tab = flatbuffers.table.Table(buf, pos)

    # GenderInfo
    def Group(self): return self._tab.Get(flatbuffers.number_types.Uint8Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # GenderInfo
    def Ratio(self): return self._tab.Get(flatbuffers.number_types.Uint8Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(1))

def CreateGenderInfo(builder, group, ratio):
    builder.Prep(1, 2)
    builder.PrependUint8(ratio)
    builder.PrependUint8(group)
    return builder.Offset()
