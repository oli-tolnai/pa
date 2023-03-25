from onvif import ONVIFCamera
# Replace with the IP address or hostname of your camera
camera = ONVIFCamera('http://192.168.1.231/pages/login.asp', 'admin', 'admin')
#camera = ONVIFCamera('http://192.168.1.100/onvif/device_service', 'username', 'password')

# Replace with the desired preset name
preset_name = 'Preset 1'

# Get the PTZ service
ptz = camera.create_ptz_service()

# Get the current profile
media = camera.create_media_service()
profiles = media.GetProfiles()
profile = profiles[0]

# Get the preset
presets = ptz.GetPresets({'ProfileToken': profile.token})

# Iterate through the presets to find the desired preset
for preset in presets:
    if preset.Name == preset_name:
        # Go to the preset
        ptz.GotoPreset({'ProfileToken': profile.token, 'PresetToken': preset.token})
        print(f'Switched to preset: {preset_name}')
        break
else:
    print(f'Preset {preset_name} not found')