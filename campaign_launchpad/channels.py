
from abc import ABC, abstractmethod
from uuid import uuid4
from .budget import GlobalBudget
from .campaign import Campaign


class ChannelClient(ABC):
    def __init__(self, name: str):
        self.name = name

    @property
    @abstractmethod
    def id_prefix(self) -> str:
        """Prefix used for the external ids issued by this channel."""

    def create_campaign(self, campaign: Campaign) -> str:
        GlobalBudget().allocate(campaign.daily_budget)
        return f"{self.id_prefix}{uuid4().hex[:12]}"

    @abstractmethod
    def pause_campaign(self, campaign_id: str) -> None:
        pass


class GoogleAdsClient(ChannelClient):
    id_prefix = "g-"

    def __init__(self):
        super().__init__("google")

    def pause_campaign(self, campaign_id: str) -> None:
        print(f"[google] paused campaign {campaign_id}")


class FacebookAdsClient(ChannelClient):
    id_prefix = "f-"

    def __init__(self):
        super().__init__("facebook")

    def pause_campaign(self, campaign_id: str) -> None:
        print(f"[facebook] paused campaign {campaign_id}")


class ChannelClientFactory:
    _clients = {
        "google": GoogleAdsClient,
        "facebook": FacebookAdsClient,
    }

    @staticmethod
    def create(channel: str) -> ChannelClient:
        client_cls = ChannelClientFactory._clients.get(str(channel).strip().lower())
        if client_cls is None:
            raise ValueError(f"Unsupported channel: {channel}")
        return client_cls()
