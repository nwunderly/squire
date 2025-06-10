from auth import CLOUD_CREDS_FILE, CLOUD_PROJ_ID
from google.cloud.translate_v3.services.translation_service import (
    TranslationServiceAsyncClient,
)
from google.cloud.translate_v3.types.translation_service import (
    GetSupportedLanguagesRequest,
    TranslateTextRequest,
)
from google.oauth2.service_account import Credentials


class Translate:
    def __init__(self):
        credentials = Credentials.from_service_account_file(CLOUD_CREDS_FILE)
        self.client = TranslationServiceAsyncClient(credentials=credentials)
        self.lang_cache = {}

    async def get_all_langs(self):
        result = await self.client.get_supported_languages(
            request=GetSupportedLanguagesRequest(
                **{
                    "parent": f"projects/{CLOUD_PROJ_ID}/locations/global",
                    "display_language_code": "en",
                }
            )
        )
        for lang in result.languages:
            self.lang_cache[lang.display_name.lower()] = lang.language_code
            self.lang_cache[lang.language_code] = lang.language_code

    async def convert_lang(self, arg):
        if not self.lang_cache:
            await self.get_all_langs()

        return self.lang_cache.get(arg.lower())

    async def translate(self, text, lang="en"):
        result = await self.client.translate_text(
            TranslateTextRequest(
                **{
                    "parent": f"projects/{CLOUD_PROJ_ID}/locations/global",
                    "contents": [text],
                    "mime_type": "text/plain",  # mime types: text/plain, text/html
                    "target_language_code": lang,
                }
            )
        )
        translation = result.translations[0]
        return translation.translated_text, translation.detected_language_code