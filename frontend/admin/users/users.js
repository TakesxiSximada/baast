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
        UserManager: function(selector){
            var db = {
                'mode': '',
                'users': [],
                'new_user': {
                    'name': '',
                    'email': '',
                    'password': '',
                    'password_confirm': ''
                },
                'current_user': {
                    'id': '',
                    'name': '',
                    'email': ''
                }
            };
            var app = new Vue({
                el: selector,
                data: db,
                created: function (){
                    this.init_new_user_entry();
                    this.fetch_users();
                },
                methods: {
                    view_default: function (){
                        this.mode = '';
                        this.fetch_users();
                    },
                    view_new: function(){
                        this.mode = 'new';
                    },
                    view_show: function(userId){
                        this.mode = 'show';
                        this.fetch_current_user(userId);
                        if (!this.current_user.id){
                            notification('error', 'ユーザがいません', '');
                        }
                    },
                    view_delete: function(){
                        this.mode = 'delete';
                    },
                    fetch_current_user: function(userId){
                        if (this.current_user.id != userId){
                            this.init_current_user_entry();
                        }
                        if (this.current_user.id == ''){
                            var target_users = [];
                            $.each(this.users, function (ii, user){
                                if(user.id == userId){
                                    target_users.push(user);
                                }
                            });
                            if(target_users.length == 0){
                                this.fetch_users([userId]);
                            }
                            $.each(this.users, function (ii, user){
                                if(user.id == userId){
                                    target_users.push(user);
                                }
                            });
                            if(target_users.length > 0){
                                this.current_user.id = target_users[0].id;
                                this.current_user.name = target_users[0].name;
                                this.current_user.email = target_users[0].email;
                            }else{
                                console.log("no user");
                            }
                        }
                    },
                    init_current_user_entry: function(){
                        this.current_user.id  = '';
                        this.current_user.name  = '';
                        this.current_user.email = '';
                    },
                    init_new_user_entry: function(){
                        this.new_user.name  = '';
                        this.new_user.email = '';
                        this.new_user.password = '';
                        this.new_user.password_confirm = '';
                    },
                    delete_user: function(){
                        var req = {
                            'userId': this.current_user.id
                        };
                        $.ajax({
                            'url': '/api/users/delete',
                            'type': 'POST',
                            'dataType': 'json',
                            'data': req,
                            'success': function (res, status, xhr){
                                notification('success', 'ユーザを削除しました', '');;
                            },
                            'error': function (res, status, xhr){
                                notification('error', 'ユーザを削除できませんでした', res.statusText);
                            }
                        });
                    },
                    update_user: function(){
                        var user = this.current_user;
                        $.ajax({
                            'url': '/api/users/update',
                            'method': 'POST',
                            'type': 'json',
                            'dataType': 'json',
                            'data': user,
                            'success': function (res, status, xhr){
                                notification('success', 'ユーザ情報を更新しました', '');;
                            },
                            'error': function (res, status, xhr){
                                notification('error', 'ユーザ情報を更新できませんでした', res.statusText);
                            }
                        });
                    },
                    register_user: function (){
                        var user = this.new_user;
                        $.ajax({
                            'url': '/api/users/new',
                            'type': 'POST',
                            'data': user,
                            'success': function (res, status, xhr){
                                notification('success', 'ユーザを作成しました', '');;
                            },
                            'error': function (res, status, xhr){
                                notification('error', 'ユーザを作成できませんでした', res.statusText);
                            }
                        });

                    },
                    fetch_users: function(userIds){
                        if (!userIds){
                            userIds = [];
                        }
                        var users = this.users;
                        var req = {userIds: userIds};
                        $.ajax({
                            'url': '/api/users',
                            'type': 'GET',
                            'data': req,
                            'dataType': 'json',
                            'contentType': 'application/json',
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
        }
        // ,
        // UserCollector: function (selector){
        //     var db = {
        //         'aabbcc': 1,
        //         'users': [],
        //         'count': 0
        //     }
        //     var app = new Vue({
        //         el: selector,
        //         data: db,
        //         created: function(){
        //             this.$watch('users', function (){
        //                 this.count = this.users.length;
        //             });
        //             this.update(db.users);
        //         },
        //         methods: {
        //             aaa: function (){
        //                 this.aabbcc = 'test';
        //             },
        //             update: function(users){
        //                 $.ajax({
        //                     'url': '/api/users',
        //                     'method': 'GET',
        //                     'dataType': 'json',
        //                     'beforeSending': function (xhr, settings){
        //                         console.log('getting user collection...');
        //                     },
        //                     'complete': function (xhr, status){
        //                         console.log(xhr);
        //                     },
        //                     'success': function (res, status, xhr){
        //                         $.each(res, function(ii, user){
        //                             users.push(user);
        //                         });
        //                     },
        //                     'error': function (res, status, xhr){
        //                         notification('error', 'ユーザを取得できませんでした', res.statusText);
        //                     }
        //                 });
        //             }
        //         }
        //     });
        //     return app;
        // },
        // UserCreator: function (selector){
        //     var app = new Vue({
        //         el: selector,
        //         created: function (){
        //         },
        //         methods: {
        //             register: function (evnet){
        //                 var form = $($(this.$el).find('form'));
        //                 $.ajax({
        //                     'url': '/api/users/new',
        //                     'method': 'POST',
        //                     'data': form.serialize(),
        //                     'beforeSending': function (xhr, settings){
        //                         console.log('register user...');
        //                     },
        //                     'complete': function (xhr, status){
        //                         console.log(xhr);
        //                     },
        //                     'success': function (res, status, xhr){
        //                         notification('success', 'ユーザを作成しました', '');
        //                         setTimeout(function (){
        //                             location.href='/admin/users';
        //                         }, 3000, true);
        //                     },
        //                     'error': function (res, status, xhr){
        //                         notification('error', 'ユーザを作成できませんでした', res.statusText);
        //                     }
        //                 });
        //             }
        //         }
        //     });
        //     return  app;
        // }
    };
    exports.baast.users = users;
})(this);
