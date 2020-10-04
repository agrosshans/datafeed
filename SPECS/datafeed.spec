Name:       datafeed
Version:    1
Release:    2%{?dist}
Summary:    datafeed
License:    FIXME

Requires(pre): shadow-utils

%description
This package is itended to deploy ssh authorized keys to the correct location for GFE to connect through ssh

%prep
if [ -d ${RPM_BUILD_DIR} ]; then
  rm -rf ${RPM_BUILD_DIR}/*
else
  mkdir -p ${RPM_BUILD_DIR}
fi
 
%build
if [ -d ${RPM_BUILD_DIR} ]; then
  cd ${RPM_BUILD_DIR}
  git clone git@github.com:agrosshans/datafeed.git
fi

%install
cd $RPM_BUILD_DIR/%{name}
for userdir in `find . -type f -name authorized_keys -exec dirname {} \; | sed -e 's/\.\///'`; do
  mkdir -p ${RPM_BUILD_ROOT}/appli/sshkeys/${userdir}
  install -m600 $RPM_BUILD_DIR/%{name}/${userdir}/authorized_keys $RPM_BUILD_ROOT/appli/sshkeys/${userdir}/
done

mkdir -p ${RPM_BUILD_ROOT}/appli/sshkeys

%files
%defattr(0600,-,sftpusers,0700)
/appli/sshkeys/*

%clean
if [ -d ${RPM_BUILD_DIR} ]; then
  rm -rf ${RPM_BUILD_DIR}
fi

%pre
mkdir -p /appli/sshkeys
mkdir -p /appli/FTP

#getent group sftpusers >/dev/null || groupadd -f -g 9999 -r sftpusers
#chmod 0755 /appli/sshkeys/
#chown root:root /appli/sshkeys/
#cd /appli/sshkeys/
#for userdir in `find . -type f -name authorized_keys -exec dirname {} \; | sed -e 's/\.\///'`; do
#  if ! getent passwd ${userdir} >/dev/null ; then
#      useradd -r -g sftpusers -c "${userdir} Datafeed User Id." -d /appli/FTP/${userdir} -m -s /sbin/nologin ${userdir}
#  fi
#done

%post
mkdir -p /appli/FTP/
mkdir -p /appli/sshkeys/
chown root:root /appli/sshkeys/
groupadd -g 9999 sftpusers
chmod 0755 /appli/sshkeys/
chown root:root /appli/sshkeys/
cd /appli/sshkeys/
for userdir in `find . -type f -name authorized_keys -exec dirname {} \; | sed -e 's/\.\///'`; do
  if ! getent passwd ${userdir} >/dev/null ; then
      useradd -r -g sftpusers -c "${userdir} Datafeed User Id." -d /appli/FTP/${userdir} -m -s /sbin/nologin ${userdir}
  fi
  chown ${userdir}:sftpusers /appli/sshkeys/${userdir}
  chown ${userdir}:sftpusers /appli/sshkeys/${userdir}/authorized_keys
  chmod 0700 /appli/sshkeys/${userdir}
  chmod 0600 /appli/sshkeys/${userdir}/authorized_keys
done

%changelog
  * Sun Oct 4 2020 Aurelien Grosshans <ngr@ubp.ch>
    - Updated to ver. 1.2. Add user toto