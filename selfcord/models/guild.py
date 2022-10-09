from .user import User

class Guild:
    def __init__(self, data) -> None:
        self.roles = []
        self.emojis = []
        self.members = []
        self.channels = []
        self.ids = data.get(id)
        self.name = None
        self.icon = None
        self.region = None
        self.splash = None
        self.mfa_level = None
        self.features = None
        self.verification_level = None
        self.explicit_content_filter = None

    def _update(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.icon = data.get('icon')
        self.region = data.get('region')
        self.splash = data.get('splash')
        self.mfa_level = data.get('mfa_level')
        self.features = data.get('features')
        self.unavailable = data.get('unavailable', True)
        self.verification_level = data.get('verification_level')
        self.explicit_content_filter = data.get('explicit_content_filter')
        self.owner_id = data.get('owner_id')
        for member in data.get('members'):
            user = User(member)
            self.members.append(user)
            



