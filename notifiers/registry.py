class NotifierIdExistsException(Exception):
    pass

class NotifierRegistry:
    def __init__(self):
        """Creates a new instance of the NotifierRegistry.

        A NotifierRegistry is a lightweight wrapper around a dict, making it easy
        to centrally manage notifiers available to process possible secret discoveries.
        """
        self.registry = {}

    def register(self, notifier_id, notifier_cls):
        """Registers a new notifier class

        Arguments:
            notifier_id {str} -- The notifier class ID
            notifier_cls {notifier.Notifier} -- [description]
        """
        if notifier_id in self.registry:
            raise NotifierIdExistsException

        self.registry[notifier_id] = notifier_cls

    def get(self, notifier_id):
        """Gets a notifier class from the registry.

        Arguments:
            notifier_id {str} -- The notifier class ID

        Returns:
            notifier.Notifier -- The subclass of notifier.Notifier that maps to the provided
                notifier_id
        """
        return self.registry.get(notifier_id)

    def notifiers(self):
        """Returns a list of notifier classes in the registry.

        Returns:
            list -- A list of notifier class IDs
        """
        return self.registry.keys()

    def delete(self, notifier_id):
        """Removes a notifier class from the registry.

        Arguments:
            notifier_id {str} -- The notifier class ID
        """
        self.registry.pop(notifier_id)

    def reset(self):
        """Resets the registry to a clean state.
        """
        self.registry = {}
