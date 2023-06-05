from django.contrib import admin
from django.contrib.auth.models import User
from rangefilter.filters import DateRangeFilterBuilder

from .models import Post, Comment, PostUser, BlockedUser

# Register your models here.

class PostUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name",)
    exclude = ("user",)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset

        blogger = request.user
        blocked_users = BlockedUser.objects.filter(blockedUser=blogger)  # blocked user
        blocked_user_ids = blocked_users.values_list('postUser_id', flat=True)  # post user
        queryset = queryset.exclude(user_id__in=blocked_user_ids)

        return queryset

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user == obj.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user == obj.user:
            return True
        return False

admin.site.register(PostUser,PostUserAdmin)



class CommentAdmin (admin.ModelAdmin):
    list_display = ("user", "date_left",)

    exclude = ("user",)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)


    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset

        blogger = request.user
        blocked_users = BlockedUser.objects.filter(blockedUser=blogger)  # blocked user
        blocked_user_ids = blocked_users.values_list('postUser_id', flat=True)  # post user
        queryset = queryset.exclude(user_id__in=blocked_user_ids)

        return queryset

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user == obj.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user == obj.user:
            return True
        return False



admin.site.register(Comment, CommentAdmin)


class CommentInlineAdmin (admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):

    list_display = ("title", "user")
    list_filter = (("creation_date", DateRangeFilterBuilder()),)
    search_fields = ("title", "content")

    inlines = [CommentInlineAdmin, ]
    exclude = ("user",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset

        blogger = request.user
        blocked_users = BlockedUser.objects.filter(blockedUser=blogger)  # blocked user
        blocked_user_ids = blocked_users.values_list('postUser_id', flat=True)  # post user
        queryset = queryset.exclude(user_id__in=blocked_user_ids)

        return queryset

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user == obj.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user == obj.user:
            return True
        return False

admin.site.register(Post, PostAdmin)



class BlockedUserAdmin(admin.ModelAdmin):
   list_display = ("blockedUser", "postUser")
   exclude = ("blockedUser",)

   def save_model(self, request, obj, form, change):
       obj.blockedUser = request.user
       return super().save_model(request, obj, form, change)

   def has_change_permission(self, request, obj=None):
       if request.user.is_superuser:
           return True
       if obj and request.user == obj.blockedUser:
           return True
       return False

   def has_delete_permission(self, request, obj=None):
       if request.user.is_superuser:
           return True
       if obj and request.user == obj.blockedUser:
           return True
       return False


admin.site.register(BlockedUser, BlockedUserAdmin)

