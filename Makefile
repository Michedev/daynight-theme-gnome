install-user-service:
	cp daynight-gnome-theme.service ~/.local/share/systemd/user/
	systemctl enable --user daynight-gnome-theme.service
	systemctl start --user daynight-gnome-theme.service