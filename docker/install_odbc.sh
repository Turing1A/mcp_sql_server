set -e

apt-get update

apt-get install -y \
    curl \
    gnupg2 \
    ca-certificates \
    apt-transport-https

curl -sSL -O https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb

dpkg -i packages-microsoft-prod.deb

rm packages-microsoft-prod.deb

apt-get update

ACCEPT_EULA=Y apt-get install -y \
    msodbcsql18 \
    unixodbc-dev  

apt-get clean

rm -rf /var/lib/apt/lists/*