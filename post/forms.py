from django import forms

from .models import Product, Comment, Category


class ProductCreateForm2(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea())
    image = forms.ImageField(required=False)
    rate = forms.IntegerField(min_value=1, max_value=5)


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'image', 'category')


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)
