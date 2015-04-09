# set PYTHONPATH to use the current directory first
import sys
sys.path.insert(0,'.')

# get release version
from arcondtools import ArcondToolsPkgInfo
release_version = ArcondToolsPkgInfo.release_version

import os
import re
from distutils.core import setup
from distutils.command.install_data import install_data as install_data_org

# generates files using templates and install them
class install_data_arcond (install_data_org):
    def initialize_options (self):
        install_data_org.initialize_options (self)
        self.prefix = None
        self.root   = None
        self.install_purelib = None
        self.install_scripts = None

    def finalize_options (self):
        # set install_purelib
        self.set_undefined_options('install',
                                   ('prefix','prefix'))
        self.set_undefined_options('install',
                                   ('root','root'))
        self.set_undefined_options('install',
                                   ('install_purelib','install_purelib'))
        self.set_undefined_options('install',
                                   ('install_scripts','install_scripts'))
                                            
    def run (self):
        # set install_dir
        if self.install_dir == None:
            if self.root != None:
                # rpm
                self.install_dir = self.root
            else:
                # sdist
                self.install_dir = self.prefix
        self.install_dir = os.path.expanduser(self.install_dir)
        self.install_dir = os.path.abspath(self.install_dir)

        # remove these file (will be relocated)
        files_clean=['example.sh',
                     'arcond.conf',
                     'schema.site.atlas51.cmd',
                     'schema.site.atlas52.cmd',
                     'schema.site.atlas53.cmd',
                     'Analysis_jobOptions_BASIC.py',
                     'ShellScript_BASIC.sh',
                     'UserAnalysis.tgz',
                     'arcond_setup.sh.template', 
                     'arcond_setup.csh.template',
                     'input.conf',
                     'version.txt',
                     'gen_version',
                     'submit_job.sh', 
                     'submit_BASIC.sh',
                     'schema.job.generic.sh',
                     'send_dq2.sh',
                     'arc_command',
                     'hosts.py',
                     'arc_hosts',
                     'arc_sync'
             ]

        for i in files_clean:
               cmt= self.install_dir+'/bin/'+i
               os.remove(cmt)


        print 'Clear: ',self.install_dir+'/bin/'
 
        # remove /usr for bdist/bdist_rpm
        match = re.search('(build/[^/]+/dumb)/usr',self.install_dir)
        if match != None:
            self.install_dir = re.sub(match.group(0),match.group(1),self.install_dir)
        # remove /var/tmp/*-buildroot for bdist_rpm
        match = re.search('(/var/tmp/.*-buildroot)/usr',self.install_dir)
        if match != None:
            self.install_dir = re.sub(match.group(0),match.group(1),self.install_dir)
        # create tmp area
        tmpDir = 'build/tmp'
        self.mkpath(tmpDir)
        new_data_files = []
        for destDir,dataFiles in self.data_files:
            newFilesList = []
            for srcFile in dataFiles:
                # dest filename
                destFile = re.sub('\.template$','',srcFile)
                destFile = destFile.split('/')[-1]
                destFile = '%s/%s' % (tmpDir,destFile)
                # open src
                inFile = open(srcFile)
                # read
                filedata=inFile.read()
                # close
                inFile.close()
                # replace patterns
                for item in re.findall('@@([^@]+)@@',filedata):
                    if not hasattr(self,item):
                        raise RuntimeError,'unknown pattern %s in %s' % (item,srcFile)
                    # get pattern
                    patt = getattr(self,item)
                    # convert to absolute path
                    if item.startswith('install'):
                        patt = os.path.abspath(patt)
                    # remove build/*/dump for bdist
                    patt = re.sub('build/[^/]+/dumb','',patt)
                    # remove /var/tmp/*-buildroot for bdist_rpm
                    patt = re.sub('/var/tmp/.*-buildroot','',patt)                    
                    # replace
                    filedata = filedata.replace('@@%s@@' % item, patt)
                # write to dest
                oFile = open(destFile,'w')
                oFile.write(filedata)
                oFile.close()
                # append
                newFilesList.append(destFile)
            # replace dataFiles to install generated file
            new_data_files.append((destDir,newFilesList))
        # install
        self.data_files = new_data_files
        install_data_org.run(self)


setup(
    name="arcond",
    version=release_version,
    description='Arcond Client Package for Tier3g clusters',
    long_description='''This package contains Arcond front-end of Condor''',
    license='GPL',
    author='Sergei Chekanov',
    author_email='chakanau@hep.anl.gov',
    url='http://atlaswww.hep.anl.gov/asc/arcond',
    packages = [ 'arcondtools', 'psshlib'
                 ],
    scripts = [ 'scripts/arcond', 
                'scripts/arc_add',
                'scripts/arc_check',
                'scripts/arc_exe',                
                'scripts/arc_ls',
                'scripts/arc_cp',
                'scripts/arc_mv',
                'scripts/arc_clean',
                'scripts/arc_setup',
                'scripts/arc_setup_admin',
                'scripts/submit_db.sh',
                'scripts/collect.sh',
                'scripts/databuilder.sh',
                'scripts/arc_help',
                'scripts/admin/arc_get',
                'scripts/admin/arc_split',
                'scripts/admin/input.conf',
                'scripts/admin/gen_version',
                'scripts/admin/version.txt',
                'scripts/admin/send_dq2.sh',
                'scripts/admin/arcsync_data',
                'scripts/submit_BASIC.sh',
                'scripts/submit_job.sh',
                'scripts/tar_project.sh',
                'scripts/schema.job.generic.sh',
                'scripts/admin/arc_ssh',
                'scripts/admin/pnuke', 
                'scripts/admin/pscp', 
                'scripts/admin/pssh',
                'scripts/admin/prsync',
                'templates/arcond_setup.sh.template', 
                'templates/arcond_setup.csh.template',
                'share/example.sh', 
                'share/arcond.conf',
                'patterns/schema.site.atlas51.cmd',
                'patterns/schema.site.atlas52.cmd',
                'patterns/schema.site.atlas53.cmd',         
                'user/Analysis_jobOptions_BASIC.py',
                'user/ShellScript_BASIC.sh',
                'Job/UserAnalysis.tgz',
                'scripts/admin/hosts.py',
                'scripts/admin/arc_hosts',
                'scripts/admin/arc_command',
                'scripts/admin/arc_sync'
                ],
    data_files = [ ('etc/arcond', ['templates/arcond_setup.sh.template',
                                   'templates/arcond_setup.csh.template'
                                  ]
                    ),
    
                ('etc/arcond/admin', [ 
                'scripts/admin/hosts.py',
                'scripts/admin/arc_hosts',
                'scripts/admin/arcsync_data',
                'scripts/admin/arc_command',
                'scripts/admin/arc_sync']
                ),


               ('etc/arcond/share', ['share/example.sh',
                                         'share/arcond.conf',
                                         'patterns/schema.site.atlas51.cmd',
                                         'patterns/schema.site.atlas52.cmd',
                                         'patterns/schema.site.atlas53.cmd',
                                         'user/Analysis_jobOptions_BASIC.py',
                                         'user/ShellScript_BASIC.sh',
                                         'Job/UserAnalysis.tgz',
                                         'scripts/admin/input.conf',
                                         'scripts/admin/version.txt',
                                         'scripts/admin/gen_version',
                                         'scripts/submit_BASIC.sh',
                                         'scripts/submit_job.sh',
                                         'scripts/schema.job.generic.sh',
                                         'scripts/admin/send_dq2.sh',
                                        ]
                    ),
                                     
                   ],
   


    cmdclass={'install_data': install_data_arcond}
)
