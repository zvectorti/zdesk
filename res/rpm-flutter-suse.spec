Name:       zdesk 
Version:    1.2.0
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils curl libXtst6 libappindicator-gtk3 libvdpau1 libva2
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

%description
The best open-source remote desktop client software, written in Rust. 

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/lib/zdesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/lib/zdesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/zdesk.service -t "%{buildroot}/usr/share/zdesk/files"
install -Dm 644 $HBB/res/zdesk.desktop -t "%{buildroot}/usr/share/zdesk/files"
install -Dm 644 $HBB/res/zdesk-link.desktop -t "%{buildroot}/usr/share/zdesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/zdesk/files/zdesk.png"

%files
/usr/lib/zdesk/*
/usr/share/zdesk/files/zdesk.service
/usr/share/zdesk/files/zdesk.png
/usr/share/zdesk/files/zdesk.desktop
/usr/share/zdesk/files/zdesk-link.desktop

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
ln -s /usr/lib/zdesk/zdesk /usr/bin/zdesk 
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
    rm /usr/bin/zdesk || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
