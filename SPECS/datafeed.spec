Name:       datafeed
Version:    1
Release:    10%{?dist}
Summary:    datafeed
License:    FIXME

Requires(pre): shadow-utils

%description
This package is itended to deploy ssh authorized keys to the correct location for GFE to connect through ssh

%prep

%install
find ${RPM_BUILD_DIR}/ -type d -name ".DS_Store" -exec rmdir {} \;
cd ${RPM_BUILD_DIR}
for userdir in `find . -type f -name authorized_keys -exec dirname {} \; | awk -F\/ '{ print $NF }'`; do
  mkdir -p ${RPM_BUILD_ROOT}/appli/sshkeys/${userdir}
  mkdir -p ${RPM_BUILD_ROOT}/appli/FTP/${userdir}
  install -m600 ${RPM_BUILD_DIR}/appli/sshkeys/${userdir}/authorized_keys ${RPM_BUILD_ROOT}/appli/sshkeys/${userdir}/
  install -m600 ${RPM_BUILD_DIR}/appli/FTP/${userdir}/.create             ${RPM_BUILD_ROOT}/appli/FTP/${userdir}/
done

%files
%defattr(0600,root,sftpusers,0700)
/appli/sshkeys/
/appli/FTP/

%clean
if [ -d ${RPM_BUILD_DIR} ]; then
  rm -rf ${RPM_BUILD_DIR}
fi

%pre
mkdir -p /appli/sshkeys
mkdir -p /appli/FTP

%post
mkdir -p /appli/FTP/
mkdir -p /appli/sshkeys/
chown root:root /appli/sshkeys/
groupadd -g 9999 sftpusers
chmod 0755 /appli/sshkeys/
chown root:root /appli/sshkeys/
cd /appli/sshkeys/
for userdir in `ls`; do
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
  * Sun Oct 4 2020 Aurelien Grosshans <ngr@ubp.ch>
    - Updated to ver. 1.3. Add user user5
  * Sun Oct 4 2020 Aurelien Grosshans <ngr@ubp.ch>
    - Updated to ver. 1.4. Add user user6
  * Sun Oct 4 2020 Aurelien Grosshans <ngr@ubp.ch>
    - Updated to ver. 1.5. Directory reorg
  * Sun Oct 4 2020 Aurelien Grosshans <ngr@ubp.ch>
    - Updated to ver. 1.7. Add user user7
  * Sun Oct 4 2020 Aurelien Grosshans <ngr@ubp.ch>
    - Updated to ver. 1.8. modify useradd
  * Sun Oct 4 2020 Aurelien Grosshans <ngr@ubp.ch>
    - Updated to ver. 1.9. modify defattr
  * Sun Oct 4 2020 Aurelien Grosshans <ngr@ubp.ch>
    - Updated to ver. 1.10. Add user user8