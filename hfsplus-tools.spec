Summary:	Tools to create/check Apple HFS+ filesystems
Name:		hfsplus-tools
Version:	540.1.linux3
Release:	1
License:	APSL 2.0
Group:		Base
Source0:	http://cavan.codon.org.uk/~mjg59/diskdev_cmds/diskdev_cmds-%{version}.tar.gz
# Source0-md5:	0435afc389b919027b69616ad1b05709
URL:		http://gentoo-wiki.com/HOWTO_hfsplus
BuildRequires:	clang
BuildRequires:	libuuid-devel
BuildRequires:	openssl-devel
# those tools are outdated, given the rebuilt mkfs/fsck.hfsplus in this
# package.  However, I don't want to Obsolete that package yet, as some people
# may have a valid use for it on their systems.
Conflicts:	hfsplusutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# we want this to end up with the other mkfs.*'s, in /sbin
%define		_exec_prefix	/

%description
HFS+, HFS Plus, or Mac OS Extended are names for a file system
developed by Apple Computer to replace their Hierarchical File System
(HFS). In addition to being the default file system on modern Apple
computers, HFS+ is one of two formats, FAT being the other, that are
supported by the iPod hard-disk based music player. Unlike FAT, HFS+
supports UNIX style file permissions, which makes it useful, for
serving and sharing files in a secured manner. As Apple Computer's
devices and systems become increasingly ubiquitous, it becomes
important that Linux fully support this format. This package provides
tools to create and check HFS+ filesystems under Linux.

The Linux kernel does not support writing to HFS+ journals, writing to
a hfsplus partition is recommended only after disabling journaling;
however, the kernel, as of version 2.6.16, supports case-sensitivity
(also known as HFSX) commit.

%prep
%setup -q -n diskdev_cmds-%{version}

# remove errant execute bits
find -type f -name '*.[ch]' -exec chmod -c a-x {} +

%build
export CFLAGS="%{rpmcflags}"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

# the actual install...
install -d $RPM_BUILD_ROOT%{_sbindir}
install -p newfs_hfs.tproj/newfs_hfs $RPM_BUILD_ROOT%{_sbindir}/mkfs.hfsplus
install -p fsck_hfs.tproj/fsck_hfs $RPM_BUILD_ROOT%{_sbindir}/fsck.hfsplus

# man pages -- a mildly non-invasive name change is in order
install -d $RPM_BUILD_ROOT%{_mandir}/man8
cat fsck_hfs.tproj/fsck_hfs.8 | sed -e 's/[F|f]sck_hfs/fsck.hfsplus/g' \
    > $RPM_BUILD_ROOT%{_mandir}/man8/fsck.hfsplus.8
cat newfs_hfs.tproj/newfs_hfs.8 | sed -e 's/[N|n]ewfs_hfs/mkfs.hfsplus/g' \
    > $RPM_BUILD_ROOT%{_mandir}/man8/mkfs.hfsplus.8

# and a utility symlink...
ln -s fsck.hfsplus $RPM_BUILD_ROOT%{_sbindir}/fsck.hfs
echo '.so man8/fsck.hfsplus.8' > $RPM_BUILD_ROOT%{_mandir}/man8/fsck.hfs.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mkfs.hfsplus
%attr(755,root,root) %{_sbindir}/fsck.hfsplus
%attr(755,root,root) %{_sbindir}/fsck.hfs
%{_mandir}/man8/mkfs.hfsplus.8*
%{_mandir}/man8/fsck.hfsplus.8*
%{_mandir}/man8/fsck.hfs.8*
