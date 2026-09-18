
from abc import ABC, abstractmethod
from uuid import uuid4
from .budget import GlobalBudget
from .campaign import Campaign

class ChannelClient(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def create_campaign(self, campaign: Campaign) -> str:
        ...

    @abstractmethod
    def pause_campaign(self, campaign_id: str) -> None:
        ...

    def _allocate_budget(self, campaign: Campaign) -> None:
        GlobalBudget().allocate(campaign.daily_budget)

    def _gen_external_id(self) -> str:
        return f'{self.name[0]}-{uuid4().hex[:12]}'

class GoogleAdsClient(ChannelClient):
    def __init__(self):
        super().__init__('google')

    def create_campaign(self, campaign: Campaign) -> str:
        self._allocate_budget(campaign)
        return self._gen_external_id()

    def pause_campaign(self, campaign_id) -> None:
        print(f'google campaign {campaign_id} paused')

class FacebookAdsClient(ChannelClient):
    def __init__(self):
        super().__init__('facebook')

    def create_campaign(self, campaign: Campaign) -> str:
        self._allocate_budget(campaign)
        return self._gen_external_id()

    def pause_campaign(self, campaign_id) -> None:
        print(f'facebook campaign {campaign_id} paused')

class ChannelClientFactory:
    _clients = {
        'google': GoogleAdsClient,
        'facebook': FacebookAdsClient,
    }

    @classmethod
    def create(cls, channel: str) -> ChannelClient:
        try:
            return cls._clients[channel]()
        except KeyError:
            raise ValueError(f'Unsupported channel: {channel!r}') from None
