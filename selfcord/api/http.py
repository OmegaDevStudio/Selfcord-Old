import httpx
import asyncio
import time
from selfcord.api.errors import LoginFailure


from ..models import User, Client

class http:
    def __init__(self) -> None:
        self.token = None
        self.base_url = "https://discord.com/api/v9"


    def static_login(self, token: str):
        self.token = token
        data = self.request("get", "/users/@me")
        self.client = Client(data)
        return data

    def request(self, method: str, endpoint: str, *args, **kwargs) -> dict:
        url = self.base_url + endpoint

        headers = {
            "authorization": self.token,
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.139 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
            "content-type": "application/json"
        }

        while True:
            with httpx.Client(headers=headers) as client:
                request = getattr(client, method)

                resp = request(url=url, *args, **kwargs)
                if resp.status_code == 429:
                    try:
                        json = resp.json()
                        time.sleep(json["retry_after"])
                    except Exception as e:
                        print(f"Error: {e}")
                        break
                elif resp.status_code == 401:
                    json = resp.json()
                    raise LoginFailure(json, resp.status_codde)
                elif resp.status_code == 403:
                    json = resp.json()
                    raise LoginFailure(json, resp.status_code)
                elif resp.status_code == 201:
                    data = resp.json()
                    break
                elif resp.status_code == 204:
                    data = resp.json()
                    break
                elif resp.status_code == 200:
                    data = resp.json()
                    break
                else:
                    data = resp.json()
                    raise LoginFailure(data, resp.status_code)


        return data

