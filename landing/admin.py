from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage, Category, Tag, ProductMeta, UserProfile, Feedback
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

User = get_user_model()

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0
    can_delete = False

admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]

class ProductMetaInline(admin.StackedInline):
    model = ProductMeta
    extra = 0

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "is_primary", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 120px; border-radius: 8px;" />',
                obj.image.url
            )
        return "No image"

    image_preview.short_description = "Preview"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "title",
        "price",
        "category",
        "condition",
        "location",
        "available",
        "seller"
    )
    list_filter = (
        "available",
        "condition",
        "location",
        "category",
        "seller"
    )
    search_fields = (
        "title",
        "description",
        "seller__username",
        "seller__email"
    )
    inlines = [ProductMetaInline, ProductImageInline]

    def image_preview(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if not primary_image:
            primary_image = obj.images.first()

        if primary_image and primary_image.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; border-radius: 6px;" />',
                primary_image.image.url
            )
        return "No image"

    image_preview.short_description = "Image"

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(UserProfile)
admin.site.register(Feedback)
