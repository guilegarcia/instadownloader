# coding=utf-8
import time

from bs4 import BeautifulSoup
from django.shortcuts import render
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


def index(request):
    """
    Exibe a página inicic com o form para buscar fotos instagram
    """
    return render(request, 'index.html')


def instagram(request):
    """
    Recebe a url da foto ou do instagram e pega as fotos
    """
    list_photos = []

    # Firefox private
    # profile = webdriver.FirefoxProfile()
    # # profile.set_preference("browser.privatebrowsing.autostart", True)
    # # driver = webdriver.Firefox(firefox_profile=profile)
    driver = webdriver.PhantomJS(executable_path='/home/guilegarcia/node_modules/phantomjs/lib/phantom/bin/phantomjs')
    driver.get(request.POST['foto'])

    # Scrowdown
    elem = driver.find_element_by_tag_name('html')  # todo testar: driver.execute_script("window.scrollTo(0, Y)") *Y é quanto baixar
    elem.send_keys(Keys.END)

    # Clica in "Load more"
    try:
        element = driver.find_elements_by_link_text("LOAD MORE")
        if element:
            element[0].click()  # Clica no primeiro link
    except NoSuchElementException:
        print "Não achou o elemento"

    # Scrowdown again
    for x in range(0, 20):
        elem = driver.find_element_by_tag_name('html')
        elem.send_keys(Keys.END)
        time.sleep(1)
        elem.send_keys(Keys.HOME)

    # Get the page code
    source = BeautifulSoup(driver.page_source)

    # Get Links photos end save in list_photos
    for link in source.find_all('img'):
        list_photos.append(link.get('src'))

    # Get name of instagram account
    title = source.find('title').string
    title_string = title.replace(" Instagram photos and videos", "")

    driver.close()

    return render(request, 'photos.html',
                  {'list_photos': list_photos, 'title_instagram': title_string})  # 'list_photos': list_photos
