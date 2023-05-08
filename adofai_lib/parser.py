import json

class ADOFAIParser:
    chartActions = [
        "Twirl", "SetSpeed", "Hold", "Pause", # Basic Chart Actions
        "EditorComment", "Bookmark", "SetPlanetRotation", "ScaleRadius", "ScalePlanets", "PositionTrack" # Extra Chart Actions
    ]

    def __init__(self, file):
        self.file = file
        self.content = ""
        self.parsed = {"parsed": False}
    
    def parse(self):
        self.content = self.file.read()
        if self.content[0] == u'\ufeff':
            self.content = self.content[1:]

        self.content = self.content.replace(", },\n", "},\n")
        self.parsed = json.loads(self.content)
        return self.parsed
    
    def getChartData(self):
        angleData = self.parsed["angleData"]
        settings = self.parsed["settings"]

        actions = []
        for action in self.parsed["actions"]:
            if action["eventType"] in ADOFAIParser.chartActions:
                actions.append(action)

        return {"angleData": angleData, "settings": settings, "actions": actions}
    
    def getDefaultWith(self, data):
        angleData = [0 for i in range(10)]
        if "angleData" in data:
            angleData = data["angleData"]
        
        settings = {
            "requiredMods": [], # Mod Settings
		    "version": 12, # ADOFAI Level File Version
		    "artist": "", "specialArtistType": "None", "artistPermission": "", "song": "", "author": "", # Basic Level Settings
		    "previewImage": "", "previewIcon": "", "previewIconColor": "003f52", "previewSongStart": 0, "previewSongDuration": 10, # Preview Settings
		    "seizureWarning": "Disabled", # Warning Settings
		    "levelDesc": "", "levelTags": "", "artistLinks": "", "difficulty": 1, # Level Desc Settings
		    "songFilename": "", # Music File
		    "bpm": 100, "volume": 100, "offset": 0, "pitch": 100, # Music Settings
		    "hitsound": "Kick", "hitsoundVolume": 100, # Hitsound Settings
		    "countdownTicks": 4, "separateCountdownTime": "Enabled", # Level Countdown Settings
		    "trackColor": "debb7b", "secondaryTrackColor": "ffffff", "trackStyle": "Standard", "trackGlowIntensity": 100, # Track Color Settings
		    "trackColorType": "Single", "beatsAhead": 3, "trackDisappearAnimation": "None", "beatsBehind": 4, "trackAnimation": "None", "trackColorAnimDuration": 2, "trackColorPulse": "None", "trackPulseLength": 10, # Track Animation Settings
		    "backgroundColor": "000000", "showDefaultBGIfNoImage": "Enabled", "bgImage": "", "bgImageColor": "ffffff", # Background Settings
            "parallax": [100, 100], "bgDisplayMode": "FitToScreen", "lockRot": "Disabled", "loopBG": "Disabled", "unscaledSize": 100, # Background Extra Settings
		    "relativeTo": "Player", "position": [0, 0], "rotation": 0, "zoom": 100, "pulseOnFloor": "Enabled", "startCamLowVFX": "Disabled",
		    "bgVideo": "", "loopVideo": "Disabled", "vidOffset": 0, # Video Background Settings
		    "floorIconOutlines": "Disabled", "stickToFloors": "Enabled", # Floor Settings
		    "planetEase": "Linear", "planetEaseParts": 1, "planetEasePartBehavior": "Mirror", # Planet Settings
		    "legacyFlash": False, "legacyCamRelativeTo": False, "legacySpriteTiles": False, # Legacy Settings
            "customClass": "", # Useless Dev Settings
	    }

        if "settings" in data:
            settings = data["settings"]

        actions = []
        if "actions" in data:
            actions = data["actions"]

        decorations = []
        if "decorations" in data:
            decorations = data["decorations"]

        return {"angleData": angleData, "settings": settings, "actions": actions, "decorations": decorations}
