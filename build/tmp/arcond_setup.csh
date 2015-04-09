setenv PATH /tmp/Arcond/bin:$PATH
if ($?PYTHONPATH) then 
    setenv PYTHONPATH /tmp/Arcond/lib/python2.4/site-packages:$PYTHONPATH
else 
    setenv PYTHONPATH /tmp/Arcond/lib/python2.4/site-packages
endif 
setenv ARCOND_CONFIG_ROOT ~/.pathena
setenv ARCOND_SYS /tmp/Arcond
