destfolder = /usr/bin/

build-standalone-executable-config:
	echo -e "#!/usr/bin/python3\n\n" > daynight_theme_config
	cat daynight_theme_config.py >> daynight_theme_config


build-standalone-executable:
	echo -e "#!/usr/bin/python3\n\n" > daynight_theme
	cat daynight_theme.py >> daynight_theme


install-theme: build-standalone-executable-config build-standalone-executable
	mkdir -p $(destfolder)
	chmod +x daynight_theme_config
	mv daynight_theme_config daynight-theme-config
	sudo mv daynight-theme-config $(destfolder)
	chmod +x daynight_theme
	mv daynight_theme daynight-theme
	sudo mv daynight-theme $(destfolder)


copy-daynight-theme-service:
	mkdir -p ~/.config/systemd/user
	cp daynight-gnome-theme.service ~/.config/systemd/user

enable-daynight-theme-service:
	systemctl enable --user daynight-gnome-theme
	systemctl start --user daynight-gnome-theme

install-daynight-theme-service: copy-daynight-theme-service enable-daynight-theme-service

all: install-theme install-daynight-theme-service