__author__ = 'Administrator'
from django.contrib import admin
from django.shortcuts import HttpResponse,redirect
from crm import models
# Register your models here.
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from crm.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name')


class CourseRecordAdmin(admin.ModelAdmin):
    list_display = ('from_class','day_num','teacher','has_homework','homework_title','date')
    def initialize_studyrecords(self,request,queryset):
        if len(queryset)>1:
            return HttpResponse("nonono")
        #print(queryset[0].from_class.enrollment_set.all())#反查出所有报名此班级课程的学员
        new_obj_list = []
        for enroll_obj in queryset[0].from_class.enrollment_set.all():

            new_obj_list.append(models.StudyRecord(
                student = enroll_obj,
                course_record = queryset[0],
                record = 0,
                score = 0,
            ))
        try:
            models.StudyRecord.objects.bulk_create(new_obj_list)#批量创建
        except Exception as e:
            print('批量创建失败,请检查是否有对应记录')

        return redirect("/admin/crm/studyrecord/%s%s"%('?course_record_id_exact=',queryset[0].id))
    initialize_studyrecords.short_description = "初始化本节所有学员的上课记录"
    actions = ['initialize_studyrecords']

class StudyRecordAdmin(admin.ModelAdmin):
    list_display = ('student','course_record','record','score','date')
    list_filter = ['course_record','score','record']
    list_editable = ['score','record']


admin.site.register(models.Customer)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Enrollment)
admin.site.register(models.ClassList)
admin.site.register(models.Course)
admin.site.register(models.CourseRecord,CourseRecordAdmin)
admin.site.register(models.StudyRecord,StudyRecordAdmin)
# admin.site.register(models.UserProfile)
admin.site.register(models.Payment)
admin.site.register(models.Role)
admin.site.register(models.Branch)
admin.site.register(models.Menu)
admin.site.register(models.Contract)

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(models.UserProfile, UserProfileAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)




