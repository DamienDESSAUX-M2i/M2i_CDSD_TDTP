FROM nginx

WORKDIR /usr/share/nginx/html

RUN apt update
RUN apt upgrade
RUN apt install -y git

RUN git clone https://github.com/withaarzoo/3D-Rotate-Tube

RUN mv ./3D-Rotate-Tube/* . 

EXPOSE 80