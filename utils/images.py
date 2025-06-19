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
def create_table_image_blanks(headers, data, narrow_width=60, wide_width=300, medium_width=120, cell_height=40):
    """
    Создает изображение таблицы с разной шириной колонок и переносом текста
    """
    result = BytesIO()

    # Предварительная обработка данных - берем только первые 5 элементов из каждой строки
    processed_data = []
    for row in data[:-1]:
        if len(row) >= len(headers):
            # Берем только количество элементов, соответствующее количеству заголовков
            processed_row = row[:len(headers)]
            processed_data.append(processed_row)
    processed_data.append([data[-1][0], '', '', data[-1][-2], data[-1][-1]])
    # Цвета из CSS
    header_bg_color = "#5ab97f"
    cell_border_color = "#e4e4e4"
    text_color = "#000000"
    cell_bg_color = "#ffffff"

    # Размеры таблицы
    rows = len(processed_data) + 1  # +1 для заголовков
    cols = len(headers)

    # Вычисляем ширину таблицы
    table_width = narrow_width + wide_width + (cols - 2) * medium_width

    try:
        font_bold = ImageFont.truetype(fm.findfont(fm.FontProperties(family='DejaVu Sans')), 14)
        font_regular = ImageFont.truetype(fm.findfont(fm.FontProperties(family='DejaVu Sans')), 12)
    except:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()

    # Функция для переноса текста
    def wrap_text(text, font, max_width):
        words = str(text).split()
        lines = []
        current_line = []

        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)

        for word in words:
            test_line = ' '.join(current_line + [word])
            width = temp_draw.textlength(test_line, font=font)
            if width <= max_width - 10:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)

        if current_line:
            lines.append(' '.join(current_line))

        return lines if lines else ['']

    # Функции для вычисления позиций и размеров
    def get_column_x(col_index):
        x = 0
        for i in range(col_index):
            if i == 0:
                x += narrow_width
            elif i == 1:
                x += wide_width
            else:
                x += medium_width
        return x

    def get_column_width(col_index):
        if col_index == 0:
            return narrow_width
        elif col_index == 1:
            return wide_width
        else:
            return medium_width

    # Вычисляем максимальное количество строк для каждой строки данных
    max_lines_per_row = []
    for row_data in processed_data:
        max_lines_in_row = 1
        for col_idx, cell_data in enumerate(row_data):
            cell_width = get_column_width(col_idx)
            wrapped_lines = wrap_text(str(cell_data), font_regular, cell_width)
            max_lines_in_row = max(max_lines_in_row, len(wrapped_lines))
        max_lines_per_row.append(max_lines_in_row)

    # Вычисляем общую высоту таблицы
    line_height = 18
    table_height = cell_height  # заголовок
    for max_lines in max_lines_per_row:
        row_height = max(cell_height, max_lines * line_height + 10)
        table_height += row_height

    # Создаем изображение
    img = Image.new('RGB', (table_width, table_height), 'white')
    draw = ImageDraw.Draw(img)

    # Рисуем заголовки
    for col, header in enumerate(headers):
        cell_width = get_column_width(col)
        x = get_column_x(col)
        y = 0

        draw.rectangle([x, y, x + cell_width, y + cell_height],
                       fill=header_bg_color, outline=cell_border_color)

        text_bbox = draw.textbbox((0, 0), header, font=font_bold)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = x + (cell_width - text_width) // 2
        text_y = y + (cell_height - text_height) // 2

        draw.text((text_x, text_y), header, fill=text_color, font=font_bold)

    # Рисуем данные с переносом текста
    current_y = cell_height

    for row_idx, row_data in enumerate(processed_data):
        row_height = max(cell_height, max_lines_per_row[row_idx] * line_height + 10)

        for col_idx, cell_data in enumerate(row_data):
            cell_width = get_column_width(col_idx)
            x = get_column_x(col_idx)
            y = current_y

            draw.rectangle([x, y, x + cell_width, y + row_height],
                           fill=cell_bg_color, outline=cell_border_color)

            cell_text = str(cell_data)
            wrapped_lines = wrap_text(cell_text, font_regular, cell_width)

            text_y = y + 5
            for line in wrapped_lines:
                if col_idx == 1:  # широкая колонка
                    text_x = x + 5
                else:
                    text_bbox = draw.textbbox((0, 0), line, font=font_regular)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_x = x + (cell_width - text_width) // 2

                draw.text((text_x, text_y), line, fill=text_color, font=font_regular)
                text_y += line_height

        current_y += row_height

    img.save(result, format='PNG')
    result.seek(0)
    return result
