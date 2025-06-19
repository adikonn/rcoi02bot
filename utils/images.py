import matplotlib.font_manager as fm
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
def create_table_image(headers, data, cell_width=120, cell_height=40):
    """
    Создает изображение таблицы на основе CSS стилей tb_result

    Args:
        headers: список заголовков
        data: список списков с данными таблицы
        cell_width: ширина ячейки
        cell_height: высота ячейки
    """
    result = BytesIO()
    # Цвета из CSS
    header_bg_color = "#5ab97f"  # Фон заголовков
    cell_border_color = "#e4e4e4"  # Цвет границ ячеек
    text_color = "#000000"  # Цвет текста
    cell_bg_color = "#ffffff"  # Фон ячеек данных

    # Размеры таблицы
    rows = len(data) + 1  # +1 для заголовков
    cols = len(headers)

    table_width = cols * cell_width
    table_height = rows * cell_height

    # Создаем изображение
    img = Image.new('RGB', (table_width, table_height), 'white')
    draw = ImageDraw.Draw(img)

    # Загружаем шрифт (используем системный или укажите путь к шрифту)
    try:
        font_bold = ImageFont.truetype(fm.findfont(fm.FontProperties(family='DejaVu Sans')), 14)
        font_regular = ImageFont.truetype(fm.findfont(fm.FontProperties(family='DejaVu Sans')), 12)
    except:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()

    # Рисуем заголовки
    for col, header in enumerate(headers):
        x = col * cell_width
        y = 0

        # Фон заголовка
        draw.rectangle([x, y, x + cell_width, y + cell_height],
                       fill=header_bg_color, outline=cell_border_color)

        # Текст заголовка (жирный, по центру)
        text_bbox = draw.textbbox((0, 0), header, font=font_bold)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = x + (cell_width - text_width) // 2
        text_y = y + (cell_height - text_height) // 2

        draw.text((text_x, text_y), header, fill=text_color, font=font_bold)

    # Рисуем данные
    for row_idx, row_data in enumerate(data):
        for col_idx, cell_data in enumerate(row_data):
            x = col_idx * cell_width
            y = (row_idx + 1) * cell_height  # +1 для заголовков

            # Фон ячейки
            draw.rectangle([x, y, x + cell_width, y + cell_height],
                           fill=cell_bg_color, outline=cell_border_color)

            # Текст ячейки (по центру)
            cell_text = str(cell_data)

            # Обрезаем текст если он слишком длинный
            if len(cell_text) > 15:
                cell_text = cell_text[:12] + "..."

            text_bbox = draw.textbbox((0, 0), cell_text, font=font_regular)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            text_x = x + (cell_width - text_width) // 2
            text_y = y + (cell_height - text_height) // 2

            draw.text((text_x, text_y), cell_text, fill=text_color, font=font_regular)
    img.save(result, format='PNG')
    result.seek(0)
    return result
