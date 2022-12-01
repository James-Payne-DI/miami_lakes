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
