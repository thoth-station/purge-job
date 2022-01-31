Thoth's purge job
-----------------

A job that purges old Thoth data in a Thoth deployment.

Deployment
==========

See `thoth-station/thoth-application
<https://github.com/thoth-station/thoth-application/>`__ repository for
manifests needed to deploy this job.

Running purge-job
=================

The job is run in a deployment based on Thoth operator request. If you wish to
develop this job, check `thoth-station/storages repository
<https://github.com/thoth-station/storages>`__ stating information on how to
setup a local database instance for experimenting with this job.

.. code-block:: conosle

  git clone https://github.com/thoth-station/purge-job  # or use SSH
  cd purge-job
  pipenv install --dev
  pipenv run python3 ./app.py
