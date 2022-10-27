Name:           lipstick2vnc
Summary:        A VNC server for Sailfish OS QA
Version:        0.1
Release:        1
License:        GPLv2+
URL:            https://github.com/mer-qa/lipstick2vnc
Source0:        %{name}-%{version}.tar.bz2
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(libvncserver)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  qt5-qtwayland-wayland_egl-devel
BuildRequires:  oneshot
Requires:       oneshot
Requires:       jolla-sessions-qt5 >= 1.2.7
Requires(pre):  sailfish-setup
#%%%{_oneshot_requires_post}
%{systemd_requires}

%description
%{summary}.

Don't install this package if you care about security.
There is no protection in this VNC server.

%prep
%setup -q -n %{name}-%{version}


%build
%qmake5 CONFIG+=release
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%qmake5_install

# systemd integration
mkdir -p %{buildroot}%{_userunitdir}/sockets.target.wants/
ln -s ../vnc.socket %{buildroot}%{_userunitdir}/sockets.target.wants/vnc.socket

%post
%systemd_user_post stop vnc.service || :
%systemd_user_post daemon-reload || :
%{_bindir}/add-oneshot 20-lipstick2vnc-configurator || :

%preun
%systemd_user_preun vnc.service || :
%systemd_user_preun vnc.socket || :

%postun
%systemd_user_postun

%files
%defattr(-,root,root,-)
%attr(2755, root, privileged) %{_bindir}/%{name}
%attr(755, root, root) %{_oneshotdir}/20-lipstick2vnc-configurator
%{_userunitdir}/vnc.socket
%{_userunitdir}/vnc.service
%{_userunitdir}/sockets.target.wants/vnc.socket
