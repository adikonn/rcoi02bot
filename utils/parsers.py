import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
import logging

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


def print_result(html_content: Dict[str, Any]) -> str:
    """
    Функция для извлечения и вывода таблицы с классом tb_result
    """
    if not html_content['success']:
        return 'error server'

    soup = BeautifulSoup(html_content['response'], 'html.parser')
    table = soup.find('table', class_='tb_result')

    if not table:
        return 'account does not exist. please check and try again'

    res = ''

    # Извлекаем заголовки таблицы
    headers = []
    header_row = table.find('tr')
    if header_row:
        for th in header_row.find_all(['th', 'td']):
            headers.append(th.text.strip())


    # Извлекаем и выводим данные из всех строк
    rows = table.find_all('tr')[1:] if headers else table.find_all('tr')

    for row in rows:
        cells = []
        for td in row.find_all(['td', 'th']):
            cell_data = td.text.strip()
            cells.append(cell_data)

        if cells:
            res += " | ".join(cells) + '\n\n'

    return res


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
            result += f"{s[2]} - {s[4]}\n"

    return result
