if [[ $USER == makerpm ]]; then
  unset verl
  unset verc
  unset rel
  if ! [[ -d $HOME/atom ]]; then
    git clone https://github.com/atom/atom $HOME/atom
  fi
  pushd ~/atom
  git checkout stable
  git pull origin stable
  verl=$(git describe --tags | sed 's/^v//;s/-/./g')
  popd
  verc=$(sed -n 's/Version:\s\s\s\s\s\s\s\s*//p' SPECS/atom.spec)
  rel=$(sed -n 's/Release:\s\s\s\s\s\s\s\s*//p' SPECS/atom.spec)
  if [[ $verc == $verl ]]; then
    echo "Atom is up-to-date"
  else
    sed -i -e "s/Version:\s\s\s\s\s\s\s\s$verc/Version:\s\s\s\s\s\s\s\s$verl/g" SPECS/atom.spec
    rm SOURCES/v$verc.tar.gz
    wget -c https://github.com/atom/atom/archive/v$verl.tar.gz -O- > SOURCES/v$verl.tar.gz
    rpmbuild -ba SPECS/atom
    read -p "Do you wish to install Atom $verl?" yn
    case $yn in
        [Yy]* ) sudo zypper in -y /home/makerpm/rpmbuild/RPMS/$CPU/atom-$verl-$rel.$CPU.rpm; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
  fi
else
  echo "You need to be logged into the mock account makerpm to work with this package"
fi
