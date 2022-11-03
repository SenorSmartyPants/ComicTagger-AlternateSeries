import re, os

#Some important constants
FOLDER = os.path.dirname(os.path.realpath(__file__)) + "/"
SETTINGSFILE = FOLDER + "settings.dat"

def LoadSettings():
	global settings
    #Define some default settings
	settings = {"field" : "Story Arc", "GroupKeywordColon" : "True", "StripLeadingThe" : "False"}

    #The settings file should be formated with each line as SettingName:Value. eg Prefix:Scanner:
	try:
		with open(SETTINGSFILE, 'r') as settingsfile:
			for line in settingsfile:
				match = re.match("(?P<setting>.*?):(?P<value>.*)", line)
				settings[match.group("setting")] = match.group("value").strip()

	except Exception as ex:
		print("Something has gone wrong loading the settings file. The error was: " + str(ex))

	return settings

def SaveSettings(settings):

    with open(SETTINGSFILE, 'w') as settingsfile:
        for setting in settings:
            settingsfile.write(setting + ":" + settings[setting] + "\n")