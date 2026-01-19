class InMemorySessionService:
    def __init__(self):
        """Initialize the InMemorySessionService."""
        self.session = {}

    def set(self, key, value):
        """Set a value in the session."""
        self.session[key] = value


    def get(self, key, default=None):
        """Get a value from the session."""
        return self.session.get(key, default)


    def clear(self):
        """Clear the session."""
        self.session = {}