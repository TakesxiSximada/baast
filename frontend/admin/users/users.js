// -*- coding: utf-8 -*-
(function (exports){
    if (exports.baast == null){
        exports.baast = {};
    }
    if (exports.baast.users){
        return;
    }
    var notification = (function(type, title, message){
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
    });

    var users = {
        UserCollector: function (selector){
            var db = {
                'users': [],
                'count': 0
            }
            var app = new Vue({
                el: selector,
                data: db,
                created: function(){
                    this.$watch('users', function (){
                        this.count = this.users.length;
                    });
                    this.update(db.users);
                },
                methods: {
                    update: function(users){
                        $.ajax({
                            'url': '/api/users',
                            'method': 'GET',
                            'dataType': 'json',
                            'beforeSending': function (xhr, settings){
                                console.log('getting user collection...');
                            },
                            'complete': function (xhr, status){
                                console.log(xhr);
                            },
                            'success': function (res, status, xhr){
                                $.each(res, function(ii, user){
                                    users.push(user);
                                });
                            },
                            'error': function (res, status, xhr){
                                notification('error', 'ユーザを取得できませんでした', res.statusText);
                            }
                        });
                    }
                }
            });
            return app;
        },
        UserCreator: function (selector){
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
                                notification('success', 'ユーザを作成しました', '');
                                setTimeout(function (){
                                    location.href='/admin/users';
                                }, 3000, true);
                            },
                            'error': function (res, status, xhr){
                                notification('error', 'ユーザを作成できませんでした', res.statusText);
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
