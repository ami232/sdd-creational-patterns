
from abc import ABC, abstractmethod
from uuid import uuid4
from .budget import GlobalBudget
from .campaign import Campaign


class ChannelClient(ABC):
    # Prefix each channel stamps on the external ids it hands back.
    prefix: str = ""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def create_campaign(self, campaign: Campaign) -> str:
        # Create a campaign on this channel and return an external id.
        ...

    @abstractmethod
    def pause_campaign(self, campaign_id: str) -> None:
        ...

    def _charge_and_mint_id(self, campaign: Campaign) -> str:
        """Take the campaign's daily budget out of the shared wallet, then mint an id."""
        GlobalBudget().allocate(campaign.daily_budget)
        return f"{self.prefix}-{uuid4().hex}"


class GoogleAdsClient(ChannelClient):
    prefix = "g"

    def __init__(self):
        super().__init__("Google Ads")

    def create_campaign(self, campaign: Campaign) -> str:
        return self._charge_and_mint_id(campaign)

    def pause_campaign(self, campaign_id: str) -> None:
        print(f"[{self.name}] paused campaign {campaign_id}")


class FacebookAdsClient(ChannelClient):
    prefix = "f"

    def __init__(self):
        super().__init__("Facebook Ads")

    def create_campaign(self, campaign: Campaign) -> str:
        return self._charge_and_mint_id(campaign)

    def pause_campaign(self, campaign_id: str) -> None:
        print(f"[{self.name}] paused campaign {campaign_id}")


class ChannelClientFactory:
    _clients = {
        "google": GoogleAdsClient,
        "facebook": FacebookAdsClient,
    }

    @staticmethod
    def create(channel: str) -> ChannelClient:
        # Return the appropriate client based on the channel.
        client_cls = ChannelClientFactory._clients.get(str(channel).lower())
        if client_cls is None:
            supported = ", ".join(sorted(ChannelClientFactory._clients))
            raise ValueError(f"Unsupported channel '{channel}'. Supported: {supported}")
        return client_cls()
