from onvif import ONVIFCamera

# Set the IP address and port of the camera
IP_ADDRESS = "192.168.1.100"
PORT = 80

# Set the username and password for the camera
USERNAME = "admin"
PASSWORD = "password"

# Create an ONVIFCamera object
cam = ONVIFCamera(IP_ADDRESS, PORT, USERNAME, PASSWORD)

# Get the PTZ service
ptz = cam.create_ptz_service()

# Get the current PTZ status
status = ptz.GetStatus()

# Print the current PTZ status
print(status)