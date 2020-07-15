destfolder = ~/.local/share/daynight-gnome-theme

build-standalone-executable-config:
	echo -e "#!/usr/bin/env python3\n\n" > auto_theme_config
	cat auto_theme_config.py >> auto_theme_config


build-standalone-executable:
	echo -e "#!/usr/bin/env python3\n\n" > auto_theme
	cat auto_theme.py >> auto_theme


install-theme: build-standalone-executable-config build-standalone-executable
	mkdir -p $(destfolder)
	chmod +x auto_theme_config
	mv auto_theme_config auto-theme-config
	mv auto-theme-config $(destfolder)
	chmod +x auto_theme
	mv auto_theme auto-theme
	mv auto-theme $(destfolder)


copy-auto-theme-service:
	cp auto-gnome-theme-changer.service ~/.config/systemd/user

enable-auto-theme-service:
	systemctl enable --user auto-gnome-theme-changer
	systemctl start --user auto-gnome-theme-changer

install-auto-theme-service: copy-auto-theme-service enable-auto-theme-service

install-theme-service: install-theme install-auto-theme-service
