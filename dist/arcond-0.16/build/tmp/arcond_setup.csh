setenv PATH /share/grid/Arcond/bin:$PATH
if ($?PYTHONPATH) then 
    setenv PYTHONPATH /share/grid/Arcond/lib/python2.4/site-packages:$PYTHONPATH
else 
    setenv PYTHONPATH /share/grid/Arcond/lib/python2.4/site-packages
endif 
setenv ARCOND_CONFIG_ROOT ~/.pathena
setenv ARCOND_SYS /share/grid/Arcond
