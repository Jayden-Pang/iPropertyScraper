import requests
import Configuration.py as con
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as Action

# Property Configuration Section
# 1) Determines the type of houses
properties = ['1-sty-terrace-link-house',  #0
              '2-sty-terrace-link-house',  #1
              '3-sty-terrace-link-house',  #2
              '1-5-sty-terrace-link-house',  #3
              '2-5-sty-terrace-link-house',  #4
              '3-5-sty-terrace-link-house',  #5
              '4-5-sty-terrace-link-house',  #6
              '4-sty-terrace-link-house',  #7
              'townhouse',  #8
              'cluster-house',  #9
              'bungalow',  #10
              'semi-detached-house',  #11
              'condominium',  #12
              'apartment',  #13
              'flat'  #14
              ]
# 2) Determines the states in Malaysia
states = ['selangor',  #0
          'kuala-lumpur', #1
          'johor', #2
          'penang',  #3
          'perak',  #4
          'negeri-sembilan', #5
          'pahang', #6
          'melaka', #7
          'sabah', #8
          'sarawak', #9
          'kedah', #10
          'putrajaya', #11
          'kelantan', #12
          'terengganu', #13
          'perlis', #14
          'labuan' #15
          ]

def getData (container, type, refer, data_holder) :
    try:
        data = container.find_all(type,class_= refer)[0].text
    except:
        data = "No Data"
    data_holder.append(data)

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
properties = properties[con.property_start:con.property_end+1]
states = states[con.state_start:con.state_end+1]
directory = con.directory
driver = con.driver
segments = list()
cutoff = 0
diff = 100000
while cutoff != 10000000:
    cutoff += diff
    segments.append(str(cutoff))
    if cutoff == 1000000:
        diff = 1000000

column = ['Price', 'Title', 'Size', 'Area', 'Bedroom','Carpark','Bathroom','Url','Connected','Main Address','Sub Address','Type','Built-Up','Land Area','Posted Date','Playground','Security','Google URL']
first_column = column[:8]

for state in states:
    for property in properties:
        prices, titles, sizes, areas, bedrooms, carparks, bathrooms, urls = [], [], [], [], [], [], [], []
        filename = directory + '\\' + property + ' (' + state +').xlsx'
        if os.path.isfile(filename):
            print("Skipped:", filename)
            continue
        for segment in range(len(segments)-1):
            for page in range(1,101):
                print(page)
                print("Lines: " + str(len(titles)))
                if segment == 1:
                    if page == 1:
                        web = 'https://www.iproperty.com.my/sale/' + state + '/'+ property + '/?maxPrice=' + segments[segment]
                    else:
                        web = 'https://www.iproperty.com.my/sale/' + state + '/'+ property + '/?maxPrice=' + segments[segment] + '&page=' + str(page)
                elif segment == len(segments)-1:
                    if page == 1:
                        web = 'https://www.iproperty.com.my/sale/' + state + '/'+ property + '/?minPrice=' + segments[segment+1]
                    else:
                        web = 'https://www.iproperty.com.my/sale/' + state + '/'+ property + '/?minPrice=' + segments[segment+1] + '&page=' + str(page)
                else:
                    if page == 1:
                        web = 'https://www.iproperty.com.my/sale/' + state + '/'+ property +'/?'+'minPrice=' + segments[segment] + '&maxPrice=' + segments[segment+1]
                    else:
                        web = 'https://www.iproperty.com.my/sale/' + state + '/'+ property +'/?'+'minPrice=' + segments[segment] + '&maxPrice=' + segments[segment+1] + '&page=' + str(page)
                response = requests.get(web, headers=headers)
                html_soup = BeautifulSoup(response.text, 'html.parser')
                house_containers = html_soup.find_all('div',class_= 'PremiumCardstyle__DescriptionWrapper-fIqxyF bgYgqk Premium')
                print("House Containers: " + str(len(house_containers)))
                for container in house_containers:
                    #Prices
                    getData(container, 'li', 'ListingPricestyle__ItemWrapper-cBCBVa jXCKCc', prices)

                    #Title
                    getData(container,'h2','PremiumCardstyle__TitleWrapper-cBmVrL ePWFgo',titles)

                    #Size
                    getData(container,'p','ListingAttributesstyle__ListingAttrsDescriptionItemWrapper-fQKuaA fJmpgN attributes-description-item',sizes)

                    #Area
                    getData(container,'div', 'PremiumCardstyle__AddressWrapper-ldsjqp gRJjrp', areas)

                    #Bedroom
                    getData(container, 'li', 'ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF eAeBYm attributes-facilities-item-wrapper bedroom-facility', bedrooms)

                    #Carpark
                    getData(container, 'li', 'ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF eAeBYm attributes-facilities-item-wrapper carPark-facility', carparks)

                    #Bathroom
                    getData(container, 'li', 'ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF eAeBYm attributes-facilities-item-wrapper bathroom-facility', bathrooms)

                    #Url
                    url = "https://iproperty.com.my" + container.find_all('a', class_='depth-listing-card-link')[0].get('href')
                    urls.append(url)

                house_containers_2 = html_soup.find_all('div', class_= 'FeaturedCardstyle__DescriptionWrapper-bQDlAm gjztoh')
                print("House Containers: " + str(len(house_containers_2)))
                for container in house_containers_2:
                    #Prices
                    getData(container, 'li', 'ListingPricestyle__ItemWrapper-cBCBVa jXCKCc', prices)

                    #Title
                    getData(container,'h2','FeaturedCardstyle__TitleWrapper-gWzPBw iWvAMz',titles)

                    #Size
                    getData(container,'p','ListingAttributesstyle__ListingAttrsDescriptionItemWrapper-fQKuaA fJmpgN attributes-description-item',sizes)

                    #Area
                    getData(container,'div', 'FeaturedCardstyle__AddressWrapper-cYWHjq bHEVGg', areas)

                    #Bedroom
                    getData(container, 'li', 'ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF eAeBYm attributes-facilities-item-wrapper bedroom-facility', bedrooms)

                    #Carpark
                    getData(container, 'li', 'ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF eAeBYm attributes-facilities-item-wrapper carPark-facility', carparks)

                    #Bathroom
                    getData(container, 'li', 'ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF eAeBYm attributes-facilities-item-wrapper bathroom-facility', bathrooms)

                    #Url
                    url = "https://iproperty.com.my" + container.find_all('a', class_='depth-listing-card-link')[0].get('href')
                    urls.append(url)


                house_containers_3 = html_soup.find_all('div', class_= 'BasicCardstyle__DescriptionWrapper-fTpXQ evhBND')
                print("House Containers: " + str(len(house_containers_3)))
                for container in house_containers_3:
                    #Prices
                    getData(container, 'li', 'ListingPricestyle__ItemWrapper-cBCBVa cHOkPJ', prices)

                    #Title
                    getData(container,'h2','BasicCardstyle__TitleWrapper-fXYNcq kWrxzR',titles)

                    #Size
                    getData(container,'p','ListingAttributesstyle__ListingAttrsDescriptionItemWrapper-fQKuaA fJmpgN attributes-description-item',sizes)

                    #Area
                    getData(container,'div', 'BasicCardstyle__AddressWrapper-eNdohY bzzAbF', areas)

                    #Bedroom
                    getData(container, 'li', 'ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF hVUBeP attributes-facilities-item-wrapper bedroom-facility', bedrooms)

                    #Carpark
                    getData(container, 'li', 'ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF hVUBeP attributes-facilities-item-wrapper carPark-facility', carparks)

                    #Bathroom
                    getData(container, 'li', 'ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF hVUBeP attributes-facilities-item-wrapper bathroom-facility', bathrooms)

                    #Url
                    url = "https://iproperty.com.my" + container.find_all('a', class_='depth-listing-card-link')[0].get('href')
                    urls.append(url)

                time.sleep(random.randint(0,1))

                if len(house_containers)+len(house_containers_2)+len(house_containers_3) == 0:
                    break

        first_listing = pd.DataFrame({'Price': prices,
                                      'Title': titles,
                                      'Size': sizes,
                                      'Area': areas,
                                      'Bedroom': bedrooms,
                                      'Carpark': carparks,
                                      'Bathroom': bathrooms,
                                      'Url': urls})[first_column]
        first_listing.to_excel(filename)

    stopper = 5000

    for property in properties:
        connecteds, main_address, sub_address, property_type, built_up, land_area, posted_date, playground, security, google_url = [], [], [], [], [], [], [], [], [], []
        filename = directory + '\\' + property + ' (' + state + ').xlsx'
        data = pd.read_excel(filename)
        target_url_list = data['Url'].tolist()
        file_name_3 = directory + '\\' + property + ' (' + state + ') Complete_end.xlsx'
        if os.path.isfile(file_name_3):
            print("Skipped:", file_name_3)
            continue
        url = 0
        while url < len(target_url_list):
            print(url)
            if url % stopper == 0:
                if url != 0 and len(connecteds) != 0:
                    start = url-stopper
                    end = url
                    filename_2 = directory + '\\' + property + ' (' + state + ') Complete_' + str(url) + '.xlsx'
                    listing = pd.DataFrame({'Price': data['Price'][start:end],
                                            'Title': data['Title'][start:end],
                                            'Size': data['Size'][start:end],
                                            'Area': data['Area'][start:end],
                                            'Bedroom': data['Bedroom'][start:end],
                                            'Carpark': data['Carpark'][start:end],
                                            'Bathroom': data['Bathroom'][start:end],
                                            'Url': data['Url'][start:end],
                                            'Connected': connecteds,
                                            'Main Address': main_address,
                                            'Sub Address': sub_address,
                                            'Type': property_type,
                                            'Built-Up': built_up,
                                            'Land Area': land_area,
                                            'Posted Date': posted_date,
                                            'Playground': playground,
                                            'Security': security,
                                            'Google URL': google_url})[column]
                    listing.to_excel(filename_2)
                    print('Saved: ' + filename_2)
                    connecteds, main_address, sub_address, property_type, built_up, land_area, posted_date, playground, security, google_url = [], [], [], [], [], [], [], [], [], []

                check_file = str((url+stopper))
                check_file_name = directory + '\\' + property + ' (' + state + ') Complete_' + check_file + '.xlsx'
                if os.path.isfile(check_file_name):
                    print("Skipped:", check_file_name)
                    url += stopper
                    continue
            connect_url = target_url_list[url]
            attribute_checker = {"Property Type": "No Data", "Built-up Size": "No Data", "Land Area Size": "No Data", "Posted Date": "No Data"}
            facilities_checker = {"Playground": "No", "24-hours security": "No"}
            try:
                response = requests.get(connect_url, headers=headers)
                html_soup = BeautifulSoup(response.text, 'html.parser')
                connecteds.append("True")
            except:
                connecteds.append("False")
                property_type.append("Not Connected")
                built_up.append("Not Connected")
                land_area.append("Not Connected")
                posted_date.append("Not Connected")
                playground.append("Not Connected")
                security.append("Not Connected")
                google_url.append("Not Connected")
                url += 1
                continue

            #MainAddress
            getData(html_soup, 'h1','PropertySummarystyle__ProjectTitleWrapper-kAhflS PNQmp',main_address)

            #SubAddress
            getData(html_soup, 'span', 'property-address sale-default', sub_address)

            attribute_containers = html_soup.find_all('div', class_='PropertyDetailsListstyle__AttributeItemContainer-dPQXaS GilNZ')
            count = 0
            for attribute in attribute_containers:
                x = attribute.text.split(":")[0]
                if x in attribute_checker:
                    attribute_checker[x] = attribute.text.split(":")[1]
                    count += 1
                if count == 4:
                    break
            property_type.append(attribute_checker["Property Type"])
            built_up.append(attribute_checker["Built-up Size"])
            land_area.append(attribute_checker["Land Area Size"])
            posted_date.append(attribute_checker["Posted Date"])

            facilities_container = html_soup.find_all('div',class_= 'AttributeItemstyle__AttributeItemContainer-huepXU giYSnN')
            count = 0
            for facilities in facilities_container:
                x = facilities.text
                if x in facilities_checker:
                    facilities_checker[x] = "Yes"
                    count += 1
                if count == 2:
                    break
            playground.append(facilities_checker["Playground"])
            security.append(facilities_checker["24-hours security"])

            map_container = html_soup.find_all('div',class_= 'GoogleMapstyle__ExploreAllMask-dnTfEe fXfIve mask-explore-all')
            if len(map_container) == 0:
                google_url.append("No Data")
                url += 1
                continue
            else:
                driver = webdriver.Chrome(driver)
                driver.get(connect_url)
                xpath_1 = '/html/body/div[@class="page-content"]/div[@id="app"]/div/div[@class="DetailContainerstyle__DetailWrapper-gOTxDn fJCHkB"]/div[@class="ListingDetailstyle__Detail-leUXpB davqsX"]/div[@class="ListingDetailstyle__MainContainer-fckUjw dsRKkO"]/div[@class="ListingDetailstyle__LeftContainerWrapper-kzCUBn dYqgCF"]/div[@class="ListingDetailstyle__PropertyInfo-nYNvB hfNcQw"]/div[@class="ListingDetailstyle__MainContentContainer-groYjV dMOnQB"]/div/div[@class="ListingDetailstyle__ListingMapWrapper-dNtLGB gVUHqq"]/div[@class="ListingDetailstyle__GoogleMapWrapper-iHDAwO jlHBmg google-map-wrapper ppp-section-item"]/div[@class="GoogleMapstyle__MapContainer-PXlA-d eNEal"]'
                xpath_2 = '/html/body/div[@class="page-content"]/div[@id="app"]/div/div[@class="DetailContainerstyle__DetailWrapper-gOTxDn fJCHkB"]/div[@class="ListingDetailstyle__Detail-leUXpB davqsX"]/div[@class="ImageCoveragestyle__ImageCoverageWrapper-gsZOXs jwyxKA"]/div[@class="ImageCoveragestyle__ImageBarGroupWrapper-cVZbkU cjWWkH"]/div[@class="image-bar-nav-items"]/div[@class="ImageModalstyle__ImageModalWrapper-exUdZA dopBTz"]/ div[@class="ImageModalstyle__ImageModalMainContainer-jUoGFT fMAvqW"]/div[@class="map-container"]/div[@class="GoogleMapstyle__MapContainer-PXlA-d eNEal"]/div[@class="GoogleMapViewSwitchstyle__ViewSwitchWrapper-ihipMR cUnBvu"]/ul/li[2]'
                xpath_3 = '/html/body/div[@class="page-content"]/div[@id="app"]/div/div[@class="DetailContainerstyle__DetailWrapper-gOTxDn fJCHkB"]/div[@class="ListingDetailstyle__Detail-leUXpB davqsX"]/div[@class="ImageCoveragestyle__ImageCoverageWrapper-gsZOXs jwyxKA"]/div[@class="ImageCoveragestyle__ImageBarGroupWrapper-cVZbkU cjWWkH"]/div[@class="image-bar-nav-items"]/div[@class="ImageModalstyle__ImageModalWrapper-exUdZA dopBTz"]/ div[@class="ImageModalstyle__ImageModalMainContainer-jUoGFT fMAvqW"]/div[@class="map-container"]/div[@class="GoogleMapstyle__MapContainer-PXlA-d eNEal"]/div[@class="google-map-box-fullHeight"]/div[@class="gm-style"]/div[2]/div[2]/div[@class="gm-iv-address"]/div[@class="gm-iv-address-link"]'

                try:
                    locator = driver.find_element(By.XPATH, xpath_1)
                except:
                    google_url.append("No Data")
                    driver.quit()
                    url += 1
                    continue
                driver.execute_script('arguments[0].scrollIntoView();', locator)
                Action(driver).move_to_element_with_offset(locator, 0, 0)
                locator.click()

                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath_2)))
                except:
                    google_url.append("No Data")
                    driver.quit()
                    url += 1
                    continue
                locator2 = driver.find_element(By.XPATH, xpath_2)
                Action(driver).move_to_element_with_offset(locator2, 0, 0)
                locator2.click()

                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath_3)))
                except:
                    google_url.append("No Data")
                    driver.quit()
                    url += 1
                    continue
                locator3 = driver.find_element(By.XPATH, xpath_3)
                Action(driver).move_to_element_with_offset(locator3, 0, 0)
                locator3.click()

                try:
                    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
                except:
                    google_url.append("No Data")
                    driver.quit()
                    url += 1
                    continue
                try:
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    google_url.append(driver.current_url)
                except:
                    google_url.append("No Data")
                    driver.quit()
                    url += 1
                    continue
                driver.quit()
            url += 1

        length = len(data['Price'])-(len(data['Price'])%stopper)
        listing = pd.DataFrame({'Price': data['Price'][length:],
                                'Title': data ['Title'][length:],
                                'Size': data['Size'][length:],
                                'Area': data['Area'][length:],
                                'Bedroom': data['Bedroom'][length:],
                                'Carpark': data['Carpark'][length:],
                                'Bathroom': data['Bathroom'][length:],
                                'Url': data['Url'][length:],
                                'Connected': connecteds,
                                'Main Address': main_address,
                                'Sub Address': sub_address,
                                'Type': property_type,
                                'Built-Up': built_up,
                                'Land Area': land_area,
                                'Posted Date': posted_date,
                                'Playground': playground,
                                'Security': security,
                                'Google URL': google_url})[column]
        listing.to_excel(file_name_3)
        print('Saved: ' + file_name_3)


