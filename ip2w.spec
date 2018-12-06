License:        BSD
Vendor:         Otus
Group:          PD01
URL:            http://otus.ru/lessons/3/
Source0:        otus-%{current_datetime}.tar.gz
#Source0:        otus.tar.gz
BuildRoot:      %{_tmppath}/otus-%{current_datetime}
Name:           ip2w
Version:        0.0.1
Release:        1
BuildArch:      noarch
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
Requires: epel-release python python-pip nginx
Summary:  "uWSGI daemon"


%description
"uWSGI ip2w daemon"
Git version: %{git_version} (branch: %{git_branch})

%define __etcdir    /usr/local/etc
%define __logdir    /var/log/
%define __bindir    /usr/local/ip2w/
%define __systemddir /usr/lib/systemd/system/

%prep
tar xf %{SOURCE0} --strip-component=1

%install
[ "%{buildroot}" != "/" ] && rm -fr %{buildroot}
%{__mkdir} -p %{buildroot}/%{__systemddir}
%{__mkdir} -p %{buildroot}/%{__bindir}
%{__mkdir} -p %{buildroot}/%{__etcdir}/%{name}
%{__mkdir} -p %{buildroot}/%{__logdir}%{name}
%{__install} -pD -m 644 %{name}.service %{buildroot}/%{__systemddir}/%{name}.service
%{__install} -pD -m 644 %{name}.ini %{buildroot}/%{__bindir}/%{name}.ini
%{__install} -pD -m 755 %{name}.py %{buildroot}/%{__bindir}/%{name}.py
%{__install} -pD -m 644 %{name}.cfg %{buildroot}/%{__etcdir}/%{name}/%{name}.cfg

%post
%systemd_post %{name}.service
systemctl daemon-reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%clean
[ "%{buildroot}" != "/" ] && rm -fr %{buildroot}

%files
%{__logdir}
%{__bindir}
%{__systemddir}
%{__etcdir}
