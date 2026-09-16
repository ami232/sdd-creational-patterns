
from abc import ABC, abstractmethod
from uuid import uuid4
from .budget import GlobalBudget
from .campaign import Campaign


class ChannelClient(ABC):
    id_prefix: str

    def __init__(self, name: str):
        self.name = name
        self._paused = set()

    @abstractmethod
    def create_campaign(self, campaign: Campaign) -> str:
        # TODO: Create a campaign on this channel and return an external id.
        pass

    @abstractmethod
    def pause_campaign(self, campaign_id: str) -> None:
        pass

    def _allocate(self, campaign: Campaign) -> str:
        GlobalBudget().allocate(campaign.daily_budget)
        return f"{self.id_prefix}-{uuid4()}"


class GoogleAdsClient(ChannelClient):
    id_prefix = "g"

    def __init__(self):
        super().__init__("google")

    def create_campaign(self, campaign: Campaign) -> str:
        return self._allocate(campaign)

    def pause_campaign(self, campaign_id: str) -> None:
        self._paused.add(campaign_id)


class FacebookAdsClient(ChannelClient):
    id_prefix = "f"

    def __init__(self):
        super().__init__("facebook")

    def create_campaign(self, campaign: Campaign) -> str:
        return self._allocate(campaign)

    def pause_campaign(self, campaign_id: str) -> None:
        self._paused.add(campaign_id)


class ChannelClientFactory:
    _clients = {
        "google": GoogleAdsClient,
        "facebook": FacebookAdsClient,
    }

    @staticmethod
    def create(channel: str) -> ChannelClient:
        client_cls = ChannelClientFactory._clients.get(str(channel).lower())
        if client_cls is None:
            raise ValueError(f"Unsupported channel: {channel}")
        return client_cls()
