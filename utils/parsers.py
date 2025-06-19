from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
import logging
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from io import BytesIO
logger = logging.getLogger(__name__)


def get_content(family: str, name: str, father: str, number: str, class_: str = '11') -> Dict[str, Any]:
    """
    Выполняет POST запрос к rcoi02.ru и сохраняет ответ в HTML файл
    """
    url = f"https://rcoi02.ru/gia{class_}_result/lk/pageall.php"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://rcoi02.ru',
        'priority': 'u=0, i',
        'referer': f'https://rcoi02.ru/gia{class_}_result/',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    form_data = {
        'family': family,
        'name': name,
        'father': father,
        'number': number,
        'region': 'Республика Башкортостан',
        'pd': 'on',
        'do': 'Войти'
    }

    try:
        response = requests.post(url, headers=headers, data=form_data, timeout=30)

        if response.status_code == 200:
            return {
                'success': True,
                'status_code': response.status_code,
                'response': response.text,
                'content_length': len(response.text)
            }
        else:
            logger.error(f"Ошибка запроса. Статус: {response.status_code}")
            return {
                'success': False,
                'status_code': response.status_code,
                'error': f"HTTP {response.status_code}"
            }

    except requests.exceptions.Timeout:
        logger.error("Ошибка: Превышено время ожидания запроса")
        return {'success': False, 'error': 'Timeout'}

    except requests.exceptions.ConnectionError:
        logger.error("Ошибка: Не удалось подключиться к серверу")
        return {'success': False, 'error': 'Connection Error'}

    except Exception as e:
        logger.error(f"Неожиданная ошибка: {str(e)}")
        return {'success': False, 'error': str(e)}

def get_page(family: str, name: str, father: str, number: str, class_: str, page_id: str):
    session = requests.Session()
    url = f"https://rcoi02.ru/gia{class_}_result/lk/pageall.php"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://rcoi02.ru',
        'priority': 'u=0, i',
        'referer': f'https://rcoi02.ru/gia{class_}_result/',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    form_data = {
        'family': family,
        'name': name,
        'father': father,
        'number': number,
        'region': 'Республика Башкортостан',
        'pd': 'on',
        'do': 'Войти'
    }

    try:
        response = session.post(url, headers=headers, data=form_data, timeout=30)
        if response.status_code == 200:
            url = f"https://rcoi02.ru/gia{class_}_result/lk/page.php?id={page_id}"
            try:
                response = session.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    return {
                        'success': True,
                        'response': response.text,
                        'class': class_
                    }
                else:
                    return {
                        'success': False,
                        'error': f"Ошибка: {response.status_code}"
                    }
            except Exception as e:
                return {
                    'success': False,
                    'error': f"Ошибка: {str(e)}"
                }
        else:
            logger.error(f"Ошибка запроса. Статус: {response.status_code}")
            return {
                'success': False,
                'status_code': response.status_code,
                'error': f"HTTP {response.status_code}"
            }

    except requests.exceptions.Timeout:
        logger.error("Ошибка: Превышено время ожидания запроса")
        return {'success': False, 'error': 'Timeout'}

    except requests.exceptions.ConnectionError:
        logger.error("Ошибка: Не удалось подключиться к серверу")
        return {'success': False, 'error': 'Connection Error'}

    except Exception as e:
        logger.error(f"Неожиданная ошибка: {str(e)}")
        return {'success': False, 'error': str(e)}
def print_result(html_content: Dict[str, Any]) -> tuple:
    """
    Функция для извлечения и вывода таблицы с классом tb_result
    """
    if not html_content['success']:
        return 'error server'

    soup = BeautifulSoup(html_content['response'], 'html.parser')
    table = soup.find('table', class_='tb_result')

    if not table:
        return 'account does not exist. please check and try again'


    # Извлекаем заголовки таблицы
    headers = []
    header_row = table.find('tr')
    if header_row:
        for th in header_row.find_all(['th', 'td']):
            headers.append(th.text.strip())


    # Извлекаем и выводим данные из всех строк
    rows = table.find_all('tr')[1:] if headers else table.find_all('tr')
    data = []
    for row in rows:
        cells = []
        for td in row.find_all(['td', 'th']):
            cell_data = td.text.strip()
            cells.append(cell_data)

        if cells:
            data.append(cells)

    return headers, data


def extract_table_tb_result(html_content: Dict[str, Any]) -> str:
    """
    Функция для извлечения и вывода таблицы с классом tb_result
    """
    if html_content['success']:
        html_content_text = html_content['response']
    else:
        return 'error server'

    soup = BeautifulSoup(html_content_text, 'html.parser')
    table = soup.find('table', class_='tb_result')

    if not table:
        return 'account does not exist. please check and try again'

    # Извлекаем заголовки таблицы
    headers = []
    header_row = table.find('tr')
    if header_row:
        for th in header_row.find_all(['th', 'td']):
            headers.append(th.text.strip())

    # Извлекаем и выводим данные из всех строк
    rows = table.find_all('tr')[1:] if headers else table.find_all('tr')
    strs = []
    for row in rows:
        cells = []
        for td in row.find_all(['td', 'th']):
            cell_data = td.text.strip()
            cells.append(cell_data)
        if cells:
            strs.append(cells)

    result = ''
    for s in strs:
        if len(s) >= 5:
            word = 'баллов'
            i = s[4]
            if not s[4].isdigit():
                word = ''
            elif i == '100':
                word = 'баллов'
            elif 10 <= int(i) <= 20:
                word = 'баллов'
            elif i[-1] == '1':
                word = 'баллов'
            elif 2<= int(i[-1]) <= 4:
                word = 'балла'
            elif 5 <= int(i[-1]) <= 9:
                word = 'баллов'



            result += f"*{s[2]}* - {s[4]} {word}\n"
    return result
def extract_page_info(html_content: Dict[str, Any]):
    """
    Извлекает информацию о страницах (название и ID) - ИСПРАВЛЕННАЯ ВЕРСИЯ
    """

    pages_info = []
    soup = BeautifulSoup(html_content['response'], 'html.parser')
    links = soup.find_all('a', href=True)

    for link in links:
        href = link['href']
        if 'page.php?id=' in href:
            try:
                # ИСПРАВЛЕНИЕ: правильное извлечение ID
                page_id = href.split('id=')[1].split('&')[0]
                page_title = link.get_text(strip=True)

                pages_info.append({
                    'id': f"id{page_id}",
                    'title': page_title,
                })
            except IndexError:
                continue

    return pages_info


def create_inline_keyboard(data_list):
    """
    Создает InlineKeyboardMarkup из списка словарей

    Args:
        data_list: список словарей вида [{"id": "435234", "title": "Физика"}, ...]

    Returns:
        InlineKeyboardMarkup
    """
    # Создаем список кнопок
    buttons = []
    for item in data_list:
        button = InlineKeyboardButton(
            text=item["title"],
            callback_data=item["id"]
        )
        buttons.append([button])  # Каждая кнопка в отдельной строке

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def download_image_to_bytesio(url: str):
    """
    Скачивает изображение по URL и возвращает объект BytesIO с содержимым изображения.

    Args:
        url: URL изображения

    Returns:
        BytesIO объект с содержимым изображения или сообщение об ошибке
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Создаем BytesIO объект
        image_bytes = BytesIO(response.content)
        image_bytes.seek(0)  # Устанавливаем указатель в начало

        return image_bytes

    except requests.exceptions.RequestException as e:
        return f'Ошибка при скачивании: {str(e)}'
    except Exception as e:
        return f'Неожиданная ошибка: {str(e)}'

def get_images(html_content: Dict[str, Any]):
    images = []
    base_url = f'https://rcoi02.ru/gia{html_content["class"]}_result/lk/'
    soup = BeautifulSoup(html_content['response'], "html.parser")
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            url = urljoin(base_url, src)
            images.append(download_image_to_bytesio(url))
    return images
