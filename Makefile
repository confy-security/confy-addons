changelog:
	github_changelog_generator -u confy-security -p confy-addons -o CHANGELOG --no-verbose;

pkgbuild:
	pip2pkgbuild confy_addons -p python -n confy-addon;

build:
	makepkg --syncdeps;

install:
	sudo pacman -U --noconfirm *.zst;

uninstall:
	sudo pacman -Rns --noconfirm python-confy-addons;

clean:
	rm -rf src pkg cli;
	rm -f *.zst;

srcinfo:
	makepkg --printsrcinfo > .SRCINFO;


.PHONY: changelog pkgbuild clean build install uninstall srcinfo