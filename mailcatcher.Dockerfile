FROM ruby
RUN gem install mailcatcher --no-document
ENV PATH=/usr/local/bundle/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
EXPOSE 1080/tcp
EXPOSE 1025/tcp
CMD mailcatcher --foreground --ip=0.0.0.0
