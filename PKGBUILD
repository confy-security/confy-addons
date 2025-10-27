# Maintainer: Henrique Sebastião <contato@henriquesebastiao.com>

pkgname='python-confy-addons'
_module='confy-addons'
_src_folder='confy_addons-1.1.0'
pkgver='1.1.0'
pkgrel=1
pkgdesc="Implementation of symmetric and asymmetric encryption with AES and RSA algorithms for client applications of the Confy communication system"
url="https://github.com/confy-security/confy-addons"
depends=('python')
makedepends=('python-poetry' 'python-build' 'python-installer' 'python-wheel')
license=('custom:GNU General Public License v3 (GPLv3)')
arch=('any')
source=("https://files.pythonhosted.org/packages/03/ed/5e592c4e409032d9fb2d59e25ed95c4784b1592e259f9f6feb60c8d1372d/confy_addons-1.1.0.tar.gz")
sha256sums=('2236a5df3ebd3f99b33276495324921de140ae83a9cafd71700d1698d0372ae7')

build() {
    cd "${srcdir}/${_src_folder}"
    poetry build -f wheel --no-interaction --no-ansi --no-cache
}

package() {
    cd "${srcdir}/${_src_folder}"

    install -Dm644 -t "${pkgdir}/usr/share/licenses/${pkgname}" LICENSE
    install -Dm644 -t "${pkgdir}/usr/share/doc/${pkgname}" README.md

    python -m installer --destdir="${pkgdir}" dist/*.whl
}
