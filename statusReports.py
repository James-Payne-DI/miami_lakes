import os
import config
#Format:
#{"Title":{'post_data':data,'error_list':[],'image_file_paths':image_file_paths}
#data - from scrape.py controller functions

GLOBAL_STATUS_REPORT = {}

#Creates The Status Report .txt file and saves it to your desktop
def create_status_report(GSP):
    gsp_path = config.DESKTOP_PATH + '/' + config.dealership_name + '_' + 'REST_run_report'
    if os.path.exists(gsp_path):
        os.remove(gsp_path)
        print("››› Deleting '" + gsp_path + "' file that was created prior to this run ...")
    with open(gsp_path, 'w') as file:
        post_counter = 0
        for post in GSP:
            post_counter += 1
            file.write('\n\n\n\n#' + str(post_counter)+ "_"*100 + '\n')
            file.write(post)
            for item in GSP[post]:
                file.write('\n\n--»' + str(item) + ' |\t')
                file.write(str(GSP[post][item]))


        file.close()


def specialPrint(print_me, location):
    print("‹◊› ALERT__________from:[{}]".format(str(location)))
    print(print_me)
    print("˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜\n")

def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)

    return list
def getComporableSlug(slug):
    slug_dict = {
    '/new-vehicles-miami-lakes-fl/':'/new-vehicles/',
    '/new-vehicle-sales-miami-lakes-fl/':'/new-vehicles/new-vehicle-specials/',
    '/new-chevrolet-miami-lakes-fl/':'/new-vehicles/chevrolet/',
    '/new-chrysler-miami-lakes-fl/':'/new-vehicles/chrysler/',
    '/new-dodge-miami-lakes-fl/':'/new-vehicles/dodge/',
    '/new-jeep-miami-lakes-fl/':'/new-vehicles/jeep/',
    '/new-ram-miami-lakes-fl/':'/new-vehicles/ram/',
    '/new-kia-miami-lakes-fl/':'/new-vehicles/kia/',
    '/new-mitsubishi-miami-lakes-fl/':'/new-vehicles/mitsubishi/',
    '/used-vehicles-miami-lakes-fl/':'/used-vehicles/',
    '/used-car-sales-miami-lakes-fl/':'/used-vehicles/used-vehicle-specials/',
    # '/used-alfa-romeo-miami-lakes-fl/':'',
    # '/used-audi-miami-lakes-fl/':'',
    # '/used-cadillac-miami-lakes-fl/':'',
    # '/used-dodge-miami-lakes-fl/':'',
    # '/used-ford-miami-lakes-fl/':'',
    # '/used-chevrolet-miami-lakes-fl/':'',
    # '/used-gmc-miami-lakes-fl/':'',
    # '/used-honda-miami-lakes-fl/':'',
    # '/used-hyundai-miami-lakes-fl/':'',
    # '/used-infiniti-miami-lakes-fl/':'',
    # '/used-jeep-miami-lakes-fl/':'',
    # '/used-kia-miami-lakes-fl/':'',
    # '/used-lexus-miami-lakes-fl/':'',
    # '/used-mazda-miami-lakes-fl/':'',
    # '/used-mercedes-benz-miami-lakes-fl/':'',
    # '/used-mini-miami-lakes-fl/':'',
    # '/used-mitsubishi-miami-lakes-fl/':'',
    # '/used-nissan-miami-lakes-fl/':'',
    # '/used-genesis-miami-lakes-fl/':'',
    # '/used-porsche-miami-lakes-fl/':'',
    # '/used-ram-miami-lakes-fl/':'',
    # '/used-subaru-miami-lakes-fl/':'',
    # '/used-tesla-miami-lakes-fl/':'',
    # '/used-toyota-miami-lakes-fl/':'',
    # '/used-volkswagen-miami-lakes-fl/':'',
    '/used-vehicles-miami-lakes-fl?isCertified=1/':'/used-vehicles/certified-pre-owned-vehicles/',
    '/used-vehicles-miami-lakes-fl?isCertified=1':'/used-vehicles/certified-pre-owned-vehicles/',
    '/vehicle-financing-miami-lakes-fl/':'/finance/',
    '/car-service-in-miami-lakes-fl/':'/service/',
    '/schedule-car-maintenance-or-auto-repair-miami-lakes-fl/':'/service/schedule-service/',
    '/auto-parts-in-miami-lakes-fl/':'/parts/',
    '/trade-appraisal-miami-lakes-fl/':'/value-your-trade/'
    }
    key_list = getList(slug_dict)
    for key in key_list:
        if str(key) == str(slug):
            print(str(key)," »»» ",slug_dict[key])
            return (slug_dict[key])
    return slug


#test Links Miami Lakes Auto Mall ------ BLOG
# https://www.miamilakesautomall.com/ram-blog/ram-unveils-the-all-new-2022-ram-1500-trx-sandblast-edition/
# https://www.miamilakesautomall.com/mitsubishi-blog/spice-up-thanksgiving-with-this-thai-soup-recipe/
# https://www.miamilakesautomall.com/jeep-blog/jeep-grand-cherokee-4xe-earns-green-4x4-of-the-year/
# https://www.miamilakesautomall.com/dodge-blog/dodge-debuts-803-horsepower-king-daytona-charger/
# https://www.miamilakesautomall.com/chrysler-blog/all-of-the-ways-to-benefit-from-chryslers-extended-warranty/
# https://www.miamilakesautomall.com/ram-blog/3-reasons-to-consider-the-2023-ram-2500-rebel/
# https://www.miamilakesautomall.com/ram-blog/2024-ram-1500-ev-clay-model-shows-expected-design/
# https://www.miamilakesautomall.com/ram-blog/all-electric-ram-pickup-dubbed-ram-1500-rev/
# https://www.miamilakesautomall.com/ram-blog/understand-car-eligible-buyback-program/
# https://www.miamilakesautomall.com/ram-blog/2-ram-truck-concepts-named-best-rock-crawling-trucks-2016/
# https://www.miamilakesautomall.com/ram-blog/4x4-awd-trucks-suvs-offer-performance-roading-capabilities/
# https://www.miamilakesautomall.com/ram-blog/the-seven-year-itch-is-no-match-for-the-ram-1500/
