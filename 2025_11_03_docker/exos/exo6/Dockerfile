FROM nginx:latest
WORKDIR /home
RUN rm -f /usr/share/nginx/html/*
RUN apt update
RUN apt upgrade
RUN apt install -y git
RUN git clone https://github.com/withaarzoo/3D-Rotate-Tube
RUN cp 3D-Rotate-Tube/index.html /usr/share/nginx/html/
RUN cp 3D-Rotate-Tube/style.css /usr/share/nginx/html/
COPY . .
EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]