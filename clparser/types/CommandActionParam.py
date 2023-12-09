
class CommandActionParam:
    
    flags: list
    
    def __init__(self): 
        pass
    
    def containsFlag(self, flag: str) -> bool:
        """
        Checks if the flag was mentioned

        :param flag: the flag to look for
        :type flag: str
        :return: whether the flag was mentioned or not
        :rtype: bool
        """        
        # making sure that flag exist
        if self.flags:
            if flag in self.flags:
                return True
            return False
        
        return False