// -*- coding: utf-8 -*-
(function (exports){
    if (exports.baast == null){
        exports.baast = {};
    }

    if (exports.baast.authentications){
        return;
    }

    var notification = (function(type, title, message){
        var notify = new PNotify({
            title: title,
            text: message,
            type: type,
            nonblock: {
                nonblock: true
            },
            before_close: function(PNotify){
                // You can access the notice's options with this. It is read only.
                //PNotify.options.text;

                // You can change the notice's options after the timer like this:
                PNotify.update({
                    title: PNotify.options.title+" - Enjoy your Stay",
                    before_close: null
                });
                PNotify.queueRemove();
                return false;
            }
        });
    });
    exports.baast.authentications = {
        AuthenticationManager: function (selector){
            var db = {
                'mode': 'login',
                'authentication_data': {
                    'email': '',
                    'password': ''
                },
                'result': '',
                'init_authentication_data': function (){
                    this.authentication_data.email = '';
                    this.authentication_data.password = '';
                }
            };
            return new Vue({
                el: selector,
                data: db,
                created: function (){
                    this.init_authentication_data();
                },
                methods: {
                    login: function (){
                        var authentication_data = this.authentication_data;
                        console.log(authentication_data);
                        $.ajax({
                            'url': '/api/users/login',
                            'type': 'POST',
                            'data': authentication_data,
                            'xhrFields': {'withCredentials': true},
                            'success': function (res, status, xhr){
                                notification('success', 'ログインしました', '');
                            },
                            'error': function (res, status, xhr){
                                notification('error', 'ログインできませんでした', res.statusText);
                            }
                        });
                    }
                }
            });
        }
    };
})(this);
