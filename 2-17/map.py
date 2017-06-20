import folium
import time
import os
from selenium import webdriver
def GetMap(coord):
        print(coord)
        map_osm = folium.Map(location=[coord[0], coord[1]], zoom_start=15)
        # 마커 지정
        folium.Marker([coord[0], coord[1]], popup='Mt. Hood Meadows').add_to(map_osm)
        # html 파일로 저장\
        delay = 5
        fn = 'osm.html'
        map_osm.save(fn)
        tmpurl = 'file://{path}/{mapfile}'.format(path=os.getcwd(), mapfile=fn)

        browser = webdriver.Chrome('C:/Users/LG/PycharmProjects/tkinter/chromedriver.exe')
        #browser = webdriver.Firefox()
        browser.get(tmpurl)
        # Give the map tiles some time to load
        time.sleep(delay)
        browser.save_screenshot('SearchMap.gif')
        browser.quit()