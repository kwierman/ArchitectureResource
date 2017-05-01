# ArchitectureResource
Some Utility Functions for Doing Architecture Resource Utilization Studies

# Requirements

The information fetched out by this script is produced in the [More IO branch of the Larbys Caffe fork](https://github.com/LArbys/caffe/tree/more_io_thread).

# Installation

You REALLY want to make sure that this doesn't go into the system directory, so use this command EXACTLY. That is, unless you're working in a `virtualenv` ... with ROOT... 

~~~ bash
  pip install --user git+https://github.com/kwierman/ArchitectureResource
~~~

## For Developers

If you want to work on a local copy, and you installed using the command above, remove the old copy with this command:


~~~ bash
  pip uninstall ArchictureResource
~~~

Heck, you might just want to do that anyway once yer done with the study.

Locally, you can setup using dist utils.

~~~ bash
  python setup.py install
~~~

With local installation, using the above `pip` command to uninstall works as well.


## Running the code

TBD