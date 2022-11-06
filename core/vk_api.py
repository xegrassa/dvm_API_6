import logging
import urllib.parse
from typing import NamedTuple, Optional

import requests
from requests.exceptions import HTTPError

from core.constant import LOGGER_NAME, VK_BASE_URL

logger = logging.getLogger(LOGGER_NAME)


def _check_vk_response(json: dict):
    if "error" in json:
        error_code = json["error"]["error_code"]
        error_msg = json["error"]["error_msg"]
        raise HTTPError(f'Код ошибки: {error_code}, Сообщение ошибки: {error_msg}')


class UploadedInfo(NamedTuple):
    server: int
    photo: list[dict]
    hash: str


class VKApi:

    def __init__(self, token: str, api_version: str, club_id: Optional[int] = None):
        self.token = token
        self.api_version = api_version
        self.club_id = club_id

    def _get_upload_url(self) -> str:
        """Получение адреса для загрузки фото."""
        url = urllib.parse.urljoin(VK_BASE_URL, "photos.getWallUploadServer")
        params = {
            "access_token": self.token,
            "v": self.api_version,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        json_answer = response.json()

        _check_vk_response(json_answer)

        upload_url = json_answer["response"]["upload_url"]
        return upload_url

    def upload_image(self, img_path: str) -> UploadedInfo:
        """Загрузка фото на сервер."""
        upload_url = self._get_upload_url()

        with open(img_path, 'rb') as f:
            params = {
                "v": self.api_version,
            }
            files = {
                'photo': f,
            }
            response = requests.post(upload_url, params=params, files=files)
            response.raise_for_status()

        _check_vk_response(response.json())
        z = response.json()
        return UploadedInfo(server=z["server"], photo=z["photo"], hash=z["hash"])

    def save_image(self, info: UploadedInfo) -> tuple[str, str]:
        """Сохранение фото в альбоме группы."""
        url = urllib.parse.urljoin(VK_BASE_URL, "photos.saveWallPhoto")

        params = {
            "access_token": self.token,
            "v": self.api_version,

            "server": info.server,
            "photo": info.photo,
            "hash": info.hash,
        }

        response = requests.post(url, params=params)
        response.raise_for_status()

        _check_vk_response(response.json())

        owner_id = response.json()["response"][0]["owner_id"]
        media_id = response.json()["response"][0]["id"]
        return owner_id, media_id

    def publish_record(self, msg: str, owner_id: str, media_id: str) -> None:
        """Публикация записи в группе."""
        url = urllib.parse.urljoin(VK_BASE_URL, "wall.post")

        params = {
            "access_token": self.token,
            "v": self.api_version,

            "message": msg,
            "owner_id": -self.club_id,
            "from_group": "",
            "attachments": f"photo{owner_id}_{media_id}",
        }

        response = requests.post(url, params=params)
        response.raise_for_status()

        _check_vk_response(response.json())

        logger.info("Комикс успешно размещен на стене сообщества")
