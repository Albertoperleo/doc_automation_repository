class Contributor:
    
    def __init__(self, user_id, nickname, url, user_type, site_admin, contributions, contrib_dict=None) -> None:
        
        if contrib_dict == None:
            self.user_id = user_id
            self.nickname = nickname
            self.url = url
            self.user_type = user_type
            self.site_admin = site_admin == 'true'
            self.contributions = contributions
        else:
            self.user_id = contrib_dict['id']
            self.nickname = contrib_dict['name']
            self.url = contrib_dict['url']
            self.user_type = contrib_dict['type']
            self.site_admin = contrib_dict['site_admin'] == 'true'
            self.contributions = int(contrib_dict['contributions'])
            