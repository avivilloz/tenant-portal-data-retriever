from abc import ABC, abstractmethod


class TenantPortal(ABC):
    """Abstract base class for tenant portals."""

    @abstractmethod
    def retrieve_data(self, username, password):
        """
        Retrieve tenant data from the portal.

        :param username: Portal authentication username
        :param password: Portal authentication password
        :return: Dictionary containing tenant data
        :raises NotImplementedError: If not implemented by subclass
        """
        pass
