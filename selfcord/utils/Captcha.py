from twocaptcha import TwoCaptcha


# Use https://2captcha.com/?from=15127673
class CaptchaSolver:
    def __init__(self, api_key: str,
                 site_key: str = "4c672d35-0701-42b2-88c3-78380b0db560",
                 site_url: str = "discord.com"
                 ):
        self.two_captcha = TwoCaptcha(apiKey=api_key)
        self.site_key = site_key
        self.site_url = site_url

    async def _get_captcha_solution(self):
        try:
            solution = await self.two_captcha.hcaptcha(sitekey=self.site_key, url=self.site_url)
            return solution
        except Exception as e:
            print(f"Failed to get captcha solution {e}")  # Replace this with your logger
            return None

    async def solve_captcha(self):
        return await self._get_captcha_solution()
