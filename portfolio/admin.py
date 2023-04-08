from django.contrib import admin

from .models import Project, Team, Skill, Comment

# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    list_filter = ("team_lead", "skills", "date",)
    list_display = ("name", "youtube_link", "date",)
    prepopulated_fields = {"slug": ("name",)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_email", "user_name", "comment_text", "project",)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Team)
admin.site.register(Skill)
admin.site.register(Comment, CommentAdmin)
