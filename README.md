backbone_music_server
=====================

Backend for streaming HTML5 Media player client using backbone.js

Sample Nginx config
===================

                                                                                                                                                                          126,1         Bot
    server {
        listen 8080;

        auth_basic            "Restricted";
        auth_basic_user_file  htpasswd;

        location /api/ { 

            expires epoch;

            fastcgi_param  QUERY_STRING       $query_string;
            fastcgi_param  REQUEST_METHOD     $request_method;
            fastcgi_param  CONTENT_TYPE       $content_type;
            fastcgi_param  CONTENT_LENGTH     $content_length;

            fastcgi_param  REQUEST_URI        $request_uri;
            fastcgi_param  DOCUMENT_URI       $document_uri;
            fastcgi_param  DOCUMENT_ROOT      $document_root;
            fastcgi_param  SERVER_PROTOCOL    $server_protocol;

            fastcgi_param  GATEWAY_INTERFACE  CGI/1.1;
            fastcgi_param  SERVER_SOFTWARE    nginx/$nginx_version;

            fastcgi_param  REMOTE_ADDR        $remote_addr;
            fastcgi_param  REMOTE_PORT        $remote_port;
            fastcgi_param  SERVER_ADDR        $server_addr;
            fastcgi_param  SERVER_PORT        $server_port;
            fastcgi_param  SERVER_NAME        $http_host;
            fastcgi_param  SITE_NAME          $server_name;

            fastcgi_pass 127.0.0.1:9002;

        }

        location ~ / {

            root /srv/ww1/static;
            autoindex on; 
            allow all;
            expires epoch;

        }

    }   