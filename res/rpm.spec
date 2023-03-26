Name:       zdesk 
Version:    1.2.0
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb libxdo libXfixes alsa-lib curl libappindicator libvdpau1 libva2

%description
The best open-source remote desktop client software, written in Rust. 

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/lib/zdesk/
mkdir -p %{buildroot}/usr/share/zdesk/files/
install -m 755 $HBB/target/release/zdesk %{buildroot}/usr/bin/zdesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/lib/zdesk/libsciter-gtk.so
install $HBB/res/zdesk.service %{buildroot}/usr/share/zdesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/zdesk/files/zdesk.png
install $HBB/res/zdesk.desktop %{buildroot}/usr/share/zdesk/files/
install $HBB/res/zdesk-link.desktop %{buildroot}/usr/share/zdesk/files/

%files
/usr/bin/zdesk
/usr/lib/zdesk/libsciter-gtk.so
/usr/share/zdesk/files/zdesk.service
/usr/share/zdesk/files/zdesk.png
/usr/share/zdesk/files/zdesk.desktop
/usr/share/zdesk/files/zdesk-link.desktop
/usr/share/zdesk/files/__pycache__/*

%changelog
# let's skip this for now

# https://www.cnblogs.com/xingmuxin/p/8990255.html
%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop zdesk || true
  ;;
esac

%post
cp /usr/share/zdesk/files/zdesk.service /etc/systemd/system/zdesk.service
cp /usr/share/zdesk/files/zdesk.desktop /usr/share/applications/
cp /usr/share/zdesk/files/zdesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable zdesk
systemctl start zdesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop zdesk || true
    systemctl disable zdesk || true
    rm /etc/systemd/system/zdesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/zdesk.desktop || true
    rm /usr/share/applications/zdesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
