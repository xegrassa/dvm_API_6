import logging
import os
import random
import urllib.parse
from tempfile import TemporaryDirectory

import requests
from dotenv import load_dotenv

from core.vk_api import VKApi
from core.constant import LOGGER_NAME, XKCD_BASE_URL, VK_API_VERSION
from core.helpers import check_allow_log_level, configure_logger, download_image

logger = logging.getLogger(LOGGER_NAME)


def get_random_link_and_msg() -> tuple[str, str]:
    """Возвращает ссылку для скачивания комикса и комментарий автора."""
    url = urllib.parse.urljoin(XKCD_BASE_URL, "info.0.json")
    response = requests.get(url)
    response.raise_for_status()

    comics_count = response.json()["num"]
    comics_num = str(random.randint(1, comics_count))
    logger.debug(f"Максимальное кол-во комиксов {comics_count} комикс для скачивания {comics_num}")

    url = urllib.parse.urljoin(XKCD_BASE_URL, f"{comics_num}/info.0.json")
    response = requests.get(url)
    response.raise_for_status()

    comics = response.json()
    return comics['img'], comics['alt']


def main():
    load_dotenv()
    configure_logger(LOGGER_NAME, check_allow_log_level(10))

    vk_access_token = os.getenv("VK_ACCESS_TOKEN")
    vk_club_id = os.getenv("VK_CLUB_ID")

    vk_api = VKApi(token=vk_access_token, api_version=VK_API_VERSION, club_id=int(vk_club_id))

    with TemporaryDirectory() as tmp_dir:
        file_path = os.path.join(tmp_dir, "temp.png")
        image_link, image_alt_msg = get_random_link_and_msg()
        download_image(image_link, file_path)

        info = vk_api.upload_image(img_path=file_path)

        owner_id, media_id = vk_api.save_image(info)
        vk_api.publish_record(msg=image_alt_msg, owner_id=owner_id, media_id=media_id)


if __name__ == '__main__':
    main()
