import os
import shutil
from tqdm import tqdm
import urllib.request
import zipfile

chrome_driver_url = "https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_win32.zip"
ffmpeg_driver_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
chrome_name = 'chromedriver.exe'
ffmpeg_name = 'ffmpeg.exe'
folder = 'dependencies'

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def ObtainFromZip(url, destination_folder, file_relative_address, skip_first_folder = False):
    file_split = file_relative_address.split('/')
    file_name = file_split[-1]
    zip_name = '{}/{}'.format(destination_folder, file_name.split(".exe")[0] + ".zip")
            
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=zip_name, reporthook=t.update_to)
    
    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)
    
    if os.path.exists(zip_name):
        os.remove(zip_name)
        
    if skip_first_folder:
        first_folder = [name for name in os.listdir("./{}".format(destination_folder)) if os.path.isdir("{}/{}".format(destination_folder, name))][0]
        file_split.insert(0, first_folder)
        file_split.insert(0, destination_folder)
        os.rename("/".join(file_split), '{}/{}'.format(destination_folder, file_name))
        shutil.rmtree("{}/{}".format(destination_folder, first_folder))
    return
    
def Install():
    os.makedirs(folder, exist_ok=True)
    if not os.path.isfile("{}/{}".format(folder, chrome_name)):
        ObtainFromZip(chrome_driver_url, folder, chrome_name)
        
    if not os.path.isfile("{}/{}".format(folder, ffmpeg_name)):
        ObtainFromZip(ffmpeg_driver_url, folder, 'bin/{}'.format(ffmpeg_name), skip_first_folder = True)

if __name__ == '__main__':
    Install()