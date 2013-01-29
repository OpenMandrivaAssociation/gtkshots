%define		sname	gtkShots

Name:		gtkshots
Version:	0.1
Release:	1
Summary:	An utility to capture screenshots continuously
Group:		Graphics
License:	GPLv2+
URL:		http://gtkshots.sourceforge.net
Source:		http://sourceforge.net/projects/gtkshots/files/%{name}/%{version}/%{sname}-%{version}.tar.gz
BuildRequires:	imagemagick
Requires:	pygtk2
Buildarch:	noarch

%description
GTKShots is a python/GTK application to capture screenshots continuosly.
It is a hand tool to automatically save the screenshots in a (un)specified
period of time, with the possibility to schedule it and to choose options
for each screenshot to be saved, such as the size, the parent folder and
the time interval between them.

GTKShots could be used for a lot of different aims, for instance to create
presentations, to monitor desktop activity, or for any other scope that
needs a screenshots sequence.

GTKShots is actually a GUI frontend to pyshots, my command-line python
script to do the same job. Thus, if you need to work on the terminal
sessions, you could take advantage of this.

%prep
%setup -q -n %{sname}-%{version}

%build
for N in 16 32 64 128; do convert %{name}.svg -resize ${N}x${N} $N.png; done

%install
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/bash

pushd %{_datadir}/%{name}
python ./gtkshots.py \$@
popd
EOF

chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/%{name}
install -m 0644 gtkshots.glade %{buildroot}%{_datadir}/%{name}/
install -m 0755 gtkshots.py %{buildroot}%{_datadir}/%{name}/
install -m 0755 pyshots.py %{buildroot}%{_datadir}/%{name}/

install -D 16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D 32.png %{buildroot}%{_liconsdir}/%{name}.png
install -D 64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
install -D 128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

# menu-entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=gtkShots
Comment=An utility to capture screenshots continuously
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Graphics;
EOF

%files
%doc COPYING
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.png

