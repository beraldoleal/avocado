Configuration Reference
=======================

global options
--------------

============== =============================== ====== ================= =================================
Command        Command-line arg                type   default           configuration section        
============== =============================== ====== ================= =================================
avocado        --verbose, -V                   bool   False             core.verbose
avocado        --paginator [1]_                str    'off'             core.paginator
============== =============================== ====== ================= =================================


assets command
--------------

============== =============================== ====== ================= =================================
Sub-Command    Command-line arg                type   default           configuration section        
============== =============================== ====== ================= =================================
assets fetch   references                      list    []               assets.fetch.references
============== =============================== ====== ================= =================================

config command
--------------

============== =============================== ====== ================= =================================
Sub-Command    Command-line arg                type   default           configuration section        
============== =============================== ====== ================= =================================
config         --datadir                       bool   False             config.datadir
============== =============================== ====== ================= =================================

diff command
------------

============== =============================== ====== ================= =================================
Sub-Command    Command-line arg                type   default           configuration section        
============== =============================== ====== ================= =================================
diff           job job                         list   []                diff.jobids
diff           --html                          str    None              diff.html
diff           --open-browser                  bool   False             diff.open_browser
diff           --diff-filter                   list   [all] [4]_        diff.filter
diff           --diff-strip-id                 bool   False             diff.strip_id
diff           --create-reports                bool   False             diff.create_reports
============== =============================== ====== ================= =================================

distro command
--------------

============== =============================== ====== ================= =================================
Sub-Command    Command-line arg                type   default           configuration section        
============== =============================== ====== ================= =================================
distro         --distro-def-create [2]_        bool   False             distro.distro_def_create     
distro         --distro-def-name [2]_          str    ''                distro.distro_def_name       
distro         --distro-def-version [2]_       str    ''                distro.distro_def_version    
distro         --distro-def-release [2]_       str    ''                distro.distro_def_release    
distro         --distro-def-arch [2]_          str    ''                distro.distro_def_arch       
distro         --distro-def-path [2]_          str    ''                distro.distro_def_path       
distro         --distro-def-type [2]_          str    ''                distro.distro_def_type       
============== =============================== ====== ================= =================================

list command
------------

============== =============================== ====== ================= =================================
Sub-Command    Command-line arg                type   default           configuration section        
============== =============================== ====== ================= =================================
list           references                      list    []               list.references
============== =============================== ====== ================= =================================

nlist command
-------------

============== =============================== ====== ================= =================================
Sub-Command    Command-line arg                type   default           configuration section        
============== =============================== ====== ================= =================================
nlist          references                      list    []               nlist.references
nlist          --verbose, -V                   bool    False            nlist.verbose
nlist          --write-recipes-to-directory    str     None             nlist.recipes.write_to_directory
============== =============================== ====== ================= =================================

nrun command
------------

============== =============================== ====== ================= =================================
Sub-Command    Command-line arg                type   default           configuration section        
============== =============================== ====== ================= =================================
nrun           references                      list    []               nrun.references
nrun           --disable-task-randomization    bool    False            nrun.disable_task_randomization
nrun           --status-server                 str    '127.0.0.1:8888'  nrun.status_server.listen
============== =============================== ====== ================= =================================


run command
-----------

============== =============================== ====== ================= =================================
Sub-Command    Command-line arg                type   default           configuration section        
============== =============================== ====== ================= =================================
run            references                      list   []                run.references
run            --archive                       bool   False             run.results.archive
run            --dry-run-no-cleanup            bool   False             run.dry_run.no_cleanup
run            --execution_order               str    None              run.execution_order
run            --failfast [1]_                 str    'off'             run.failfast
run            --json                          str    None              run.json.output
run            --json-job-result [1]_          str    'on'              run.json.job_result
run            --journal                       bool   False             run.journal.enabled
run            --keep-tmp [1]_                 str    'off'             run.keep_tmp
run            --ignore-missing-references     str    'off'             run.ignore_missing_references
run            --test-parameter, -p            list   []                run.test_parameters
run            --replay                        str    ''                run.replay.job_id
run            --replay-ignore                 list   []                run.replay.ignore
run            --replay-test-status [2]_       list   []                run.replay.test_status           
run            --replay-resume                 bool   False             run.replay.resume
run            **--sysinfo** [1]_ [2]_         str    'on'              **sysinfo.collect.enabled** [3]_
run            --store-logging-stream          list   []                run.store_logging_stream
run            --tap                           str    None              run.tap.output
run            --tap-include-logs              bool   False             run.tap.include_logs
run            --tap-job-result [1]_           str    'on'              run.tap.job_result
run            --force-job-id                  str    None              run.unique_job_id
run            --wrapper                       list   []                run.wrapper.wrappers
run            --job-category                  str    None              run.job_category
run            --job-results-dir               str    None              run.results_dir
run            --job-timeout                   str    '0'               run.job_timeout
run            --json-variants-load            str    None              run.json_variants_load
run            --log-test-data-directories     bool   False             run.log_test_data_directories
run            --output-check [1]_             str    'on'              run.output_check
run            --output-check-record           str    None              run.output_check_record
run            --xunit                         str    None              run.xunit.output
run            --xunit-job-result [1]_         str    'on'              run.xunit.job_result
run            --xunit-job-name                str    None              run.xunit.job_name
run            --xunit-max-test-log-chars      str    '100000'          run.xunit.max_test_log_chars
============== =============================== ====== ================= =================================

sysinfo command
---------------

============== =============================== ====== ================= =================================
Sub-Command    Command-line arg                type   default           configuration section        
============== =============================== ====== ================= =================================
sysinfo        sysinfodir [2]_                 str    './'              sysinfo.collect.sysinfodir   
============== =============================== ====== ================= =================================

variants command
----------------

============== =============================== ====== ================= =================================
Sub-Command    Command-line arg                type   default           configuration section        
============== =============================== ====== ================= =================================
variants       --summary [2]_                  int    0                 variants.summary
variants       --variants [2]_                 int    1                 variants.variants
variants       --contents, -c                  bool   False             variants.contents
variants       --json-variants-dump            str    None              variants.json_variants_dump
variants       --json-variants-load            str    None              variants.json_variants_load
variants       --debug, -d                     bool   False             variants.debug
variants       --tree, -t                      bool   False             variants.tree
variants       --inherit, -i                   bool   False             variants.inherit
============== =============================== ====== ================= =================================


vmimage command
---------------

============== =============================== ====== ================= =================================
Sub-Command    Command-line arg                type   default           configuration section        
============== =============================== ====== ================= =================================
vmimage get    --distro                        str    ''                vmimage.get.distro
vmimage get    --version                       str    ''                vmimage.get.version
vmimage get    --arch                          str    ''                vmimage.get.arch
============== =============================== ====== ================= =================================


TO-DO
=====

#. Find for more `.add_argument(` on `core/`, and replace with `register_option()`::
  

        $ grep "add_argument(" avocado/core/* -R | wc -l
        23

#. Find for more `.add_argument(` on `optional_plugins/`, and replace with `register_option()`::

        $ grep "add_argument(" optional_plugins/* -R | wc -l
        43

#. Find for any old `settings.get_value(` and replace by `future.get('....')`
   This will need two things:
   
    #. register the option in some place with `register_option()` (even
       that is not a command-line option, we should use this method);

    #. replace the `get_value("` with `future.get('...')`;

#. Find for any remaining old settings, usage.
   Useful grep: `grep "from.*settings.*import"  * -R | grep -v future`

#. Move core.future.settings to core.settings

Done
====

#. plugins/assets.py
#. plugins/archive.py
#. plugins/config.py [#plugins_config]_ 
#. plugins/diff.py
#. plugins/distro.py
#. plugins/jsonresult.py
#. plugins/json_variants.py
#. plugins/journal.py
#. plugins/list.py
#. plugins/nlist.py
#. plugins/nrun.py [#plugins_nrun]_
#. plugins/plugins.py
#. plugins/replay.py [#plugins_replay]_
#. plugins/run.py
#. plugins/runner.py
#. plugins/sysinfo
#. plugins/tap.py
#. plugins/vmimage.py [#plugins_vmimage]_
#. plugins/wrapper.py
#. plugins/xunit.py


Will be deprecated
==================

#. plugins/runnable_run.py
#. plugins/runnable_run_recipe.py
#. plugins/task_run.py
#. plugins/task_run_recipe.py

Footnotes
=========

 * There is no plugin dependency, but some plugins depend on other' configs
 * avocado config --paginator -> avocado --paginator config
 * avocado config --verbose -> avocado --verbose config
 * removed --system-wide from plugins/variants
 * moved --keep_env to a optional_plugin/remote_nrunner
 * removed gdb_run_bin get from plugins/wrapper

.. [1] This should be a bool
.. [2] We should think on a better name to make sense
.. [3] Should this be moved to run.sysinfo ?
.. [4] Actually this: ['cmdline', 'time', 'variants', 'results', 'config', 'sysinfo']
.. [#plugins_vmimage] Still uses config.get('vmimage_subcommand')
.. [#plugins_config] Need to migrate some methods here to the use the new
                     module.
.. [#plugins_replay] Old code still updating config['VAR'] here
.. [#plugins_nrun] status_server is used by other parts. core/job.py need to be changed.
