from abc import ABCMeta, abstractmethod

class LocalSearch:
  __metaclass__ = ABCMeta
  @abstractmethod
  def search(self):
    pass
