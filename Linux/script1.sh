nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh

nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh

nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh

nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh

nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh

nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh

nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh

nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh

nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh

nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh

nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh

nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh

nmtui-edit                           zipgrep
 nmtui-hostname                       zipinfo
 nohup                                zipnote
 nproc                                zipsplit
 nroff                                zless
 nsenter                              zmore
 numfmt                               znew
 od                                   zsoelim
[root@RockyLinux3 bin]# vim script1.sh
# this script takes two files and copies them both to second directory,
# then makes a third directory inside second directory 
# inside the third directory, followed by a forth, fifth, and sixth directory
# Creates a new file and copies the contents of two old files into the new file
# moves new file and two old files into forth, fifth, and sixth directories respectively
# creates seventh directory, a copy of the second directory at the same level
# creates eigth directory, a copy of the third directory at the same level
# creates two copies of a old file (renaming them) in same directory
#! /bin/bash
mkdir /home/justin
cp ./../home/yu/labfiles/nursery ./../home/yu/labfiles/sonnet  ./../home/justin
mkdir ./../home/justin/files1; mkdir ./../home/justin/files1/sonnets; mkdir ./../home/justin/files1/rhymes; mkdir ./../home/justin/files1/combos
touch poems; cat /home/justin/files1/sonnets/sonnet > poems; cat /home/justin/files1/rhymes/nursery >> poems 
mv /home/justin/labfiles/sonnet /home/justin/files1/sonnets/sonnet; mv /home/justin/labfiles/nursery /home/justin/files1/rhymes/nursery; mv ./poems /home/justin/files1/combos/poems
cd /
cd home
cd yu
cp -r ./../justin ./../ahmed 
cd /home/justin
cp -r files1 ./files2
cd /home/justin/files1/sonnets
cp sonnet bonnet
cp sonnet donnet
exit 0
