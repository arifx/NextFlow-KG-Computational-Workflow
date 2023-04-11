FROM python:3.9.13-slim-buster

####METADATA####
LABEL description="runtime environment for KG process of CSV and xlsx datasets using Nextflow."

#Add the python script to the root.
ADD requirements.txt /
RUN pip install -r requirements.txt


# Set user and group
ARG user=appuser
ARG group=appuser
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group}
RUN useradd -u ${uid} -g ${group} -s /bin/sh -m ${user} # <--- the '-m' creates a user home directory

# Switch to user
USER ${uid}:${gid}
