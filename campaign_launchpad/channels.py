
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
        super().__init__("google")

    def create_campaign(self, campaign: Campaign) -> str:
        GlobalBudget().allocate(campaign.daily_budget)
        campaign_id = f"g-{uuid4()}"
        print(f"[Google Ads] Created campaign '{campaign.name}' -> {campaign_id}")
        return campaign_id

    def pause_campaign(self, campaign_id: str) -> None:
        print(f"[Google Ads] Paused campaign {campaign_id}")


class FacebookAdsClient(ChannelClient):
    def __init__(self):
        super().__init__("facebook")

    def create_campaign(self, campaign: Campaign) -> str:
        GlobalBudget().allocate(campaign.daily_budget)
        campaign_id = f"f-{uuid4()}"
        print(f"[Facebook Ads] Created campaign '{campaign.name}' -> {campaign_id}")
        return campaign_id

    def pause_campaign(self, campaign_id: str) -> None:
        print(f"[Facebook Ads] Paused campaign {campaign_id}")


class ChannelClientFactory:
    _clients = {
        "google": GoogleAdsClient,
        "facebook": FacebookAdsClient,
    }

    @staticmethod
    def create(channel: str) -> ChannelClient:
        client_cls = ChannelClientFactory._clients.get(channel.lower())
        if client_cls is None:
            raise ValueError(f"Unsupported channel: {channel}")
        return client_cls()
