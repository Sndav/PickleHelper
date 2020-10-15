import struct
import codecs

class PickleBuilder():
    def __init__(self):
        self.data = b""
        self.MARK           = b'('   # push special markobject on stack
        self.STOP           = b'.'   # every pickle ends with STOP
        self.POP            = b'0'   # discard topmost stack item
        self.POP_MARK       = b'1'   # discard stack top through topmost markobject
        self.DUP            = b'2'   # duplicate top stack item
        self.FLOAT          = b'F'   # push float object; decimal string argument
        self.INT            = b'I'   # push integer or bool; decimal string argument
        self.BININT         = b'J'   # push four-byte signed int
        self.BININT1        = b'K'   # push 1-byte unsigned int
        self.LONG           = b'L'   # push long; decimal string argument
        self.BININT2        = b'M'   # push 2-byte unsigned int
        self.NONE           = b'N'   # push None
        self.PERSID         = b'P'   # push persistent object; id is taken from string arg
        self.BINPERSID      = b'Q'   #  "       "         "  ;  "  "   "     "  stack
        self.REDUCE         = b'R'   # apply callable to argtuple, both on stack
        self.STRING         = b'S'   # push string; NL-terminated string argument
        self.BINSTRING      = b'T'   # push string; counted binary string argument
        self.SHORT_BINSTRING= b'U'   #  "     "   ;    "      "       "      " < 256 bytes
        self.UNICODE        = b'V'   # push Unicode string; raw-unicode-escaped'd argument
        self.BINUNICODE     = b'X'   #   "     "       "  ; counted UTF-8 string argument
        self.APPEND         = b'a'   # append stack top to list below it
        self.BUILD          = b'b'   # call __setstate__ or __dict__.update()
        self.GLOBAL         = b'c'   # push self.find_class(modname, name); 2 string args
        self.DICT           = b'd'   # build a dict from stack items
        self.EMPTY_DICT     = b'}'   # push empty dict
        self.APPENDS        = b'e'   # extend list on stack by topmost stack slice
        self.GET            = b'g'   # push item from memo on stack; index is string arg
        self.BINGET         = b'h'   #   "    "    "    "   "   "  ;   "    " 1-byte arg
        self.INST           = b'i'   # build & push class instance
        self.LONG_BINGET    = b'j'   # push item from memo on stack; index is 4-byte arg
        self.LIST           = b'l'   # build list from topmost stack items
        self.EMPTY_LIST     = b']'   # push empty list
        self.OBJ            = b'o'   # build & push class instance
        self.PUT            = b'p'   # store stack top in memo; index is string arg
        self.BINPUT         = b'q'   #   "     "    "   "   " ;   "    " 1-byte arg
        self.LONG_BINPUT    = b'r'   #   "     "    "   "   " ;   "    " 4-byte arg
        self.SETITEM        = b's'   # add key+value pair to dict
        self.TUPLE          = b't'   # build tuple from topmost stack items
        self.EMPTY_TUPLE    = b')'   # push empty tuple
        self.SETITEMS       = b'u'   # modify dict by adding topmost key+value pairs
        self.BINFLOAT       = b'G'   # push float; arg is 8-byte float encoding
        self.TRUE           = b'I01\n'  # not an opcode; see INT docs in pickletools.py
        self.FALSE          = b'I00\n'  # not an opcode; see INT docs in pickletools.py
        self.PROTO          = b'\x80'  # identify pickle protocol
        self.NEWOBJ         = b'\x81'  # build object by applying cls.__new__ to argtuple
        self.EXT1           = b'\x82'  # push object from extension registry; 1-byte index
        self.EXT2           = b'\x83'  # ditto, but 2-byte index
        self.EXT4           = b'\x84'  # ditto, but 4-byte index
        self.TUPLE1         = b'\x85'  # build 1-tuple from stack top
        self.TUPLE2         = b'\x86'  # build 2-tuple from two topmost stack items
        self.TUPLE3         = b'\x87'  # build 3-tuple from three topmost stack items
        self.NEWTRUE        = b'\x88'  # push True
        self.NEWFALSE       = b'\x89'  # push False
        self.LONG1          = b'\x8a'  # push long from < 256 bytes
        self.LONG4          = b'\x8b'  # push really big long
        self.BINBYTES       = b'B'   # push bytes; counted binary string argument
        self.SHORT_BINBYTES = b'C'   #  "     "   ;    "      "       "      " < 256 bytes
        self.SHORT_BINUNICODE = b'\x8c'  # push short string; UTF-8 length < 256 bytes
        self.BINUNICODE8      = b'\x8d'  # push very long string
        self.BINBYTES8        = b'\x8e'  # push very long bytes string
        self.EMPTY_SET        = b'\x8f'  # push empty set on the stack
        self.ADDITEMS         = b'\x90'  # modify set by adding topmost stack items
        self.FROZENSET        = b'\x91'  # build frozenset from topmost stack items
        self.NEWOBJ_EX        = b'\x92'  # like NEWOBJ but work with keyword only arguments
        self.STACK_GLOBAL     = b'\x93'  # same as GLOBAL but using names on the stacks
        self.MEMOIZE          = b'\x94'  # store top of the stack in memo
        self.FRAME            = b'\x95'  # indicate the beginning of a new frame
        self.BYTEARRAY8       = b'\x96'  # push bytearray
        self.NEXT_BUFFER      = b'\x97'  # push next out-of-band buffer
        self.READONLY_BUFFER  = b'\x98'  # make top of stack readonly
    def push_bool(self,val):
        if val:
            self.data += self.INT+self.TRUE[1:]
        else:
            self.data += self.INT+self.FALSE[1:]
    def push_int(self,val):
        self.data += self.INT + str(val).encode() + b"\n"
    def push_str(self,val):
        self.data += self.STRING
        self.data += b"'"+codecs.escape_decode(val.encode())[0]+b"'"
        self.data += b"\n"
    def build_tuple(self):
        self.data += self.TUPLE
    def build_dict(self):
        self.data += self.DICT
    def push_mark(self):
        self.data += self.MARK
    def pop_mark(self):
        self.data += self.POP_MARK
    def build(self):
        self.data += self.BUILD
    def load_class(self,module,name):
        self.data += self.GLOBAL + module.encode() + b"\n"
        self.data += name.encode() + b"\n"
    def put_memo(self,num):
        self.data += self.PUT
        self.data += str(num).encode() + b"\n"
    def get_memo(self,num):
        self.data += self.GET
        self.data += str(num).encode() + b"\n"
    def load_inst(self,module,name):
        self.data += self.INST
        self.data += module.encode() + b'\n'
        self.data += name.encode() + b'\n'
    def compile(self):
        return self.data+self.STOP