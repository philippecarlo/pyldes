# from unittest import TestCase
# from abc import abstractmethod

# from abstract import AbstractBaseType
# from overrides import override


# class SuperClass(AbstractBaseType):
#     @abstractmethod
#     def abstract_method():
#         raise NotImplementedError

#     @abstractmethod
#     def abstract_method_with_params(self, test: str):
#         raise NotImplementedError


# class SubClass(SuperClass):
#     @override
#     def abstract_method():
#         pass

#     @override
#     def abstract_method_with_params(self, test: str):
#         pass


# class SubClassWithoutOverrides(SuperClass):
#     def abstract_method():
#         pass

#     def abstract_method_with_params(self, test: str):
#         pass


# class SubClassWithMissingAbstractMethod(SuperClass):
#     @override
#     def abstract_method():
#         pass


# class SubClassWithIncorrectMethodSignature(SuperClass):
#     @override
#     def abstract_method(self):
#         pass

#     @override
#     def abstract_method_with_params(self):
#         pass


# def test_interface_inheritance(subclass, subclass_missing_an_abstract_method, subclass_with_incorrect_method_signature):
#     pass

# def test_enforce_interface():
#     TestCase().assertRaises(TypeError, SubClassWithoutOverrides())
