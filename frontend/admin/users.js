// -*- coding: utf-8 -*-
(function (exports){
    if (exports.baast == null){
        exports.baast = {};
    }
    if (exports.baast.users){
        return;
    }

    var users = {
        UserCreator: function (selector){
            var info = function(type, title, message){
                new PNotify({
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
            };

            var app = new Vue({
                el: selector,
                created: function (){
                },
                methods: {
                    register: function (evnet){
                        var form = $($(this.$el).find('form'));
                        $.ajax({
                            'url': '/api/users/new',
                            'method': 'POST',
                            'data': form.serialize(),
                            'beforeSending': function (xhr, settings){
                                console.log('register user...');
                            },
                            'complete': function (xhr, status){
                                console.log(xhr);
                            },
                            'success': function (res, status, xhr){
                                info('success', 'ユーザを作成しました', '');
                            },
                            'error': function (res, status, xhr){
                                info('error', 'ユーザを作成できませんでした', res.statusText);
                            }
                        });
                    }
                }
            });
            return  app;
        }
    };
    exports.baast.users = users;
})(this);
