
from abc import ABC, abstractmethod
from uuid import uuid4
from .budget import GlobalBudget
from .campaign import Campaign


class ChannelClient(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def create_campaign(self, campaign: Campaign) -> str:
        # TODO: Create a campaign on this channel and return an external id.
        pass

    @abstractmethod
    def pause_campaign(self, campaign_id: str) -> None:
        pass


class GoogleAdsClient(ChannelClient):
    def __init__(self):
        super().__init__("Google Ads")

    def create_campaign(self, campaign: Campaign) -> str:
        GlobalBudget().allocate(campaign.daily_budget)
        return f"g-{uuid4().hex[:10]}"

    def pause_campaign(self, campaign_id: str) -> None:
        pass


class FacebookAdsClient(ChannelClient):
    def __init__(self):
        super().__init__("Facebook Ads")

    def create_campaign(self, campaign: Campaign) -> str:
        GlobalBudget().allocate(campaign.daily_budget)
        return f"f-{uuid4().hex[:10]}"

    def pause_campaign(self, campaign_id: str) -> None:
        pass


class ChannelClientFactory:
    _clients = {
        "google": GoogleAdsClient,
        "facebook": FacebookAdsClient,
    }

    @staticmethod
    def create(channel: str) -> ChannelClient:
        client_cls = ChannelClientFactory._clients.get((channel or "").lower())
        if client_cls is None:
            raise ValueError(f"Unsupported channel: {channel}")
        return client_cls()
