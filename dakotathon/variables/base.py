"""An abstract base class for all Dakota variable types."""

from abc import ABCMeta, abstractmethod
from ..utils import to_iterable


class VariablesBase(object):

    """Describe features common to all Dakota variable types."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, variables="continuous_design", descriptors=(), **kwargs):
        """Create default variables parameters.

        Parameters
        ----------
        descriptors : str or tuple or list of str, optional
            Labels for the variables.
        variables : str, optional
            The type of parameter set (default is 'continuous_design').

        """
        self.variables = variables
        self._descriptors = descriptors

    @property
    def descriptors(self):
        """Labels attached to Dakota variables."""
        return self._descriptors

    @descriptors.setter
    def descriptors(self, value):
        """Set labels for Dakota variables.

        Parameters
        ----------
        value : str or list or tuple of str
          The new variables labels.

        """
        if type(value) is str:
            value = (value,)
        if not isinstance(value, (tuple, list)):
            raise TypeError("Descriptors must be a string, tuple or list")
        self._descriptors = value

    def __str__(self):
        """Define the variables block of a Dakota input file."""
        descriptors = to_iterable(self.descriptors)
        s = "variables\n" + "  {0} = {1}\n".format(self.variables, len(descriptors))
        s += "    descriptors ="
        for vd in descriptors:
            s += " {!r}".format(vd)
        return s
