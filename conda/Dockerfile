FROM continuumio/anaconda3:latest

ADD meta.yaml /homoeditdistance/meta.yaml
RUN conda update anaconda
RUN conda config --set anaconda_upload yes

CMD conda-build /homoeditdistance
