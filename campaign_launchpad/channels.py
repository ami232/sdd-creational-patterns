
from abc import ABC, abstractmethod
from uuid import uuid4
from .budget import GlobalBudget
from .campaign import Campaign


class ChannelClient(ABC):
    # Initial used to prefix external ids, e.g. "g-" for Google Ads.
    id_prefix = ""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def create_campaign(self, campaign: Campaign) -> str:
        # Create a campaign on this channel and return an external id.
        pass

    @abstractmethod
    def pause_campaign(self, campaign_id: str) -> None:
        pass

    def _charge_and_mint_id(self, campaign: Campaign) -> str:
        """
        Shared launch mechanics: take the daily budget out of the one global
        wallet, then mint a channel-prefixed external id. Raises ValueError if
        the budget cannot cover the campaign, in which case no id is issued.
        """
        GlobalBudget().allocate(campaign.daily_budget)
        return f"{self.id_prefix}-{uuid4().hex[:12]}"


class GoogleAdsClient(ChannelClient):
    id_prefix = "g"

    def __init__(self):
        super().__init__("Google Ads")

    def create_campaign(self, campaign: Campaign) -> str:
        external_id = self._charge_and_mint_id(campaign)
        print(f"[{self.name}] launched '{campaign.name}' as {external_id}")
        return external_id

    def pause_campaign(self, campaign_id: str) -> None:
        print(f"[{self.name}] paused {campaign_id}")


class FacebookAdsClient(ChannelClient):
    id_prefix = "f"

    def __init__(self):
        super().__init__("Facebook Ads")

    def create_campaign(self, campaign: Campaign) -> str:
        external_id = self._charge_and_mint_id(campaign)
        print(f"[{self.name}] launched '{campaign.name}' as {external_id}")
        return external_id

    def pause_campaign(self, campaign_id: str) -> None:
        print(f"[{self.name}] paused {campaign_id}")


class ChannelClientFactory:
    # Factory Method: callers ask for a channel by name and get back the right
    # concrete client, without knowing which class implements it.
    _CLIENTS = {
        "google": GoogleAdsClient,
        "facebook": FacebookAdsClient,
    }

    @staticmethod
    def create(channel: str) -> ChannelClient:
        # Return the appropriate client based on the channel.
        key = channel.strip().lower() if isinstance(channel, str) else channel
        if key not in ChannelClientFactory._CLIENTS:
            supported = ", ".join(sorted(ChannelClientFactory._CLIENTS))
            raise ValueError(
                f"Unsupported channel {channel!r}. Supported channels: {supported}."
            )
        return ChannelClientFactory._CLIENTS[key]()
