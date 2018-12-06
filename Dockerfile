FROM centos:centos7

RUN yum clean all
RUN yum -y update; yum clean all
RUN yum -y install epel-release
RUN yum -y install python-pip python-devel nginx gcc
RUN pip install uwsgi
RUN yum -y install rpm-build
RUN yum -y install git
RUN git config --global user.name "Tatyana Emelyanova"
RUN git config --global user.email lisstic.tt@gmail.com

EXPOSE 80
