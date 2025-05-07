from naoqi import ALProxy
from PIL import Image
import paramiko
import os

# Define paths and robot login
image_path = '/data/home/nao/images/image_test.png'
robot_IP = '172.18.16.53'
robot_username = 'nao'
robot_password = 'nao'

# Path on your host machine
local_folder = 'C:/Users/callu/Documents/MsC Robotics and AI/Deep Learning/Test'
local_image_path = os.path.join(local_folder, 'image_test.png')

# Capture the image on the NAO robot
try:
    photoCaptureProxy = ALProxy("ALPhotoCapture", robot_IP, 9559)
    photoCaptureProxy.setResolution(2)  # VGA
    photoCaptureProxy.setPictureFormat("png")
    photoCaptureProxy.takePictures(1, "/data/home/nao/images", "image_test")
    print("Image captured on NAO robot.")
except Exception as e:
    print("Error capturing image on NAO:", e)
    exit(1)

# Download the image via SSH
try:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(robot_IP, username=robot_username, password=robot_password)
    
    sftp = ssh_client.open_sftp()
    sftp.get(image_path, local_image_path)    
    sftp.close()
    ssh_client.close()

except Exception as e:
    exit(1)
