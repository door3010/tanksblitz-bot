from config import AimTank, Minimap

class MleModel:
    def __init__(self):

        self.__model = AimTank.mle_model_path

    def load(self):
        return self.__model

class ArrowModel:
    def __init__(self):

        self.__model = Minimap.arrow_model_path

    def load(self):
        return self.__model

# class BuildingsModel:
#     def __init__(self):
#
#         self.__model = mle_model_path
#
#     def load(self):
#         return self.__model

def Factory(model:str=None):
    """Factory Method"""
    load = {
        "Mle": MleModel,
        "Arrow": ArrowModel,
        # "Buildings": BuildingsModel,
    }

    return load[model]()