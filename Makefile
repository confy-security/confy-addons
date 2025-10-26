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

.PHONY: pkgbuild clean build install uninstall srcinfo