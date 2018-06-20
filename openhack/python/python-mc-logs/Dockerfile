FROM python:3
ADD omsdata.py /
ADD config.yml /
RUN pip install mcstatus
RUN pip install pyyaml
RUN pip install requests
CMD [ "python", "./omsdata.py" ]