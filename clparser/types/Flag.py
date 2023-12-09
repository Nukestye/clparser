
from clparser.types.FlagActionType import FlagActionType


class Flag:
    # format (short notation, long notation)
    __notation: (str, str)
    
    # name of the flag, used to look up
    # inside a dictionary
    __name: str
    
    # used inside help, for end user
    # to figure what the flag is for
    __desc: str
    
    # The action the flag intendeds to take
    __action_type: FlagActionType
    
    def __init__(self, name: str, desc: str, notation: str | list, action: FlagActionType):
        self.__name = name
        
        self.__desc = desc
        
        # Specify the correct format
        # for the notation varaible
        # small notation takes first index '0'
        # whereas long notation is second index '1'
        if type(notation) == list:
            self.__notation = notation
        elif notation.startswith('-'):
            self.__notation = (notation, '')
        elif self.__notation.startswith('--'):
            self.__notation = ('', notation)
        else:
            print(f'Invalid notation specified for flag \'{name}\'')
            return
        
        # Making sure the flag
        # action type is in range of 1 to 4
        if action.value > 4 or action.value < 1:
            print(f'Invalid action type specified for flag \'{name}\'')
            return
        
        self.__action_type = action
    
    
    # Getter functions
    
    def get_flag_name(self): return self.__name
    def get_flag_desc(self): return self.__desc
    def get_flag_action_type(self): return self.__action_type
    def get_flag_notation(self): return self.__notation
