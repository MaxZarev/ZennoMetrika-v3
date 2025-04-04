import requests
from playwright.sync_api import sync_playwright
import random

def open_browser(profile_number: int) -> dict:
    params = dict(serial_number=profile_number)
    url = "http://local.adspower.net:50325/api/v1/browser/start"
    response = requests.get(url, params=params)
    data = response.json()
    return data

def main():
    profile_data = open_browser(949)
    url_connect = profile_data.get('data').get('ws').get('puppeteer')
    pw = sync_playwright().start()
    browser = pw.chromium.connect_over_cdp(url_connect, slow_mo=1000)
    if not browser.is_connected():
        print("Browser not connected")
        exit(1)
    context = browser.contexts[0]
    page = context.pages[0]

    page.set_default_timeout(5000)
    page.goto('https://pancakeswap.finance/swap?chain=polygonZkEVM', timeout=30000)

    # поиск элементов с помощью xpath
    button = page.locator('//button[@data-dd-action-name="Select currency"]').first
    button.click()

    # поиск элементов с помощью css
    button = page.locator('button[data-dd-action-name="Select currency"]').first
    button.click()

    # поиск элементов по классу или id
    element = page.locator('.class-value')
    element = page.locator('#id-value')

    # поиск по тегу + класс/id
    element = page.locator('div.class-value')
    element = page.locator('div#id-value')

    # поиск по видимым элементам
    element = page.locator('button:visible')

    # поиск по атрибуту data-testid
    element = page.get_by_test_id('test-id')

    # поиск по тексту
    element = page.get_by_text('Connect Wallet', exact=True)

    # поиск по title
    element = page.get_by_title('title-value')

    # поиск по placeholder
    element = page.get_by_placeholder('placeholder-value')

    # поиск по label
    element = page.get_by_label('label-value')

    # поиск по alt картинки
    image = page.get_by_alt_text('alt-value')

    # поиск по role
    element = page.get_by_role('button', name='text', exact=True)

    # поиск внутри ранее найденных локаторов
    element = page.get_by_role('dialog').get_by_text('ETH', exact=True).first

    # вторичный поиск элементов внутри ранее найденных элементов
    elements = element.locator('div')
    element = elements.get_by_text('text-value', exact=True).first

    # поиск по двум условиям оператор И
    element = element.locator('div').and_(locator=page.locator('button'))

    # поиск по двум условиям оператор ИЛИ
    element = element.locator('div').or_(locator=page.locator('button'))

    # фильтрация ранее найденных элементов
    elements = element.locator('div')
    element = elements.filter(has_text='text-value').first

    # получение списка локаторов
    buttons = page.locator('button').all()
    for button in buttons:
        button.hover()

    # количество элементов по заданному поиску
    page.locator('button').count()

    connect = page.get_by_role('button', name='Connect Wallet').first

    # использование как проверки существования элемента
    if connect.count():
        connect.click()
        # описываем логику подключения кошелька

    # проверка видимости элемента
    if connect.is_visible():
        connect.click()
        # описываем логику подключения кошелька

    # ожидание состояния элемента, вызывает ошибка если не достигнуто
    connect.wait_for(state='visible', timeout=5000)

    # получение координат элемента и его размеров
    connect.bounding_box()

    # получение всех текстов внутри элемента
    connect.all_text_contents()

    # получение всех внутренних видимых текстов элемента
    connect.all_inner_texts()

    # получение атрибута элемента
    connect.get_attribute('class')

    # подсветить найденные элементы
    connect.highlight()

    # внутренний html элемента
    connect.inner_html()

    # получение текста элемента
    connect.inner_text()

    # получение видимого текста элемента
    connect.input_value()

    # получение видимого текста элемента
    page.get_by_role('checkbox').first.is_checked()

    # проверка на атрибут disabled
    button.is_disabled()
    for _ in range(100):
        if not button.is_disabled():
            button.click()
            break

    # проверка нет ли атрибута disabled
    button.is_enabled()

    # проверка на возможность ввода текста
    page.get_by_role('textbox').is_editable()

    # проверка на скрытость элемента
    button.is_hidden()




















if __name__ == '__main__':
    main()
