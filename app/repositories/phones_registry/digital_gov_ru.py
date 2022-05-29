import csv
import os
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from app.core.settings import (
	REGISTRY_LINK_CLASS,
	DOWNLOAD_FOLDER,
	CSV_DELIMITER
)
from app.domain.entities.phone_registry_record import PhoneRegistryRecord, DigitRange
from app.domain.exceptions.external_service_exception import ExternalServiceException
from app.domain.exceptions.validation_exception import ValidationException
from .base import AbstractPhonesRegistry


class DigitalGovRu(AbstractPhonesRegistry):
	async def parse_data(self, url: Optional[str] = None):
		"""
		Генератор, который отдает сформированную запись реестра для добавления/обновления в бд.
		"""
		if not url:
			raise ValidationException(msg="No url for parse")

		links = await self.get_links_for_parse(url)

		for link in links:
			# скачиваем файлы
			filename = await DigitalGovRu._download_file(link)

			# возвращаем по одной обработанной записи из файла
			async for processed_records in self._process_file(filename):
				yield processed_records

	async def _process_file(self, filename: str):
		"""
		Генератор, который читает файл и отдает сформированную запись реестра.
		"""
		with open(os.path.join(DOWNLOAD_FOLDER, filename), "r", encoding="utf-8") as f:
			reader = csv.reader(f, delimiter=CSV_DELIMITER)

			for i, line in enumerate(reader):
				if i > 0:
					city = line[5].strip().split("|")[0]
					timezone = await self.region_info_repository.get_timezone(city)

					record = PhoneRegistryRecord(
						prefix=line[0].strip(),
						digit_range=DigitRange(from_=int(line[1].strip()), to_=int(line[2].strip())),
						provider=line[4].strip(),
						region=line[5].strip(),
						timezone=timezone
					)
					yield record

	async def get_links_for_parse(self, url: Optional[str] = None) -> List[str]:
		"""
		Получение данных для дальнейшего парсинга.
		Возвращает список ссылок на файлы, которые содержат данные регистра.
		"""
		if not url:
			raise ValidationException(msg="No url for parse")

		page = requests.get(url)

		if page.status_code != 200:
			raise ExternalServiceException(msg=f"service on url: {url} is unavailable")

		soup = BeautifulSoup(page.text, "html.parser")

		links = []
		for link in soup.findAll("a", class_=REGISTRY_LINK_CLASS, href=True):
			links.append(link["href"])

		if not links:
			raise ValidationException(msg="No available files to parse")

		return links

	@staticmethod
	async def _download_file(link: str) -> str:
		"""
		Сохраняет файл, и возвращает имя файла.
		"""
		response = requests.get(link, stream=True)
		filename = link.split("/")[-1].split("?")[0]

		with open(os.path.join(DOWNLOAD_FOLDER, filename), "wb") as f:
			for chunk in response.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)

		return filename
