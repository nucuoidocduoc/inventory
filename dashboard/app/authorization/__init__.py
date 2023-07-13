
import vakt
import uuid
from vakt.rules import Eq, Any, NotEq, StartsWith, In, RegexMatch, CIDR, And, Greater, Less
import os

# policies = [
#     vakt.Policy(
#         str(uuid.uuid4()),
#         actions=[Eq('get'), Eq('list'), Eq('read')],
#         resources=[StartsWith('repos/google/tensor')],
#         subjects=[Any()],
#         effect=vakt.ALLOW_ACCESS,
#         description='Grant read-access for all Google repositories starting with "tensor" to any User'
#     ),
#     vakt.Policy(
#         str(uuid.uuid4()),
#         actions=[In('delete', 'prune', 'exterminate')],
#         resources=[RegexMatch(r'repos\/.*?\/.*?')],
#         subjects=[{'name': Any(), 'role': Eq('admin')}, {'name': Eq('defunkt')}, Eq('defunkt')],
#         effect=vakt.ALLOW_ACCESS,
#         description='Grant delete-access for any repository to any User with "admin" role, or to a User named defunkt'
#     )
# ]

# policies = vakt.Policy.from_json("abac_policy.json")
# i=0


class Guardian:
    def __init__(self) -> None:
        self.storage = self._create_storage()
        self.guard = vakt.Guard(self.storage, vakt.RulesChecker())

    def check(self, inquiry: vakt.Inquiry) -> bool:
        return self.guard.is_allowed(inquiry)
    
    def add_policy(self, policy: vakt.Policy) -> None:
        self.storage.add(policy)

    @staticmethod
    def _create_storage():
            return vakt.MemoryStorage()

guardian = Guardian()
