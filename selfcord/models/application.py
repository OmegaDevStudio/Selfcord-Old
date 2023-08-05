from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api.http import http
    from ..bot import Bot

class Application:
    def __init__(self, AppPayload: dict, http: http):
        self.http: http = http

        self.id = AppPayload.get("id")
        self.name = AppPayload.get("name")
        self.icon = AppPayload.get("icon")
        self.description = AppPayload.get("description")
        # self.bot = something
        self.approximate_guild_count = AppPayload.get("approximate_guild_count")
        self.interactions_event_types = AppPayload.get("interactions_event_types")
        self.interactions_version = AppPayload.get("interactions_version")
        self.explicit_content_filter = AppPayload.get("explicit_content_filter")
        self.rpc_application_state = AppPayload.get("rpc_application_state")
        self.store_application_state = AppPayload.get("store_application_state")
        self.creator_monetization_state = AppPayload.get("creator_monetization_state")
        self.verification_state = AppPayload.get("verification_state")
        self.public = AppPayload.get("integration_public")
        self.requires_oauth = AppPayload.get("integration_require_code_grant")
        self.discoverability_state = AppPayload.get("discoverability_state")
        self.discovery_eligibility_flags = AppPayload.get("discovery_eligibility_flags")

        self.token = None

    async def reset_token(self):
        data = await self.http.request("post", f"/applications/{self.id}/bot/reset")
        self.token = data["token"]

    async def add_redirect_url(self, url: str):
        await self.http.request("patch", f"/applications/{self.id}", json={"redirect_uris":[url],"rpc_origins":[],"custom_install_url":None,"install_params":None})

    # TODO add oauth2 url generator im too lazy to add that entire list
