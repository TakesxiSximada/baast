// -*- coding: utf-8 -*-
(function (exports){
    if (exports.baast == null){
        exports.baast = {};
    }

    if (exports.baast.users){
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
    var users = {
        UserManager: function(selector){
            var db = {
                'mode': '',
                'users': [],
                'current_user_id': 0,
                'current_user': {
                    'id': '',
                    'name': '',
                    'email': ''
                },
                'new_user': {
                    'name': '',
                    'email': '',
                    'password': '',
                    'password_confirm': ''
                }
            };
            var app = new Vue({
                el: selector,
                data: db,
                created: function (){
                    this.$watch('current_user_id', this.fetch_current_user);
                    this.$watch('users', this.fetch_current_user, deep=true);
                    this.init_new_user_entry();
                    this.fetch_users();
                },
                methods: {
                    view_default: function (update){
                        this.mode = '';
                        if(update){
                            this.fetch_users();
                        }
                    },
                    view_new: function(){
                        this.mode = 'new';
                    },
                    view_show: function(userId){
                        this.mode = 'show';
                        this.current_user_id = userId;
                    },
                    view_delete: function(){
                        this.mode = 'delete';
                    },
                    fetch_current_user: function(){
                        var current_user = this.current_user;
                        var current_user_id = this.current_user_id;
                        if (this.current_user.id != this.current_user_id){
                            $.each(this.users, function(ii, user){
                                if(user.id == current_user_id){
                                    current_user.id = user.id;
                                    current_user.name = user.name;
                                    current_user.email = user.email;
                                }
                            });
                        }
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
                                if(res.status == 401){
                                    exports.location = "auth";
                                }
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
                                if(res.status == 401){
                                    exports.location = "auth";
                                }
                            }
                        });
                    },
                    register_user: function (continiouse){
                        var user = this.new_user;
                        var redirct = continiouse ? this.view_new : this.view_default;
                        var init_new_user_entry = this.init_new_user_entry;
                        $.ajax({
                            'url': '/api/users/new',
                            'type': 'POST',
                            'data': user,
                            'complete': function (){
                                init_new_user_entry();
                            },
                            'success': function (res, status, xhr){
                                notification('success', 'ユーザを作成しました', '');
                                redirct();
                            },
                            'error': function (res, status, xhr){
                                notification('error', 'ユーザを作成できませんでした', res.statusText);
                                if(res.status == 401){
                                    exports.location = "auth";
                                }

                            }
                        });

                    },
                    fetch_users: function(userIds){
                        if (!userIds){
                            userIds = [];
                        }
                        var users = this.users;
                        var req = {userIds: userIds};
                        var id_user = {};
                        $.ajax({
                            'url': '/api/users',
                            'type': 'GET',
                            'data': req,
                            'dataType': 'json',
                            'contentType': 'application/json',
                            'xhrFields': {'withCredentials': true},
                            'success': function (res, status, xhr){
                                users.length = 0;
                                $.each(res, function(ii, user){
                                    users.push(user);
                                });
                            },
                            'error': function (res, status, xhr){
                                notification('error', 'ユーザを取得できませんでした', res.statusText);
                                if(res.status == 401){
                                    exports.location = "auth";
                                }
                            }
                        });
                    }
                }
            });
            return app;
        }
    };
    exports.baast.users = users;
})(this);
