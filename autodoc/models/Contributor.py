from __future__ import annotations
from typing import List
import json

class Contributor:
        def __init__(self, user_id, nickname, url, user_type, site_admin, contributions) -> None:
                self.user_id = user_id
                self.nickname = nickname
                self.url = url
                self.user_type = user_type
                self.site_admin = site_admin == 'true'
                self.contributions = contributions

        @staticmethod
        def create(contributor_json) -> Contributor:
                contributor_id = contributor_json['id']
                login = contributor_json['login']
                url = contributor_json['url']
                user_type = contributor_json['type']
                site_admin = contributor_json['site_admin'] == 'true'
                contributions = int(contributor_json['contributions'])
                return Contributor(contributor_id, login, url, user_type, site_admin, contributions)
        
        @staticmethod
        def createContributors(contributors_json) -> List[Contributor]:
                return [Contributor.create(c) for c in contributors_json]